import copy,hashlib,importlib.util,json,socket,tempfile,unittest,urllib.request
from pathlib import Path
from unittest.mock import patch
import pandas as pd

BASE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('pilots',BASE/'scripts/run_pilots.py');runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
def read(p):return json.loads(Path(p).read_text())
class CatalogTests(unittest.TestCase):
    def test_exact_reconciliation_and_routes(self):
        r=read(BASE/'catalog/reconciliation.json');s=read(BASE/'catalog/sources.json');q=read(BASE/'catalog/questions.json')
        self.assertEqual([len(r[k]) for k in ['original_ids','initially_selected_ids','initially_omitted_ids','later_proposed_ids']],[78,37,41,8])
        self.assertEqual(set(r['initially_selected_ids'])|set(r['initially_omitted_ids']),set(r['original_ids']))
        self.assertFalse(set(r['initially_selected_ids'])&set(r['initially_omitted_ids']))
        ids={z['id'] for z in s};self.assertEqual(len(ids),86);self.assertEqual(len(q),516);self.assertEqual(len({z['canonical_id'] for z in q}),516)
        self.assertEqual(len({z['macrocategory'] for z in s}),13)
        for sid in ids:
            routes=[z for z in q if z['source_id']==sid];self.assertEqual({z['route'] for z in routes},{'A','B','C','D1','D2','E'})
            self.assertEqual(len({z['question'] for z in routes}),6)
        self.assertEqual(sum(z['original_question'] is not None for z in q),270)
        for z in q:
            self.assertIn(z['source_id'],ids)
            for k in ['hypothesis','objective','metric','denominator','period','required_fields','route_simple','route_advanced','refutation_criterion','limitations']:self.assertTrue(z[k],(z['id'],k))
    def test_no_unearned_readiness_and_bts(self):
        s={z['id']:z for z in read(BASE/'catalog/sources.json')};self.assertFalse(any(z['ready_for_class'] for z in s.values()))
        self.assertIn('MBID',s['bts-kpop-musica']['entity_disambiguation']);self.assertIn('U.S. DOT',s['bts-puntualidad-vuelos']['entity_disambiguation'])
        for z in s.values():self.assertEqual(z['human_45min_rehearsal']['status'],'PENDIENTE')

class PilotTests(unittest.TestCase):
    def test_offline_and_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(socket,'create_connection',side_effect=AssertionError('Red prohibida')),patch.object(urllib.request,'urlopen',side_effect=AssertionError('HTTP prohibido')):
            for case in runner.CASES:
                a=runner.run(case,Path(tmp)/'a');b=runner.run(case,Path(tmp)/'b');self.assertEqual(a,b)
                self.assertEqual(a,read(BASE/'evidence/pilot_runs'/f'{case}.json'))
                pa=Path(tmp)/'a'/case/'comparison.png';pb=Path(tmp)/'b'/case/'comparison.png'
                self.assertEqual(runner.sha(pa),runner.sha(pb))
                self.assertGreaterEqual(len(a['routes']),2)
                self.assertEqual(a['classroom_status'],'PENDIENTE_ENSAYO_HUMANO_45_MIN')
    def test_tampered_snapshot_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            t=Path(tmp);f=t/'pilots/uci-retail/data';f.mkdir(parents=True)
            m=read(BASE/'pilots/uci-retail/data/manifest.json');(f/'manifest.json').write_text(json.dumps(m));(f/'snapshot.csv').write_text('tampered')
            with patch.object(runner,'BASE',t),self.assertRaisesRegex(ValueError,'hash'):runner.load('uci-retail')
    def test_domain_corruption_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            d,_=runner.load('bob-ross-elementos');d.loc[0,'TREE']='2'
            with self.assertRaisesRegex(ValueError,'binarias'):runner.bob(d,Path(tmp))
            d,_=runner.load('nba-elo');d=d.iloc[1:]
            with self.assertRaises(AssertionError):runner.nba(d,Path(tmp))
    def test_retaining_credits_and_no_customer_identifiers(self):
        d,_=runner.load('uci-retail');self.assertNotIn('CustomerID',d)
        with tempfile.TemporaryDirectory() as tmp:
            out=runner.retail(d,Path(tmp));self.assertGreater(float(out['totals']['credits']),0)
            from decimal import Decimal
            self.assertEqual(Decimal(out['totals']['gross'])-Decimal(out['totals']['credits']),Decimal(out['totals']['net']))

if __name__=='__main__':unittest.main()
