#!/usr/bin/env python3
"""A small descriptive pilot; no model calls and no claims about artistic intent."""
import csv
import hashlib
import io
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
URL='https://raw.githubusercontent.com/fivethirtyeight/data/master/bob-ross/elements-by-episode.csv'

def main():
    req=urllib.request.Request(URL,headers={'User-Agent':'DataCollectionMov-discovery-pilot/1.0 (+https://github.com/jcval94/DataCollectionMov)'})
    with urllib.request.urlopen(req,timeout=20) as response:data=response.read(1024*1024+1)
    if len(data)>1024*1024:raise ValueError('Dataset exceeds the bounded 1 MiB download')
    rows=list(csv.DictReader(io.StringIO(data.decode('utf-8-sig'))))
    if not rows or len({r['EPISODE'] for r in rows})!=len(rows):raise ValueError('Empty dataset or duplicate episode IDs')
    cols=['TREE','TREES','MOUNTAIN','MOUNTAINS','GUEST']
    if any(r[c] not in ('0','1') for r in rows for c in cols):raise ValueError('Missing/nonbinary selected label')
    def counts(subset):
        n=len(subset)
        tree=lambda r:r['TREE']=='1' or r['TREES']=='1'
        mountain=lambda r:r['MOUNTAIN']=='1' or r['MOUNTAINS']=='1'
        t=sum(tree(r) for r in subset);m=sum(mountain(r) for r in subset);both=sum(tree(r) and mountain(r) for r in subset)
        return dict(episodes=n,with_tree=t,with_mountain=m,with_both=both,
                    p_tree=t/n,p_tree_given_mountain=both/m if m else None,
                    p_tree_given_no_mountain=(t-both)/(n-m) if n!=m else None)
    result=dict(source_url=URL,captured_at_utc=datetime.now(timezone.utc).isoformat(timespec='seconds'),sha256=hashlib.sha256(data).hexdigest(),hash_scope='complete_response',bytes=len(data),definitions=dict(tree='TREE == 1 OR TREES == 1',mountain='MOUNTAIN == 1 OR MOUNTAINS == 1'),checks=dict(unique_episode_ids=True,selected_labels_binary_and_nonmissing=True),all_episodes=counts(rows),excluding_guest=counts([r for r in rows if r['GUEST']=='0']),interpretation='Descriptive co-occurrence of human-coded labels; no causal claim or inference about the painter’s intention.')
    out=ROOT/'examples/bob_ross_discovery';out.mkdir(parents=True,exist_ok=True)
    (out/'metrics.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    n=result['all_episodes'];g=result['excluding_guest']
    lines=['# Piloto: ¿qué suele acompañar a una montaña en Bob Ross?','',
    'Este ejemplo ya está **calculado** sobre el CSV completo recuperado. Las demás propuestas de la guía siguen siendo preguntas de investigación. No se ejecutó un modelo para producir estos conteos.','',
    f"Fuente: [FiveThirtyEight]({URL}). Captura UTC: `{result['captured_at_utc']}`. Hash SHA-256 completo en [metrics.json](metrics.json).",'',
    'Definimos árboles como `TREE OR TREES` y montañas como `MOUNTAIN OR MOUNTAINS`; cada episodio se cuenta una vez. No se interpreta `TREES` como una cantidad de árboles.','',
    '| Medida descriptiva | Resultado |','| --- | ---: |',
    f"| Episodios | {n['episodes']} |",f"| Con árbol(es) | {n['with_tree']} |",f"| Con montaña(s) | {n['with_mountain']} |",f"| Con ambos | {n['with_both']} |",f"| Árboles entre episodios con montañas | {n['with_both']} / {n['with_mountain']} = {n['p_tree_given_mountain']:.1%} |",f"| Árboles entre episodios sin montañas | {n['with_tree']-n['with_both']} / {n['episodes']-n['with_mountain']} = {n['p_tree_given_no_mountain']:.1%} |",'',
    'La pregunta útil es si la coocurrencia aporta información adicional, dado que los árboles ya son muy frecuentes en el conjunto. La tabla describe esta edición del dataset; no demuestra que una montaña cause la elección de árboles.','',
    f"Como comprobación de sensibilidad, al excluir episodios marcados `GUEST`, quedan {g['episodes']} episodios y la frecuencia de árboles entre los que tienen montañas es {g['p_tree_given_mountain']:.1%}. El detalle conserva numeradores y denominadores.",'',
    'Verificaciones: identificadores de episodio únicos y variables seleccionadas binarias, sin faltantes. La codificación visual procede de terceros; no se volvió a revisar cada episodio ni se hizo una búsqueda de todas las asociaciones posibles.','',
    'Siguiente trabajo con IA: contrastar una muestra de etiquetas con las imágenes de los mismos episodios, conservar desacuerdos y revisar si el patrón depende de estación, paisaje o codificador. Esa revisión visual está pendiente.','',
    'Reproducir desde la raíz:','', '```bash','python scripts/analyze_bob_ross_pilot.py','```','']
    (out/'README.md').write_text('\n'.join(lines))
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
