#!/usr/bin/env python3
"""Combine reviewed evidence, candidate bibliography, technical runs and editorial ranking."""
from pathlib import Path
import collections,json,sys,urllib.parse
from build_catalog import BASE,read,write,export_csv

def main():
    sources=read(BASE/'catalog/sources.json');questions=read(BASE/'catalog/questions.json')
    log=read(BASE/'evidence/search_log.json');search={x['source_id']:x for x in log}
    # These are manually screened search positions, not externally reproduced results.
    select={'uci-retail':[1,2,6],'nyc-ratas':[2,8,9],'nyc-restaurantes':[5,6,7],'nasa-exoplanetas':[0,4,5],'noaa-ghcn':[5,7,8],'dracor-teatro':[1,4,9],'statsbomb-futbol':[2,6,9],'ecobici-viajes':[1,2,4],'ecobici-gbfs':[1,3,4],'gbif-biodiversidad':[0,1,2],'gutenberg-quijote':[0,1,2],'openflights-red-aerea':[1,2,3],'pgnmentor-ajedrez':[1,2,3],'apple-apps':[2,6,8],'loc-prensa-historica':[0,1,2],'aist-dance':[4,5,8]}
    records=[];reviewed=[]
    for line in (BASE/'imports/reviewed_examples.txt').read_text().splitlines():
        if not line.strip():continue
        sid,title,author,url,question,method,result,visual,limits,match,evidence=line.split('|')
        # A bibliography entry can document an existing notebook without verifying its output.
        reviewed.append(dict(source_id=sid,title=title,author=author,url=url,question=question,methodology=method,result=result,visualizations=visual,limitations=limits,dataset_match=match,evidence=evidence,status='DOCUMENTADO_EXTERNAMENTE',reproduced=False,checked_on='2026-11-16',evidence_scope='Lectura de la fuente primaria indicada; la documentación de un método no verifica sus resultados numéricos.'))
    for s in sources:
        sid=s['id'];known=[x for x in reviewed if x['source_id']==sid]
        for e in known:records.append(e)
        missing=max(0,3-len(known));hits=search[sid]['hits'];indices=select.get(sid,list(range(len(hits))))
        seen={urllib.parse.urlsplit(x['url']).path.rstrip('/') for x in known}
        for i in indices:
            if missing<=0:break
            if i>=len(hits):continue
            h=hits[i];path=urllib.parse.urlsplit(h['url']).path.rstrip('/')
            if path in seen:continue
            seen.add(path)
            records.append(dict(source_id=sid,title=h['title'],author='PENDIENTE: verificar autoría en fuente primaria',url=h['url'],question='PENDIENTE: extraer pregunta real del antecedente; el título no basta.',methodology='PENDIENTE: leer método o notebook, verificar versión y unidad.',result='PENDIENTE: localizar tabla/figura y distinguir resultado publicado de reproducción propia.',visualizations='PENDIENTE: inspeccionar figuras y vínculo con la pregunta.',limitations='PENDIENTE: revisar cobertura, denominadores y correspondencia del dataset; puede ser sólo documentación o un corpus relacionado.',dataset_match='PENDIENTE: cotejar IDs y edición; no asumir identidad por tema.',evidence='evidence/search_log.json; '+h['locator'],status='PROPUESTO',reproduced=False,checked_on='2026-11-16',evidence_scope='Candidato de búsqueda; NO cuenta como ejemplo exitoso ni antecedente ya revisado.'))
            missing-=1
        for _ in range(missing):records.append(dict(source_id=sid,title='Antecedente no localizado en búsqueda acotada',author='PENDIENTE',url=None,question='PENDIENTE',methodology='PENDIENTE',result='PENDIENTE',visualizations='PENDIENTE',limitations='No encontrado en esta consulta no prueba inexistencia. Reintentar en idioma original, bibliografía del productor y repositorios académicos.',dataset_match='PENDIENTE',evidence='evidence/search_log.json',status='NO_ENCONTRADO',reproduced=False,checked_on='2026-11-16'))
    byid={s['id']:s for s in sources}
    profiles=BASE/'evidence/original_file_profiles.json'
    if profiles.exists():
        for measured in read(profiles):
            byid[measured['source_id']]['universe_size']={'status':'MEASURED_ORIGINAL_FILE','value':measured,'limitation':'No equivale al tamaño de todos los archivos del productor ni garantiza representatividad.'}
    for s in sources:
        s.setdefault('research_idea_from_original_catalog',s['description'])
        s['description']=f"{s['name']}, producido por {s['publisher']}. Unidad declarada: {s['grain']}. Cobertura declarada: {s['coverage']}. Recurso de tipo {s['resource_type']}; el estado de prueba determina qué se comprobó realmente."
    for p in sorted((BASE/'output').glob('*/results.json')):
        r=read(p);s=byid[r['source_id']];m=read(BASE/'pilots'/s['id']/'data/manifest.json')
        evidence_path='evidence/pilot_runs/'+s['id']+'.json'
        if read(BASE/evidence_path)!=r:raise ValueError('La ejecución difiere de la evidencia fijada; revisar antes de regenerar catálogo.')
        s['evidence_status']='TECHNICALLY_VERIFIED';s['quality']={'status':'PROFILE_EXECUTED','path':evidence_path,'observed':r['quality'],'limits':r['inference']}
        s['start_date_verified']={'status':'VERIFIED_IN_SNAPSHOT','value':r.get('date_min','PENDIENTE: el dataset de episodios no trae fechas de emisión verificadas.')}
        s['end_date_verified']={'status':'VERIFIED_IN_SNAPSHOT','value':r.get('date_max','PENDIENTE: episodio no equivale a fecha de emisión.')}
        if 'date_min' not in r:s['start_date_verified']['status']=s['end_date_verified']['status']='PENDIENTE'
        s['snapshot']['technical_results']=evidence_path;s['technical_routes']=r['question_ids']
        s['snapshot']['column_count']=len(m['columns']);s['snapshot']['file_count']=1;s['snapshot']['size_MB_decimal']=m['snapshot_bytes']/1e6
        if s['id']=='uci-retail':
            s['quality']['metadata_disagreement']='La metadata UCI declara que no hay faltantes, pero el snapshot presenta CustomerID ausente. Se conserva indicador de ausencia; los controles observados prevalecen sobre la etiqueta del portal.'
            s['last_updated_verified']={'status':'PRODUCER_METADATA_VERIFIED','value':'Mon Oct 21 2024','scope':'Campo last_updated de la API UCI capturada en evidence/uci-metadata.json; no es el fin temporal de transacciones.'}
        for q in questions:
            if q['id'] in r['question_ids']:
                q.update(status='TECHNICALLY_EXECUTED',execution_evidence=evidence_path,blockers=['PENDIENTE: ensayo humano de 45 minutos y revisión docente independiente.'],required_additional_data='Ninguna para el alcance descriptivo acotado del piloto; consultar los límites.',pilot_scope=r['routes'].get(q['route']),pilot_inference_limits=r['inference'])
        records.append(dict(source_id=s['id'],title='Piloto V2 · '+s['name'],author='AI Discovery Labs / JC',url='pilots/'+s['id']+'/README.md',question_ids=r['question_ids'],question='Preguntas ejecutadas: '+', '.join(r['question_ids']),methodology='scripts/run_pilots.py; dos caminos y pruebas adversariales; semilla '+str(r['seed']),result_path=evidence_path,result='Resultados numéricos exactos en results.json; regenerados offline y contrastados por pruebas.',visualizations='Gráfico comparison.png y tablas CSV en el directorio de ejecución.',limitations=r['inference']+' Ensayo humano no realizado.',dataset_match='snapshot_hashed',evidence=evidence_path,status='REPRODUCIDO',reproduced=True,checked_on='2026-11-16',evidence_scope='Experimento didáctico propio ejecutado repetidamente; no réplica numérica de un paper externo.'))
    # Reproduction of pre-existing analyses, independently checked against their original references.
    prior=BASE/'evidence/prior_reproductions.json'
    if prior.exists():
        for r in read(prior):
            if r['status']=='PASS':records.append(dict(source_id=r['source_id'],title=r['title'],author='JC / DataCollectionMov',url=r['source_path'],question=r['question'],methodology=r['command'],result=r['result'],visualizations=r['visualizations'],limitations=r['limitations'],dataset_match='same_snapshot',evidence='evidence/prior_reproductions.json',status='REPRODUCIDO',reproduced=True,checked_on='2026-11-16',evidence_scope='Reejecución de un análisis preexistente; igualdad de métricas y hash de entrada comprobados.'))
    for i,r in enumerate(records,1):r['id']=f'EX{i:03d}'
    write(BASE/'catalog/antecedents.json',records);export_csv(BASE/'catalog/antecedents.csv',records)
    weights={'curiosity_narrative':14,'originality':12,'data_quality_availability':18,'business_social_impact':12,'learning_value':14,'technique_diversity':8,'interesting_results':8,'classroom_reproducibility':10,'execution_maintenance_cost':4}
    boosts={'bob-ross-elementos':(5,4,5,3,5,5,5,5,5),'uci-retail':(5,4,5,5,5,4,5,5,5),'nba-elo':(5,4,5,4,5,4,5,5,5),'nasa-exoplanetas':(5,4,3,4,5,5,4,3,4),'ecobici-viajes':(5,4,3,5,5,5,5,3,3),'nyc-ratas':(5,4,3,5,5,4,5,3,4),'statsbomb-futbol':(5,4,3,5,5,5,5,3,3),'openflights-red-aerea':(5,4,3,4,5,5,4,3,5),'nasa-bolidos':(5,5,3,3,5,4,4,3,5),'gsm8k-examenes':(5,4,3,5,5,4,4,3,3)}
    ranks=[]
    for s in sources:
        access=s['evidence_status'];available=3 if access in ['DATA_SAMPLE','CACHED_SAMPLE'] else 2 if access in ['DOCUMENT_SAMPLE','DOC_ONLY','METADATA_SAMPLE'] else 1
        vals=boosts.get(s['id'],(4,3,available,4,4,3,3,min(available,3),3))
        points=dict(zip(weights,vals));score=round(sum(points[k]*weights[k] for k in weights)/5,2)
        ranks.append(dict(source_id=s['id'],name=s['name'],category=s['macrocategory'],score=score,criteria=points,judgment='EDITORIAL_PROVISIONAL; 1–5, mayor es mejor. No es calidad intrínseca medida ni probabilidad de éxito.',reason=f"{s['name']}: {s['grain']}; evidencia {s['evidence_status']}. Potencial frente a la limitación de {s['resource_type']}; derechos y cobertura se evalúan por separado.",blocked_for_production=not s['ready_for_class'],blocking_reason='PENDIENTE: ensayo humano 45 min; '+('derechos, snapshot y QA de alcance suficiente.' if access!='TECHNICALLY_VERIFIED' else 'revisión docente independiente y ensayo de discusión/cierre.')))
    ranks.sort(key=lambda x:(-x['score'],x['source_id']))
    for i,r in enumerate(ranks,1):r['rank']=i
    tops={}
    for r in ranks:tops.setdefault(r['category'],[]).append(r['source_id'])
    ranking={'weights':weights,'method':'Puntuación editorial explícita, no medición de resultados futuros. Evidencia de muestra puntúa máximo 3/5 en disponibilidad/calidad; los tres snapshots ejecutados puntúan 5 en ese control limitado. El coste incluye mantenimiento y preparación, no sólo CPU. No hay fuentes aprobadas para producción.','ranking':ranks,'top_by_category':{k:v[:3] for k,v in tops.items()},'top10_production_candidates':[r['source_id'] for r in ranks[:10]]}
    write(BASE/'catalog/ranking.json',ranking);export_csv(BASE/'catalog/ranking.csv',ranks)
    write(BASE/'catalog/sources.json',sources);write(BASE/'catalog/questions.json',questions);export_csv(BASE/'catalog/sources.csv',sources);export_csv(BASE/'catalog/questions.csv',questions)
    summary={'sources':len(sources),'questions':len(questions),'questions_revised_from_original':sum(q['original_question'] is not None for q in questions),'new_questions':sum(q['original_question'] is None for q in questions),'source_categories':len({s['macrocategory'] for s in sources}),'source_statuses':dict(collections.Counter(s['evidence_status'] for s in sources)),'question_statuses':dict(collections.Counter(q['status'] for q in questions)),'antecedent_statuses':dict(collections.Counter(r['status'] for r in records)),'public_queries':len(log),'pilot_technical_count':sum(s['evidence_status']=='TECHNICALLY_VERIFIED' for s in sources),'ready_for_class':sum(s['ready_for_class'] for s in sources),'top10':ranking['top10_production_candidates'],'unfulfilled':['Ficha física, licencia y QA integral de las 83 fuentes sin snapshot de piloto.','Al menos tres antecedentes sustantivos revisados por cada fuente cuando existan: los candidatos no cuentan.','Validación de campo de las 507 preguntas diseñadas sin ejecución.','Ensayo humano de 45 minutos y revisión docente independiente para los tres pilotos.'],'anti_overclaim':'Un conteo de registros o un GET correcto no es aprobación pedagógica ni valida representatividad.'}
    write(BASE/'catalog/audit_summary.json',summary)
    print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__':main()
