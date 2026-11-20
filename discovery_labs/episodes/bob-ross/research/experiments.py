#!/usr/bin/env python3
"""Exploratory O1, offline and stdlib only. See PROTOCOL.md before interpreting."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
import platform
import random
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from audit import audit, HERE, ROOT, INCOMPLETE
from reconcile import write_csv
sys.path.insert(0, str(ROOT))
import clustering
from run import FEATURES

SEED = 20261119
MOTIFS = ('OCEAN','OVAL_FRAME','WINTER','CABIN')


def quantile(values, p):
    vals = sorted(values)
    if not vals:
        return None
    x = (len(vals)-1)*p
    low = math.floor(x); high = math.ceil(x)
    return vals[low]+(vals[high]-vals[low])*(x-low)


def adjust(ps, method='holm'):
    order = sorted(range(len(ps)), key=lambda i:ps[i])
    out = [1.]*len(ps); m=len(ps)
    if method == 'holm':
        val=0.
        for rank, i in enumerate(order):
            val=max(val, min(1., (m-rank)*ps[i])); out[i]=val
    elif method == 'bh':
        val=1.
        for rank in range(m-1,-1,-1):
            i=order[rank]; val=min(val, ps[i]*m/(rank+1)); out[i]=val
    else:
        raise ValueError(method)
    return out


def fisher(a,b,c,d):
    """Two-sided probability-order Fisher; margins fixed, no pseudocounts."""
    n=a+b+c+d; row=a+b; col=a+c
    def prob(x):
        return math.comb(col,x)*math.comb(n-col,row-x)/math.comb(n,row)
    observed=prob(a)
    return min(1.,sum(prob(x) for x in range(max(0,row-(n-col)),min(row,col)+1)
                      if prob(x)<=observed*(1+1e-12)))


def contingency(a,b):
    return [sum(x==1 and y==1 for x,y in zip(a,b)),
            sum(x==1 and y==0 for x,y in zip(a,b)),
            sum(x==0 and y==1 for x,y in zip(a,b)),
            sum(x==0 and y==0 for x,y in zip(a,b))]


def pair_stats(a,b):
    aa,bb,cc,dd=contingency(a,b); n=len(a)
    ex=(aa+bb)*(aa+cc)/n if n else 0
    return {'n':n,'n11':aa,'n10':bb,'n01':cc,'n00':dd,
            'expected_n11':ex,'lift':aa/ex if ex else None,
            'odds_ratio':aa*dd/(bb*cc) if bb*cc else None,
            'or_boundary':bool(not bb*cc), 'p_fisher_two_sided':fisher(aa,bb,cc,dd)}


def sequence_blocks(rows, population):
    """Each block stores real positions. Missing/guest episodes never close gaps."""
    grouped=defaultdict(list)
    for r in rows:
        grouped[r['season']].append(r)
    blocks=[]
    for season in sorted(grouped):
        rr=sorted(grouped[season],key=lambda r:r['id'])
        selected=[r for r in rr if (population=='all' or not r['guest'])
                  and (population!='host_complete' or r['id'] not in INCOMPLETE)]
        positions=[int(r['id'][-2:]) for r in selected]
        edges=[(i,i+1) for i in range(len(selected)-1) if positions[i+1]==positions[i]+1]
        blocks.append((selected,edges))
    return blocks


def sequence(rows, population, permutations):
    rng=random.Random(SEED)
    blocks=sequence_blocks(rows,population)
    obs=[0]*4; expected=[0.]*4; transitions=[[[0,0],[0,0]] for _ in MOTIFS]
    n_edges=sum(len(edges) for _,edges in blocks)
    vectors=[]
    for rr,edges in blocks:
        x=[tuple(r['flags'][m] for m in MOTIFS) for r in rr]
        vectors.append((x,edges))
        for j in range(4):
            k=sum(v[j] for v in x); n=len(x)
            expected[j]+=len(edges)*k*(k-1)/(n*(n-1)) if n>1 else 0
            for a,b in edges:
                transitions[j][x[a][j]][x[b][j]]+=1
                obs[j]+=x[a][j]*x[b][j]
    nulls=[[] for _ in MOTIFS]
    for _ in range(permutations):
        count=[0]*4
        for x,edges in vectors:
            shuffled=x.copy(); rng.shuffle(shuffled)
            for a,b in edges:
                va,vb=shuffled[a],shuffled[b]
                for j in range(4): count[j]+=va[j]*vb[j]
        for j in range(4): nulls[j].append(count[j])
    results=[]
    for j,m in enumerate(MOTIFS):
        lower=(1+sum(v<=obs[j] for v in nulls[j]))/(permutations+1)
        upper=(1+sum(v>=obs[j] for v in nulls[j]))/(permutations+1)
        tr=transitions[j]
        results.append({'motif':m, 'population':population, 'episodes':sum(len(rr) for rr,_ in blocks),
                        'eligible_edges':n_edges,'observed_11':obs[j],'expected_11_exact':expected[j],
                        'ratio_observed_expected':obs[j]/expected[j] if expected[j] else None,
                        'null_interval_95':[quantile(nulls[j],.025),quantile(nulls[j],.975)],
                        'null_mean_mc':sum(nulls[j])/permutations,
                        'p_inhibition':lower,'p_runs_exploratory':upper,
                        'mc_se_inhibition':math.sqrt(lower*(1-lower)/(permutations+1)),
                        'transition_counts_00_01_10_11':[tr[0][0],tr[0][1],tr[1][0],tr[1][1]],
                        'markov_p1_given1':tr[1][1]/sum(tr[1]) if sum(tr[1]) else None,
                        'markov_p1_given0':tr[0][1]/sum(tr[0]) if sum(tr[0]) else None})
    for r,p,pu in zip(results,adjust([r['p_inhibition'] for r in results]),
                     adjust([r['p_runs_exploratory'] for r in results])):
        r['p_inhibition_holm']=p; r['p_runs_holm_exploratory']=pu
        r['supports_H8_inhibition']=p<.05 and r['ratio_observed_expected'] is not None and r['ratio_observed_expected']<.7
    return results, nulls


def cabin_winter(rows, permutations, bootstrap):
    host=[r for r in rows if not r['guest']]
    x=[r['flags']['CABIN'] for r in host]; y=[r['flags']['WINTER'] for r in host]
    out=pair_stats(x,y)
    groups=[[r for r in host if r['season']==s] for s in range(1,32)]
    rng=random.Random(SEED+1); null=[]
    for _ in range(permutations):
        count=0
        for g in groups:
            winter=[r['flags']['WINTER'] for r in g]; rng.shuffle(winter)
            count+=sum(r['flags']['CABIN']*v for r,v in zip(g,winter))
        null.append(count)
    ex=sum(sum(r['flags']['CABIN'] for r in g)*sum(r['flags']['WINTER'] for r in g)/len(g) for g in groups)
    out['expected_n11_within_season']=ex
    out['p_season_permutation_two_sided']=(1+sum(abs(v-ex)>=abs(out['n11']-ex)-1e-12 for v in null))/(permutations+1)
    boot=[]
    for _ in range(bootstrap):
        sample=[r for _ in groups for r in rng.choice(groups)]
        a=sum(r['flags']['CABIN'] for r in sample); b=sum(r['flags']['WINTER'] for r in sample)
        both=sum(r['flags']['CABIN']*r['flags']['WINTER'] for r in sample)
        if a*b: boot.append(both*len(sample)/(a*b))
    out['lift_season_bootstrap_interval_95']=[quantile(boot,.025),quantile(boot,.975)]
    out['valid_bootstrap_replicates']=len(boot)
    out['complete_case_sensitivity']=pair_stats(
        [r['flags']['CABIN'] for r in host if r['id'] not in INCOMPLETE],
        [r['flags']['WINTER'] for r in host if r['id'] not in INCOMPLETE])
    return out


def associations(rows):
    host=[r for r in rows if not r['guest']]; out=[]
    for a,b in itertools.combinations(FEATURES,2):
        out.append({'motif_a':a,'motif_b':b,**pair_stats([r['motifs'][a] for r in host],
                                                       [r['motifs'][b] for r in host]),
                    'shared_input_columns':';'.join(sorted(set(FEATURES[a])&set(FEATURES[b])))})
    for r,q in zip(out,adjust([r['p_fisher_two_sided'] for r in out],'bh')):
        r['q_bh_66']=q
    return out


def clusters(rows, bootstrap):
    host=[r for r in rows if not r['guest']]
    points=[tuple(r['motifs'][key] for key in FEATURES) for r in host]
    dj=clustering.matrix(points,'jaccard'); de=clustering.matrix(points,'euclidean')
    grid=[]; lj=cj=None
    for k in range(2,7):
        labels,centers=clustering.medoids(dj,k=k)
        grid.append({'k':k,'sizes':[labels.count(g) for g in range(k)],
                     'medoids':[host[i]['id'] for i in centers],
                     'silhouette_same_jaccard_space':clustering.silhouette(dj,labels)})
        if k==4: lj,cj=labels,centers
    le,ce=clustering.medoids(de,k=4)
    nt=[p[1:] for p in points]; ln,_=clustering.medoids(clustering.matrix(nt,'jaccard'),k=4)
    complete=[i for i,r in enumerate(host) if r['id'] not in INCOMPLETE]
    lc,cc=clustering.medoids([[dj[i][j] for j in complete] for i in complete],k=4)
    season_indices=[[i for i,r in enumerate(host) if r['season']==s] for s in range(1,32)]
    rng=random.Random(SEED+2); ari_boot=[]
    for _ in range(bootstrap):
        ids=[i for _ in season_indices for i in rng.choice(season_indices)]
        ari_boot.append(clustering.ari([lj[i] for i in ids],[le[i] for i in ids]))
    assignments=[{'episode':r['id'],'season':r['season'],'jaccard_k4':lj[i],
                  'euclidean_k4':le[i],'without_tree_k4':ln[i],
                  'is_jaccard_medoid':i in cj} for i,r in enumerate(host)]
    report={'n':len(host),'feature_names':list(FEATURES),'k_grid':grid,
            'ari_jaccard_euclidean_k4':clustering.ari(lj,le),
            'ari_without_tree_k4':clustering.ari(lj,ln),
            'ari_excluding_three_zero_rows_refit':clustering.ari([lj[i] for i in complete],lc),
            'complete_case_medoids':[host[complete[i]]['id'] for i in cc],
            'conditional_ari_bootstrap_interval_95':[quantile(ari_boot,.025),quantile(ari_boot,.975)],
            'bootstrap_caveat':'31 seasons resampled; fixed full-data partitions; NOT refit stability',
            'status':'EXECUTED_PARTIAL_H6; no palettes/KMeans/Bernoulli or visual validation',
            'negative_control':'No episode identifiers, season or author flags entered feature matrix'}
    return report,assignments


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--permutations',type=int,default=10000)
    ap.add_argument('--bootstrap',type=int,default=2000)
    ap.add_argument('--output',type=Path,default=HERE/'results')
    args=ap.parse_args()
    if args.permutations<1 or args.bootstrap<1: ap.error('positive replicate counts required')
    check,rows=audit()
    args.output.mkdir(exist_ok=True,parents=True)
    seq=[]
    for population in ('all','host','host_complete'):
        stats,nulls=sequence(rows,population,args.permutations); seq.extend(stats)
        write_csv(args.output/f'sequence_null_{population}.csv',[
            {'replicate':i+1,**{m:nulls[j][i] for j,m in enumerate(MOTIFS)}} for i in range(args.permutations)])
        print(f'BR-14 {population} complete',flush=True)
    write_csv(args.output/'sequence.csv',seq)
    assoc=associations(rows); write_csv(args.output/'associations.csv',assoc)
    cw=cabin_winter(rows,args.permutations,args.bootstrap)
    cl,assign=clusters(rows,args.bootstrap); write_csv(args.output/'cluster_assignments.csv',assign)
    report={'protocol':'PROTOCOL.md','source_sha256':check['sha256'],
            'status':'EXECUTED_EXPLORATORY_NOT_APPROVED','seed':SEED,
            'permutations':args.permutations,'bootstrap_replicates':args.bootstrap,
            'BR-14':{'results':seq,'status':'EXECUTED_O1; prediction and recording chronology not identified'},
            'BR-07':{'tested_pairs':66,'fdr_bh_below_05':sum(r['q_bh_66']<.05 for r in assoc),
                     'cabin_winter':cw,'status':'EXECUTED_O1_PAIRS; H3 timing and triples not executed'},
            'BR-09':cl}
    (args.output/'o1_results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    source_paths=[Path(__file__),HERE/'audit.py',HERE/'reconcile.py',HERE/'PROTOCOL.md',ROOT/'run.py',ROOT/'clustering.py',ROOT/'entry_pack/questions_master.json']
    manifest={'executed_at_utc':datetime.now(timezone.utc).isoformat(),
              'python':platform.python_version(),'platform':platform.platform(),
              'source_sha256':check['sha256'],'command':f'python research/experiments.py --permutations {args.permutations} --bootstrap {args.bootstrap}',
              'input_code_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths},
              'output_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(args.output.iterdir()) if p.is_file() and p.name!='run_manifest.json'},
              'replication':'Offline stdlib, seed fixed; manifest clock/platform can differ; numeric artifacts deterministic in same Python version'}
    (args.output/'run_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'BR-14':seq[:4],'BR-07_CABIN_WINTER':cw,'BR-09':cl},ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
