#!/usr/bin/env python3
"""Incremental source registry for Batch 1; currently the historical OpenFlights adapter."""
import argparse
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import shutil
import sys
import tempfile
import time
import zipfile

from v3.data import BASE, require, sha, write
from v3.delivery import HOOKS, build, gallery
from run_research import artifact_hashes, disable_network
from batch1 import openflights
from batch1.figures import export
from batch1.storytelling import enrich

REGISTRY={openflights.CASE:openflights}
HOOKS[openflights.CASE]=('El aeropuerto que parecía imprescindible',
    'Una isla quiere entender de qué conexiones depende. Alguien propone contar rutas y otro pregunta qué pasaría si un aeropuerto desapareciera de la red. Hoy no tenemos pasajeros ni precios: sí podemos investigar la estructura histórica, comparar definiciones de importancia y comprobar qué cambia con un supuesto. Antes de mirar el mapa, elige qué pregunta merece tu apuesta.')


def code_hash():
    files=[Path(__file__),BASE/'scripts/run_research.py',*sorted((BASE/'scripts/v3').glob('*.py')),*sorted((BASE/'scripts/batch1').glob('*.py'))]
    return hashlib.sha256(''.join(str(p.relative_to(BASE))+sha(p) for p in files).encode()).hexdigest()


def fingerprint(case):
    _,m=REGISTRY[case].load()
    review=BASE/'evidence/v3/batch1a/visual-review.json'
    return dict(code_sha256=code_hash(),snapshot_sha256=m['snapshot_sha256'],manifest_sha256=sha(BASE/'pilots'/case/'data/manifest.json'),
        contracts_sha256=sha(BASE/'contracts/batch1a.json'),dictionary_sha256=sha(BASE/'pilots'/case/'DICCIONARIO.md'),
        visual_review_sha256=sha(review) if review.exists() else None,python=sys.version.split()[0],
        dependencies={name:version(name) for name in ['networkx','numpy','pandas','scipy','scikit-learn','matplotlib','pillow']},seed=openflights.SEED)


def verify(folder):
    receipt=json.loads((folder/'receipt.json').read_text())
    require(receipt['fingerprint']==fingerprint(receipt['case']),'Changed source, code, contract or environment')
    require(receipt['artifacts']==artifact_hashes(folder),'Changed or missing output artifact')
    return receipt


def package(case,out):
    student=out/'student';student.mkdir()
    for name in ['index.html','ALUMNO.md']:shutil.copy(out/'education'/name,student/name)
    text=(student/'index.html').read_text().replace('../gold/','tables/');(student/'index.html').write_text(text)
    (student/'tables').mkdir()
    for source in (out/'gold').glob('*.csv'):shutil.copy(source,student/'tables'/source.name)
    shutil.copy(BASE/'pilots'/case/'DICCIONARIO.md',student/'DICCIONARIO.md')
    engine=student/'research_engine/discovery_labs'
    files=[BASE/'scripts/run_batch1.py',BASE/'scripts/run_research.py',BASE/'scripts/v3/__init__.py',BASE/'scripts/v3/data.py',
           BASE/'scripts/v3/delivery.py',BASE/'scripts/v3/research.py',BASE/'scripts/v3/visuals.py',
           *sorted((BASE/'scripts/batch1').glob('*.py')),BASE/'contracts/batch1a.json',
           BASE/'requirements.txt',BASE/'requirements-ci.txt',BASE/'requirements-batch1.txt',BASE/'pilots'/case/'DICCIONARIO.md',
           *sorted((BASE/'pilots'/case/'data').iterdir())]
    for source in files:
        destination=engine/source.relative_to(BASE);destination.parent.mkdir(parents=True,exist_ok=True);shutil.copy(source,destination)
    (student/'EJECUTAR.md').write_text(f'''# OpenFlights · kit candidato offline

Preparar Python 3.12 y requirements-batch1.txt antes de clase. Desde esta carpeta:

```sh
python research_engine/discovery_labs/scripts/run_batch1.py --case {case}
```

El análisis no usa red ni claves. La galería precalculada es index.html y los datos conservan atribución y ODbL-1.0.
No son vuelos ni pasajeros. Rutas históricas; no sirve para navegación ni decisiones comerciales actuales.
No hay evaluación formal ni referencias docentes. Clase sin ensayo humano ni aprobación de distribución curricular.
''')
    (student/'DATOS_LICENCIA.md').write_text('Base derivada y tablas: ODbL-1.0. Contenidos: ODC-DbCL-1.0. Atribución OpenFlights / Airline Route Mapper / OurAirports. Texto íntegro del productor dentro de research_engine/discovery_labs/pilots/openflights-red-aerea/data/LICENSE. Figuras originales ADL, sin imágenes o mapas copiados del sitio del productor. No se afirma patrocinio o aval.\n')
    hashes={str(p.relative_to(student)):sha(p) for p in sorted(student.rglob('*')) if p.is_file()}
    write(student/'package-manifest.json',dict(distribution='student',files=hashes,teacher_reference_files_included=False,
        classroom_approved=False,published=False,data_license='ODbL-1.0'))
    with zipfile.ZipFile(out/'student-offline.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(student.rglob('*')):
            if p.is_file():
                entry=zipfile.ZipInfo(str(p.relative_to(student)),date_time=(2026,11,17,0,0,0));entry.compress_type=zipfile.ZIP_DEFLATED;entry.external_attr=0o644<<16
                z.writestr(entry,p.read_bytes())


def gates(case,out,contracts,claims,figures,stories):
    review_path=BASE/'evidence/v3/batch1a/visual-review.json'
    review=json.loads(review_path.read_text()) if review_path.exists() else {}
    reviewed=set(review.get('reviewed_png_sha256',[]));questions={}
    for c in contracts:
        relevant=[f for f in figures if c['id'] in f['question_ids']]
        visual=bool(relevant) and review.get('rendered_inspection') is True and all(v['png_sha256'] in reviewed for f in relevant for v in f['variants'])
        story=next((s for s in stories if s['question_id']==c['id']),None)
        questions[c['id']]=dict(RESEARCH_READY=c['id'] in claims,VISUAL_READY=c['id'] in claims and visual,
            STORY_READY=story is not None and len(story['acts'])==7,CLASS_READY=False,PUBLISHED=False,
            reason=c['blocking_reason'] or 'Ensayo humano y revisión docente independiente no observados.')
    return dict(source_id=case,DATA_READY=all(r['passed'] for r in json.loads((out/'quality/checks.json').read_text())),
                questions=questions,independent_teacher_review=False,human_rehearsal=False,
                all_six_routes_technically_ready=len(claims)==6)


def run(case,output=BASE/'output/v3',force=False):
    require(case in REGISTRY,'Source outside registered allowlist')
    output=Path(output);output.mkdir(parents=True,exist_ok=True);target=output/case
    if not force and (target/'receipt.json').exists():
        try:
            verify(target);print(json.dumps(dict(case=case,status='CACHE_VERIFIED')));return target
        except (ValueError,FileNotFoundError):pass
    started=time.perf_counter()
    with tempfile.TemporaryDirectory(prefix='.'+case+'-',dir=output) as temp:
        out=Path(temp)
        try:
            raw,m=REGISTRY[case].load();silver,edges,profile,transformations,checks=REGISTRY[case].prepare(raw)
            for directory in ['bronze','silver','gold','quality','research','visualization']:(out/directory).mkdir()
            write(out/'bronze/receipt.json',m)
            for key,frame in silver.items():frame.to_csv(out/'silver'/f'{key}.csv',index=False)
            write(out/'quality/profile.json',profile);write(out/'quality/transformations.json',transformations);write(out/'quality/checks.json',checks)
            tables,claims=REGISTRY[case].analyze(silver,edges)
            for key,frame in tables.items():frame.to_csv(out/'gold'/f'{key}.csv',index=False)
            contracts=[c for c in json.loads((BASE/'contracts/batch1a.json').read_text()) if c['source_id']==case]
            require(set(claims)=={c['id'] for c in contracts if c['execution_status']=='EXECUTABLE'},'Contract and execution IDs differ')
            write(out/'research/contracts.json',contracts);write(out/'research/results.json',claims)
            figures=export(tables,claims,m,out/'visualization',code_hash())
            stories=enrich(out,build(case,out,contracts,claims,figures));gallery(case,out,contracts,figures);package(case,out)
            write(out/'gates.json',gates(case,out,contracts,claims,figures,stories))
            write(out/'runtime.json',dict(seconds=time.perf_counter()-started,network='DISABLED',seed=openflights.SEED))
            write(out/'receipt.json',dict(case=case,fingerprint=fingerprint(case),artifacts=artifact_hashes(out)))
            backup=output/f'.{case}-previous'
            if backup.exists():shutil.rmtree(backup)
            if target.exists():target.rename(backup)
            out.rename(target)
            if backup.exists():shutil.rmtree(backup)
            (output/f'{case}-error.json').unlink(missing_ok=True)
            print(json.dumps(dict(case=case,status='EXECUTED',routes=len(claims),figures=len(figures),seconds=round(time.perf_counter()-started,2))),flush=True)
        except Exception as exc:
            write(output/f'{case}-error.json',dict(case=case,type=type(exc).__name__,message=str(exc),state='FAILED_NOT_PROMOTED'));raise
    return target


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--case',choices=list(REGISTRY),default=openflights.CASE)
    parser.add_argument('--output',type=Path,default=BASE/'output/v3');parser.add_argument('--force',action='store_true')
    args=parser.parse_args();disable_network();run(args.case,args.output,args.force)
