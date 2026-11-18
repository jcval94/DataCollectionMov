#!/usr/bin/env python3
"""Replay a manifest's exact bounded bytes before class; live revisions fail closed."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import tempfile
import urllib.request

from v3.data import BASE, require


def replay(case,download=False):
    folder=BASE/'pilots'/case/'data';m=json.loads((folder/'manifest.json').read_text())
    current=gzip.decompress((folder/'snapshot.csv.gz').read_bytes())
    require(hashlib.sha256(current).hexdigest()==m['snapshot_sha256'],'Bundled snapshot corrupt')
    if not download:return dict(case=case,status='BUNDLED_HASH_VERIFIED',bytes=len(current))
    request=urllib.request.Request(m['download_url'],headers={'User-Agent':'ADL-reproducibility/3 (bounded educational snapshot)'})
    with urllib.request.urlopen(request,timeout=90) as response:
        received=response.read(m['snapshot_bytes']+1)
    require(len(received)==m['snapshot_bytes'] and hashlib.sha256(received).hexdigest()==m['snapshot_sha256'],
        'Live source changed or truncated; archived snapshot preserved. A refresh requires a new reviewed manifest/version.')
    packed=gzip.compress(received,mtime=0)
    require(hashlib.sha256(packed).hexdigest()==m['files']['snapshot.csv.gz']['sha256'],'Compressed bytes differ; preserve current snapshot')
    with tempfile.NamedTemporaryFile(dir=folder,delete=False) as temp:
        temp.write(packed);name=Path(temp.name)
    name.replace(folder/'snapshot.csv.gz')
    return dict(case=case,status='EXACT_UPSTREAM_REPLAY',bytes=len(received))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--case',choices=['nasa-exoplanetas','nyc-ratas'],required=True);p.add_argument('--download',action='store_true')
    args=p.parse_args();print(json.dumps(replay(args.case,args.download)))
