#!/usr/bin/env python3
"""Offline forensic audit. No inferred recoding and no external requests."""
from __future__ import annotations
import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from run import load, RAW

HERE = Path(__file__).resolve().parent
INCOMPLETE = ('S09E10', 'S15E04', 'S26E10')
AUTHOR = ('GUEST', 'STEVE_ROSS', 'DIANE_ANDRE')


def git_blob(data):
    return hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()


def audit():
    rows, digest = load()
    labels = list(rows[0]['flags'])
    assert {r['id'] for r in rows} == {
        f'S{s:02d}E{e:02d}' for s in range(1, 32) for e in range(1, 14)}
    groups = defaultdict(list)
    for r in rows:
        groups[r['title']].append(r['id'])
    rules = [('TREES', 'TREE'), ('MOUNTAINS', 'MOUNTAIN'),
             ('SNOWY_MOUNTAIN', 'MOUNTAIN'), ('CIRRUS', 'CLOUDS'),
             ('CUMULUS', 'CLOUDS')]
    rules += [(k, 'FRAMED') for k in labels if k.endswith('_FRAME') or k == 'WOOD_FRAMED']
    hierarchy = [{'child': a, 'parent': b,
                  'exceptions': [r['id'] for r in rows if r['flags'][a] and not r['flags'][b]]}
                 for a, b in rules]
    archive = json.loads((ROOT/'entry_pack/research_received/MANIFEST.json').read_text())
    # Resolve recorded repository-relative paths without depending on cwd.
    repo = ROOT.parents[2]
    integrity = {f['name']: git_blob((repo/f['path']).read_bytes()) == f['blob_sha']
                 for f in archive['files']}
    if not all(integrity.values()):
        raise ValueError('Received archive differs from its historical manifest')
    total = sum(sum(r['flags'].values()) for r in rows)
    report = {
        'status': 'PASS_FOR_TAG_ANALYSES', 'sha256': digest,
        'git_blob_sha': git_blob(RAW.read_bytes()), 'bytes': RAW.stat().st_size,
        'rows': len(rows), 'columns': len(labels)+2, 'binary_columns': len(labels),
        'unique_ids': len({r['id'] for r in rows}), 'seasons': 31,
        'episodes_per_season': 13, 'missing_values': 0, 'invalid_binary_values': 0,
        'positive_marks_all_67_columns': total,
        'positive_marks_without_author_flags': total-sum(r['flags'][k] for r in rows for k in AUTHOR),
        'count_discrepancies': {'3224_minus_snapshot': 3224-total,
                                '3324_minus_snapshot': 3324-total,
                                'historical_cause': 'UNRESOLVED; do not repair three values to match prose'},
        'host': sum(not r['guest'] for r in rows), 'guest': sum(r['guest'] for r in rows),
        'guest_name_flags': {k: sum(r['flags'][k] for r in rows) for k in AUTHOR[1:]},
        'guest_identity_coverage': '12/22 named by original flags; 10/22 unspecified, not independently credited',
        'duplicate_title_groups': {k:v for k,v in groups.items() if len(v)>1},
        'person': [r['id'] for r in rows if r['flags']['PERSON']],
        'chimney_column_exists': 'CHIMNEY' in labels,
        'zero_positive_rows': [r['id'] for r in rows if not any(r['flags'].values())],
        'vignette_incomplete_ids': list(INCOMPLETE),
        'host_excluding_vignette_incomplete': sum(not r['guest'] and r['id'] not in INCOMPLETE for r in rows),
        'column_totals': dict(Counter({k:sum(r['flags'][k] for r in rows) for k in labels})),
        'hierarchy_checks': hierarchy, 'received_archive_blob_checks': integrity,
        'limits': ['PASS certifies schema, not visual truth or annotator agreement',
                   'GUEST=0 is a label-defined population, not independent authorship verification',
                   'Ordinal SxxExx is not a recording date',
                   'All-zero rows retained; exclusions must be named sensitivity analyses']}
    return report, rows


def write():
    report, rows = audit()
    out = HERE/'evidence'
    out.mkdir(exist_ok=True)
    (out/'data_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    with (out/'episode_audit.csv').open('w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['episode','season','episode_num','title','guest','steve_ross','diane_andre',
                    'vignette_incomplete','positive_marks','person'])
        for r in rows:
            w.writerow([r['id'], r['season'], int(r['id'][-2:]), r['title'], r['guest'],
                        r['flags']['STEVE_ROSS'], r['flags']['DIANE_ANDRE'],
                        int(r['id'] in INCOMPLETE), sum(r['flags'].values()), r['flags']['PERSON']])
    print(json.dumps({k:report[k] for k in ['status','rows','columns','positive_marks_all_67_columns',
                                         'duplicate_title_groups','person','zero_positive_rows']}, ensure_ascii=False))


if __name__ == '__main__':
    write()
