#!/usr/bin/env python3
"""Offline, reproducible reference analysis for the Bob Ross classroom case."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score

HERE = Path(__file__).resolve().parent
RAW = HERE / 'data/elements-by-episode.csv'
EXPECTED_SHA256 = '42045c8b8aaa8296095d6b294927fb9d0f73a57259f59b560c375844c0fe01cf'
FEATURES = {
    'arboles': ['TREE', 'TREES'],
    'montanas': ['MOUNTAIN', 'MOUNTAINS', 'SNOWY_MOUNTAIN'],
    'lagos': ['LAKE', 'LAKES'],
    'rios': ['RIVER'],
    'mar': ['OCEAN'],
    'nieve': ['SNOW', 'SNOWY_MOUNTAIN'],
    'cascadas': ['WATERFALL'],
    'estructuras': ['STRUCTURE'],
    'nubes': ['CLOUDS'],
    'rocas': ['ROCKS'],
    'sol': ['SUN'],
    'flores': ['FLOWERS'],
}
DISPLAY = ['Árboles', 'Montañas', 'Lagos', 'Ríos', 'Mar', 'Nieve',
           'Cascadas', 'Estructuras', 'Nubes', 'Rocas', 'Sol', 'Flores']
SEED = 42
N_INIT = 50
K = 4  # A museum constraint, never an inferred number of natural styles.


def checked_frame(frame):
    if frame.empty or frame['EPISODE'].isna().any() or frame['EPISODE'].duplicated().any():
        raise ValueError('Se necesitan episodios únicos y no vacíos.')
    if not frame['EPISODE'].str.fullmatch(r'S\d{2}E\d{2}').all():
        raise ValueError('Formato de episodio inesperado.')
    labels = sorted({c for columns in FEATURES.values() for c in columns} | {'GUEST'})
    if not set(labels + ['TITLE']) <= set(frame):
        raise ValueError('Faltan columnas del contrato.')
    if frame[labels].isna().any().any() or not frame[labels].isin([0, 1]).all().all():
        raise ValueError('Etiquetas ausentes o no binarias: no imputar silenciosamente.')
    return frame


def load_data(path=RAW, verify_hash=True):
    raw = Path(path).read_bytes()
    if verify_hash and hashlib.sha256(raw).hexdigest() != EXPECTED_SHA256:
        raise ValueError('El archivo no coincide con la edición fijada; revisar antes de seguir.')
    frame = checked_frame(pd.read_csv(path))
    return frame


def prepare(frame, exclude_guests=True):
    checked_frame(frame)
    rows = frame.loc[frame.GUEST.eq(0)].copy() if exclude_guests else frame.copy()
    # Sort identifiers only to make the analysis deterministic, never as features.
    rows = rows.sort_values('EPISODE').reset_index(drop=True)
    X = pd.DataFrame({name: rows[columns].max(axis=1).astype('int64')
                      for name, columns in FEATURES.items()})
    return rows, X


def cluster(X, k=K, seed=SEED):
    model = KMeans(n_clusters=k, n_init=N_INIT, random_state=seed, algorithm='lloyd')
    original = model.fit_predict(np.asarray(X, dtype=float))
    # Only display labels change: largest room first, original label as tie-break.
    order = sorted(range(k), key=lambda label: (-int((original == label).sum()), label))
    mapping = {old: new for new, old in enumerate(order)}
    labels = np.array([mapping[v] for v in original], dtype=int)
    return labels, float(model.inertia_)


def q(value):
    return round(float(value), 8)


def compute():
    raw = load_data()
    rows, X = prepare(raw)
    labels, inertia = cluster(X)
    values = X.to_numpy()
    distances = squareform(pdist(values, metric='euclidean'))
    rooms = []
    for group in range(K):
        members = np.flatnonzero(labels == group)
        frequencies = values[members].mean(axis=0)
        # A medoid is a real episode closest on average to all room members.
        mean_distance = distances[np.ix_(members, members)].mean(axis=1)
        medoid = int(members[np.argmin(mean_distance)])
        farthest = int(members[np.argmax(distances[medoid, members])])

        def example(index):
            return dict(episode=rows.iloc[index].EPISODE,
                        title=rows.iloc[index].TITLE.strip('"'),
                        features=[name for name, bit in zip(FEATURES, values[index]) if bit],
                        distance_to_medoid=q(distances[medoid, index]))

        rooms.append(dict(room=group + 1, size=int(len(members)),
                          counts={key: int(values[members, i].sum()) for i, key in enumerate(FEATURES)},
                          frequencies={key: q(v) for key, v in zip(FEATURES, frequencies)},
                          medoid=example(medoid), boundary_example=example(farthest)))

    grid = []
    for k in range(2, 9):
        lab, loss = cluster(X, k=k)
        grid.append(dict(k=k, silhouette_euclidean=q(silhouette_score(values, lab)),
                         smallest_room=int(np.bincount(lab).min()), inertia=q(loss),
                         sizes=np.bincount(lab).tolist()))

    seeds = [dict(seed=s, ari=q(adjusted_rand_score(labels, cluster(X, seed=s)[0]))) for s in range(10)]
    no_trees = cluster(X.drop(columns='arboles'))[0]
    all_rows, all_X = prepare(raw, exclude_guests=False)
    all_labels = cluster(all_X)[0]
    common = pd.Series(all_labels, index=all_rows.EPISODE).loc[rows.EPISODE].to_numpy()
    # An explicitly constructed bad experiment. This number is NOT in the CSV.
    sequence_id = rows.EPISODE.str.slice(1, 3).astype(int) * 13 + rows.EPISODE.str.slice(4, 6).astype(int)
    contaminated = np.column_stack([values, sequence_id.to_numpy() * 10])
    bad_labels = cluster(contaminated)[0]
    bad_silhouette = silhouette_score(contaminated, bad_labels)

    result = dict(
        question='¿Cómo organizar cuatro salas de Bob Ross por elementos representados y defender la decisión?',
        source_sha256=EXPECTED_SHA256,
        population=dict(raw_episodes=len(raw), excluded_guest=int(raw.GUEST.sum()), included_episodes=len(rows),
                        all_zero_profiles=int((values.sum(axis=1) == 0).sum()),
                        unique_profiles=int(len(np.unique(values, axis=0)))),
        model=dict(algorithm='KMeans', k=K, random_state=SEED, n_init=N_INIT, initialization='k-means++',
                   metric='euclidean', objective='within-cluster sum of squared Euclidean distances',
                   scaling='none; twelve binary motif families, equal weights',
                   k_reason='Four exhibition rooms: an external teaching/design constraint, not a claim of four natural styles.'),
        feature_mapping=FEATURES,
        rooms=rooms,
        diagnostics=dict(silhouette_k4=q(silhouette_score(values, labels)), inertia_k4=q(inertia), k_grid=grid),
        sensitivity=dict(seed_runs=seeds, min_seed_ari=q(min(r['ari'] for r in seeds)),
                         no_trees_ari=q(adjusted_rand_score(labels, no_trees)),
                         with_guests_common_episodes_ari=q(adjusted_rand_score(labels, common))),
        bad_experiment=dict(definition='Add 10 * (season * 13 + episode_number) as a thirteenth feature.',
                            deliberately_constructed=True,
                            ari_vs_main=q(adjusted_rand_score(labels, bad_labels)),
                            silhouette_in_contaminated_space=q(bad_silhouette),
                            warning='Scores in different feature spaces are not a common quality scale. This high score can reward chronological grouping.'),
        interpretation='Exploratory grouping of twelve human-coded motif families, not artistic intent, quality, popularity or a validated taxonomy of styles.',
    )
    return result, rows, X, labels, bad_labels


def plots(result, rows, output):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11,
                         'svg.fonttype': 'none', 'svg.hashsalt': 'bob-ross-class-demo',
                         'axes.spines.top': False, 'axes.spines.right': False})
    frequencies = np.array([list(room['frequencies'].values()) for room in result['rooms']])
    fig, ax = plt.subplots(figsize=(14, 5.8), layout='constrained')
    fig.get_layout_engine().set(rect=(0, .09, 1, .91))
    image = ax.imshow(frequencies, vmin=0, vmax=1, cmap='YlGnBu', aspect='auto')
    ax.set_xticks(range(12), DISPLAY, rotation=32, ha='right')
    ax.set_yticks(range(4), [f'Sala {r["room"]}\nn={r["size"]}' for r in result['rooms']])
    for row in range(4):
        for col in range(12):
            value = frequencies[row, col]
            ax.text(col, row, f'{value:.0%}', ha='center', va='center', fontsize=11,
                    color='white' if value > .55 else '#14242e')
    ax.set_title('¿Qué aparece en cada sala?\nFrecuencia de cada motivo dentro del grupo', loc='left', pad=18, fontsize=18)
    fig.colorbar(image, ax=ax, shrink=.75, label='Proporción de episodios')
    fig.text(.02, .01, '381 episodios sin GUEST · 12 familias binarias · K-means, k=4 · no se usaron títulos ni imágenes', fontsize=10)
    fig.savefig(output / 'profiles.svg', metadata={'Date': None})
    plt.close(fig)

    grid = result['diagnostics']['k_grid']
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), layout='constrained')
    axes[0].plot([g['k'] for g in grid], [g['silhouette_euclidean'] for g in grid], marker='o', color='#14756b', linewidth=2)
    axes[0].axvline(4, color='#b06f1b', linestyle='--', label='4 salas disponibles')
    axes[0].set(xlabel='Número de grupos, k', ylabel='Silhouette (espacio original de 12 motivos)', title='La métrica sigue mejorando después de k=4')
    axes[0].legend()
    axes[1].bar([g['k'] for g in grid], [g['smallest_room'] for g in grid], color='#536e89')
    axes[1].set(xlabel='Número de grupos, k', ylabel='Episodios del grupo más pequeño', title='Más grupos también cambian el tamaño de las salas')
    fig.suptitle('Elegir k requiere una decisión; una métrica no resuelve el encargo', fontsize=15)
    fig.savefig(output / 'k_diagnostics.svg', metadata={'Date': None})
    plt.close(fig)


def trap_plot(rows, labels, bad_labels, result, output):
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    fig, axes = plt.subplots(2, 1, figsize=(13, 4.6), layout='constrained')
    fig.get_layout_engine().set(rect=(0, .10, 1, .90))
    for ax, lab, colors, title in zip(axes, [labels, bad_labels],
            [['#156f6a', '#edbb4e', '#3b6294', '#ad5554'], ['#645273', '#969ea5', '#ca8c67', '#617557']],
            ['A · Sólo motivos del paisaje', 'B · Motivos + ID secuencial × 10 (experimento deliberadamente incorrecto)']):
        ax.imshow(lab[np.newaxis, :], aspect='auto', cmap=ListedColormap(colors), vmin=0, vmax=3, interpolation='nearest')
        ticks=np.linspace(0, len(rows)-1, 6, dtype=int)
        ax.set_xticks(ticks, rows.iloc[ticks].EPISODE)
        ax.set_yticks([])
        ax.set_title(title, loc='left', fontsize=12)
        ax.set_xlabel('Episodios ordenados por temporada y número')
    fig.suptitle(f'Un agrupamiento nítido puede responder la pregunta equivocada · ARI A/B={result["bad_experiment"]["ari_vs_main"]:.3f}', fontsize=14)
    fig.text(.01, .01, 'Cada franja es un episodio. Colores identifican grupos; no hay correspondencia semántica entre los colores de A y B.', fontsize=9)
    fig.savefig(output / 'metadata_trap.svg', metadata={'Date': None})
    plt.close(fig)


def write(result, rows, X, labels, bad_labels, output):
    output.mkdir(parents=True, exist_ok=True)
    (output / 'report.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    X.assign(EPISODE=rows.EPISODE).to_csv(output / 'features.csv', index=False)
    rows[['EPISODE', 'TITLE']].assign(room=labels+1, bad_experiment_room=bad_labels+1).to_csv(output / 'assignments.csv', index=False)
    pd.DataFrame([dict(room=r['room'], n=r['size'], **r['frequencies']) for r in result['rooms']]).to_csv(output / 'centroids.csv', index=False)
    pd.DataFrame(result['diagnostics']['k_grid']).to_csv(output / 'k_grid.csv', index=False)
    runtime = dict(python=platform.python_version(), packages={p: importlib.metadata.version(p) for p in ['numpy','pandas','scipy','scikit-learn','matplotlib']},
                   script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), feature_input_sha256=hashlib.sha256((output/'features.csv').read_bytes()).hexdigest())
    (output / 'runtime.json').write_text(json.dumps(runtime, ensure_ascii=False, indent=2) + '\n')
    plots(result, rows, output)
    trap_plot(rows, labels, bad_labels, result, output)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=HERE/'output')
    parser.add_argument('--check', action='store_true', help='Recompute offline and compare with the committed analytical reference.')
    args=parser.parse_args()
    result, rows, X, labels, bad_labels=compute()
    if args.check:
        expected=json.loads((HERE/'reference/report.json').read_text())
        if result != expected:
            raise SystemExit('FAIL: los resultados difieren de reference/report.json. Revisar versiones, datos y cambios; no sobrescribir la referencia sin inspección.')
        print('PASS: referencia analítica reproducida sin red; 381 episodios, 12 variables, cuatro salas.')
    else:
        write(result, rows, X, labels, bad_labels, args.output)
        print(json.dumps(dict(output=str(args.output), episodes=len(rows), sizes=[r['size'] for r in result['rooms']], silhouette=result['diagnostics']['silhouette_k4']),ensure_ascii=False))


if __name__ == '__main__':
    main()
