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


def limits():
    resource.setrlimit(resource.RLIMIT_AS, (4*1024**3, 4*1024**3))
    resource.setrlimit(resource.RLIMIT_CPU, (50, 50))
    resource.setrlimit(resource.RLIMIT_FSIZE, (32*1024**2, 32*1024**2))
    resource.setrlimit(resource.RLIMIT_NOFILE, (128, 128))
    os.umask(0o077)


def dispatch(action, case=None, question=None):
    contracts = json.loads((BASE/'contracts/batch0.json').read_text())
    if action == 'catalog':
        overrides = {c['id']:c for c in contracts}
        sources = json.loads((BASE/'catalog/sources.json').read_text())
        questions = json.loads((BASE/'catalog/questions.json').read_text())
        return dict(sources=[dict(id=s['id'], name=s['name'], resource_type=s['resource_type']) for s in sources],
                    questions=[dict(id=q['id'], source=q['source_id'], question=q['question'],
                                    status=overrides[q['id']]['execution_status'] if q['id'] in overrides else q['status']) for q in questions])
    require(case in CASES, 'case obligatorio y permitido')
    output = BASE/'output/v3'/case
    if action == 'schema':
        _, m = load(case); return m
    if action == 'run':
        matches = [c for c in contracts if c['source_id']==case and c['id']==question]
        require(len(matches)==1 and matches[0]['execution_status']=='EXECUTABLE', 'Ruta bloqueada o ajena a esta fuente')
        # Do not inherit API tokens or arbitrary runtime configuration.
        env = {key:os.environ[key] for key in ['PATH','HOME','LANG','LD_LIBRARY_PATH','MPLCONFIGDIR'] if key in os.environ}
        env.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONHASHSEED='0')
        result = subprocess.run([sys.executable, str(BASE/'scripts/run_research.py'), '--case', case],
            env=env, cwd=BASE.parent, capture_output=True, text=True, timeout=60, preexec_fn=limits)
        require(result.returncode==0, 'Ejecución falló: '+result.stderr[-1500:])
    from run_research import verify
    verify(output)
    if action in ['results','run']:
        results = json.loads((output/'research/results.json').read_text())
        if question:
            require(question in results, 'No hay resultado ejecutado para esta pregunta')
            return dict(question=question, result=results[question], figures=json.loads((output/'visualization/figures.json').read_text()))
        return results
    paths = {'quality':'quality/profile.json', 'storyboard':'education/storyboards.json', 'verify':'receipt.json'}
    require(action in paths, 'Herramienta desconocida')
    return json.loads((output/paths[action]).read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['catalog','schema','quality','run','results','storyboard','verify'])
    parser.add_argument('--case', choices=CASES)
    parser.add_argument('--question')
    args = parser.parse_args()
    try:
        print(json.dumps(dict(ok=True, data=dispatch(args.action, args.case, args.question)), ensure_ascii=False, allow_nan=False))
    except (ValueError, FileNotFoundError, subprocess.TimeoutExpired) as exc:
        print(json.dumps(dict(ok=False, error=str(exc)), ensure_ascii=False)); sys.exit(1)


if __name__=='__main__': main()
