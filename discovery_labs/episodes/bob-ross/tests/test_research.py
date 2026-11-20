"""Scientific invariants and counterexamples, offline stdlib tests."""
import importlib.util
import itertools
import json
import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'research'))
import audit
import experiments as ex
from reconcile import MAPPING


class ExactTests(unittest.TestCase):
    def test_fisher_reference_table(self):
        # Published standard 2x2 example, independently checked against scipy.
        self.assertAlmostEqual(ex.fisher(1,9,11,3),0.0027594561852200836,places=12)
        self.assertAlmostEqual(ex.fisher(1,9,11,3),ex.fisher(3,11,9,1),places=12)
        self.assertEqual(ex.fisher(0,0,0,10),1.)

    def test_adjustments_known_values(self):
        self.assertEqual(ex.adjust([.01,.04,.03]),[.03,.06,.06])
        got=ex.adjust([.01,.04,.03],'bh')
        for a,b in zip(got,[.03,.04,.04]): self.assertAlmostEqual(a,b)

    def test_exact_adjacency_expectation_by_enumeration(self):
        states=set(itertools.permutations([1,1,0,0]))
        observed=[sum(a*b for a,b in zip(x,x[1:])) for x in states]
        self.assertAlmostEqual(sum(observed)/len(states),2*(2-1)/4)

    def test_filter_never_creates_adjacency(self):
        def row(e,guest=0):return {'id':f'S01E{e:02d}','season':1,'guest':guest}
        rr=[row(1),row(2,1),row(3),row(4)]
        selected,edges=ex.sequence_blocks(rr,'host')[0]
        self.assertEqual([r['id'] for r in selected],['S01E01','S01E03','S01E04'])
        self.assertEqual(edges,[(1,2)])

    def test_constant_sequence_has_no_inhibition(self):
        rr=[{'id':f'S01E{e:02d}','season':1,'guest':0,'flags':dict.fromkeys(ex.MOTIFS,1)} for e in range(1,14)]
        stats,_=ex.sequence(rr,'all',20)
        self.assertTrue(all(r['expected_11_exact']==12 and r['p_inhibition']==1. for r in stats))
        self.assertTrue(all(not r['supports_H8_inhibition'] for r in stats))


class AuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report,cls.rows=audit.audit()

    def test_actual_schema_overrules_received_prose(self):
        self.assertEqual(self.report['positive_marks_all_67_columns'],3221)
        self.assertEqual(self.report['person'],['S03E10'])
        self.assertFalse(self.report['chimney_column_exists'])
        self.assertEqual(len(self.report['duplicate_title_groups']),2)

    def test_source_archive_stays_intact(self):
        self.assertTrue(all(self.report['received_archive_blob_checks'].values()))

    def test_no_silent_incomplete_exclusion(self):
        self.assertEqual(set(self.report['zero_positive_rows']),set(audit.INCOMPLETE))
        self.assertEqual(self.report['host_excluding_vignette_incomplete'],378)
        self.assertEqual(len(self.rows),403)

    def test_every_H_has_exactly_one_primary_canonical_parent(self):
        bank=json.loads((ROOT/'entry_pack/questions_master.json').read_text())['questions']
        self.assertEqual(set(MAPPING),{f'H{i}' for i in range(1,11)})
        self.assertTrue(all(v[0] in {q['id'] for q in bank} for v in MAPPING.values()))

    def test_sequence_denominators_do_not_bridge_gaps(self):
        counts={p:sum(len(e) for _,e in ex.sequence_blocks(self.rows,p)) for p in ('all','host','host_complete')}
        self.assertEqual(counts['all'],372)
        self.assertLess(counts['host'],381-31)
        self.assertLess(counts['host_complete'],counts['host'])


if __name__=='__main__':unittest.main()
