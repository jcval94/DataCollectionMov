#!/usr/bin/env python3
"""Create immutable DRAFT HF packets from measured evidence; never infer approval."""
import csv
import hashlib
import html
import json
import re
from collections import Counter
from pathlib import Path
from audit import HERE, ROOT, audit

def esc(s): return html.escape(str(s))
def read(p): return json.loads(p.read_text())
def write_once(p,text):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists() and p.read_text()!=text:
        raise ValueError(f'Immutable version differs: {p}; create v02')
    if not p.exists(): p.write_text(text,encoding='utf-8')

def bars(title,labels,series,colors,maximum,unit):
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 {130+len(labels)*55}" role="img" aria-labelledby="t d"><title id="t">{esc(title)}</title><desc id="d">{esc(unit)}; cifras exactas en tabla contigua.</desc><rect width="100%" height="100%" fill="white"/><text x="25" y="30" font-family="sans-serif" font-size="19">{esc(title)}</text>']
    for i,label in enumerate(labels):
        y=65+i*55
        out.append(f'<text x="20" y="{y+12}" font-family="sans-serif" font-size="14">{esc(label)}</text>')
        for j,values in enumerate(series):
            val=values[i];yy=y+j*15
            out.append(f'<rect x="250" y="{yy}" width="{550*val/maximum}" height="13" fill="{colors[j]}"/><text x="{260+550*val/maximum}" y="{yy+12}" font-family="sans-serif" font-size="12">{val}</text>')
    out.append(f'<text x="25" y="{105+len(labels)*55}" font-family="sans-serif" font-size="13">{esc(unit)} · escala desde cero; no categorías artísticas</text></svg>')
    return '\n'.join(out)

def main():
    audit_result,rows=audit()
    o1=read(HERE/'results/o1_results.json')
    o2=read(HERE/'progressive_results/br09_o2.json')
    claims=list(csv.DictReader((HERE/'evidence/source_claim_matrix.csv').open()))
    coverage=Counter('PENDIENTE' if r['independent_status']=='PENDING_INDEPENDENT_VERIFICATION' else
                     'PARCIAL' if 'PARTIAL' in r['independent_status'] else 'REVISADA' for r in claims)
    cols=sorted(audit_result['column_totals'],key=audit_result['column_totals'].get,reverse=True)[:12]
    host=[sum(r['flags'][c] for r in rows if not r['guest']) for c in cols]
    guest=[sum(r['flags'][c] for r in rows if r['guest']) for c in cols]
    topchart=bars('Etiquetas frecuentes: anfitrión e invitados',cols,[host,guest],['#225d69','#a7482f'],400,'Presencias · azul 381 GUEST=0 · rojo 22 GUEST=1; grupos de distinto tamaño')
    covlabels=['REVISADA','PARCIAL','PENDIENTE']
    covchart=bars('Cobertura de revisión independiente',covlabels,[[coverage[k] for k in covlabels]],['#225d69'],54,'54 registros; revisada no significa confirmada')
    k4=next(r for r in o1['BR-09']['k_grid'] if r['k']==4)
    groupchart=bars('k=4 incluye tres filas vacías',['Grupo 1','Grupo 2','Grupo 3','Grupo 4 · 3 filas vacías'],[k4['sizes']],['#225d69'],250,'381 episodios GUEST=0; agrupamiento descriptivo sin IC de verdad artística')
    changechart=bars('Sensibilidad de asignaciones con matching',['Distancia Euclídea','Retirar árbol','Omitir una temporada'],[[179,75,0]],['#a7482f'],381,'Cambios sobre 381; última fila 0 en los 31 reajustes')
    packets=[
        ('HF-00','ORIENTATION',None,'Brújula y auditoría retrospectiva',
         'El CSV auditado contiene 403 episodios, 67 indicadores y 3,221 marcas positivas. PERSON sí existe y hay dos títulos repetidos; tres filas tienen todas sus etiquetas en cero. Desde el paquete de entrada pasamos de afirmaciones recibidas a conteos, hashes y contradicciones documentadas. Aún no hay un insight sorprendente confirmado en este checkpoint de auditoría. Recomiendo priorizar secuencias, asociaciones y robustez de agrupamiento, conservando color como ruta bloqueada por permisos. Este paquete se preparó retrospectivamente al integrarse el nuevo protocolo HF: no acredita una decisión humana anterior a la ejecución. Las fuentes históricas siguen parcialmente pendientes y las etiquetas no validan por sí mismas el contenido de todas las versiones físicas.',
         'Paquete de entrada → auditoría y conciliación de 14 BR/10 H.',
         'Aún no hay un insight sorprendente confirmado en este checkpoint de auditoría.',
         [('top_tags.svg',topchart,'BR-05',403,'403 episodios; 381 y 22 en barras distintas',False),
          ('review_coverage.svg',covchart,'BR-11',54,'54 registros de evidencia, no fuentes independientes',True)],
         {'columns':cols,'host_counts':host,'guest_counts':guest,'review_coverage':dict(coverage)},
         '¿Mantenemos como prioridad las tres rutas ejecutables de CSV y posponemos color hasta resolver permisos?',
         ['Mantener tres rutas de CSV','Reorientar prioridades'],
         'Mantener tres rutas de CSV'),
        ('HF-01','RESEARCH_FEEDBACK','HF-00/v01','Primeros resultados O1',
         'Las O1 ya tienen scripts y siete artefactos replicados byte a byte. Las cuatro pruebas de secuencia no respaldan inhibición tras Holm; ausencia de repeticiones no equivale a programación deliberada. Cabañas e invierno se asocian en 381 episodios y el control por temporada conserva la señal, sin identificar su causa. El resultado metodológico más claro es que tres filas vacías forman un grupo en todos los k probados de 2 a 6: un patrón de datos puede parecer un estilo. Frente a HF-00 pasamos de datos conciliados a resultados y nulos medidos. Recomiendo revisar primero ese artefacto. Este informe es retrospectivo, no una aprobación anterior; siguen pendientes validación visual y verificación independiente de anotaciones.',
         'HF-00 sin experimentos → tres O1 exploratorias, dos de alcance parcial.',
         'Las tres filas vacías forman un grupo para todos los k=2…6 probados.',
         [('sequence_null.svg',(HERE/'figures/sequence_null.svg').read_text(),'BR-14',403,'403 episodios y 372 transiciones dentro de temporada',True),
          ('empty_group.svg',groupchart,'BR-09',381,'381 GUEST=0; tamaños 236/106/36/3',True)],
         {'sequence':o1['BR-14'],'cabin_winter':o1['BR-07']['cabin_winter'],'cluster_k_grid':o1['BR-09']['k_grid']},
         '¿Qué resultado tiene mayor valor para la siguiente revisión: artefacto de agrupamiento o composición cabañas–invierno?',
         ['Artefacto de agrupamiento','Composición cabañas–invierno'],
         'Artefacto de agrupamiento'),
        ('HF-02','O2_PRIORITY_DECISION','HF-01/v01','Revisión actual de la profundización',
         'DR-05a encontró una razón medible para profundizar agrupamiento: filas vacías crean una sala aparente y las métricas discrepan. Los cálculos de sensibilidad se ejecutaron con el plan leído al iniciar la sesión, antes de integrarse PR #17. Se conservan como evidencia, sin registrarlos como una decisión humana: cambiar a Euclídea mueve 179 de 381 asignaciones, retirar árbol mueve 75 y omitir una temporada no mueve ninguna en 31 reajustes. La representación importa más que esa perturbación temporal específica. Frente a HF-01 añadimos controles, pero su promoción editorial sigue retenida hasta HF-02. Recomiendo priorizar validación de anotaciones y algoritmos antes de afirmar estilos. Faltan permisos para validación humana e imágenes y QA visual del informe.',
         'HF-01/DR-05a → controles ya calculados, decisión humana actual pendiente.',
         'Hay desacuerdo entre métricas y estabilidad frente a las 31 omisiones de temporada.',
         [('cluster_sensitivity.svg',(HERE/'figures/cluster_sensitivity.svg').read_text(),'BR-09',381,'381 total; sensibilidad 378 tras excluir tres vacíos',True),
          ('assignment_changes.svg',changechart,'BR-09',381,'381 episodios, matching exacto; 31 reajustes por temporada',True)],
         {'legacy_computed_o2':o2,'publication_status':'WITHHELD_PENDING_HF02','human_response':None},
         '¿Priorizamos BR-09 para revisar anotaciones y comparar algoritmos antes de buscar estilos o color?',
         ['Priorizar BR-09','Aplazar profundización','Reorientar a BR-07'],
         'Priorizar BR-09')
    ]
    shared=ROOT.parents[1]/'shared/templates'
    css=re.search(r'<style>([\s\S]*?)</style>',(shared/'HUMAN_FEEDBACK_REPORT_TEMPLATE.html').read_text()).group(1)
    css+='.chart-scroll{overflow-x:auto}figure img{width:100%;height:auto;min-width:640px}figure{margin:18px 0}.chart-table{overflow:auto}h1{font-size:clamp(1.5rem,4vw,2.4rem)}header.hero{padding-top:20px}.summary-grid{grid-template-columns:1fr}summary{cursor:pointer}'
    for ident,gate,prev,title,summary,delta,surprise,charts,data,question,options,recommended in packets:
        folder=ROOT/'human_feedback'/ident/'v01'
        data_text=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
        write_once(folder/'data/evidence.json',data_text)
        chart_meta=[];figures=[]
        for filename,svg,qid,n,den,adversarial in charts:
            write_once(folder/'charts'/filename,svg)
            meta={'chart_id':ident+'-'+filename.removesuffix('.svg'),'title':re.search(r'<title[^>]*>(.*?)</title>',svg).group(1),
                  'question_id':qid,'type':'SVG from measured data','chart_path':'charts/'+filename,
                  'data_source':'Walt Hickey/FiveThirtyEight; derived results','dataset_hash':audit_result['sha256'],
                  'evidence_ref':'data/evidence.json','code_ref':'../../../research/build_feedback.py',
                  'population':'Snapshot de etiquetas; '+den,'n':n,'denominator':den,
                  'unit':'episodios, marcas o registros de evidencia según figura',
                  'baseline':'Cero para barras; nulo intra-temporada para secuencia; Jaccard y n=381 para sensibilidad',
                  'uncertainty':'Banda nula 95% en secuencia; k-grid y filtros como sensibilidad; conteos exactos del snapshot sin IC muestral',
                  'alt_text':re.search(r'<title[^>]*>(.*?)</title>',svg).group(1),
                  'rights_status':'DATA_ONLY','mobile_checked':False,'desktop_checked':False,'adversarial':adversarial}
            chart_meta.append(meta)
            figures.append(f'<figure><div class="fig-top"><h3>{esc(meta["title"])}</h3></div><div class="chart-scroll" tabindex="0" aria-label="Gráfica desplazable"><img src="charts/{filename}" alt="{esc(meta['alt_text'])}"></div><figcaption>{esc(den)}. {esc(meta["baseline"])}. {esc(meta["uncertainty"])}. <a href="data/evidence.json">Datos y tabla numérica JSON</a>. DATA_ONLY; legibilidad móvil/desktop pendiente.</figcaption></figure>')
        insight={'id':ident+'-I1','headline':surprise,'status':'VERIFIED' if ident!='HF-00' else 'INCONCLUSIVE',
                 'how':'Auditoría del snapshot y protocolo exploratorio reproducible; ver datos y scripts.',
                 'why':'Separar evidencia de afirmaciones heredadas, prevalencias y decisiones de representación.',
                 'what_for':'Orientar el siguiente experimento sin promover estilos ni mecanismos causales.',
                 'limitations':'Anotaciones sin validación visual; fuentes históricas parciales; no novedad mundial demostrada.',
                 'evidence_refs':['data/evidence.json']}
        checkpoint={'schema_version':'human-feedback-checkpoint-1.0','checkpoint_id':ident,
                    'dataset_id':'bob-ross-elementos','version':1,'created_at':'2026-11-19',
                    'phase':'Fase 1; retrospective packet / current review','status':'DRAFT',
                    'source_commit':'2f2bf8ec3647582b48ff36168dc74c320ace4310',
                    'previous_checkpoint':prev,'report_path':'report.html','report_starts_with_summary':True,
                    'executive_summary':{'summary':summary,'delta':delta,'surprise':surprise,
                                         'recommendation':recommended,'limitation':'QA visual pendiente; anotación no validada.'},
                    'question_ids':sorted({c['question_id'] for c in chart_meta}),'dataset_hash':audit_result['sha256'],
                    'changes_since_prior':[{'description':delta,'previous':'Entry Pack' if prev is None else prev,
                                             'current':title,'impact':'Evidencia concreta para revisión, sin aprobación inferida',
                                             'evidence_ref':'data/evidence.json'}],
                    'insights':[insight],'charts':chart_meta,
                    'user_questions':[{'id':ident+'-Q1','question':question,'options':options,
                                       'recommended_option':recommended,'reason':'Mayor evidencia disponible y coste de CPU bajo; no compra ni scraping.',
                                       'impact_if_postponed':'Se conservan cálculos; no se promueve otra O2 ni se inicia audiovisual.',
                                       'human_response':None,'responded_at':None}],
                    'recommendation':{'proposed_action':recommended,'default_action':'Conservar resultados y esperar decisión; sin nueva promoción O2',
                                      'next_action':'Revisión de evidencia y QA visual antes de ampliar',
                                      'prerequisites':['Decisión HF-02 para promoción O2','Permisos para nuevas imágenes','QA visual']},
                    'human_gate':gate,'decision_status':'PENDING','human_approval_ref':None,
                    'qa':{'summary_first':True,'chart_provenance_checked':True,'uncertainty_checked':True,
                          'mobile_checked':False,'desktop_checked':False,'keyboard_checked':False,
                          'references_resolve':True,'has_adversarial_review':True,'no_unverified_surprise':True}}
        write_once(folder/'checkpoint.json',json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n')
        feedback=f'# {ident} v01 · feedback PENDING\n\nCreación retrospectiva del paquete; no hubo respuesta ni aprobación humana registrada. Consulta PROTOCOL_TRANSITION.md.\n\n{question}\n\nOpciones: '+ ' / '.join(options)+f'. Recomendación: {recommended}.\n\nCoste: CPU local; imágenes requieren resolver permisos. Si se pospone, conservamos resultados y no promovemos otra O2. Respuesta: PENDING. Fecha de respuesta: ninguna. human_approval_ref: null.\n'
        write_once(folder/'feedback.md',feedback)
        table='<table><tr><th>Antes</th><th>Ahora</th><th>Impacto</th></tr><tr><td>'+esc(prev or 'Paquete de entrada')+'</td><td>'+esc(delta)+'</td><td>Decisión PENDING; cálculos no equivalen a aprobación</td></tr></table>'
        report=f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Bob Ross · {ident} v01</title><style>{css}</style></head><body><main class="wrap"><header class="hero"><div class="eyebrow">AI Discovery Labs · Bob Ross · {ident}</div><h1>{esc(title)}</h1><p>19-11-2026 · v01 · DRAFT · decisión PENDING</p></header>
<section class="paper summary" aria-labelledby="summary-title"><h2 id="summary-title">Resumen ejecutivo</h2><p class="lead">{esc(summary)}</p><p class="note"><strong>Recomendación:</strong> {esc(recommended)}. No se registra aprobación humana.</p></section>
<section class="paper"><h2>Qué cambió</h2><div class="table-scroll">{table}</div></section>
<section class="paper"><h2>Hallazgo y límite</h2><p>{esc(surprise)}</p><p>Resultado descriptivo del snapshot/método; no inferir estilos, intención ni salud. <a href="data/evidence.json">Cifras y evidencia</a>.</p></section>
<section class="paper"><h2 id="charts-title">Gráficas de evidencia y sensibilidad</h2>{''.join(figures)}<details><summary>Tabla alternativa y procedencia</summary><pre>{esc(data_text)}</pre></details></section>
<section class="paper"><h2>Cómo, por qué y para qué</h2><p><strong>CÓMO:</strong> CSV auditado y transformaciones declaradas, nulos condicionados, correcciones múltiples y controles; código en research/. <strong>POR QUÉ:</strong> los vacíos, prevalencias y representación producen patrones distintos. <strong>PARA QUÉ:</strong> escoger qué vale la pena comprobar y enseñar con incertidumbre.</p></section>
<section class="paper"><h2>Una pregunta para JC</h2><p>{esc(question)}</p><p>Opciones: {esc(' / '.join(options))}. Recomiendo {esc(recommended)}. Coste de continuar: CPU local y revisión; no se autoriza descarga de imágenes. Si se aplaza, se conservan resultados sin nueva promoción O2.</p><p>Respuesta: PENDING. <a href="feedback.md">Registro de feedback</a>.</p></section>
<section class="paper"><h2>Evidencia y siguiente decisión</h2><p>Continuar revisión de datos vacíos/algoritmos solo dentro del alcance autorizado. HF-02 sigue pendiente y el audiovisual bloqueado. Este paquete aún requiere QA visual a 360px/1280px y teclado.</p><p><a href="../../../research/PROTOCOL_TRANSITION.md">Transición de protocolo PR17</a> · <a href="../../../research/README.md">Informe científico</a> · <a href="../../../research/QA.md">QA y límites</a> · <a href="checkpoint.json">Metadatos del checkpoint</a> · <a href="../../../research/build_feedback.py">Generador</a>.</p><p>SHA-256 del dataset: <code>{audit_result['sha256']}</code>. Atribución: Walt Hickey/FiveThirtyEight, CC BY 4.0; gráficos propios derivados de etiquetas, sin pinturas ajenas. Versión v01: primera entrega de este hito, retrospectiva; no inventa versión aprobada previa.</p></section></main></body></html>'''
        write_once(folder/'report.html',report)
        print(ident,'DRAFT / PENDING',len(summary.split()),'words')
    print('No HF-03/HF-04 fabricated; no human response inferred.')

if __name__=='__main__':main()

