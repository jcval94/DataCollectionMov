#!/usr/bin/env python3
"""Reproduce Batch 0 without a network. Only pre-registered Python analyses run."""
import argparse
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import shutil
import socket
import sys
import tempfile
import time

from v3.data import BASE, CASES, load, prepare, require, sha, write
from v3.research import ANALYSES, SEED
from v3.visuals import export
from v3.delivery import build, gallery, package


def code_hash():
    files = [Path(__file__), *sorted((BASE/'scripts/v3').glob('*.py'))]
    return hashlib.sha256(''.join(p.name+sha(p) for p in files).encode()).hexdigest()


def fingerprint(case):
    _, m = load(case)
    return dict(code_sha256=code_hash(), contract_sha256=sha(BASE/'contracts/batch0.json'),
        manifest_sha256=sha(BASE/'pilots'/case/'data/manifest.json'), snapshot_sha256=m['snapshot_sha256'],
        v2_reference_sha256=sha(BASE/'evidence/pilot_runs'/f'{case}.json'),
        dictionary_sha256=sha(BASE/'pilots'/case/'DICCIONARIO.md'),
        visual_review_sha256=sha(BASE/'evidence/v3/visual-review.json') if (BASE/'evidence/v3/visual-review.json').exists() else None,
        python=sys.version.split()[0],
        dependencies={name:version(name) for name in ['numpy','pandas','scipy','scikit-learn','matplotlib']}, seed=SEED)


def artifact_hashes(folder):
    return {str(p.relative_to(folder)):sha(p) for p in sorted(folder.rglob('*'))
            if p.is_file() and str(p.relative_to(folder)) not in ['receipt.json', 'runtime.json'] and '__pycache__' not in p.parts}


def verify(folder):
    receipt = json.loads((folder/'receipt.json').read_text())
    require(receipt['fingerprint'] == fingerprint(receipt['case']), 'Código, contrato, snapshot o entorno cambiaron')
    require(receipt['artifacts'] == artifact_hashes(folder), 'Un artefacto cambió o falta')
    return receipt


def gates(case, out, contracts, claims, figures, stories):
    review_path = BASE/'evidence/v3/visual-review.json'
    review = json.loads(review_path.read_text()) if review_path.exists() else {}
    visual_checks = []
    for figure in figures:
        for variant in figure['variants']:
            digest = variant['png_sha256']
            visual_checks.append(digest in review.get('reviewed_png_sha256', []) and review.get('rendered_inspection') is True)
    data_ready = all(r['passed'] for r in json.loads((out/'quality/checks.json').read_text()))
    return dict(source_id=case, DATA_READY=data_ready,
        questions={c['id']:dict(RESEARCH_READY=data_ready and c['id'] in claims,
            VISUAL_READY=data_ready and c['id'] in claims and all(visual_checks),
            STORY_READY=data_ready and c['id'] in claims and any(s['question_id']==c['id'] and len(s['acts'])==7 for s in stories),
            CLASS_READY=False, PUBLISHED=False, reason=c['blocking_reason'] or 'Falta ensayo humano observado y revisión docente independiente.') for c in contracts},
        visual_approval_scope='Sólo hashes de PNG inspeccionados; controles automatizados adicionales no sustituyen observación.',
        classroom_release=dict(required_executable_routes=6, actual_executable_routes=len(claims),
            all_six_routes_technically_ready=len(claims)==6, human_rehearsal='NOT_OBSERVED', independent_teacher_review='NOT_OBSERVED'))


def run(case, output=BASE/'output/v3', force=False):
    output = Path(output); output.mkdir(parents=True, exist_ok=True); target = output/case
    if not force and (target/'receipt.json').exists():
        try:
            verify(target)
            print(json.dumps(dict(case=case, status='CACHE_VERIFIED'), ensure_ascii=False))
            return target
        except (ValueError, FileNotFoundError):
            pass
    started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix=f'.{case}-', dir=output) as tmp:
        out = Path(tmp)
        try:
            raw, manifest = load(case)
            silver, profile, transformations, checks = prepare(case, raw, manifest)
            for folder in ['bronze', 'silver', 'gold', 'quality', 'research', 'visualization']:
                (out/folder).mkdir()
            # Snapshot is already immutable bronze, not an altered copy of the producer's full data.
            write(out/'bronze/receipt.json', dict(snapshot_path=f'pilots/{case}/data/snapshot.csv', **manifest,
                original_retained='Original upstream hash retained; original full files stay in external pre-class cache.',
                raw_privacy='Retail bronze here is the already minimized V2 snapshot, not an unredacted customer file.'))
            silver.to_csv(out/'silver/records.csv', index=False)
            write(out/'quality/profile.json', profile); write(out/'quality/transformations.json', transformations)
            write(out/'quality/checks.json', checks)
            previous = json.loads((BASE/'evidence/pilot_runs'/f'{case}.json').read_text())
            tables, claims = ANALYSES[case](silver, raw, previous)
            for name, table in tables.items(): table.to_csv(out/'gold'/f'{name}.csv', index=False)
            contracts = [c for c in json.loads((BASE/'contracts/batch0.json').read_text()) if c['source_id']==case]
            require(set(claims) == {c['id'] for c in contracts if c['execution_status']=='EXECUTABLE'}, 'Rutas declaradas y ejecutadas no coinciden')
            write(out/'research/results.json', claims); write(out/'research/contracts.json', contracts)
            figures = export(case, tables, claims, manifest, out/'visualization', code_hash())
            stories = build(case, out, contracts, claims, figures)
            gallery(case, out, contracts, figures); package(case, out)
            write(out/'gates.json', gates(case, out, contracts, claims, figures, stories))
            write(out/'runtime.json', dict(seconds=time.perf_counter()-started, network='DISABLED', seed=SEED))
            # Receipt is last. Interrupted/failed staging never counts as a successful execution.
            write(out/'receipt.json', dict(case=case, fingerprint=fingerprint(case), artifacts=artifact_hashes(out)))
            backup = output/f'.{case}-previous'
            if backup.exists(): shutil.rmtree(backup)
            (output/f'{case}-error.json').unlink(missing_ok=True)
            if target.exists(): target.rename(backup)
            out.rename(target)
            if backup.exists(): shutil.rmtree(backup)
            print(json.dumps(dict(case=case, status='EXECUTED', routes=len(claims), figures=len(figures), seconds=round(time.perf_counter()-started, 2)), ensure_ascii=False), flush=True)
        except Exception as exc:
            write(output/f'{case}-error.json', dict(case=case, type=type(exc).__name__, message=str(exc), state='FAILED_NOT_PROMOTED'))
            raise
    return target


def disable_network():
    def denied(*args, **kwargs): raise RuntimeError('Red deshabilitada durante investigación offline')
    socket.create_connection = denied
    socket.socket.connect = denied
    socket.socket.connect_ex = denied


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', choices=[*CASES, 'all'], default='all')
    parser.add_argument('--output', type=Path, default=BASE/'output/v3')
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args(); disable_network()
    for case in CASES if args.case=='all' else [args.case]: run(case, args.output, args.force)


if __name__ == '__main__': main()
