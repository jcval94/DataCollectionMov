#!/usr/bin/env python3
"""Offline reference experiments. No API, model inference, or credential loading."""
from __future__ import annotations
import argparse,csv,hashlib,json,math,platform,re,time,sys
from decimal import Decimal
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from scipy.spatial.distance import pdist,squareform
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score,adjusted_rand_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE=Path(__file__).resolve().parents[1]
SEED=20261116
CASES=['uci-retail','nba-elo','bob-ross-elementos']
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(path,obj):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def load(case):
    folder=BASE/'pilots'/case/'data';m=json.loads((folder/'manifest.json').read_text());p=folder/'snapshot.csv'
    if sha(p)!=m['snapshot_sha256']:raise ValueError('Snapshot modificado: hash no coincide')
    d=pd.read_csv(p,dtype=str,keep_default_na=False)
    if list(d)!=m['columns'] or len(d)!=m['rows']:raise ValueError('Esquema o número de filas no coincide')
    if d.empty:raise ValueError('Snapshot vacío')
    return d,m
def quality(d):
    return {'rows':len(d),'columns':len(d.columns),'blank_by_column':{k:int((d[k]=='').sum()) for k in d},'exact_duplicate_rows':int(d.duplicated().sum()),'schema':list(d)}
def wilson(w,n):
    if not n:return None
    z=1.95996398454;p=w/n;den=1+z*z/n;c=(p+z*z/(2*n))/den;h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return [c-h,c+h]
def bar(path,labels,a,b,labela,labelb,xlabel,title):
    y=np.arange(len(labels));fig,ax=plt.subplots(figsize=(9,5));ax.barh(y-.18,a,.35,label=labela,color='#24546a');ax.barh(y+.18,b,.35,label=labelb,color='#c54e36');ax.set_yticks(y,labels);ax.invert_yaxis();ax.set_xlabel(xlabel);ax.set_title(title);ax.legend();fig.tight_layout();fig.savefig(path,dpi=120,metadata={'Software':'AI Discovery Labs V2'});plt.close(fig)

def retail(d,out):
    required={'InvoiceNo','StockCode','Quantity','UnitPrice','InvoiceDate','Country','customer_id_missing'}
    if not required<=set(d):raise ValueError('Faltan columnas retail')
    if 'CustomerID' in d:raise ValueError('No distribuir identificadores de cliente')
    dates=pd.to_datetime(d.InvoiceDate,errors='raise');assert dates.min()>=pd.Timestamp('2011-11-01') and dates.max()<pd.Timestamp('2011-12-01')
    mask=d.StockCode.str.fullmatch(r'\d{5}[A-Za-z]*')
    qty=d.Quantity.map(Decimal);price=d.UnitPrice.map(Decimal)
    assert all(x.is_finite() and x==x.to_integral_value() for x in qty)
    assert all(x.is_finite() for x in price)
    valid=mask & price.gt(0) & qty.ne(0) & ~(d.InvoiceNo.str.upper().str.startswith('C') & qty.gt(0))
    x=d.loc[valid].copy();x['value']=[q*p for q,p in zip(qty[valid],price[valid])]
    def totals(frame):
        result={}
        for code,g in frame.groupby('StockCode',sort=True):
            vals=list(g.value);gross=sum((max(v,Decimal(0)) for v in vals),Decimal(0));credits=sum((max(-v,Decimal(0)) for v in vals),Decimal(0));result[code]={'gross':gross,'credits':credits,'net':gross-credits,'lines':len(g)}
        for field in ['gross','net']:
            for rank,code in enumerate(sorted(result,key=lambda c:(-result[c][field],c)),1):result[code]['rank_'+field]=rank
        return result
    raw=totals(x);dedup=totals(x.drop_duplicates(subset=list(d)))
    # Independent route: Pandas group-by uses exact Decimal values, checked against loop totals.
    independent=x.groupby('StockCode').value.sum().to_dict()
    assert all(independent[k]==v['net'] for k,v in raw.items())
    assert sum(v['gross']-v['credits'] for v in raw.values())==sum(v['net'] for v in raw.values())
    rows=[dict(code=c,**{k:str(v) if isinstance(v,Decimal) else v for k,v in vals.items()}) for c,vals in raw.items()]
    pd.DataFrame(rows).sort_values('rank_gross').to_csv(out/'ranking.csv',index=False)
    top=sorted(raw,key=lambda c:raw[c]['rank_gross'])[:10]
    bar(out/'comparison.png',top,[float(raw[c]['gross']) for c in top],[float(raw[c]['net']) for c in top],'Bruto positivo','Neto firmado','GBP, muestra de 300 facturas','El denominador también cuenta una historia')
    missing_lines=float(d.customer_id_missing.astype(int).mean());missing_invoices=float(d.groupby('InvoiceNo').customer_id_missing.first().astype(int).mean())
    bar(out/'denominators.png',['Datos sin ID'],[100*missing_lines],[100*missing_invoices],'Por líneas','Por facturas','Porcentaje; denominadores diferentes','La exclusión depende de qué estás contando')
    sumfields=lambda z:{k:str(sum(v[k] for v in z.values())) for k in ['gross','credits','net']}
    changed=sum(v['rank_gross']!=v['rank_net'] for v in raw.values())
    return {'question_ids':['D31-A','D31-E','D31-B'],'routes':{'A':'Ranking de neto firmado, no margen','E':'Comparar bruto/neto y duplicados','B':'Completitud: líneas frente a facturas sin identificador'},'input_rows':len(d),'eligible_rows':len(x),'excluded_rows':int((~valid).sum()),'invoices':int(d.InvoiceNo.nunique()),'products':len(raw),'date_min':str(dates.min()),'date_max':str(dates.max()),'totals':sumfields(raw),'deduplicated_totals':sumfields(dedup),'products_changing_position':changed,'rank_correlation':float(spearmanr([v['rank_gross'] for v in raw.values()],[v['rank_net'] for v in raw.values()]).statistic),'missing_customer_line_fraction':float(d.customer_id_missing.astype(int).mean()),'missing_customer_invoice_fraction':float(d.groupby('InvoiceNo').customer_id_missing.first().astype(int).mean()),'adversarial_result':'Se ejecutan bruto/neto, eliminación de duplicados y cambio de denominador líneas/facturas. Los créditos muestreados no están emparejados necesariamente con ventas muestreadas.','inference':'Descripción exacta del snapshot seleccionado por factura. Sin intervalo iid por línea; no es estimación del margen ni del mercado.','checks':['hash','schema','finite_integer_quantity','positive_price_policy','independent_net_computation','gross_minus_credit_equals_net','duplicate_sensitivity','denominator_sensitivity','customer_id_removed']}

def nba(d,out):
    required={'game_id','game_location','forecast','pts','opp_pts','elo_i','elo_n','year_id','date_game','is_playoffs','_iscopy','team_id'}
    if not required<=set(d):raise ValueError('Faltan columnas NBA')
    if not d.year_id.eq('2015').all():raise ValueError('Temporada no esperada')
    counts=d.groupby('game_id').size();assert counts.eq(2).all()
    assert not d.duplicated(['game_id','team_id']).any()
    numeric=['forecast','pts','opp_pts','elo_i','elo_n'];d=d.copy()
    for k in numeric:d[k]=pd.to_numeric(d[k],errors='raise')
    assert d.forecast.between(0,1).all() and (d.pts!=d.opp_pts).all()
    assert d.groupby('game_id').forecast.sum().sub(1).abs().max()<1e-3
    games=d[d._iscopy.eq('0')].copy();assert games.game_id.nunique()==len(games)==len(counts)
    home=d[d.game_location.eq('H')].copy();assert home.game_id.nunique()==len(home)
    home['win']=(home.pts>home.opp_pts).astype(int)
    phase=[]
    for p,g in home.groupby('is_playoffs'):
        wins=int(g.win.sum());phase.append({'phase':'Playoffs' if p=='1' else 'Regular','wins':wins,'n':len(g),'rate':wins/len(g),'wilson_descriptive_only':wilson(wins,len(g))})
    # Each date is one resampling block, preserving games played on that date.
    daily=home.groupby('date_game').win.agg(['sum','count']).to_numpy();rng=np.random.default_rng(SEED)
    boot=[]
    for _ in range(1000):
        z=daily[rng.integers(0,len(daily),len(daily))];boot.append(float(z[:,0].sum()/z[:,1].sum()))
    ci=np.quantile(boot,[.025,.975]).tolist()
    phase_boot={}
    for p0,g0 in home.groupby('is_playoffs'):
        z0=g0.groupby('date_game').win.agg(['sum','count']).to_numpy()
        phase_boot[p0]=[]
        for _ in range(1000):
            z=z0[rng.integers(0,len(z0),len(z0))];phase_boot[p0].append(float(z[:,0].sum()/z[:,1].sum()))
    phase_difference=float(home.loc[home.is_playoffs.eq('1'),'win'].mean()-home.loc[home.is_playoffs.eq('0'),'win'].mean())
    phase_difference_interval=np.quantile(np.asarray(phase_boot['1'])-np.asarray(phase_boot['0']),[.025,.975]).tolist()
    pd.DataFrame(phase).to_csv(out/'phases.csv',index=False)
    fig,ax=plt.subplots(figsize=(7,4));ax.bar([f"{z['phase']}\nn={z['n']} partidos" for z in phase],[100*z['rate'] for z in phase],color=['#24546a','#c54e36']);ax.axhline(50,color='#777',linestyle='--');ax.set(ylim=(0,100),ylabel='Porcentaje de victorias del equipo local',title='Fases comparables: mostrar también el tamaño de muestra');fig.tight_layout();fig.savefig(out/'phases.png',dpi=120,metadata={'Software':'AI Discovery Labs V2'});plt.close(fig)
    y=(games.pts>games.opp_pts).astype(int);p=games.forecast
    brier=float(np.mean((p-y)**2));baseline=float(np.mean((.5-y)**2))
    # Mirror perspective changes sign of y and complements p; Brier is invariant.
    ally=(d.pts>d.opp_pts).astype(int);allbrier=float(np.mean((d.forecast-ally)**2));assert abs(brier-allbrier)<1e-4
    cal=pd.DataFrame({'p':p,'y':y});cal['bin']=pd.cut(p,[0,.2,.4,.6,.8,1],include_lowest=True)
    c=cal.groupby('bin',observed=True).agg(predicted=('p','mean'),observed=('y','mean'),n=('y','size')).reset_index();c['bin']=c['bin'].astype(str);c.to_csv(out/'calibration.csv',index=False)
    fig,ax=plt.subplots(figsize=(7,5));ax.plot([0,1],[0,1],color='#777',ls='--');ax.scatter(c.predicted,c.observed,s=c.n,color='#24546a',alpha=.7);ax.set(xlim=(0,1),ylim=(0,1),xlabel='Probabilidad previa media',ylabel='Fracción observada de victorias',title='Calibración: un punto por intervalo; área = partidos');fig.tight_layout();fig.savefig(out/'comparison.png',dpi=120,metadata={'Software':'AI Discovery Labs V2'});plt.close(fig)
    return {'question_ids':['D10-D2','D10-E'],'routes':{'D2':'Comparar victoria local por fase','E':'Calibración de forecast previo y filas espejo'},'team_game_rows':len(d),'unique_games':len(games),'home_games':len(home),'home_win_rate':float(home.win.mean()),'block_bootstrap_date_95':ci,'phases':phase,'phase_difference_playoffs_minus_regular':phase_difference,'phase_difference_block_95':phase_difference_interval,'brier':brier,'baseline_brier':baseline,'mirror_brier':allbrier,'mirror_game_count_inflation':len(d)/len(games),'date_min':str(pd.to_datetime(d.date_game).min()),'date_max':str(pd.to_datetime(d.date_game).max()),'feature_allowlist':['forecast','elo_i','game_location','is_playoffs'],'forbidden_postgame_features':['pts','opp_pts','elo_n'],'adversarial_result':'Se deduplican partidos, se verifican probabilidades complementarias y se calcula sensibilidad del Brier por perspectiva. elo_n está prohibido como predictor: incorpora el resultado. Marcadores sólo son etiquetas.','inference':'El bootstrap por fecha es sensibilidad exploratoria; no captura toda dependencia por equipos/series ni estima efecto causal de jugar en casa. Wilson iid se muestra únicamente como contraste didáctico. La comparación por fase confunde composición de equipos y selección a playoffs.','checks':['hash','schema','mirror_pairs','unique_team_game','complementary_forecasts','one_row_per_game','independent_mirror_brier','prefeature_allowlist','date_block_bootstrap']}

def bob(d,out):
    labels=[c for c in d if c not in ['EPISODE','TITLE']]
    if d.EPISODE.duplicated().any() or not d.EPISODE.str.fullmatch(r'S\d{2}E\d{2}').all():raise ValueError('IDs Bob Ross inválidos')
    if not d[labels].isin(['0','1']).all().all():raise ValueError('Etiquetas no binarias')
    x=d[labels].astype(int);host=x[x.GUEST.eq(0)].copy()
    tree=host[['TREE','TREES']].max(axis=1);alltree=x[['TREE','TREES']].max(axis=1)
    exceptions=d.loc[host.index[tree.eq(0)],['EPISODE','TITLE']]
    exceptions.to_csv(out/'counterexamples.csv',index=False)
    # Zero shared-positive vectors are legitimate; Jaccard distance(empty,empty)=0.
    motifs=['TREE','TREES','MOUNTAIN','MOUNTAINS','SNOW','SNOWY_MOUNTAIN','LAKE','RIVER','OCEAN','CLOUDS','ROCKS','FLOWERS']
    a=host[motifs].to_numpy(dtype=bool);distance=squareform(pdist(a,metric='jaccard'));assert np.isfinite(distance).all() and np.allclose(distance,distance.T)
    model=AgglomerativeClustering(n_clusters=4,metric='precomputed',linkage='average');groups=model.fit_predict(distance)
    silhouette=float(silhouette_score(distance,groups,metric='precomputed'))
    # Compare a different metric, same k and sample; neither number is a discovered truth.
    otherdist=squareform(pdist(a.astype(float),metric='euclidean'));other=AgglomerativeClustering(n_clusters=4,metric='precomputed',linkage='average').fit_predict(otherdist)
    ari=float(adjusted_rand_score(groups,other));counts=np.bincount(groups,minlength=4)
    profile=pd.DataFrame(a.astype(int),columns=motifs).assign(group=groups).groupby('group').mean();profile.to_csv(out/'profiles.csv')
    fig,ax=plt.subplots(figsize=(10,4));im=ax.imshow(profile,vmin=0,vmax=1,cmap='YlGnBu');ax.set_xticks(range(len(motifs)),motifs,rotation=60,ha='right');ax.set_yticks(range(4),[f'Grupo {i}: n={n}' for i,n in enumerate(counts)]);ax.set_title('Cuatro grupos propuestos: prevalencia de motivos, sin ID');fig.colorbar(im,ax=ax,label='Fracción de episodios');fig.tight_layout();fig.savefig(out/'comparison.png',dpi=120,metadata={'Software':'AI Discovery Labs V2'});plt.close(fig)
    mountain=host[['MOUNTAIN','MOUNTAINS']].max(axis=1).eq(1);snow=host[['SNOW','SNOWY_MOUNTAIN']].max(axis=1).eq(1)
    bar(out/'beliefs.png',['Árboles registrados','Nieve si hay montaña'],[int(tree.sum()),int((mountain&snow).sum())],[int((tree==0).sum()),int((mountain&~snow).sum())],'Con motivo','Sin motivo','Episodios; denominador propio por fila','Un contraejemplo alcanza para cuestionar todos')
    return {'question_ids':['D85-C','D85-D1','D85-D2','D85-B'],'routes':{'C':'Clustering Jaccard frente a Euclídea','D1':'Buscar contraejemplos a todos tienen árboles','D2':'Nieve condicionada a montaña','B':'Invitados frente a anfitrión'},'episodes':len(d),'host_episodes':len(host),'guest_episodes':len(d)-len(host),'host_tree_n':int(tree.sum()),'host_tree_fraction':float(tree.mean()),'guest_tree_fraction':float(alltree[x.GUEST.eq(1)].mean()),'all_tree_fraction':float(alltree.mean()),'tree_counterexample_count':len(exceptions),'mountain_episodes':int(mountain.sum()),'mountain_without_snow':int((mountain&~snow).sum()),'jaccard_silhouette':silhouette,'jaccard_euclidean_ARI':ari,'cluster_sizes':counts.tolist(),'features':motifs,'k':4,'k_reason':'Restricción narrativa de cuatro salas, no número inferido de estilos naturales.','adversarial_result':'Se excluyen identificadores y temporada; se comparan invitados, se buscan contraejemplos y se cambia la distancia. La estabilidad se mide sin inventar etiquetas de verdad.','inference':'Censo del archivo de etiquetas de episodios, no muestra aleatoria de todas las pinturas; sin p-valores poblacionales. Etiquetas humanas no son píxeles ni número de árboles.','checks':['hash','schema','unique_episode','binary_labels','explicit_guest_exclusion','valid_jaccard_matrix','metric_sensitivity','counterexample_export','no_id_features']}

RUNNERS={'uci-retail':retail,'nba-elo':nba,'bob-ross-elementos':bob}
def run(case,output):
    start=time.perf_counter();d,m=load(case);out=Path(output)/case;out.mkdir(parents=True,exist_ok=True)
    result=RUNNERS[case](d,out)
    result.update(source_id=case,snapshot_sha256=m['snapshot_sha256'],quality=quality(d),seed=SEED,technical_status='EXECUTED_OFFLINE',classroom_status='PENDIENTE_ENSAYO_HUMANO_45_MIN',real_data=True,rights_reviewed=True)
    write(out/'results.json',result)
    elapsed=time.perf_counter()-start
    write(out/'runtime.json',{'seconds':elapsed,'python':platform.python_version(),'platform':platform.platform(),'script_sha256':sha(__file__),'numpy':np.__version__,'pandas':pd.__version__})
    print(json.dumps({'case':case,'status':result['technical_status'],'seconds':round(elapsed,3),'checks':len(result['checks'])},ensure_ascii=False),flush=True)
    return result
def main():
    p=argparse.ArgumentParser();p.add_argument('--case',choices=CASES+['all'],default='all');p.add_argument('--output',type=Path,default=BASE/'output');args=p.parse_args()
    for case in CASES if args.case=='all' else [args.case]:run(case,args.output)
if __name__=='__main__':main()
