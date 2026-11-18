#!/usr/bin/env python3
"""Fixed-tool JSON interface. Suitable for a future thin MCP adapter, not an arbitrary-code tool."""
import argparse
import json
import os
from pathlib import Path
import resource
import subprocess
import sys

from v3.data import BASE, CASES, load, require

BATCH1_CASES=('openflights-red-aerea',)
FIELD_CASES=('nasa-exoplanetas','nyc-ratas')


def limits():
    resource.setrlimit(resource.RLIMIT_AS, (4*1024**3, 4*1024**3))
    resource.setrlimit(resource.RLIMIT_CPU, (50, 50))
    resource.setrlimit(resource.RLIMIT_FSIZE, (32*1024**2, 32*1024**2))
    resource.setrlimit(resource.RLIMIT_NOFILE, (128, 128))
    os.umask(0o077)


def dispatch(action, case=None, question=None):
    contracts = json.loads((BASE/'contracts/batch0.json').read_text())
    if (BASE/'contracts/batch1a.json').exists():contracts+=json.loads((BASE/'contracts/batch1a.json').read_text())
    for source in FIELD_CASES:
        contracts+=json.loads((BASE/'contracts'/f'{source}.json').read_text())
    if action == 'catalog':
        overrides = {c['id']:c for c in contracts}
        sources = json.loads((BASE/'catalog/sources.json').read_text())
        questions = json.loads((BASE/'catalog/questions.json').read_text())
        return dict(sources=[dict(id=s['id'], name=s['name'], resource_type=s['resource_type']) for s in sources],
                    questions=[dict(id=q['id'], source=q['source_id'], question=overrides[q['id']]['question'] if q['id'] in overrides else q['question'],
                                    status=overrides[q['id']]['execution_status'] if q['id'] in overrides else q['status']) for q in questions])
    require(case in (*CASES,*BATCH1_CASES,*FIELD_CASES), 'case obligatorio y permitido')
    output = BASE/'output/v3'/case
    if action == 'schema':
        if case in FIELD_CASES:
            from run_fieldlab import REGISTRY
            raw,m=REGISTRY[case].load()
            return dict(manifest=m,columns=list(raw.columns),grain=m['selection'],dictionary=f'pilots/{case}/DICCIONARIO.md')
        if case in BATCH1_CASES:
            from batch1.openflights import load as load_batch1
            raw,m=load_batch1()
            return dict(manifest=m,columns={name:list(frame.columns) for name,frame in raw.items()},
                        keys=dict(airports=['airport_id'],routes='Airline route records; raw perspective need not be unique',gold_edges=['source_id','destination_id']),
                        units=dict(latitude='WGS84 degrees',longitude='WGS84 degrees',altitude_ft='feet',stops='integer stop count'))
        _, m = load(case); return m
    if action == 'run':
        matches = [c for c in contracts if c['source_id']==case and c['id']==question]
        require(len(matches)==1 and matches[0]['execution_status']=='EXECUTABLE', 'Ruta bloqueada o ajena a esta fuente')
        # Do not inherit API tokens or arbitrary runtime configuration.
        env = {key:os.environ[key] for key in ['PATH','HOME','LANG','LD_LIBRARY_PATH','MPLCONFIGDIR'] if key in os.environ}
        env.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONHASHSEED='0')
        script='run_fieldlab.py' if case in FIELD_CASES else 'run_batch1.py' if case in BATCH1_CASES else 'run_research.py'
        result = subprocess.run([sys.executable, str(BASE/'scripts'/script), '--case', case],
            env=env, cwd=BASE.parent, capture_output=True, text=True, timeout=60, preexec_fn=limits)
        require(result.returncode==0, 'Ejecución falló: '+result.stderr[-1500:])
    if case in FIELD_CASES:
        from run_fieldlab import verify
    elif case in BATCH1_CASES:
        from run_batch1 import verify
    else:
        from run_research import verify
    verify(output)
    if action in ['results','run']:
        results = json.loads((output/'research/results.json').read_text())
        if question:
            require(question in results, 'No hay resultado ejecutado para esta pregunta')
            figures=json.loads((output/'visualization/figures.json').read_text())
            return dict(question=question, result=results[question], figures=[f for f in figures if question in f['question_ids']])
        return results
    paths = {'quality':'quality/profile.json', 'storyboard':'education/storyboards.json', 'verify':'receipt.json'}
    require(action in paths, 'Herramienta desconocida')
    return json.loads((output/paths[action]).read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['catalog','schema','quality','run','results','storyboard','verify'])
    parser.add_argument('--case', choices=(*CASES,*BATCH1_CASES,*FIELD_CASES))
    parser.add_argument('--question')
    args = parser.parse_args()
    try:
        print(json.dumps(dict(ok=True, data=dispatch(args.action, args.case, args.question)), ensure_ascii=False, allow_nan=False))
    except (ValueError, FileNotFoundError, subprocess.TimeoutExpired) as exc:
        print(json.dumps(dict(ok=False, error=str(exc)), ensure_ascii=False)); sys.exit(1)


if __name__=='__main__': main()
