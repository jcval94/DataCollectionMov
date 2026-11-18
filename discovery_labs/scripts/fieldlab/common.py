"""Shared provenance and rendering only; adapters own their scientific methods."""
import gzip
import hashlib
import io
import json
import textwrap

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.text import Text
import numpy as np
import pandas as pd

from v3.data import BASE, require, sha, write

BLUE, RED, GOLD = '#24546a', '#b84331', '#885f1d'
COLORS = [BLUE, RED, GOLD, '#79609a', '#087f8c', '#614939']


def load(case):
    folder=BASE/'pilots'/case/'data'
    manifest=json.loads((folder/'manifest.json').read_text())
    for name,entry in manifest['files'].items():
        path=folder/name
        require(sha(path)==entry['sha256'] and path.stat().st_size==entry['bytes'], 'Source hash/size mismatch: '+name)
    data=gzip.decompress((folder/'snapshot.csv.gz').read_bytes())
    require(hashlib.sha256(data).hexdigest()==manifest['snapshot_sha256'], 'Uncompressed snapshot hash mismatch')
    raw=pd.read_csv(io.BytesIO(data),dtype=str,keep_default_na=False)
    require(list(raw)==manifest['columns'] and len(raw)==manifest['rows'], 'Snapshot schema/row mismatch')
    require(manifest['server_count']==len(raw), 'Server count and received rows differ')
    return raw,manifest


def profile(raw,silver,manifest,key,units):
    fields={}
    for name in raw:
        s=raw[name]; present=s[s.ne('')]; numeric=pd.to_numeric(present,errors='coerce')
        info=dict(raw_type='string',silver_type=str(silver[name].dtype),missing_count=int(s.eq('').sum()),
            missing_pct=100*float(s.eq('').mean()),cardinality=int(present.nunique()),unit=units.get(name,'category / reference'),
            frequent_values={str(k):int(v) for k,v in present.value_counts().head(5).items()})
        if len(numeric) and numeric.notna().all() and pd.api.types.is_numeric_dtype(silver[name]):
            require(np.isfinite(numeric).all(),'Non-finite value: '+name)
            info['quantiles']={str(k):float(v) for k,v in numeric.quantile([0,.25,.5,.75,1]).items()}
            a,b=numeric.quantile([.25,.75]);info['outside_1_5_IQR_count']=int(((numeric<a-1.5*(b-a))|(numeric>b+1.5*(b-a))).sum())
            info['outlier_policy']='Flag only; no automatic deletion.'
        fields[name]=info
    return dict(scope='Measured downloaded query, not entire producer catalogue.',rows=len(raw),columns=fields,
        column_count=len(raw.columns),physical_compressed_bytes=manifest['files']['snapshot.csv.gz']['bytes'],
        physical_original_bytes=manifest['snapshot_bytes'],raw_memory_bytes=int(raw.memory_usage(deep=True).sum()),
        silver_memory_bytes=int(silver.memory_usage(deep=True).sum()),exact_duplicates=int(raw.duplicated().sum()),
        business_key=key,business_key_repetitions=int(raw.duplicated(key).sum()),selection=manifest['selection'],
        representativeness=manifest['limitations'])


def export(adapter,tables,claims,manifest,out,code_hash):
    metadata=[]
    for name,questions,table in adapter.SPECS:
        variants=[]
        for mobile in [False,True]:
            plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10 if mobile else 12,'svg.hashsalt':'ADL-fieldlab-v3'})
            fig,ax=plt.subplots(figsize=(4.8,8.8) if mobile else (11.5,8.0))
            title,denominator,note,alt=adapter.draw(name,ax,tables,claims,mobile)
            width=48 if mobile else 123
            fig.suptitle(textwrap.fill(title,28 if mobile else 80),x=.05,y=.98,ha='left',fontweight='bold',fontsize=15 if mobile else 19)
            fig.text(.05,.88,textwrap.fill(denominator,width),va='top',fontsize=9 if mobile else 11)
            footer=f'Fuente: {manifest["attribution_short"]}\nPeriodo: {manifest["period_label"]}\n{note}\nSnapshot {manifest["snapshot_sha256"][:12]} · código {code_hash[:12]} · ADL V3'
            fig.text(.05,.015,'\n'.join(textwrap.fill(line,width) for line in footer.splitlines()),va='bottom',fontsize=7.7 if mobile else 9)
            fig.subplots_adjust(left=.23 if mobile else .16,right=.94,top=.71,bottom=.40 if mobile else .28)
            ax.spines[['top','right']].set_visible(False)
            if mobile:
                ax.set_xlabel(textwrap.fill(ax.get_xlabel(),30))
                ax.set_ylabel(textwrap.fill(ax.get_ylabel(),30))
            fig.canvas.draw();renderer=fig.canvas.get_renderer();undrawn=set()
            for coord,limits in [(ax.xaxis,ax.get_xlim()),(ax.yaxis,ax.get_ylim())]:
                low,high=sorted(limits)
                for tick in coord.get_major_ticks()+coord.get_minor_ticks():
                    if not low<=tick.get_loc()<=high:undrawn.update([tick.label1,tick.label2])
            clipped=[]
            for text in fig.findobj(Text):
                if text not in undrawn and text.get_visible() and text.get_text():
                    box=text.get_window_extent(renderer)
                    if box.x0 < -1 or box.y0 < -1 or box.x1>fig.bbox.width+1 or box.y1>fig.bbox.height+1:clipped.append(text.get_text())
            require(not clipped,f'Clipped figure {name}/{mobile}: {clipped}')
            variant='mobile' if mobile else 'projection';prefix=out/f'{name}-{variant}'
            fig.savefig(prefix.with_suffix('.png'),dpi=120,metadata={'Software':'AI Discovery Labs'})
            fig.savefig(prefix.with_suffix('.svg'),metadata={'Date':None,'Creator':'AI Discovery Labs'})
            variants.append(dict(variant=variant,png=prefix.with_suffix('.png').name,svg=prefix.with_suffix('.svg').name,
                png_sha256=sha(prefix.with_suffix('.png')),svg_sha256=sha(prefix.with_suffix('.svg')),
                width=round(fig.get_figwidth()*120),height=round(fig.get_figheight()*120),denominator=denominator,note=note,
                text_bounds_check='PASS'))
            plt.close(fig)
        metadata.append(dict(id=name,title=title,alt=alt,question_ids=questions,table='../gold/'+table+'.csv',
            table_sha256=sha(out.parent/'gold'/f'{table}.csv'),source_url=manifest['source_url'],
            source_sha256=manifest['snapshot_sha256'],code_sha256=code_hash,period=manifest['period_label'],variants=variants))
    write(out/'figures.json',metadata)
    return metadata
