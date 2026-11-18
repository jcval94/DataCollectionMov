#!/usr/bin/env python3
"""Offline execution of registered scientific/civic adapters; no arbitrary code or URLs."""
import argparse
import gzip
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
from fieldlab import nasa
from fieldlab.common import export

REGISTRY={nasa.CASE:nasa}


def code_hash(case):
    adapter=REGISTRY[case]
    files=[Path(__file__),Path(adapter.__file__),BASE/'scripts/fieldlab/common.py',BASE/'scripts/fieldlab/__init__.py',
        BASE/'scripts/run_research.py',*sorted((BASE/'scripts/v3').glob('*.py'))]
    return hashlib.sha256(''.join(str(p.relative_to(BASE))+sha(p) for p in files).encode()).hexdigest()


def fingerprint(case):
    _,m=REGISTRY[case].load();review=BASE/'evidence/v3/fieldlab'/case/'visual-review.json'
    return dict(code_sha256=code_hash(case),snapshot_sha256=m['snapshot_sha256'],
        manifest_sha256=sha(BASE/'pilots'/case/'data/manifest.json'),contracts_sha256=sha(BASE/'contracts'/f'{case}.json'),
        dictionary_sha256=sha(BASE/'pilots'/case/'DICCIONARIO.md'),visual_review_sha256=sha(review) if review.exists() else None,
        python=sys.version.split()[0],dependencies={name:version(name) for name in ['numpy','pandas','scipy','scikit-learn','matplotlib','pillow']},seed=REGISTRY[case].SEED)


def verify(folder):
    receipt=json.loads((folder/'receipt.json').read_text())
    require(receipt['fingerprint']==fingerprint(receipt['case']),'Changed source, code, contract or environment')
    require(receipt['artifacts']==artifact_hashes(folder),'Changed or missing output artifact')
    return receipt


def package(case,out):
    student=out/'student';student.mkdir()
    for name in ['index.html','ALUMNO.md']:shutil.copy(out/'education'/name,student/name)
    (student/'index.html').write_text((student/'index.html').read_text().replace('../gold/','tables/'))
    (student/'tables').mkdir()
    for source in (out/'gold').glob('*.csv'):shutil.copy(source,student/'tables'/source.name)
    shutil.copy(BASE/'pilots'/case/'DICCIONARIO.md',student/'DICCIONARIO.md')
    shutil.copy(BASE/'pilots'/case/'data/RIGHTS.md',student/'DATOS_LICENCIA.md')
    engine=student/'research_engine/discovery_labs'
    files=[BASE/'scripts/run_fieldlab.py',BASE/'scripts/run_research.py',*sorted((BASE/'scripts/v3').glob('*.py')),
        *sorted((BASE/'scripts/fieldlab').glob('*.py')),BASE/'contracts'/f'{case}.json',
        BASE/'requirements.txt',BASE/'requirements-ci.txt',BASE/'requirements-batch1.txt',BASE/'pilots'/case/'DICCIONARIO.md',
        *sorted((BASE/'pilots'/case/'data').iterdir())]
    for source in files:
        dest=engine/source.relative_to(BASE);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy(source,dest)
    (student/'EJECUTAR.md').write_text(f'''# Kit candidato · {REGISTRY[case].TITLE}

Preparar Python 3.12 y requirements-batch1.txt antes de clase. Desde esta carpeta:

```sh
python research_engine/discovery_labs/scripts/run_fieldlab.py --case {case}
```

La ejecución no usa red ni claves. index.html es la alternativa precalculada sin instalaciones.
Consultar DATOS_LICENCIA.md y el diccionario. El snapshot es la consulta archivada, no una actualización en vivo.
No se incluyen referencias docentes ni evaluación formal. Ensayo humano y aprobación curricular pendientes.
''')
    hashes={str(p.relative_to(student)):sha(p) for p in sorted(student.rglob('*')) if p.is_file()}
    write(student/'package-manifest.json',dict(distribution='student',files=hashes,teacher_reference_files_included=False,classroom_approved=False,published=False))
    with zipfile.ZipFile(out/'student-offline.zip','w',compression=zipfile.ZIP_DEFLATED) as archive:
        for p in sorted(student.rglob('*')):
            if p.is_file():
                entry=zipfile.ZipInfo(str(p.relative_to(student)),date_time=(2026,11,17,0,0,0));entry.compress_type=zipfile.ZIP_DEFLATED;entry.external_attr=0o644<<16
                archive.writestr(entry,p.read_bytes())


def enrich(adapter,out,stories):
    for story in stories:
        title,prompt,complication,adversarial,transfer=adapter.STORIES[story['question_id']]
        story.update(title=title,hook_30_60_seconds=adapter.HOOK,two_paths=['Describir la métrica y su denominador.','Contrastar la sensibilidad indicada en el contrato.'],transfer_question=transfer)
        story['acts'][0]['audience_question']=prompt
        story['acts'][3]['facilitation']=complication
        story['acts'][5]['facilitation']=adversarial
        story['acts'][6]['audience_question']=transfer
    write(out/'education/storyboards.json',stories)
    (out/'teacher/FACILITACION.md').write_text((out/'teacher/FACILITACION.md').read_text()+'\n'+
        '\n\n'.join(f'## {s["question_id"]} · {s["title"]}\n'+ '\n'.join(f'{a["act"]}. {a["name"]}: {a["facilitation"]} Pregunta: {a["audience_question"]}' for a in s['acts']) for s in stories))
    return stories


def gates(case,out,contracts,claims,figures,stories):
    review_path=BASE/'evidence/v3/fieldlab'/case/'visual-review.json'
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
        questions=questions,independent_teacher_review=False,human_rehearsal=False,all_six_routes_technically_ready=len(claims)==6)


def run(case,output=BASE/'output/v3',force=False):
    require(case in REGISTRY,'Source outside registered allowlist')
    adapter=REGISTRY[case];HOOKS[case]=(adapter.TITLE,adapter.HOOK)
    output=Path(output);output.mkdir(parents=True,exist_ok=True);target=output/case
    if not force and (target/'receipt.json').exists():
        try:verify(target);print(json.dumps(dict(case=case,status='CACHE_VERIFIED')));return target
        except (ValueError,FileNotFoundError):pass
    started=time.perf_counter()
    with tempfile.TemporaryDirectory(prefix='.'+case+'-',dir=output) as temp:
        out=Path(temp)
        try:
            raw,m=adapter.load();silver,profile,transformations,checks=adapter.prepare(raw,m)
            for name in ['bronze','silver','gold','quality','research','visualization']:(out/name).mkdir()
            write(out/'bronze/receipt.json',m)
            (out/'silver/observations.csv.gz').write_bytes(gzip.compress(silver.to_csv(index=False).encode(),mtime=0))
            write(out/'quality/profile.json',profile);write(out/'quality/transformations.json',transformations);write(out/'quality/checks.json',checks)
            tables,claims=adapter.analyze(silver)
            for name,table in tables.items():table.to_csv(out/'gold'/f'{name}.csv',index=False)
            contracts=json.loads((BASE/'contracts'/f'{case}.json').read_text())
            require(set(claims)=={c['id'] for c in contracts if c['execution_status']=='EXECUTABLE'},'Contract and execution IDs differ')
            write(out/'research/contracts.json',contracts);write(out/'research/results.json',claims)
            figures=export(adapter,tables,claims,m,out/'visualization',code_hash(case))
            stories=enrich(adapter,out,build(case,out,contracts,claims,figures));gallery(case,out,contracts,figures);package(case,out)
            write(out/'gates.json',gates(case,out,contracts,claims,figures,stories))
            write(out/'runtime.json',dict(seconds=time.perf_counter()-started,network='DISABLED',seed=adapter.SEED))
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
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--case',choices=list(REGISTRY),default=nasa.CASE)
    parser.add_argument('--output',type=Path,default=BASE/'output/v3');parser.add_argument('--force',action='store_true')
    args=parser.parse_args();disable_network();run(args.case,args.output,args.force)
