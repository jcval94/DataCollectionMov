"""Surveillance regressions: events != properties, treatment != negative, pairing != causality."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

import pandas as pd

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'scripts'))
from fieldlab import nyc
from run_fieldlab import run,verify
from agent_tools import dispatch


class SurveillanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.raw,cls.manifest=nyc.load()

    def fixture(self):
        cols=['job_id','inspection_date','inspection_type','borough','result','bbl']
        positive='Failed for Rat Activity'
        rows=[['a1','2024-01-05T08:00:00','Initial','Manhattan',positive,'1000000001'],
            ['a2','2024-07-05T08:00:00','Initial','Manhattan','Passed','1000000001'],
            ['a1','2024-01-05T08:00:00','Initial','Manhattan',positive,'1000000001'],
            ['b1','2024-01-01T08:00:00','Initial','Manhattan','Passed','1000000002'],
            ['b2','2024-07-01T08:00:00','Initial','Manhattan',positive,'1000000002'],
            ['missing','2024-07-01T08:00:00','Initial','Manhattan','Passed',''],
            ['mismatch','2024-07-01T08:00:00','Initial','Manhattan',positive,'3000000001'],
            ['treat','2024-07-01T08:00:00','Treatments','Manhattan','Bait applied','1000000003'],
            ['zero','2024-07-01T08:00:00','Initial','Manhattan','Passed','0000000000']]
        return pd.DataFrame(rows,columns=cols)

    def test_missing_keys_duplicates_and_treatments_do_not_change_meaning(self):
        raw=self.fixture();d,*_=nyc.prepare(raw,self.manifest)
        self.assertEqual(len(d),9);self.assertEqual(int(d.duplicate_exact.sum()),1)
        self.assertEqual(int(d.initial_eligible.sum()),7);self.assertEqual(int(d.property_eligible.sum()),4)
        self.assertTrue(pd.isna(d.loc[d.job_id.eq('treat'),'positive']).all())
        first=nyc.first_property_events(d[d.property_eligible])
        self.assertEqual(first.job_id.tolist(),['b1','a1']);self.assertEqual(int(first.positive.sum()),1)
        self.assertEqual(int(first.positive.size),2)

    def test_conflicting_administrative_event_and_future_window_rejected(self):
        raw=self.fixture();raw.loc[2,'result']='Passed'
        with self.assertRaises(ValueError):nyc.prepare(raw,self.manifest)
        raw=self.fixture();raw.loc[0,'inspection_date']='2025-01-01T00:00:00'
        with self.assertRaises(ValueError):nyc.prepare(raw,self.manifest)

    def test_pairing_uncertainty_and_calendar_order(self):
        equal=pd.DataFrame({'Winter':[0,1],'Summer':[1,0]})
        result=nyc.paired_statistics(equal)
        self.assertEqual(result['difference'],0);self.assertEqual(result['bootstrap_percentile95'],[-1,1])
        constant=pd.DataFrame({'Winter':[0,0],'Summer':[1,1]})
        result=nyc.paired_statistics(constant)
        self.assertEqual(result['difference'],1);self.assertEqual(result['bootstrap_percentile95'],[1,1])
        raw=self.fixture();raw.loc[0,'inspection_date']='2024-12-05T08:00:00';raw.loc[2,'inspection_date']='2024-12-05T08:00:00'
        d,*_=nyc.prepare(raw,self.manifest);selected=nyc.first_property_events(d[d.property_eligible],True)
        a=selected[selected.bbl.eq('1000000001')]
        self.assertEqual(set(a.season),{'Winter','Summer'})
        self.assertGreater(a[a.season.eq('Winter')].inspection_date.iloc[0],a[a.season.eq('Summer')].inspection_date.iloc[0])

    def test_closed_window_quality_and_reconciliation(self):
        d,p,_,_=nyc.prepare(self.raw,self.manifest);tables,claims=nyc.analyze(d)
        self.assertEqual(len(d),234596);self.assertEqual(p['coverage']['duplicate_exact'],10)
        self.assertEqual(p['coverage']['invalid_bbl'],5830);self.assertEqual(p['coverage']['bbl_borough_disagreement'],202)
        self.assertEqual(int(tables['monthly'].denominator.sum()),claims['D04-B']['initial_events'])
        self.assertEqual(int(tables['paired_cross'].properties.sum()),claims['D04-D1']['paired']['properties'])
        self.assertEqual(claims['D04-D1']['paired_bootstrap2000']['properties'],claims['D04-D1']['paired']['properties'])
        self.assertEqual(claims['D04-D1']['paired_bootstrap2000']['repetitions'],2000)
        self.assertLess(claims['D04-D1']['paired_winter_jan_feb_only']['properties'],claims['D04-D1']['paired']['properties'])
        self.assertTrue(tables['policy_rates'].fraction.between(0,1).all())
        for frame in tables.values():self.assertFalse(set(frame).intersection({'bbl','job_id','house_number','street_name'}))
        for q in ['D04-A','D04-D2','D05-C']:
            with self.assertRaises(ValueError):dispatch('run',nyc.CASE,q)
        catalog=dispatch('catalog');self.assertEqual(len(catalog['sources']),86);self.assertEqual(len(catalog['questions']),516)
        narrowed=next(q for q in catalog['questions'] if q['id']=='D04-B')
        self.assertIn('boroughs',narrowed['question'])

    def test_offline_package_independent_replay(self):
        with tempfile.TemporaryDirectory() as temp:
            out=run(nyc.CASE,Path(temp)/'run',True);verify(out)
            with zipfile.ZipFile(out/'student-offline.zip') as archive:
                self.assertFalse(any('teacher/' in n or 'REFERENCIAS' in n for n in archive.namelist()))
                m=json.loads(archive.read('package-manifest.json'))
                for path,digest in m['files'].items():self.assertEqual(hashlib.sha256(archive.read(path)).hexdigest(),digest)
                root=Path(temp)/'standalone';archive.extractall(root)
            env={**os.environ,'PYTHONHASHSEED':'967','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'}
            result=subprocess.run([sys.executable,'research_engine/discovery_labs/scripts/run_fieldlab.py','--case',nyc.CASE],cwd=root,env=env,capture_output=True,text=True,timeout=60)
            self.assertEqual(result.returncode,0,result.stderr)
            other=root/'research_engine/discovery_labs/output/v3'/nyc.CASE
            self.assertEqual(json.loads((out/'research/results.json').read_text()),json.loads((other/'research/results.json').read_text()))
            for p in (out/'gold').glob('*.csv'):self.assertEqual(p.read_bytes(),(other/'gold'/p.name).read_bytes())
            for p in (out/'visualization').glob('*.png'):self.assertEqual(p.read_bytes(),(other/'visualization'/p.name).read_bytes())
            # A packaged sibling is not used in the science, but must invalidate a stale distributable.
            sibling=root/'research_engine/discovery_labs/scripts/fieldlab/nasa.py'
            sibling.write_text(sibling.read_text()+'\n# Edited packaged sibling for cache regression.\n')
            repeated=subprocess.run([sys.executable,'research_engine/discovery_labs/scripts/run_fieldlab.py','--case',nyc.CASE],cwd=root,env=env,capture_output=True,text=True,timeout=60)
            self.assertEqual(repeated.returncode,0,repeated.stderr)
            self.assertIn('"status": "EXECUTED"',repeated.stdout)


if __name__=='__main__':unittest.main()
