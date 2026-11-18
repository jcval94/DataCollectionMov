"""Historical route graph, with explicit ID joins and structural rather than traffic metrics."""
import gzip
import json
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components
from scipy.spatial.distance import pdist
from scipy.stats import spearmanr
from sklearn.metrics import adjusted_rand_score

from v3.data import BASE, require, sha

CASE = 'openflights-red-aerea'
SEED = 20261117
AIRPORT_COLUMNS = ['airport_id','name','city','country','iata','icao','latitude','longitude',
                   'altitude_ft','timezone_offset','dst','timezone','type','metadata_source']
ROUTE_COLUMNS = ['airline','airline_id','source_iata','source_id','destination_iata','destination_id','codeshare','stops','equipment']


def load(folder=None):
    folder = Path(folder or BASE/'pilots'/CASE/'data')
    manifest = json.loads((folder/'manifest.json').read_text())
    require({e['file'] for e in manifest['files']}=={'airports.dat.gz','routes.dat.gz','LICENSE'}, 'Unexpected snapshot file set')
    import hashlib
    composite=hashlib.sha256(''.join(e['file']+e['raw_sha256'] for e in manifest['files']).encode()).hexdigest()
    require(composite==manifest['snapshot_sha256'],'Composite snapshot hash mismatch')
    frames = {}
    for entry in manifest['files']:
        path = folder/entry['file']
        require(sha(path)==entry['stored_sha256'], 'Stored hash mismatch: '+entry['file'])
        content = gzip.decompress(path.read_bytes()) if path.suffix=='.gz' else path.read_bytes()
        import hashlib, io
        require(hashlib.sha256(content).hexdigest()==entry['raw_sha256'], 'Raw hash mismatch')
        if path.suffix=='.gz':
            key = 'airports' if path.name.startswith('airports') else 'routes'
            columns = AIRPORT_COLUMNS if key=='airports' else ROUTE_COLUMNS
            frame = pd.read_csv(io.BytesIO(content), names=columns, dtype=str, keep_default_na=False)
            require(len(frame)==entry['rows'] and entry['column_counts']==[len(columns)], 'Schema/row mismatch')
            frames[key] = frame
    require(set(frames)=={'airports','routes'}, 'Both original tables required')
    return frames, manifest


def measure(frame):
    missing = frame.isin(['', r'\N'])
    if 'codeshare' in frame:
        missing['codeshare']=frame.codeshare.eq(r'\N')
    return dict(rows=len(frame), columns=len(frame.columns), memory_bytes=int(frame.memory_usage(deep=True).sum()),
                exact_duplicates=int(frame.duplicated().sum()),
                fields={c:dict(raw_type='string', blank_count=int(frame[c].eq('').sum()),missing_count=int(missing[c].sum()), missing_pct=100*float(missing[c].mean()),
                               missing_rule='Only \\N; empty is unflagged, not missing' if c=='codeshare' else 'Empty or \\N',
                               cardinality=int(frame.loc[~missing[c], c].nunique()),
                               frequent_values={str(k):int(v) for k,v in frame.loc[~missing[c],c].value_counts().head(5).items()}) for c in frame})


def prepare(raw):
    airports = raw['airports'].copy(); routes = raw['routes'].copy(); checks = []
    def check(name, condition, detail):
        require(bool(condition), name+': '+detail); checks.append(dict(rule=name, passed=True, detail=detail))
    check('airport_primary_key', airports.airport_id.str.fullmatch(r'\d+').all() and airports.airport_id.is_unique, 'Join by airport ID, never by a guessed IATA code.')
    for c in ['latitude','longitude']:
        airports[c] = pd.to_numeric(airports[c], errors='raise')
    check('coordinates', airports.latitude.between(-90,90).all() and airports.longitude.between(-180,180).all(), 'Finite WGS84 angular coordinates; no zero-as-null heuristic.')
    routes['stops'] = pd.to_numeric(routes.stops, errors='raise')
    check('stops_domain', routes.stops.ge(0).all() and routes.stops.mod(1).eq(0).all(), 'Nonnegative integer number of stops.')
    check('codeshare_domain', routes.codeshare.isin(['','Y']).all(), 'Empty codeshare flag means not flagged, not an absent route.')
    ids = set(airports.airport_id)
    policies = dict(source_id_unresolved=~routes.source_id.isin(ids), destination_id_unresolved=~routes.destination_id.isin(ids),
                    nonzero_stops=routes.stops.ne(0), self_loop=routes.source_id.eq(routes.destination_id))
    routes['exclusion_reason'] = ['|'.join(key for key, mask in policies.items() if mask.loc[i]) for i in routes.index]
    routes['eligible'] = routes.exclusion_reason.eq('')
    # IATA values can disagree with a newer metadata file. Record this; do not silently remap IDs.
    iata = airports.set_index('airport_id').iata
    routes['source_iata_disagrees'] = routes.source_id.isin(ids) & routes.source_iata.ne(routes.source_id.map(iata))
    routes['destination_iata_disagrees'] = routes.destination_id.isin(ids) & routes.destination_iata.ne(routes.destination_id.map(iata))
    routes.insert(0, 'raw_row_id', np.arange(len(routes))); airports.insert(0, 'raw_row_id', np.arange(len(airports)))
    eligible = routes[routes.eligible]
    edges = eligible.groupby(['source_id','destination_id'], sort=True).agg(
        route_records=('raw_row_id','size'), distinct_airlines=('airline','nunique'), codeshare_records=('codeshare',lambda x:int(x.eq('Y').sum()))).reset_index()
    check('row_conservation', len(routes)==len(raw['routes']) and len(airports)==len(raw['airports']), 'All raw records retained in Silver with row IDs.')
    check('edge_reconciliation', int(edges.route_records.sum())==int(routes.eligible.sum()), 'Collapsed edges preserve count of eligible airline records.')
    check('edge_primary_key', not edges.duplicated(['source_id','destination_id']).any(), 'One unique directed connection, not a flight count.')
    check('referential_integrity', edges.source_id.isin(ids).all() and edges.destination_id.isin(ids).all(), 'Both endpoints present in fixed airport metadata.')
    profiles = {key:measure(frame) for key,frame in raw.items()}
    profiles['observed_coordinates'] = dict(latitude_min=float(airports.latitude.min()), latitude_max=float(airports.latitude.max()),
                                            longitude_min=float(airports.longitude.min()), longitude_max=float(airports.longitude.max()))
    profiles['temporal'] = dict(event_dates_available=False, route_vintage='Producer states updates ended June 2014',
                               airport_vintage='Fixed repository metadata; not a verified 2014 airport census')
    profiles['granularity'] = 'Airline route records collapse into binary directed airport-to-airport adjacency; no frequency, capacity or passenger weights.'
    transformations = [dict(step=key, affected_rows=int(mask.sum()), excluded_only_from='Gold zero-stop graph',
                            consequence='Graph scope changes; rows remain in Silver and may have several flags.') for key,mask in policies.items()]
    transformations += [dict(step='coordinate_types',affected_rows=len(airports),columns=['latitude','longitude'],
                             consequence='Parse WGS84 degrees without rounding or zero imputation; exact raw bytes retained in Bronze.'),
                        dict(step='collapse_airline_records', input_rows=len(eligible), output_edges=len(edges),
                             consequence='Distinct airlines and codeshares do not become additional binary edges or passenger volume.'),
                        dict(step='iata_metadata_disagreement', affected_rows=int((routes.source_iata_disagrees|routes.destination_iata_disagrees).sum()),
                             consequence='IDs kept as supplied. Metadata vintage and recycled codes limit interpretation.')]
    return dict(airports=airports, routes=routes), edges, profiles, transformations, checks


def graph_from(edges):
    graph = nx.DiGraph()
    graph.add_nodes_from(sorted(set(edges.source_id)|set(edges.destination_id)))
    graph.add_edges_from(sorted(zip(edges.source_id, edges.destination_id)))
    return graph


def rank(frame, column):
    order = frame.sort_values([column,'airport_id'], ascending=[False,True]).index
    result = pd.Series(index=frame.index, dtype=int)
    result.loc[order] = np.arange(1,len(frame)+1)
    return result.astype(int)


def haversine_pairs(nodes):
    """All unordered pairs of active graph nodes. Great-circle rather than screen distance."""
    lat = np.deg2rad(nodes.latitude.to_numpy()); lon = np.deg2rad(nodes.longitude.to_numpy())
    first, second = np.triu_indices(len(nodes), 1)
    value = np.sin((lat[second]-lat[first])/2)**2 + np.cos(lat[first])*np.cos(lat[second])*np.sin((lon[second]-lon[first])/2)**2
    distance = 6371.0088 * 2*np.arcsin(np.sqrt(np.clip(value,0,1)))
    return first, second, distance


def country_resilience(graph, nodes):
    """Same remaining-node denominator after each removal, compared with uniform local removal."""
    undirected = graph.to_undirected()
    component = max(nx.connected_components(undirected), key=lambda x:(len(x), sorted(x)))
    order = sorted(component); index = {node:i for i,node in enumerate(order)}
    matrix = nx.to_scipy_sparse_array(undirected.subgraph(order), nodelist=order, dtype=np.int8, format='csr')
    node_data = nodes.set_index('airport_id').loc[order]
    rng = np.random.default_rng(SEED); rows = []
    def lost_others(removed, positions):
        keep = np.ones(len(order),dtype=bool); keep[index[removed]] = False
        n_components, labels = connected_components(csr_matrix(matrix[keep][:,keep]), directed=False)
        largest = int(np.bincount(labels).argmax())
        surviving_indices = np.flatnonzero(keep)
        retained = set(surviving_indices[labels==largest])
        return len(positions)-1-len(set(positions)&retained)
    for country,g in node_data.groupby('country', sort=True):
        if len(g)<5: continue
        members = list(g.index); positions = [index[x] for x in members]
        hub = sorted(members,key=lambda x:(-undirected.degree(x),x))[0]
        observed = lost_others(hub,positions)
        baseline_members = rng.choice(members,size=min(20,len(members)),replace=False).tolist()
        baseline = [lost_others(x,positions) for x in baseline_members]
        rows.append(dict(country=country, initial_airports_in_giant=len(members), removed_hub=hub,
                         remaining_denominator=len(members)-1, other_airports_disconnected=observed,
                         loss_fraction=observed/(len(members)-1), baseline_removals=len(baseline),
                         baseline_mean_other_disconnected=float(np.mean(baseline)),
                         baseline_max_other_disconnected=int(max(baseline))))
    return pd.DataFrame(rows)


def analyze(silver, edges):
    graph = graph_from(edges); undirected = graph.to_undirected()
    airports = silver['airports'].set_index('airport_id')
    nodes = airports.loc[sorted(graph)].reset_index()
    nodes['in_degree'] = nodes.airport_id.map(dict(graph.in_degree()))
    nodes['out_degree'] = nodes.airport_id.map(dict(graph.out_degree()))
    nodes['unique_neighbors'] = nodes.airport_id.map(dict(undirected.degree()))
    between = nx.betweenness_centrality(graph,k=min(128,len(graph)),normalized=True,seed=SEED)
    between_small = nx.betweenness_centrality(graph,k=min(64,len(graph)),normalized=True,seed=SEED)
    between_undirected = nx.betweenness_centrality(undirected,k=min(128,len(graph)),normalized=True,seed=SEED)
    nodes['betweenness_128'] = nodes.airport_id.map(between)
    nodes['betweenness_64'] = nodes.airport_id.map(between_small)
    nodes['betweenness_undirected'] = nodes.airport_id.map(between_undirected)
    for col in ['out_degree','unique_neighbors','betweenness_128','betweenness_64','betweenness_undirected']:
        nodes['rank_'+col] = rank(nodes,col)
    partitions = {}
    # Integer node labels make set iteration independent of Python's randomized string hash seed.
    canonical_ids=sorted(graph); numeric_graph=nx.relabel_nodes(undirected,{node:i for i,node in enumerate(canonical_ids)},copy=True)
    for resolution in [.8,1,1.2]:
        numeric_groups = nx.community.louvain_communities(numeric_graph, resolution=resolution,seed=SEED)
        groups = [{canonical_ids[i] for i in group} for group in numeric_groups]
        groups = sorted(groups,key=lambda g:(-len(g),sorted(g)))
        partitions[resolution] = {node:i for i,g in enumerate(groups) for node in g}
    nodes['community'] = nodes.airport_id.map(partitions[1])
    groups = [set(nodes.loc[nodes.community.eq(i),'airport_id']) for i in sorted(nodes.community.unique())]
    community_summary = nodes.groupby('community',sort=True).agg(airports=('airport_id','size'),route_neighbors=('unique_neighbors','sum')).reset_index()
    countries = nodes.groupby('community').country.apply(lambda x:', '.join(x.value_counts().head(2).index)).to_dict()
    community_summary['top_countries'] = community_summary.community.map(countries)
    stability = pd.DataFrame([dict(resolution=r,communities=len(set(p.values())),
        ARI_vs_resolution1=float(adjusted_rand_score(nodes.community,[p[x] for x in nodes.airport_id]))) for r,p in partitions.items()])
    # Same graph and community sizes; scramble memberships, not edges. Exploratory reference, not a fitted p-value.
    rng = np.random.default_rng(SEED); null_modularity = []
    order = nodes.airport_id.to_numpy(); lengths = np.cumsum([len(g) for g in groups])[:-1]
    for repetition in range(20):
        shuffled = rng.permutation(order); random_groups = [set(g) for g in np.split(shuffled,lengths)]
        null_modularity.append(dict(replicate=repetition,modularity=float(nx.community.modularity(undirected,random_groups))))
    e = edges.assign(source_community=edges.source_id.map(partitions[1]),destination_community=edges.destination_id.map(partitions[1]))
    flows = e.groupby(['source_community','destination_community']).size().reset_index(name='directed_edges')
    # Neighbor-only geographic denominator, with thresholds registered before examining results.
    first,second,distance = haversine_pairs(nodes)
    present = {(min(a,b),max(a,b)) for a,b in undirected.edges()}
    ids = nodes.airport_id.to_numpy()
    connected = np.fromiter(((min(ids[i],ids[j]),max(ids[i],ids[j])) in present for i,j in zip(first,second)),dtype=bool,count=len(first))
    distance_table = []
    for threshold in [100,250,500]:
        mask = distance<=threshold; n = int(mask.sum()); k = int((mask&connected).sum())
        distance_table.append(dict(threshold_km=threshold,unordered_pairs=n,connected_either_direction=k,fraction=k/n if n else None))
    nearby = pd.DataFrame(distance_table)
    # A real metadata disagreement deserves an analysis, not just a caveat. Keep the node universe fixed.
    r=silver['routes']
    strict_routes=r.loc[r.eligible & ~r.source_iata_disagrees & ~r.destination_iata_disagrees & ~r.source_iata.isin(['',r'\N']) & ~r.destination_iata.isin(['',r'\N'])]
    strict_graph=nx.DiGraph();strict_graph.add_nodes_from(sorted(graph));strict_graph.add_edges_from(sorted(set(zip(strict_routes.source_id,strict_routes.destination_id))))
    strict_undirected=strict_graph.to_undirected();strict_pairs={(min(a,b),max(a,b)) for a,b in strict_undirected.edges()}
    nearby_indices=np.flatnonzero(distance<=250)
    strict_near=sum((min(ids[first[i]],ids[second[i]]),max(ids[first[i]],ids[second[i]])) in strict_pairs for i in nearby_indices)
    metadata_sensitivity=pd.DataFrame([
        dict(policy='Llaves ID resueltas',nodes=len(graph),directed_edges=graph.number_of_edges(),undirected_edges=undirected.number_of_edges(),
             nearby250_connected=int(nearby.loc[nearby.threshold_km.eq(250),'connected_either_direction'].iloc[0]),nearby250_denominator=len(nearby_indices)),
        dict(policy='Además códigos coinciden',nodes=len(strict_graph),directed_edges=strict_graph.number_of_edges(),undirected_edges=strict_undirected.number_of_edges(),
             nearby250_connected=int(strict_near),nearby250_denominator=len(nearby_indices))])
    sample = np.flatnonzero((distance<=250)&~connected)[:20]
    counterexamples = pd.DataFrame([dict(source_id=ids[first[i]],destination_id=ids[second[i]],distance_km=float(distance[i])) for i in sample])
    resilience = country_resilience(graph,nodes)
    # A separate adversary removes the first 1/5/10 nodes in the original degree ranking, never refits the ranking retrospectively.
    removal = []
    original_top = nodes.sort_values('rank_unique_neighbors').airport_id.tolist()
    for count in [0,1,5,10]:
        residual = undirected.copy(); residual.remove_nodes_from(original_top[:count])
        largest = len(max(nx.connected_components(residual),key=len))
        removal.append(dict(removed_nodes=count,remaining_nodes=len(residual),largest_component=largest,
                            largest_component_fraction=largest/len(residual)))
    degree_leader = nodes.sort_values('rank_unique_neighbors').iloc[0].airport_id
    betweenness_leader = nodes.sort_values('rank_betweenness_128').iloc[0].airport_id
    betweenness_leader_k64 = nodes.sort_values('rank_betweenness_64').iloc[0].airport_id
    top = lambda field:set(nodes.nsmallest(10,field).airport_id)
    claims = {
        'D16-B':dict(countries_evaluated=len(resilience),minimum_airports_in_initial_giant=5,
                    method='Delete own highest-degree airport; count other country airports leaving global giant. Denominator excludes deleted node. Compare with up to 20 uniform random local deletions.',
                    largest_loss=resilience.sort_values(['loss_fraction','country'],ascending=[False,True]).head(10).to_dict('records'),
                    scope='Structural fragility in the historical graph, not demand, passengers or current resilience.'),
        'D16-C':dict(nodes=len(graph),directed_edges=graph.number_of_edges(),undirected_edges=undirected.number_of_edges(),
                    communities=len(groups),modularity=float(nx.community.modularity(undirected,groups)),
                    resolution_sensitivity=stability.to_dict('records'),null_partition_modularity=null_modularity,
                    scope='Louvain groups at fixed seed; compare fixed-size random memberships on the same graph. Modularity alone does not establish real communities.'),
        'D16-D1':dict(degree_leader=degree_leader,betweenness_leader=betweenness_leader,
                     betweenness_leader_k64=betweenness_leader_k64,first_place_stable_k64_k128=betweenness_leader==betweenness_leader_k64,
                     spearman_degree_betweenness=float(spearmanr(nodes.unique_neighbors,nodes.betweenness_128).statistic),
                     top10_jaccard=len(top('rank_unique_neighbors')&top('rank_betweenness_128'))/len(top('rank_unique_neighbors')|top('rank_betweenness_128')),
                     betweenness_k64_k128_spearman=float(spearmanr(nodes.betweenness_64,nodes.betweenness_128).statistic),
                     top10_k64_k128_jaccard=len(top('rank_betweenness_64')&top('rank_betweenness_128'))/len(top('rank_betweenness_64')|top('rank_betweenness_128')),
                     counterexamples='Different rankings or first places refute metric invariance; neither centrality is a universal definition of importance.'),
        'D16-D2':dict(thresholds=nearby.to_dict('records'),registered_primary_threshold_km=250,world_unordered_pairs=len(first),
                     world_connected_pairs=undirected.number_of_edges(),world_fraction=undirected.number_of_edges()/len(first),
                     metadata_policy_sensitivity=metadata_sensitivity.to_dict('records'),
                     scope='Active graph airports only. Short great-circle distance does not imply an observed direct route; nearby unconnected examples exported.'),
        'D16-E':dict(spearman_directed_undirected_betweenness=float(spearmanr(nodes.betweenness_128,nodes.betweenness_undirected).statistic),
                     metadata_policy_sensitivity=metadata_sensitivity.to_dict('records'),
                     degree_spearman_code_agreement_policy=float(spearmanr(nodes.unique_neighbors,[strict_undirected.degree(n) for n in nodes.airport_id]).statistic),
                     fixed_ranking_removals=removal,
                     scope='Unweighted topology; sampled betweenness, seed fixed. Refitting a network is not a prediction of airline response.')}
    return dict(nodes=nodes,edges=e,communities=community_summary,community_stability=stability,community_flows=flows,
                null_modularity=pd.DataFrame(null_modularity),
                metadata_sensitivity=metadata_sensitivity,
                nearby_pairs=nearby,nearby_counterexamples=counterexamples,country_resilience=resilience,hub_removal=pd.DataFrame(removal)),claims
