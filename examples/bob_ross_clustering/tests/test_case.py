import importlib.util
from pathlib import Path
import tempfile
import unittest
import subprocess
import sys
import zipfile

import numpy as np

BASE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('bob_case',BASE/'run.py')
case=importlib.util.module_from_spec(spec)
spec.loader.exec_module(case)


class DataContract(unittest.TestCase):
    def setUp(self):
        self.raw=case.load_data()

    def test_pinned_input_and_population_are_explicit(self):
        rows,X=case.prepare(self.raw)
        self.assertEqual((len(self.raw),len(rows),int(self.raw.GUEST.sum())),(403,381,22))
        self.assertEqual(X.shape,(381,12))
        self.assertTrue(X.isin([0,1]).all().all())

    def test_modified_bytes_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'changed.csv';p.write_bytes(case.RAW.read_bytes()+b'\n')
            with self.assertRaisesRegex(ValueError,'edición fijada'):case.load_data(p)

    def test_duplicate_episode_is_rejected(self):
        self.raw.loc[1,'EPISODE']=self.raw.loc[0,'EPISODE']
        with self.assertRaisesRegex(ValueError,'únicos'):case.prepare(self.raw)

    def test_unknown_and_nonbinary_labels_are_rejected(self):
        for bad in [2,np.nan]:
            with self.subTest(value=bad):
                frame=self.raw.copy();frame.loc[0,'TREE']=bad
                with self.assertRaisesRegex(ValueError,'binarias'):case.prepare(frame)

    def test_or_merging_is_presence_not_a_count(self):
        self.raw.loc[0,['TREE','TREES']]=1
        _,X=case.prepare(self.raw)
        self.assertEqual(X.loc[0,'arboles'],1)

    def test_title_cannot_steer_the_features(self):
        _,first=case.prepare(self.raw)
        self.raw['TITLE']='OCEAN MOUNTAIN TREE 9999'
        _,second=case.prepare(self.raw)
        self.assertTrue(first.equals(second))
        self.assertNotIn('TITLE',first)
        self.assertNotIn('EPISODE',first)
        self.assertNotIn('GUEST',first)

    def test_zero_profile_is_kept_and_is_not_missing(self):
        _,X=case.prepare(self.raw)
        self.assertEqual(int(X.sum(axis=1).eq(0).sum()),3)
        self.assertFalse(X.isna().any().any())

    def test_student_export_excludes_answers_and_preserves_existing_files(self):
        with tempfile.TemporaryDirectory() as folder:
            sentinel=Path(folder)/'alumno/DOCENTE.md';sentinel.parent.mkdir();sentinel.write_text('existing user file')
            subprocess.run([sys.executable,str(BASE/'build_student_kit.py'),'--output',folder],check=True,capture_output=True)
            with zipfile.ZipFile(Path(folder)/'bob-ross-alumnos.zip') as archive:
                self.assertEqual(set(archive.namelist()),{'bob-ross-alumnos/'+n for n in ['ALUMNO.md','ATRIBUCION.md','data/elements-by-episode.csv','data/manifest.json']})
            self.assertEqual(sentinel.read_text(),'existing user file')


if __name__=='__main__':unittest.main()
