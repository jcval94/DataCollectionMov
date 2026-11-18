"""Export table-backed figures at two sizes with explicit visual provenance."""
import textwrap

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.text import Text

from .data import MOTIFS, sha, require, write

BLUE = '#24546a'
RED = '#b84331'
GOLD = '#885f1d'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'axes.spines.top': False,
                     'axes.spines.right': False, 'axes.labelcolor': '#25313a',
                     'text.color': '#25313a', 'svg.hashsalt': 'ADL-V3'})


def draw(name, ax, tables, claims, mobile):
    """Return a concrete title, denominator, note and accessibility description."""
    if name == 'retail-ranking':
        t = tables['ranking'].sort_values('rank_gross_gbp').head(6 if mobile else 10)
        y = np.arange(len(t))
        ax.barh(y-.18, t.gross_gbp.astype(float), .35, color=BLUE, label='Bruto positivo')
        ax.barh(y+.18, t.net_gbp.astype(float), .35, color=RED, label='Neto firmado')
        ax.set_yticks(y, t['product']); ax.invert_yaxis(); ax.set_xlabel('Importe registrado (GBP)'); ax.legend(fontsize=10)
        return ('Bruto y neto por producto', f'{len(t)} productos con mayor bruto; líneas elegibles de 300 facturas.',
                'No hay costos: neto no mide utilidad. Créditos sin vínculo a su venta original.',
                'Barras emparejadas para los mismos productos; comparan bruto positivo y neto después de créditos.')
    if name == 'retail-missing':
        t = tables['denominators']; y = np.arange(len(t))
        ax.barh(y, 100*t.fraction, color=[BLUE, RED]); ax.set_xlim(0, 100)
        ax.set_yticks(y, [f'{r.unit}\nn={r.denominator:,}' for r in t.itertuples()]); ax.set_xlabel('Registros sin ID (%)')
        for i, r in enumerate(t.itertuples()): ax.text(100*r.fraction+2, i, f'{100*r.fraction:.1f}%', va='center')
        return ('Una ausencia, dos denominadores', 'Todas las líneas o todas las facturas del snapshot; sin filtrar productos.',
                'Un ID ausente no identifica un perfil social ni permite seguir clientes.',
                'Dos barras muestran la ausencia de ID por línea y por factura, con sus tamaños de muestra.')
    if name == 'retail-duplicates':
        t = tables['duplicate_sensitivity']; ax.bar([0, 1], t.net_gbp.astype(float), color=[BLUE, RED]); ax.set_ylim(bottom=0)
        ax.set_xticks([0, 1], ['Con repetidos', 'Sin exactos']); ax.set_ylabel('Neto firmado (GBP)')
        for i, r in enumerate(t.itertuples()): ax.text(i, float(r.net_gbp)+1000, f'{float(r.net_gbp):,.2f}', ha='center', fontsize=10)
        ax.margins(y=.15)
        return ('¿Cuánto pesa deduplicar?', 'Misma política económica; cambia sólo conservación de líneas exactamente iguales.',
                'Repetición exacta no demuestra error. Se conservan ambos resultados.',
                'Sensibilidad del neto a retirar duplicados exactos. El eje de barras comienza en cero.')
    if name == 'nba-calibration':
        t = tables['calibration']; ax.plot([0, 1], [0, 1], '--', color=GOLD, label='Calibración ideal')
        ax.scatter(t.predicted, t.observed, s=t.n, color=BLUE, edgecolor='white')
        for r in t.itertuples(): ax.annotate(f'n={r.n}', (r.predicted, r.observed), xytext=(0, 12), textcoords='offset points', ha='center', fontsize=9)
        ax.set(xlim=(0, 1), ylim=(0, 1), xlabel='Probabilidad previa media', ylabel='Fracción de victorias'); ax.legend(fontsize=9, loc='lower right')
        return ('Pronóstico frente a resultado', '1,311 partidos únicos; área de cada punto proporcional al número de partidos.',
                'Cinco bins fijados. Comparación descriptiva; dependencia por equipo/serie.',
                'Curva de calibración con conteos por intervalo y diagonal de igualdad; sólo pronóstico anterior al partido.')
    if name == 'nba-phases':
        t = tables['phases']; values = 100*t.rate
        ax.bar(t.phase, values, color=[BLUE, RED]); ax.axhline(50, color=GOLD, ls='--')
        for i, r in enumerate(t.itertuples()): ax.text(i, 100*r.rate+3, f'{100*r.rate:.1f}%\nn={r.n}', ha='center', fontsize=11)
        ax.set(ylim=(0, 100), ylabel='Victorias locales (%)')
        interval = claims['D10-D2']['block_interval']
        return ('La localía según la fase', f'{int(t.n.sum())} partidos con equipo local; 2 neutrales fuera del denominador.',
                f'Diferencia playoffs−regular: {100*claims["D10-D2"]["difference"]:.1f} pp; sensibilidad por fecha 95% [{100*interval[0]:.1f}, {100*interval[1]:.1f}] pp. No causal.',
                'Tasas de victoria del local por fase con conteos y sensibilidad del contraste por bloques de fecha.')
    if name == 'nba-series':
        t = tables['series'].sort_values('elo_gap'); y = np.arange(len(t))
        colors = np.where(t.favorite_won, BLUE, RED)
        ax.barh(y, t.elo_gap, color=colors); ax.set_yticks(y, t.pair, fontsize=9); ax.set_xlabel('Ventaja Elo antes del primer partido')
        ax.plot([], [], 's', color=BLUE, label='Favorito gana'); ax.plot([], [], 's', color=RED, label='Favorito pierde'); ax.legend(fontsize=9, loc='lower right')
        return ('¿Qué pasó con cada favorito?', '15 series completas; favorito definido con Elo previo al primer partido.',
                'El ganador se etiqueta después. No se usa elo_n para elegir favorito; una temporada no es toda la historia.',
                'Quince barras: diferencia Elo inicial por serie. Color y leyenda distinguen si ganó o perdió el favorito.')
    if name == 'nba-scores':
        t = tables['score_sensitivity']; ax.bar([0, 1], t.brier, color=[BLUE, RED]); ax.set_xticks([0, 1], ['Forecast previo', 'Constante 0.5']); ax.set(ylim=(0, .30), ylabel='Brier (menor es mejor)')
        for i, r in enumerate(t.itertuples()): ax.text(i, r.brier+.008, f'{r.brier:.4f}', ha='center')
        c = claims['D10-E']; lo, hi = c['paired_date_delta_95']
        return ('¿Mejora una base sencilla?', 'Los mismos 1,311 partidos únicos; promedio del error cuadrático de probabilidad.',
                f'Delta emparejado {c["paired_date_delta"]:.4f}; sensibilidad por fecha 95% [{lo:.4f}, {hi:.4f}]. No captura toda dependencia entre equipos.',
                'Brier del forecast histórico y de probabilidad constante. La nota muestra la diferencia emparejada y su sensibilidad por fecha.')
    if name == 'bob-prevalence':
        features = ['TREE', 'TREES', 'MOUNTAIN', 'SNOW', 'LAKE', 'OCEAN'] if mobile else ['TREE', 'TREES', 'MOUNTAIN', 'MOUNTAINS', 'SNOW', 'LAKE', 'RIVER', 'OCEAN', 'CLOUDS', 'FLOWERS']
        for group, color, marker in [('Anfitrión', BLUE, 'o'), ('Invitados', RED, 'x')]:
            t = tables['prevalence'].query('group == @group').set_index('motif').loc[features]
            ax.scatter(100*t.fraction, np.arange(len(t)), color=color, marker=marker, s=60, label=f'{group} (n={int(t.denominator.iloc[0])})')
        ax.set_yticks(range(len(features)), features); ax.set(xlim=(-3, 103), xlabel='Episodios con motivo (%)'); ax.legend(fontsize=9, loc='lower right')
        return ('¿Cambia el paisaje con invitados?', '381 episodios del anfitrión y 22 de invitados; cada motivo usa su propio grupo.',
                'Etiquetas humanas, sin incertidumbre muestral inventada. Tamaños de grupo desiguales.',
                'Dotplot de prevalencia por motivo y autoría. Formas y colores separan anfitrión e invitados.')
    if name == 'bob-clusters':
        t = tables['profiles']; motifs = MOTIFS[:6] if mobile else MOTIFS
        image = ax.imshow(t[motifs], vmin=0, vmax=1, cmap='cividis', aspect='auto')
        ax.set_xticks(range(len(motifs)), motifs, rotation=65, ha='right', fontsize=9)
        ax.set_yticks(range(4), [f'G{i+1} n={int(n)}' for i, n in enumerate(t.n)], fontsize=10)
        ax.figure.colorbar(image, ax=ax, fraction=.04, pad=.03, label='Fracción con motivo')
        return ('Cuatro salas, ninguna verdad natural', '381 episodios anfitrión; 12 motivos para clustering Jaccard, k=4 fijo.',
                ('Versión móvil: se muestran 6 de los 12 motivos; asignaciones idénticas. ' if mobile else '') + 'Comparar con distancia alternativa y baseline de marginales permutadas.',
                'Heatmap de proporciones de motivos por grupo propuesto, con número de episodios y escala de cero a uno.')
    if name == 'bob-distances':
        c = claims['D85-C']; values = c['permuted_marginals_silhouettes']
        ax.hist(values, bins=8, color=BLUE, edgecolor='white', label='Marginales permutadas')
        ax.axvline(c['silhouette'], color=RED, linewidth=2, label='Motivos observados')
        ax.set(xlabel='Silueta Jaccard (k=4)', ylabel='Réplicas exploratorias'); ax.legend(fontsize=9)
        return ('¿La estructura supera una base simple?', '381 episodios; 30 permutaciones independientes por motivo, preservando sus prevalencias.',
                f'ARI Jaccard vs Euclídea = {c["distance_ARI"]:.3f}. No es una prueba confirmatoria ni prueba de cuatro estilos naturales.',
                'Distribución de silueta bajo marginales permutadas y línea para datos observados; la nota contrasta distancia alternativa.')
    if name == 'bob-trees':
        t = tables['trees']; y = np.arange(len(t)); ax.barh(y, 100*t.fraction, color=BLUE)
        ax.set_yticks(y, [f'{r.group}\nn={r.denominator}' for r in t.itertuples()]); ax.set(xlim=(0, 100), xlabel='TREE o TREES registrado (%)')
        for i, r in enumerate(t.itertuples()): ax.text(3, i, f'{r.count}/{r.denominator}', color='white', va='center')
        return ('La afirmación «todos» bajo prueba', 'Episodios separados por anfitrión e invitados; unión de TREE y TREES.',
                'Ausencia de etiqueta no prueba ausencia visual de todo tipo de árbol; PALM_TREES no se incluye en esta definición.',
                'Dos barras de fracción de episodios con TREE o TREES; se muestran conteos y alcance exacto de la etiqueta.')
    if name == 'bob-snow':
        c = claims['D85-D2']; ax.bar(['Con nieve', 'Sin nieve'], [c['with_snow'], c['without_snow']], color=[BLUE, RED]); ax.set_ylabel('Episodios del anfitrión')
        return ('Montaña no define nieve por sí sola', f'{c["mountain_episodes"]} episodios con MOUNTAIN o MOUNTAINS; nieve = SNOW o SNOWY_MOUNTAIN.',
                'Conteos del archivo de etiquetas; buscar los contraejemplos antes de generalizar.',
                'Conteos de episodios con y sin nieve registrados, condicionados a que exista etiqueta de montaña.')
    if name == 'bob-selection':
        t = tables['selection_curve']; ax.plot(t.episodes, t.greedy_motifs, color=BLUE, marker='o', label='Cobertura voraz'); ax.plot(t.episodes, t.chronological_motifs, color=RED, ls='--', label='Primeros episodios')
        ax.set(xlim=(1, 12), ylim=(0, claims['D85-A']['possible_motifs']), xlabel='Espacios de la exposición', ylabel='Motivos distintos cubiertos'); ax.legend(fontsize=9)
        return ('Una exposición con espacio limitado', 'Hasta 12 episodios del anfitrión; 64 etiquetas sin banderas de autoría.',
                'Baseline cronológico y 100 selecciones aleatorias en tablas. Cobertura no significa equilibrio, calidad ni demanda.',
                'Curvas de cobertura de motivos al elegir hasta doce episodios: algoritmo voraz y baseline cronológico.')
    if name == 'bob-id':
        t = tables['id_sensitivity']; ax.bar([0, 1, 2], t.ARI_vs_clean_euclidean, color=[BLUE, GOLD, RED]); ax.set_xticks([0, 1, 2], ['Sin ID', 'Temporada/31', 'Temporada']); ax.set(ylim=(-.12, 1.1), ylabel='ARI contra grupos sin temporada'); ax.axhline(0, color='#555', linewidth=.7)
        return ('Cuando el identificador decide', '381 episodios; misma Euclídea, muestra y k=4; cambia sólo escala de temporada.',
                'Control negativo deliberado. Siluetas con distancias diferentes no acreditan mejor calidad artística.',
                'Estabilidad ARI al añadir temporada normalizada o sin escalar. La referencia conserva sólo motivos.')
    raise ValueError('Figura desconocida: ' + name)


FIGURES = {
    'uci-retail': [('retail-ranking', ['D31-A', 'D31-E'], 'ranking'), ('retail-missing', ['D31-B'], 'denominators'), ('retail-duplicates', ['D31-E'], 'duplicate_sensitivity')],
    'nba-elo': [('nba-calibration', ['D10-E'], 'calibration'), ('nba-phases', ['D10-D2'], 'phases'), ('nba-series', ['D10-D1'], 'series'), ('nba-scores', ['D10-E'], 'score_sensitivity')],
    'bob-ross-elementos': [('bob-prevalence', ['D85-B'], 'prevalence'), ('bob-clusters', ['D85-C'], 'profiles'), ('bob-distances', ['D85-C'], 'null_silhouettes'), ('bob-trees', ['D85-D1'], 'trees'), ('bob-snow', ['D85-D2'], 'snow_counterexamples'), ('bob-selection', ['D85-A'], 'selection_curve'), ('bob-id', ['D85-E'], 'id_sensitivity')]}


def export(case, tables, claims, manifest, out, code_hash):
    figures = []
    for name, questions, table in FIGURES[case]:
        variants = []
        for mobile in [False, True]:
            variant = 'mobile' if mobile else 'projection'
            plt.rcParams['font.size'] = 11 if mobile else 12
            fig, ax = plt.subplots(figsize=(5.4, 7.2) if mobile else (11, 7.2))
            title, denominator, note, alt = draw(name, ax, tables, claims, mobile)
            period = 'noviembre 2011' if case == 'uci-retail' else 'temporada 2014–2015' if case == 'nba-elo' else 'S01–S31; sin fechas de emisión verificadas'
            width = 56 if mobile else 116
            fig.suptitle(textwrap.fill(title, 35 if mobile else 80), x=.06, ha='left', fontsize=15 if mobile else 18, fontweight='bold', y=.98)
            subtitle = '\n'.join(textwrap.wrap(denominator, width))
            fig.text(.06, .89, subtitle, va='top', fontsize=10 if mobile else 11)
            footer = f'{period} · {manifest["attribution"]}\n{note}\nSnapshot {manifest["snapshot_sha256"][:12]} · código {code_hash[:12]} · ADL V3'
            footer_lines = '\n'.join(textwrap.fill(line, width) for line in footer.splitlines())
            fig.text(.06, .025, footer_lines, va='bottom', fontsize=8 if mobile else 9)
            # Explicit room for all source notes and rotated labels at both sizes.
            fig.subplots_adjust(left=.27 if mobile and name in ['nba-series', 'bob-prevalence'] else .20 if mobile else .13,
                                right=.82 if mobile and name == 'bob-clusters' else .94, top=.76, bottom=.42 if mobile else .30)
            fig.canvas.draw(); renderer = fig.canvas.get_renderer(); bounds = fig.bbox
            clipped = []
            # Matplotlib allocates locator labels beyond the view interval but does not draw them.
            undrawn_ticks = set()
            for axis in fig.axes:
                for coordinate, limits in [(axis.xaxis, axis.get_xlim()), (axis.yaxis, axis.get_ylim())]:
                    lo, hi = sorted(limits)
                    for tick in coordinate.get_major_ticks() + coordinate.get_minor_ticks():
                        if not lo <= tick.get_loc() <= hi:
                            undrawn_ticks.update([tick.label1, tick.label2])
            for text in fig.findobj(Text):
                if text not in undrawn_ticks and text.get_visible() and text.get_text():
                    box = text.get_window_extent(renderer)
                    if box.x0 < -1 or box.y0 < -1 or box.x1 > bounds.width+1 or box.y1 > bounds.height+1:
                        clipped.append(text.get_text())
            require(not clipped, f'Texto cortado en {name}/{variant}: {clipped}')
            prefix = out / f'{name}-{variant}'
            fig.savefig(prefix.with_suffix('.png'), dpi=144, metadata={'Software': 'AI Discovery Labs V3'})
            fig.savefig(prefix.with_suffix('.svg'), metadata={'Date': None, 'Creator': 'AI Discovery Labs V3', 'Description': alt})
            variants.append(dict(variant=variant, png=prefix.name+'.png', svg=prefix.name+'.svg',
                denominator=denominator, note=note,
                png_sha256=sha(prefix.with_suffix('.png')), svg_sha256=sha(prefix.with_suffix('.svg')),
                width=int(fig.get_figwidth()*144), height=int(fig.get_figheight()*144),
                text_bounds_pass=True, rendered_review='REQUIRES_OBSERVED_REVIEW'))
            plt.close(fig)
        figures.append(dict(id=name, question_ids=questions, title=title, denominator=denominator, period=period,
            source_url=manifest['source_url'], license=manifest['license'], source_sha256=manifest['snapshot_sha256'],
            code_sha256=code_hash, table='gold/'+table+'.csv', table_sha256=sha(out.parent/'gold'/f'{table}.csv'),
            alt=alt, note=note, variants=variants))
    write(out / 'figures.json', figures)
    return figures
