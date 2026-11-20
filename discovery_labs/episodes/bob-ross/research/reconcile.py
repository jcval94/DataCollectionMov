#!/usr/bin/env python3
"""Build traceability views from the ONE canonical bank; never a second bank."""
import csv
import json
from pathlib import Path
from audit import HERE, ROOT

MAPPING = {
    'H1': ('BR-10', 'MC06', 'Paleta declarada; acceso 1:1 probado, permiso pendiente'),
    'H2': ('BR-01', 'MC11', 'Descriptivo temporal posible; diagnóstico y rodaje no identificados'),
    'H3': ('BR-07', 'MC04', 'Subestudio estructuras/motivos; tiempo 26 min no medido'),
    'H4': ('BR-08', 'MC09', 'GUEST verificado; créditos y selección editorial pendientes'),
    'H5': ('BR-05', 'MC13', 'Auditoría de medición ligada a contraejemplos; nueva anotación bloqueada por derechos'),
    'H6': ('BR-09', 'MC04', 'O1 de motivos parcial; KMeans/Bernoulli y fusión cromática pendientes'),
    'H7': ('BR-10', 'MC06', 'Calibración pigmentos/píxeles como extensión, bloqueada por imágenes'),
    'H8': ('BR-14', 'MC04', 'Secuencia ordinal medible; no cronología de grabación'),
    'H9': ('BR-07', 'MC13', 'Asociación de estructuras; PERSON existe, chimeneas/semántica humana no medidas'),
    'H10': ('BR-13', 'MC12', 'Extensión a recepción; target nuevo externo, no reemplaza target canónico'),
}
WEIGHTS = [15, 10, 20, 15, 15, 10, 10, 5]
DIMENSIONS = ['curiosity','historical_anchor','falsifiability','insight_potential',
              'progressive_research','visual_value','cost_teaching_45min','rights_epistemic']
SCORES = {
    'BR-14': ([5,3,5,4,5,4,5,5], 'OPEN', 'Ordinal Markov + permutación intra-temporada; R1 producción rival'),
    'BR-07': ([4,3,5,4,4,4,5,5], 'OPEN', 'Lift/Fisher/BH + control temporada; R3 ontología y R5 técnica'),
    'BR-09': ([4,2,5,4,4,5,4,5], 'OPEN_PARTIAL', 'Jaccard/Euclídea + bootstrap acuerdo; R3 representación'),
    'BR-10': ([5,4,4,5,5,5,2,2], 'BLOCKED_RIGHTS', 'Join 403/403; falta resolver permiso de paletas e imágenes'),
}


def write_csv(path, rows):
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)


def main():
    bank = json.loads((ROOT/'entry_pack/questions_master.json').read_text())['questions']
    crosswalk = []
    for q in bank:
        matches = [h for h,v in MAPPING.items() if v[0] == q['id']]
        crosswalk.append({
            'canonical_id': q['id'], 'source_DR': 'DR-01;DR-02;DR-03',
            'hypothesis_ids': ';'.join(matches),
            'claim_ids': ';'.join(sorted({MAPPING[h][1] for h in matches})),
            'O1': q['o1'], 'dataset_version': '42045c8b8aaa8296095d6b294927fb9d0f73a57259f59b560c375844c0fe01cf',
            **q['estimand'], 'candidate_model': q['model_name'],
            'separate_statistical_test': q['stat'], 'rivals': q['rival_hypothesis'],
            'integration_scope': ' | '.join(MAPPING[h][2] for h in matches) or 'Sin H equivalente; preservar arco canónico',
            'evidence_status': 'DATA_FEASIBLE' if q['id'] in ('BR-07','BR-09','BR-14') else q['status'],
            'required_rights': 'CC BY 4.0 tags; externos según gates de ficha',
            'prerequisites': q['data'],
            'next_action': 'Ejecutar protocolo O1 parcial' if q['id'] in ('BR-07','BR-09','BR-14') else 'Mantener diseño; resolver fuentes/datos antes de ejecutar',
        })
    write_csv(HERE/'evidence/reconciliation.csv', crosswalk)
    received = ROOT/'entry_pack/research_received'
    review = {
        'E09': ('CORROBORATED_ANNUAL_ONLY', 'C01', 'No episodio de traslado'),
        'E15': ('PARTIAL_INDEX_ONLY', 'C03', 'Recuperador directo 404'),
        'MC01': ('COUNTS_ONLY', 'D02', '345/381 TREE OR TREES; titularidad del mito sin verificar'),
        'MC02': ('COUNTS_CORRECTED', 'D02', '150/381 con montaña; 102/150 con nieve en diccionario OR; no 66%'),
        'MC05': ('TESTIMONY_CORROBORATED', 'C02', 'No inventario completo de versiones'),
        'MC06': ('ANTECEDENT_CONFIRMED_NOT_REPLICATED', 'P03', 'Sin prueba causal ni perceptual'),
        'MC09': ('COUNTS_ONLY', 'D06', '22 GUEST no identifica efecto de autor'),
        'MC11': ('NOT_IDENTIFIED', 'C02', 'Diagnóstico y grabación siguen pendientes'),
        'MC13': ('SCHEMA_CORRECTION', 'D03', 'PERSON sí existe; PERSON=1/403 y 1/381; CHIMNEY no'),
        'ANT01': ('ORIGINAL_URL_REDIRECT', 'A02', 'No replicación de k=10 ni 3224'),
        'ANT02': ('PRIMARY_READ_INTERNAL_CONTRADICTION', 'A01', '3324 abstract vs 3224 dataset; 2014 volume/2015 publication'),
        'ANT05': ('FILTER_REPRODUCED', 'D05', '403/381/378 conciliados'),
        'ANT06': ('PRIMARY_READ_NOT_REPLICATED', 'P03', 'Burnt Umber/Dark Sienna ya observado descriptivamente'),
        'SRC01': ('VERIFIED_SNAPSHOT', 'D01', 'Datos CC BY 4.0; no imágenes'),
        'SRC02': ('SCHEMA_JOIN_VERIFIED_RIGHTS_PENDING', 'P01', '403/403 claves; no ingestión'),
        'SRC04': ('PACKAGE_LICENSE_CONFIRMED', 'P02', 'MIT no resuelve imágenes upstream; no fuente independiente'),
        'SRC05': ('FILTER_REPRODUCED', 'D05', 'No alterar original'),
        'SRC11': ('CONTEXT_ANNUAL_ONLY', 'C01', 'Sin logs de grabación'),
    }
    claims = []
    specs = [('DR-01_timeline_events.csv','event_id','original_url','event'),
             ('DR-03_myths_claims.csv','claim_id','source_url','claim_statement'),
             ('DR-03_antecedents.csv','study_id','source_url','reported_finding'),
             ('DR-02_source_inventory.csv','source_id','url','name')]
    for filename, idkey, urlkey, textkey in specs:
        for r in csv.DictReader((received/filename).open()):
            ident = r[idkey]
            status, ref, gap = review.get(ident, ('PENDING_INDEPENDENT_VERIFICATION','','No usar como hecho verificado en esta ronda'))
            claims.append({'claim_id':ident, 'archive_file':filename, 'source_url':r[urlkey],
                           'as_received_summary':r[textkey], 'independent_status':status,
                           'evidence_ref_SOURCE_REVIEW':ref, 'contradiction_or_gap':gap,
                           'observed_at_local_date':'2026-11-19'})
    write_csv(HERE/'evidence/source_claim_matrix.csv', claims)
    ranks=[]
    for qid,(scores,gate,reason) in SCORES.items():
        ranks.append({'canonical_id':qid,'dimensions_0_to_5':dict(zip(DIMENSIONS,scores)),
                      'score_100':sum(a*b/5 for a,b in zip(scores,WEIGHTS)),
                      'gate':gate,'reason':reason,
                      'compute_cost':'CPU local; sin APIs de pago',
                      'novelty_status':'POTENTIAL_ONLY; revisión bibliográfica no exhaustiva'})
    ranks.sort(key=lambda x:(x['gate']=='BLOCKED_RIGHTS',-x['score_100']))
    (HERE/'evidence/ranking.json').write_text(json.dumps({
        'rubric':'Question Forge 100 points; gates override score',
        'weights':dict(zip(DIMENSIONS,WEIGHTS)), 'selected':ranks,
        'hypothesis_crosswalk':{k:{'canonical_id':v[0],'scope':v[2]} for k,v in MAPPING.items()},
        'not_selected':{q['id']:'Menor factibilidad inmediata o redundancia; diseño conservado' for q in bank if q['id'] not in SCORES},
    },ensure_ascii=False,indent=2)+'\n')
    print(f'{len(crosswalk)} canonical rows; {len(MAPPING)} H mapped once; {len(claims)} evidence records')


if __name__ == '__main__':
    main()
