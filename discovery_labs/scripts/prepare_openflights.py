#!/usr/bin/env python3
"""Recreate pinned lossless snapshots before class; never called by offline analyses."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import urllib.request

from v3.data import BASE, require, sha


def prepare(cache, download=False):
    folder=BASE/'pilots/openflights-red-aerea/data';manifest=json.loads((folder/'manifest.json').read_text())
    cache=Path(cache);cache.mkdir(parents=True,exist_ok=True)
    prepared=[]
    # Validate every file before replacing any pinned snapshot.
    for entry in manifest['files']:
        raw_path=cache/entry['file'].removesuffix('.gz')
        if download:
            request=urllib.request.Request(entry['source_url'],headers={'User-Agent':'AI-Discovery-Labs/3.1'})
            with urllib.request.urlopen(request,timeout=30) as response:content=response.read(8*1024*1024+1)
            require(len(content)<=8*1024*1024,'Download over byte limit')
        else:content=raw_path.read_bytes()
        require(hashlib.sha256(content).hexdigest()==entry['raw_sha256'],'Upstream version changed; no snapshot replaced')
        stored=gzip.compress(content,mtime=0) if entry['file'].endswith('.gz') else content
        require(hashlib.sha256(stored).hexdigest()==entry['stored_sha256'],'Compression/environment changed; audit before replacement')
        prepared.append((folder/entry['file'],stored,raw_path,content))
    for path,stored,raw_path,content in prepared:
        if download:raw_path.write_bytes(content)
        staging=path.with_name(path.name+'.preparing')
        staging.write_bytes(stored);staging.replace(path)
    print(json.dumps(dict(source='openflights-red-aerea',files=len(prepared),status='PINNED_BYTES_REPRODUCED')))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--download',action='store_true');p.add_argument('--cache',type=Path,default=BASE/'cache/openflights')
    a=p.parse_args();prepare(a.cache,a.download)
