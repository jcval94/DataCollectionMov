"""Scientific regressions: flags, selection, fixed-population sensitivity and standalone replay."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

import numpy as np

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'scripts'))
from fieldlab import nasa
from run_fieldlab import run, verify
from agent_tools import dispatch


class NasaDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw,cls.manifest=nasa.load();cls.silver,*_=nasa.prepare(cls.raw,cls.manifest)

    def test_reference_rows_and_limits_are_not_measurements(self):
        self.assertEqual(len(self.raw),6090)
        self.assertEqual(self.raw.pl_name.nunique(),len(self.raw))
        changed=self.raw.copy();i=changed.index[changed.pl_radelim.eq('0')][0]
        changed.loc[i,'pl_radelim']='1'
        silver,*_=nasa.prepare(changed,self.manifest)
        self.assertFalse(silver.loc[i,'pl_rade_measured'])
        self.assertFalse(silver.loc[i,'cluster_eligible'])
        self.assertEqual(len(silver),len(self.raw))
        changed.loc[i,'default_flag']='0'
        with self.assertRaises(ValueError):nasa.prepare(changed,self.manifest)

    def test_no_imputation_and_signed_errors(self):
        changed=self.raw.copy();i=changed.index[changed.pl_radelim.eq('0')][0]
        changed.loc[i,['pl_radeerr1','pl_radeerr2']]=['0.2','0.1']
        silver,*_=nasa.prepare(changed,self.manifest)
        self.assertTrue(silver.loc[i,'pl_rade_measured']);self.assertFalse(silver.loc[i,'pl_rade_errors_usable'])
        self.assertEqual(int(silver.pl_eqt.isna().sum()),4430)
        changed.loc[i,'pl_rade']='-1'
        with self.assertRaises(ValueError):nasa.prepare(changed,self.manifest)

    def test_scientific_reconciliation_and_fixed_universe(self):
        tables,claims=nasa.analyze(self.silver)
        c=claims['D05-C'];r=claims['D05-D1']
        self.assertTrue(tables['cluster_sensitivity'].rows.eq(c['complete_cases']).all())
        self.assertEqual(sum(c['cluster_counts'].values()),c['complete_cases'])
        self.assertEqual(int(tables['method_mix'].planets.sum()),c['complete_cases'])
        selected=self.silver[self.silver.pl_rade_measured]
        manual=sum(.8<=x<=1.25 for x in selected.pl_rade)
        self.assertEqual(r['in_range'],manual);self.assertEqual(r['measured_denominator'],len(selected))
        self.assertAlmostEqual(r['missing_value_bounds_all_rows'][1],(manual+len(self.raw)-len(selected))/len(self.raw))
        self.assertEqual(claims['D05-E']['permutation_repetitions'],50)
        self.assertTrue(np.isfinite(tables['clustered'][c['feature_columns']]).all().all())

    def test_agent_rejects_unanswerable_and_foreign_route(self):
        for q in ['D05-A','D05-B','D05-D2','D16-C']:
            with self.assertRaises(ValueError):dispatch('run',nasa.CASE,q)
        result=dispatch('schema',nasa.CASE)
        self.assertEqual(result['columns'],list(self.raw))
        catalogue=dispatch('catalog');self.assertEqual(len(catalogue['sources']),86);self.assertEqual(len(catalogue['questions']),516)


class NasaReplayTests(unittest.TestCase):
    def test_replay_and_package_outside_repository(self):
        # Meaningful independent process and hash seed; never include teacher references.
        with tempfile.TemporaryDirectory() as temp:
            out=run(nasa.CASE,Path(temp)/'run',force=True);verify(out)
            wanted=json.loads((out/'research/results.json').read_text())
            with zipfile.ZipFile(out/'student-offline.zip') as archive:
                self.assertFalse(any('teacher/' in n or 'REFERENCIAS' in n for n in archive.namelist()))
                manifest=json.loads(archive.read('package-manifest.json'))
                for path,digest in manifest['files'].items():self.assertEqual(hashlib.sha256(archive.read(path)).hexdigest(),digest)
                root=Path(temp)/'standalone';archive.extractall(root)
            env={**os.environ,'PYTHONHASHSEED':'881','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'}
            child=subprocess.run([sys.executable,'research_engine/discovery_labs/scripts/run_fieldlab.py','--case',nasa.CASE],cwd=root,env=env,capture_output=True,text=True,timeout=60)
            self.assertEqual(child.returncode,0,child.stderr)
            other=root/'research_engine/discovery_labs/output/v3'/nasa.CASE
            self.assertEqual(wanted,json.loads((other/'research/results.json').read_text()))
            for p in (out/'gold').glob('*.csv'):self.assertEqual(p.read_bytes(),(other/'gold'/p.name).read_bytes())
            for p in (out/'visualization').glob('*.png'):self.assertEqual(p.read_bytes(),(other/'visualization'/p.name).read_bytes())


if __name__=='__main__':unittest.main()
