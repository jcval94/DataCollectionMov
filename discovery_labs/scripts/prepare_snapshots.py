#!/usr/bin/env python3
"""Explicit pre-class preparation. Requires local originals; download is opt-in."""
import argparse,hashlib,json,urllib.request
from pathlib import Path
import pandas as pd

BASE=Path(__file__).resolve().parents[1]
def digest(raw):return hashlib.sha256(raw).hexdigest()
def prepare(retail_input,nba_input):
    specs=[('uci-retail',retail_input),('nba-elo',nba_input)]
    for case,path in specs:
        m=json.loads((BASE/'pilots'/case/'data/manifest.json').read_text())
        if not path.exists():raise FileNotFoundError(f'Original no disponible: {path}; descargar fuera de clase con --download')
        if digest(path.read_bytes())!=m['source_sha256']:raise ValueError(f'{case}: el original cambió; auditar versión antes de regenerar')
        d=pd.read_csv(path,dtype=str,keep_default_na=False)
        if case=='uci-retail':
            dates=pd.to_datetime(d.InvoiceDate,format='%m/%d/%Y %H:%M');month=d[dates.between('2011-11-01','2011-11-30 23:59:59')].copy()
            invoices=sorted(month.InvoiceNo.unique(),key=lambda x:digest(x.encode()))[:300]
            z=month[month.InvoiceNo.isin(invoices)].copy();z['customer_id_missing']=z.CustomerID.eq('').astype(int);z=z.drop(columns=['CustomerID','Description'])
            z['InvoiceDate']=pd.to_datetime(z.InvoiceDate,format='%m/%d/%Y %H:%M').dt.strftime('%Y-%m-%dT%H:%M:%S')
        else:
            # Preserve numeric formatting of the original preparation, including integer columns.
            d=pd.read_csv(path,dtype={'game_id':str});z=d[(d.year_id==2015)&(d.lg_id=='NBA')].copy()
        raw=z.to_csv(index=False,lineterminator='\n').encode()
        if digest(raw)!=m['snapshot_sha256']:raise ValueError(f'{case}: transformación no coincide con snapshot fijado')
        (BASE/'pilots'/case/'data/snapshot.csv').write_bytes(raw)
        print(case,'preparación reproducida',len(z),flush=True)
    m=json.loads((BASE/'pilots/bob-ross-elementos/data/manifest.json').read_text())
    d=pd.read_csv(BASE.parent/'examples/bob_ross_clustering/data/elements-by-episode.csv',encoding='utf-8-sig')
    raw=d.to_csv(index=False,lineterminator='\n').encode()
    if digest(raw)!=m['snapshot_sha256']:raise ValueError('Bob Ross: transformación modificada')
    (BASE/'pilots/bob-ross-elementos/data/snapshot.csv').write_bytes(raw)
    print('bob-ross-elementos preparación reproducida',len(d))
def main():
    p=argparse.ArgumentParser();p.add_argument('--cache',type=Path,default=BASE/'cache');p.add_argument('--download',action='store_true');a=p.parse_args();a.cache.mkdir(parents=True,exist_ok=True)
    paths=[]
    for case,name in [('uci-retail','retail.csv'),('nba-elo','nba.csv')]:
        path=a.cache/name;paths.append(path)
        if a.download:
            m=json.loads((BASE/'pilots'/case/'data/manifest.json').read_text())
            with urllib.request.urlopen(urllib.request.Request(m['source_url'],headers={'User-Agent':'AI-Discovery-Labs/2.0'}),timeout=30) as r:raw=r.read(64*1024*1024+1)
            if len(raw)>64*1024*1024 or digest(raw)!=m['source_sha256']:raise ValueError('Descarga excede límite o cambió de versión; no reemplazar snapshot')
            path.write_bytes(raw)
    prepare(*paths)
if __name__=='__main__':main()
