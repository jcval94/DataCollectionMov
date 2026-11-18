"""Measured profiles and domain-specific silver tables; no network or credentials."""
from decimal import Decimal
from pathlib import Path
import hashlib
import json

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[2]
CASES = ('uci-retail', 'nba-elo', 'bob-ross-elementos')
MOTIFS = ['TREE', 'TREES', 'MOUNTAIN', 'MOUNTAINS', 'SNOW', 'SNOWY_MOUNTAIN',
          'LAKE', 'RIVER', 'OCEAN', 'CLOUDS', 'ROCKS', 'FLOWERS']


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(case):
    require(case in CASES, 'Fuente fuera de la lista permitida')
    folder = BASE / 'pilots' / case / 'data'
    manifest = json.loads((folder / 'manifest.json').read_text())
    path = folder / 'snapshot.csv'
    require(sha(path) == manifest['snapshot_sha256'], 'Hash de snapshot no coincide')
    require(path.stat().st_size == manifest['snapshot_bytes'], 'Tamaño de snapshot no coincide')
    raw = pd.read_csv(path, dtype=str, keep_default_na=False)
    require(list(raw) == manifest['columns'] and len(raw) == manifest['rows'], 'Esquema/filas no coincide')
    return raw, manifest


def profile(raw, silver, manifest, key, dates=None):
    columns = {}
    for name in raw:
        s = raw[name]
        observed = s[s.ne('')]
        numeric = pd.to_numeric(observed, errors='coerce')
        info = dict(raw_type='string', silver_type=str(silver[name].dtype),
                    missing_count=int(s.eq('').sum()), missing_pct=100 * float(s.eq('').mean()),
                    cardinality=int(observed.nunique()),
                    frequent_values={str(k): int(v) for k, v in observed.value_counts().head(5).items()})
        if len(numeric) and numeric.notna().all() and (pd.api.types.is_numeric_dtype(silver[name]) or name in ['Quantity', 'UnitPrice']):
            require(np.isfinite(numeric).all(), f'Valores no finitos en {name}')
            info['numeric_measured'] = {k: float(v) for k, v in numeric.quantile([0, .25, .5, .75, 1]).rename(
                index={0: 'min', .25: 'q25', .5: 'median', .75: 'q75', 1: 'max'}).items()}
            q1, q3 = numeric.quantile([.25, .75]); iqr = q3 - q1
            info['outside_1_5_IQR_count'] = int(((numeric < q1 - 1.5 * iqr) | (numeric > q3 + 1.5 * iqr)).sum())
            info['outlier_policy'] = 'Señalar; no excluir por esta regla.'
        columns[name] = info
    temporal = {'status': 'No hay fechas observadas; EPISODE no es fecha de emisión.'}
    if dates is not None:
        temporal = dict(min=dates.min().isoformat(), max=dates.max().isoformat(),
                        frequency='Eventos irregulares; no imputar días sin evento como faltantes.',
                        observed_dates=int(dates.dt.normalize().nunique()), timezone='No verificada; mantener fecha local sin conversión.')
    return dict(scope='Snapshot medido; no universo declarado por productor.', rows=len(raw),
                column_count=len(raw.columns), physical_bytes=manifest['snapshot_bytes'],
                raw_memory_bytes=int(raw.memory_usage(deep=True).sum()),
                silver_memory_bytes=int(silver.memory_usage(deep=True).sum()),
                exact_duplicates=int(raw.duplicated().sum()),
                business_key=key, business_key_repetitions=int(raw.duplicated(key).sum()),
                key_interpretation='Repetir una factura es normal en líneas; no demuestra duplicado de negocio.' if key == ['InvoiceNo'] else 'La llave debe ser única.',
                columns=columns, temporal=temporal, selection=manifest['selection'],
                representativeness='No se infiere representatividad ni causalidad desde este archivo.')


def prepare(case, raw, manifest):
    d = raw.copy(); dates = None; transformations = []; checks = []
    def check(name, condition, detail):
        require(bool(condition), name + ': ' + detail)
        checks.append(dict(rule=name, passed=True, detail=detail))
    check('nonempty', not d.empty, 'Snapshot no vacío.')
    if case == 'uci-retail':
        check('privacy', 'CustomerID' not in d, 'Identificador eliminado antes de distribuir el snapshot.')
        dates = pd.to_datetime(d.InvoiceDate, errors='raise')
        d['InvoiceDate'] = dates
        check('period', dates.ge('2011-11-01').all() and dates.lt('2011-12-01').all(), 'Sólo noviembre 2011.')
        d['Quantity'] = d.Quantity.map(Decimal); d['UnitPrice'] = d.UnitPrice.map(Decimal)
        check('quantity', all(v.is_finite() and v == v.to_integral_value() for v in d.Quantity), 'Cantidad entera firmada.')
        check('price', all(v.is_finite() for v in d.UnitPrice), 'Precio finito, sin ocultar no positivos.')
        check('missing_flag', d.customer_id_missing.isin(['0', '1']).all(), 'Indicador binario de ausencia.')
        check('invoice_missing_coherence', d.groupby('InvoiceNo').customer_id_missing.nunique().eq(1).all(), 'Indicador consistente por factura.')
        d['customer_id_missing'] = d.customer_id_missing.astype(int)
        d['line_amount_gbp'] = d.Quantity * d.UnitPrice
        policies = {
            'non_product_code': ~d.StockCode.str.fullmatch(r'\d{5}[A-Za-z]*'),
            'nonpositive_price': d.UnitPrice.le(0),
            'zero_quantity': d.Quantity.eq(0),
            'cancel_positive': d.InvoiceNo.str.upper().str.startswith('C') & d.Quantity.gt(0)}
        d['exclusion_reason'] = ['|'.join(k for k, mask in policies.items() if mask.loc[i]) for i in d.index]
        d['eligible'] = d.exclusion_reason.eq('')
        for reason, mask in policies.items():
            transformations.append(dict(step=reason, affected_rows=int(mask.sum()),
                action='Excluir sólo del ranking económico; conservar en silver con motivos acumulables.',
                statistical_consequence='Cambia el universo de productos elegibles; las notas negativas permanecen.'))
        key = ['InvoiceNo']
        transformations.append(dict(step='exact_duplicates', affected_rows=int(raw.duplicated().sum()),
            action='Conservar en análisis principal; retirar sólo en sensibilidad.',
            statistical_consequence='No se puede probar que una línea repetida sea error de negocio.'))
    elif case == 'nba-elo':
        for col in ['pts', 'opp_pts', 'elo_i', 'elo_n', 'opp_elo_i', 'opp_elo_n', 'forecast']:
            d[col] = pd.to_numeric(d[col], errors='raise')
            check('finite_' + col, np.isfinite(d[col]).all(), 'Numérico finito.')
        dates = pd.to_datetime(d.date_game, errors='raise'); d['date_game'] = dates
        check('season', d.year_id.eq('2015').all() and d.lg_id.eq('NBA').all(), 'Una temporada NBA, no eras.')
        check('unique_team_game', not d.duplicated(['game_id', 'team_id']).any(), 'Llave equipo-partido.')
        check('mirror_count', d.groupby('game_id').size().eq(2).all(), 'Dos perspectivas por partido.')
        check('mirror_flag', all(set(g._iscopy) == {'0', '1'} for _, g in d.groupby('game_id')), 'Exactamente un original y una copia por partido.')
        check('domains', d.game_location.isin(['H', 'A', 'N']).all() and d.is_playoffs.isin(['0', '1']).all(), 'Incluye campo neutral N.')
        check('score_domain', (d.pts.ge(0) & d.opp_pts.ge(0) & d.pts.mod(1).eq(0) & d.opp_pts.mod(1).eq(0) & d.pts.ne(d.opp_pts)).all(), 'Puntos enteros no negativos; sin empate final.')
        check('probabilities', d.forecast.between(0, 1).all(), 'Probabilidades previas válidas.')
        for _, pair in d.groupby('game_id', sort=True):
            a, b = pair.iloc[0], pair.iloc[1]
            require(a.team_id == b.opp_id and a.opp_id == b.team_id, 'Rival espejo inconsistente')
            require(a.pts == b.opp_pts and a.opp_pts == b.pts, 'Marcador espejo inconsistente')
            require(a.date_game == b.date_game and a.is_playoffs == b.is_playoffs, 'Fecha/fase espejo inconsistente')
            require(set(pair.game_location) == {'H', 'A'} or pair.game_location.eq('N').all(), 'Localía espejo inconsistente')
            require(abs(a.forecast + b.forecast - 1) < .001, 'Probabilidad espejo inconsistente')
            require(abs(a.elo_i - b.opp_elo_i) < .001, 'Elo previo espejo inconsistente')
        checks.append(dict(rule='reciprocal_pairs', passed=True, detail='Equipos, marcador, fecha, localía, fase, Elo y probabilidades cotejados.'))
        d['win'] = d.pts.gt(d.opp_pts).astype(int); d['eligible'] = d._iscopy.eq('0')
        d['exclusion_reason'] = np.where(d.eligible, '', 'mirror_perspective')
        transformations.append(dict(step='one_game_one_row', affected_rows=int((~d.eligible).sum()),
            action='Una fila _iscopy=0 en gold; conservar ambas en silver.',
            statistical_consequence='Evita doblar tamaño de muestra. Las tasas locales excluyen explícitamente neutrales.'))
        key = ['game_id', 'team_id']
    else:
        labels = [c for c in d if c not in ['EPISODE', 'TITLE']]
        check('episode_key', d.EPISODE.str.fullmatch(r'S\d{2}E\d{2}').all() and not d.EPISODE.duplicated().any(), 'ID único; no feature artística.')
        check('binary_labels', d[labels].isin(['0', '1']).all().all(), 'Los ceros son ausencias registradas, no nulos.')
        d[labels] = d[labels].astype(int)
        d['season'] = d.EPISODE.str[1:3].astype(int)
        d['eligible'] = d.GUEST.eq(0); d['exclusion_reason'] = np.where(d.eligible, '', 'guest_sensitivity_only')
        d['tree_any'] = d[['TREE', 'TREES']].max(axis=1)
        d['mountain_any'] = d[['MOUNTAIN', 'MOUNTAINS']].max(axis=1)
        d['snow_any'] = d[['SNOW', 'SNOWY_MOUNTAIN']].max(axis=1)
        transformations.append(dict(step='host_scope', affected_rows=int((~d.eligible).sum()),
            action='Anfitrión en ruta principal; todos los episodios para comparación estratificada.',
            statistical_consequence='El denominador depende de la autoría; etiquetas no verificadas contra píxeles.'))
        key = ['EPISODE']
    d.insert(0, 'raw_row_id', np.arange(len(d)))
    check('row_conservation', len(d) == len(raw) and d.raw_row_id.is_unique, 'Ninguna fila desaparece de silver.')
    checks.append(dict(rule='eligible_reconciliation', passed=True,
        detail=f'{int(d.eligible.sum())} elegibles + {int((~d.eligible).sum())} fuera del alcance = {len(d)}.'))
    return d, profile(raw, d, manifest, key, dates), transformations, checks
