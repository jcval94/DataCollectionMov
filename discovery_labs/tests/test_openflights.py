"""Graph-domain and packaging failures with material consequences, not style snapshots."""
import copy
import contextlib
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import networkx as nx
import pandas as pd

BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE/'scripts'))
from batch1.openflights import load,prepare,haversine_pairs,country_resilience,CASE
from run_batch1 import run,verify
from v3.data import sha
from agent_tools import dispatch


class GraphDataTests(unittest.TestCase):
    def test_legacy_catalog_does_not_adopt_a_new_manifest(self):
        import build_catalog
        with tempfile.TemporaryDirectory() as tmp:
            sandbox=Path(tmp)
            for name in ['imports','evidence','pilots']:(sandbox/name).symlink_to(BASE/name,target_is_directory=True)
            (sandbox/'catalog').mkdir()
            (sandbox/'catalog/reconciliation.json').write_bytes((BASE/'catalog/reconciliation.json').read_bytes())
            with patch.object(build_catalog,'BASE',sandbox),contextlib.redirect_stdout(io.StringIO()):build_catalog.main()
            sources={s['id']:s for s in json.loads((sandbox/'catalog/sources.json').read_text())}
            self.assertEqual(len(sources),86)
            self.assertEqual(sources[CASE]['snapshot']['status'],'PENDIENTE')
            self.assertNotEqual(sources[CASE]['license'].get('evidence'),'evidence/538-LICENSE.txt')
            for legacy in ['uci-retail','nba-elo','bob-ross-elementos']:
                self.assertEqual(sources[legacy]['snapshot']['status'],'SNAPSHOT_HASHED')
            self.assertEqual(len(json.loads((sandbox/'catalog/questions.json').read_text())),516)

    def test_lossless_raw_hash_and_composite_rejected(self):
        _,manifest=load()
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)
            for source in (BASE/'pilots'/CASE/'data').iterdir():
                if source.is_file():(folder/source.name).write_bytes(source.read_bytes())
            bad=copy.deepcopy(manifest);bad['snapshot_sha256']='0'*64
            (folder/'manifest.json').write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError,'Composite'):load(folder)
            (folder/'manifest.json').write_text(json.dumps(manifest));(folder/'routes.dat.gz').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError,'Stored hash'):load(folder)

    def test_joins_dedup_and_no_iata_guessing(self):
        original,_=load();airports=original['airports'].head(3).copy();a,b,c=airports.airport_id.tolist()
        model=original['routes'].iloc[0].to_dict()
        records=[]
        for source,destination,stops,codeshare in [(a,b,'0',''),(a,b,'0','Y'),(b,a,'0',''),(c,a,'1',''),('999999999',b,'0',''),(a,a,'0','')]:
            row=dict(model,source_id=source,destination_id=destination,stops=stops,codeshare=codeshare)
            records.append(row)
        raw=dict(airports=airports,routes=pd.DataFrame(records))
        silver,edges,profile,_,_=prepare(raw)
        self.assertEqual(len(silver['routes']),6)
        self.assertEqual(len(edges),2);self.assertEqual(int(edges.route_records.sum()),3)
        self.assertTrue(silver['routes'].source_iata_disagrees.any())
        self.assertEqual(profile['routes']['fields']['codeshare']['missing_count'],0)
        self.assertEqual(profile['routes']['fields']['codeshare']['blank_count'],5)
        self.assertIn('source_id_unresolved',silver['routes'].iloc[4].exclusion_reason)
        self.assertNotIn('999999999',set(edges.source_id))
        for column,value in [('latitude','91'),('longitude','181')]:
            bad={key:frame.copy() for key,frame in raw.items()};bad['airports'].loc[bad['airports'].index[0],column]=value
            with self.assertRaises(ValueError):prepare(bad)
        for column,value in [('stops','-1'),('codeshare','X')]:
            bad={key:frame.copy() for key,frame in raw.items()};bad['routes'].loc[0,column]=value
            with self.assertRaises(ValueError):prepare(bad)

    def test_geodesic_antimeridian_and_removed_node_denominator(self):
        airports=pd.DataFrame(dict(latitude=[0,0],longitude=[179,-179]))
        first,second,distance=haversine_pairs(airports)
        self.assertAlmostEqual(float(distance[0]),222.390160467,places=5)
        # Five nodes in A depend on a gateway to a larger region B. Removing A0 detaches four OTHER A nodes.
        g=nx.DiGraph();g.add_edges_from([(f'A{i}','A0') for i in range(1,5)]+[('A0','B0')])
        g.add_edges_from((f'B{i}',f'B{j}') for i in range(7) for j in range(i+1,7))
        nodes=pd.DataFrame(dict(airport_id=sorted(g),country=['A' if n.startswith('A') else 'B' for n in sorted(g)]))
        result=country_resilience(g,nodes).set_index('country').loc['A']
        self.assertEqual(result.remaining_denominator,4)
        self.assertEqual(result.other_airports_disconnected,4)
        self.assertEqual(result.loss_fraction,1)

    def test_catalog_overlay_preserves_inventory_and_blocks_economics(self):
        data=dispatch('catalog')
        self.assertEqual(len(data['sources']),86);self.assertEqual(len(data['questions']),516)
        subset=[q for q in data['questions'] if q['source']==CASE]
        self.assertEqual(sum(q['status']=='EXECUTABLE' for q in subset),5)
        with self.assertRaises(ValueError):dispatch('run',CASE,'D16-A')
        with self.assertRaises(ValueError):dispatch('run',CASE,'D85-C')


class GraphReplayTests(unittest.TestCase):
    def test_replay_and_standalone_distribution(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(socket,'create_connection',side_effect=AssertionError('Network forbidden')):
            a=run(CASE,Path(tmp)/'a',True);b=run(CASE,Path(tmp)/'b',True)
            self.assertEqual(verify(a),verify(b))
            results=json.loads((a/'research/results.json').read_text())
            self.assertEqual(set(results),{'D16-B','D16-C','D16-D1','D16-D2','D16-E'})
            figures=json.loads((a/'visualization/figures.json').read_text())
            for figure in figures:
                self.assertEqual(figure['table_sha256'],sha(a/figure['table']))
                self.assertTrue(figure['alt'])
            self.assertEqual(len(figures),10)
            with zipfile.ZipFile(a/'student-offline.zip') as archive:
                names=archive.namelist()
                self.assertFalse(any('teacher/' in n or 'REFERENCIAS' in n or 'FACILITACION' in n or 'DOCENTE.md' in n for n in names))
                self.assertTrue(any(n.endswith('/data/LICENSE') for n in names))
                standalone=Path(tmp)/'standalone';archive.extractall(standalone)
            # A different string hash seed must not create different communities or figures.
            env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONHASHSEED='314159')
            entry=standalone/'research_engine/discovery_labs/scripts/run_batch1.py'
            subprocess.run([sys.executable,str(entry),'--case',CASE],env=env,check=True,capture_output=True,timeout=60)
            replay=entry.parents[1]/'output/v3'/CASE
            for artifact in ['research/results.json','gold/nodes.csv','visualization/figures.json']:
                self.assertEqual((a/artifact).read_bytes(),(replay/artifact).read_bytes(),artifact)
            g=json.loads((a/'gates.json').read_text())
            self.assertTrue(g['DATA_READY'])
            self.assertFalse(any(q['CLASS_READY'] or q['PUBLISHED'] for q in g['questions'].values()))
            self.assertFalse(g['questions']['D16-A']['RESEARCH_READY'])
            (a/'gold/edges.csv').write_text('changed')
            with self.assertRaises(ValueError):verify(a)


if __name__=='__main__':unittest.main()
