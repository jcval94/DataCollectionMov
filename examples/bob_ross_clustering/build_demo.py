#!/usr/bin/env python3
"""Build a single classroom HTML from computed references; no network or API key."""
import base64
import json
from pathlib import Path

import pandas as pd

HERE=Path(__file__).resolve().parent


def build():
    report=json.loads((HERE/'reference/report.json').read_text())
    gallery=json.loads((HERE/'reference/gallery.json').read_text())
    features=pd.read_csv(HERE/'reference/features.csv').set_index('EPISODE')
    assignments=pd.read_csv(HERE/'reference/assignments.csv').set_index('EPISODE')
    selected=[r['medoid']['episode'] for r in report['rooms']]+['S11E05']
    selected += [features.index[features.sum(axis=1).eq(0)][0]]
    cards=[dict(episode=episode,title=assignments.loc[episode,'TITLE'].strip('"'),
                bits=features.loc[episode].astype(int).tolist()) for episode in selected]
    payload=dict(report=report,gallery=gallery['gallery'],cards=cards,
                 labels=['Árboles','Montañas','Lagos','Ríos','Mar','Nieve','Cascadas','Estructuras','Nubes','Rocas','Sol','Flores'])
    html=(HERE/'template.html').read_text()
    html=html.replace('__DATA__',json.dumps(payload,ensure_ascii=False).replace('<','\\u003c'))
    for token,name in [('__PROFILES__','profiles.svg'),('__DIAG__','k_diagnostics.svg'),('__TRAP__','metadata_trap.svg')]:
        uri='data:image/svg+xml;base64,'+base64.b64encode((HERE/'reference'/name).read_bytes()).decode()
        html=html.replace(token,uri)
    if any(t in html for t in ['__DATA__','__PROFILES__','__DIAG__','__TRAP__']):raise ValueError('Plantilla sin resolver')
    (HERE/'demo.html').write_text(html)
    print('demo.html construido: datos y gráficos incrustados; cuatro reproducciones remotas opcionales.')


if __name__=='__main__':build()
