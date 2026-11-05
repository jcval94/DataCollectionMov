#!/usr/bin/env python3
"""Download and decode bounded image examples; never edits the source images."""
from __future__ import annotations
import argparse
import concurrent.futures
import hashlib
import io
import json
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'catalogs/visual_examples.json'
MAX_BYTES = 3 * 1024 * 1024

def check(example):
    result = {'checked_at_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
              'requested_url': example['image_url'], 'max_bytes': MAX_BYTES}
    try:
        req = urllib.request.Request(example['image_url'], headers={
            'User-Agent': 'DataCollectionMov-visual-check/1.0 (+https://github.com/jcval94/DataCollectionMov)'})
        with urllib.request.urlopen(req, timeout=18) as response:
            result.update(http_status=response.status, final_url=response.url,
                          content_type=response.headers.get('Content-Type'))
            data = response.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise ValueError('La imagen supera el límite de descarga; no se validó completa')
        with Image.open(io.BytesIO(data)) as image:
            image.verify()
        with Image.open(io.BytesIO(data)) as image:
            image.load()
            result.update(format=image.format, width=image.width, height=image.height)
        result.update(status='IMAGE_DECODED', bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                      hash_scope='complete_response',
                      detail='GET completo, estructura y píxeles decodificados. No verifica el contenido semántico ni OCR.')
        # Only explicitly selected public-domain/CC0 examples are copied into git.
        if example.get('local_path'):
            target = ROOT / example['local_path']
        else:
            target = ROOT / 'tmp/visuals' / (example['dataset_id'] + '.image')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    except urllib.error.HTTPError as exc:
        result.update(status='IMAGE_ERROR', http_status=exc.code, detail=str(exc))
    except Exception as exc:
        result.update(status='IMAGE_ERROR', detail=f'{type(exc).__name__}: {exc}')
    return example, result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--only', nargs='+')
    args = parser.parse_args()
    payload = json.loads(MANIFEST.read_text())
    examples = payload['examples']
    if args.only:
        unknown = set(args.only) - {e['dataset_id'] for e in examples}
        if unknown:
            parser.error('IDs desconocidos: ' + ', '.join(sorted(unknown)))
        examples = [e for e in examples if e['dataset_id'] in args.only]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for example, result in pool.map(check, examples):
            if example.get('test'):
                example.setdefault('previous_tests', []).append(example['test'])
            example['test'] = result
            print(example['dataset_id'] + ': ' + result['status'], flush=True)
    payload['verifier_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    MANIFEST.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
    return int(any(e['test']['status'] != 'IMAGE_DECODED' for e in examples))

if __name__ == '__main__':
    raise SystemExit(main())
