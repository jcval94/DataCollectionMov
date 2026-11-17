"""Allowed, bounded descriptive analyses. No fitting with post-event predictors."""
from decimal import Decimal
from itertools import combinations

import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import adjusted_rand_score, silhouette_score

from .data import MOTIFS, require

SEED = 20261116


def retail(d, raw, previous):
    x = d[d.eligible].copy()
    def aggregate(frame):
        rows = []
        for code, g in frame.groupby('StockCode', sort=True):
            gross = sum((max(v, Decimal(0)) for v in g.line_amount_gbp), Decimal(0))
            credits = sum((max(-v, Decimal(0)) for v in g.line_amount_gbp), Decimal(0))
            rows.append(dict(product=code, gross_gbp=gross, credits_gbp=credits, net_gbp=gross-credits, lines=len(g)))
        t = pd.DataFrame(rows)
        for field in ['gross_gbp', 'net_gbp']:
            order = t.sort_values([field, 'product'], ascending=[False, True]).index
            t.loc[order, 'rank_' + field] = np.arange(1, len(t)+1)
        return t
    ranking = aggregate(x)
    dedup = aggregate(x.loc[~raw.duplicated().loc[x.index]])
    independent = sum(x.line_amount_gbp, Decimal(0))
    require(sum(ranking.net_gbp, Decimal(0)) == independent == Decimal(previous['totals']['net']), 'Reconciliación V2 de neto')
    totals = {k: str(sum(ranking[k+'_gbp'], Decimal(0))) for k in ['gross', 'credits', 'net']}
    require(Decimal(totals['gross']) - Decimal(totals['credits']) == Decimal(totals['net']), 'Bruto - créditos = neto')
    denominators = pd.DataFrame([
        dict(unit='Líneas', missing=int(d.customer_id_missing.sum()), denominator=len(d)),
        dict(unit='Facturas', missing=int(d.groupby('InvoiceNo').customer_id_missing.first().sum()), denominator=d.InvoiceNo.nunique())])
    denominators['fraction'] = denominators.missing / denominators.denominator
    sensitivity = pd.DataFrame([
        dict(policy='Conservar duplicados', lines=len(x), net_gbp=totals['net']),
        dict(policy='Sin duplicados exactos', lines=len(x)-int(raw.duplicated().loc[x.index].sum()), net_gbp=str(sum(dedup.net_gbp, Decimal(0))))])
    claims = {
        'D31-A': dict(totals=totals, leader=ranking.sort_values('rank_net_gbp').iloc[0]['product'], products=len(ranking)),
        'D31-B': dict(by_unit=denominators.to_dict('records')),
        'D31-E': dict(changed_positions=int(ranking.rank_gross_gbp.ne(ranking.rank_net_gbp).sum()),
                     policies=sensitivity.to_dict('records'))}
    return dict(ranking=ranking, denominators=denominators, duplicate_sensitivity=sensitivity), claims


def nba(d, raw, previous):
    games = d[d.eligible].copy()
    home = d[d.game_location.eq('H')].copy()
    require(len(games) == previous['unique_games'], 'Partidos V2 conservados')
    require(games.game_id.is_unique, 'Gold debe tener una fila por partido')
    brier = float(((games.forecast-games.win)**2).mean())
    require(abs(brier-previous['brier']) < 1e-12, 'Brier V2 conservado')
    cal = games.assign(bin=pd.cut(games.forecast, [0, .2, .4, .6, .8, 1], include_lowest=True))
    calibration = cal.groupby('bin', observed=True).agg(predicted=('forecast', 'mean'), observed=('win', 'mean'), n=('win', 'size')).reset_index()
    calibration['bin'] = calibration.bin.astype(str)
    # Forecast vs p=.5 scored on the same games and resampled using the same dates.
    scores = games.assign(delta=(games.forecast-games.win)**2-(.5-games.win)**2)
    dates = scores.groupby('date_game').delta.agg(['sum', 'count']).to_numpy()
    rng = np.random.default_rng(SEED); means = []
    for _ in range(1000):
        sample = dates[rng.integers(0, len(dates), len(dates))]
        means.append(float(sample[:, 0].sum()/sample[:, 1].sum()))
    interval = np.quantile(means, [.025, .975]).tolist()
    phases = pd.DataFrame(previous['phases'])
    series = []
    playoffs = games[games.is_playoffs.eq('1')].copy()
    playoffs['pair'] = [':'.join(sorted([a, b])) for a, b in zip(playoffs.team_id, playoffs.opp_id)]
    for pair, g in playoffs.groupby('pair', sort=True):
        g = g.sort_values(['date_game', 'game_id']); first = g.iloc[0]
        wins = {}
        for row in g.itertuples():
            team = row.team_id if row.win else row.opp_id
            wins[team] = wins.get(team, 0)+1
        teams = pair.split(':'); tallies = {t: wins.get(t, 0) for t in teams}
        winner = max(tallies, key=tallies.get)
        require(tallies[winner] == 4 and max(tallies.values()) == 4 and min(tallies.values()) < 4, 'Serie no completa: ' + pair)
        favorite = first.team_id if first.elo_i > first.opp_elo_i else first.opp_id
        require(first.elo_i != first.opp_elo_i, 'Favorito ambiguo por empate Elo')
        series.append(dict(pair=pair, first_date=first.date_game.isoformat(), first_game=first.game_id,
                           favorite=favorite, winner=winner, favorite_won=winner == favorite,
                           elo_gap=abs(float(first.elo_i-first.opp_elo_i)), games=len(g),
                           winner_wins=tallies[winner], loser_wins=min(tallies.values())))
    series = pd.DataFrame(series)
    require(len(series) == 15 and int(series.games.sum()) == len(playoffs), '15 series completas y partidos reconciliados')
    claims = {
        'D10-D1': dict(series=len(series), favorite_wins=int(series.favorite_won.sum()),
                       counterexamples=series.loc[~series.favorite_won, ['pair', 'first_game', 'favorite', 'winner']].to_dict('records')),
        'D10-D2': dict(phases=previous['phases'], difference=previous['phase_difference_playoffs_minus_regular'],
                       block_interval=previous['phase_difference_block_95'], neutral_games_excluded=int(games.game_location.eq('N').sum())),
        'D10-E': dict(brier=brier, constant_half_brier=.25, paired_date_delta=float(scores.delta.mean()),
                      paired_date_delta_95=interval, unique_games=len(games), mirror_rows=len(d),
                      neutral_games=int(games.game_location.eq('N').sum()), calibration=calibration.to_dict('records'))}
    return dict(games=games, calibration=calibration, phases=phases, series=series,
                score_sensitivity=pd.DataFrame([dict(method='Forecast previo', brier=brier), dict(method='Constante 0.5', brier=.25)])), claims


def cluster(distance, k=4):
    require(np.isfinite(distance).all() and np.allclose(distance, distance.T), 'Matriz de distancia inválida')
    return AgglomerativeClustering(n_clusters=k, metric='precomputed', linkage='average').fit_predict(distance)


def bob(d, raw, previous):
    host = d[d.eligible].copy(); a = host[MOTIFS].to_numpy(dtype=bool)
    jaccard = squareform(pdist(a, metric='jaccard')); labels = cluster(jaccard)
    euclid = squareform(pdist(a.astype(float), metric='euclidean')); clean = cluster(euclid)
    require(abs(silhouette_score(jaccard, labels, metric='precomputed')-previous['jaccard_silhouette']) < 1e-12, 'Silueta V2 conservada')
    rng = np.random.default_rng(SEED)
    null = []
    # Preserve each binary marginal but remove joint motif structure. Exploratory benchmark, not a p-value.
    for _ in range(30):
        permuted = np.column_stack([rng.permutation(a[:, j]) for j in range(a.shape[1])])
        dist = squareform(pdist(permuted, metric='jaccard'))
        null.append(float(silhouette_score(dist, cluster(dist), metric='precomputed')))
    profiles = host[MOTIFS].assign(group=labels).groupby('group').mean()
    profiles['n'] = np.bincount(labels, minlength=4)
    stability = []
    # ID contamination deliberately isolated at the same Euclidean metric and k.
    for scale in [0, 1/31, 1]:
        features = np.column_stack([a.astype(float), host.season.to_numpy()*scale])
        dist = squareform(pdist(features, metric='euclidean')); contaminated = cluster(dist)
        stability.append(dict(season_scale=scale, ARI_vs_clean_euclidean=float(adjusted_rand_score(clean, contaminated)),
                              silhouette_own_distance=float(silhouette_score(dist, contaminated, metric='precomputed'))))
    stability = pd.DataFrame(stability)
    prevalence = []
    for group, g in [('Anfitrión', host), ('Invitados', d[d.GUEST.eq(1)])]:
        for motif in MOTIFS:
            prevalence.append(dict(group=group, motif=motif, count=int(g[motif].sum()), denominator=len(g), fraction=float(g[motif].mean())))
    prevalence = pd.DataFrame(prevalence)
    trees = []
    for group, g in [('Anfitrión', host), ('Invitados', d[d.GUEST.eq(1)])]:
        trees.append(dict(group=group, count=int(g.tree_any.sum()), denominator=len(g), fraction=float(g.tree_any.mean())))
    mountain = host[host.mountain_any.eq(1)]
    counterexamples = host.loc[host.tree_any.eq(0), ['EPISODE', 'TITLE', 'TREE', 'TREES']]
    snow_counterexamples = mountain.loc[mountain.snow_any.eq(0), ['EPISODE', 'TITLE', 'MOUNTAIN', 'MOUNTAINS', 'SNOW', 'SNOWY_MOUNTAIN']]
    # Small reproducible exhibit selection. Labels only; no commercial demand or artwork rights implied.
    features = [c for c in raw if c not in ['EPISODE', 'TITLE', 'GUEST', 'STEVE_ROSS', 'DIANE_ANDRE']]
    matrix = host[features].to_numpy(dtype=bool); remaining = list(range(len(matrix))); selected = []; covered = np.zeros(len(features), dtype=bool)
    for _ in range(12):
        # Tie break by snapshot row order, fixed before seeing economic outcomes (none available).
        best = max(remaining, key=lambda i: int((matrix[i] & ~covered).sum()))
        selected.append(best); remaining.remove(best); covered |= matrix[best]
    def coverage(indices):
        return int(matrix[indices].any(axis=0).sum())
    random_coverage = [coverage(rng.choice(len(matrix), size=12, replace=False)) for _ in range(100)]
    selection = host.iloc[selected][['EPISODE', 'TITLE']].copy(); selection['selection_order'] = np.arange(1, 13)
    selection_curve = pd.DataFrame([dict(episodes=n, greedy_motifs=coverage(selected[:n]), chronological_motifs=coverage(list(range(n)))) for n in range(1, 13)])
    claims = {
        'D85-A': dict(slots=12, possible_motifs=len(features), greedy_coverage=coverage(selected),
                      chronological_coverage=coverage(list(range(12))), random_coverage_100=random_coverage,
                      metric='Motivos distintos cubiertos; no rentabilidad ni equilibrio estético.'),
        'D85-B': dict(prevalence=prevalence.to_dict('records')),
        'D85-C': dict(k=4, silhouette=float(previous['jaccard_silhouette']), permuted_marginals_silhouettes=null,
                       distance_ARI=float(adjusted_rand_score(labels, clean))),
        'D85-D1': dict(groups=trees, host_counterexamples=len(counterexamples)),
        'D85-D2': dict(mountain_episodes=len(mountain), with_snow=int(mountain.snow_any.sum()), without_snow=len(snow_counterexamples)),
        'D85-E': dict(sensitivity=stability.to_dict('records'), control='Misma muestra, k=4 y distancia Euclídea; cambia sólo escala de temporada.')}
    return dict(profiles=profiles.reset_index(), prevalence=prevalence, trees=pd.DataFrame(trees),
                counterexamples=counterexamples, snow_counterexamples=snow_counterexamples,
                id_sensitivity=stability, selection=selection, selection_curve=selection_curve,
                null_silhouettes=pd.DataFrame(dict(replicate=range(30), silhouette=null))), claims


ANALYSES = {'uci-retail': retail, 'nba-elo': nba, 'bob-ross-elementos': bob}
