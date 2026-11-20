#!/usr/bin/env python3
"""BR-09-O2. Run only after DR-05a.md; never activates human-visual O3."""
import hashlib
import itertools
import json
from pathlib import Path
from audit import audit, HERE, ROOT, INCOMPLETE, AUTHOR
from experiments import clustering
from reconcile import write_csv
from run import FEATURES


def aligned_changes(a,b,k=4):
    """Cluster numbers are arbitrary; maximize overlap before counting changes."""
    mapping=max(itertools.permutations(range(k)),
                key=lambda p:sum(x==p[y] for x,y in zip(a,b)))
    changed=[i for i,(x,y) in enumerate(zip(a,b)) if x!=mapping[y]]
    return changed,list(mapping)


def main():
    gate=(HERE/'DR-05a.md').read_text()
    if 'Activar únicamente BR-09-O2' not in gate:
        raise ValueError('Missing scoped activation checkpoint')
    _,rows=audit();host=[r for r in rows if not r['guest']]
    saved=json.loads((HERE/'results/o1_results.json').read_text())
    points=[tuple(r['motifs'][k] for k in FEATURES) for r in host]
    dj=clustering.matrix(points,'jaccard')
    primary,_=clustering.medoids(dj,k=4)
    euclidean,_=clustering.medoids(clustering.matrix(points,'euclidean'),k=4)
    no_tree,_=clustering.medoids(clustering.matrix([p[1:] for p in points],'jaccard'),k=4)
    changes={}
    for name,labels in [('euclidean',euclidean),('without_tree',no_tree)]:
        changed,mapping=aligned_changes(primary,labels)
        changes[name]={'changed_n':len(changed),'n':len(host),'mapping_to_primary':mapping,
                       'changed_ids':[host[i]['id'] for i in changed],
                       'ari':clustering.ari(primary,labels)}
    keep=[i for i,r in enumerate(host) if r['id'] not in INCOMPLETE]
    complete_d=[[dj[i][j] for j in keep] for i in keep]
    grid=[]
    for k in range(2,7):
        labels,centers=clustering.medoids(complete_d,k=k)
        grid.append({'k':k,'n':len(keep),'sizes':[labels.count(g) for g in range(k)],
                     'medoids':[host[keep[c]]['id'] for c in centers],
                     'silhouette_same_jaccard_space':clustering.silhouette(complete_d,labels),
                     'ari_vs_full_k4_on_common_rows':clustering.ari([primary[i] for i in keep],labels)})
    raw_columns=[k for k in host[0]['flags'] if k not in AUTHOR]
    raw_points=[tuple(r['flags'][k] for k in raw_columns) for r in host]
    raw_labels,raw_centers=clustering.medoids(clustering.matrix(raw_points,'jaccard'),k=4)
    loo=[]
    for season in range(1,32):
        train=[i for i,r in enumerate(host) if r['season']!=season]
        labels,centers=clustering.medoids([[dj[i][j] for j in train] for i in train],k=4)
        centers=[train[c] for c in centers]
        assigned=[min(range(4),key=lambda g:(dj[i][centers[g]],g)) for i in range(len(host))]
        changed,mapping=aligned_changes(primary,assigned)
        loo.append({'omitted_season':season,'train_n':len(train),
                    'ari_all_381':clustering.ari(primary,assigned),
                    'changed_n_all_381':len(changed),
                    'medoids':';'.join(host[c]['id'] for c in centers)})
    result={
        'id':'BR-09-O2','parent_id':'BR-09-O1','status':'EXECUTED_EXPLORATORY',
        'trigger_evidence':'results/o1_results.json#/BR-09',
        'activation_checkpoint':'DR-05a.md','source_sha256':saved['source_sha256'],
        'aligned_changes_k4':changes,'complete_case_grid':grid,
        'representation_sensitivity':{'raw_columns':raw_columns,'n_features':len(raw_columns),
                                      'ari_12_families_vs_64_non_author_labels':clustering.ari(primary,raw_labels),
                                      'medoids_64':[host[c]['id'] for c in raw_centers]},
        'leave_one_season_out':loo,
        'limits':['LOSO compares learned labels to full-data labels, not independent artistic truth',
                  'Deterministic heuristic is not proven global PAM optimum',
                  '12-motif zero profiles may arise through aggregation; only 3 are raw-all-zero here',
                  'BR-09-O3 remains CONDITIONAL; authorized images and human protocol missing'],
    }
    out=HERE/'progressive_results';out.mkdir(exist_ok=True)
    (out/'br09_o2.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    write_csv(out/'leave_one_season_out.csv',loo)
    (out/'manifest.json').write_text(json.dumps({
        'activation_checkpoint_sha256':hashlib.sha256((HERE/'DR-05a.md').read_bytes()).hexdigest(),
        'o1_results_sha256':hashlib.sha256((HERE/'results/o1_results.json').read_bytes()).hexdigest(),
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'outputs':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.name!='manifest.json'},
    },indent=2)+'\n')
    print(json.dumps({'changes':{k:v['changed_n'] for k,v in changes.items()},
                      'complete_case_grid':grid,'loso_min_ari':min(r['ari_all_381'] for r in loo),
                      'representation_ari':result['representation_sensitivity']['ari_12_families_vs_64_non_author_labels']},indent=2))


if __name__=='__main__':main()
