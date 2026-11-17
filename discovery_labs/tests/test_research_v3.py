"""Material invariants: domain corruption, evidence lineage, output isolation and offline replay."""
import importlib.util
import json
from pathlib import Path
import socket
import os
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE/'scripts'))
from v3.data import CASES, load, prepare
from v3.research import ANALYSES
from run_research import run, verify, sha
from agent_tools import dispatch


class ResearchTests(unittest.TestCase):
    def test_mirror_score_and_future_domains_rejected(self):
        raw, m = load('nba-elo')
        opposite = '1' if raw.loc[0, '_iscopy']=='0' else '0'
        for col, value in [('pts', '999'), ('opp_id', 'INVALID'), ('_iscopy', opposite), ('game_location', 'X'), ('forecast', '2')]:
            bad = raw.copy(); bad.loc[0, col] = value
            with self.subTest(col=col), self.assertRaises(ValueError): prepare('nba-elo', bad, m)

    def test_privacy_invoice_consistency_and_binary_integrity(self):
        raw, m = load('uci-retail'); bad = raw.copy(); bad['CustomerID'] = 'never publish'
        with self.assertRaises(ValueError): prepare('uci-retail', bad, m)
        bad = raw.copy(); bad.loc[0, 'customer_id_missing'] = '3'
        with self.assertRaises(ValueError): prepare('uci-retail', bad, m)
        raw, m = load('bob-ross-elementos'); bad = raw.copy(); bad.loc[0, 'TREE'] = ''
        with self.assertRaises(ValueError): prepare('bob-ross-elementos', bad, m)

    def test_replay_lineage_and_student_isolation(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(socket, 'create_connection', side_effect=AssertionError('No network')):
            for case in CASES:
                with self.subTest(case=case):
                    a = run(case, Path(tmp)/'a', True); b = run(case, Path(tmp)/'b', True)
                    ra, rb = verify(a), verify(b)
                    self.assertEqual(ra, rb)
                    silver = (a/'silver/records.csv').read_text().splitlines()
                    raw, m = load(case); self.assertEqual(len(silver)-1, len(raw))
                    figures = json.loads((a/'visualization/figures.json').read_text())
                    for figure in figures:
                        self.assertEqual(figure['table_sha256'], sha(a/figure['table']))
                        self.assertEqual(figure['source_sha256'], m['snapshot_sha256'])
                        for variant in figure['variants']:
                            self.assertEqual(variant['png_sha256'], sha(a/'visualization'/variant['png']))
                            self.assertTrue(variant['text_bounds_pass'])
                    with zipfile.ZipFile(a/'student-offline.zip') as z:
                        names = z.namelist()
                        self.assertTrue('EJECUTAR.md' in names)
                        self.assertFalse(any('teacher/' in n or 'REFERENCIAS' in n or 'FACILITACION' in n or 'DOCENTE.md' in n for n in names))
                        self.assertFalse(any('/output/' in n for n in names))
                        if case == 'uci-retail':
                            standalone = Path(tmp)/'standalone'; z.extractall(standalone)
                            entry = standalone/'research_engine/discovery_labs/scripts/run_research.py'
                            env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
                            subprocess.run([sys.executable, str(entry), '--case', case], check=True, env=env, capture_output=True, timeout=60)
                            replay = standalone/'research_engine/discovery_labs/output/v3'/case/'research/results.json'
                            self.assertEqual(json.loads(replay.read_text()), json.loads((a/'research/results.json').read_text()))
                    gates = json.loads((a/'gates.json').read_text())
                    self.assertTrue(gates['DATA_READY'])
                    self.assertFalse(any(g['CLASS_READY'] or g['PUBLISHED'] for g in gates['questions'].values()))
                    # Bronze receipts are also part of integrity, not accidentally excluded by basename.
                    (a/'bronze/receipt.json').write_text('{}')
                    with self.assertRaises(ValueError): verify(a)

    def test_blocked_routes_never_execute(self):
        contracts = json.loads((BASE/'contracts/batch0.json').read_text())
        self.assertEqual(len(contracts), 18)
        self.assertEqual(sum(c['execution_status']=='EXECUTABLE' for c in contracts), 12)
        for c in contracts:
            self.assertFalse(c['feasibility_45_min']['human_rehearsal_approved'])
            if c['execution_status']=='BLOCKED':
                with self.assertRaises(ValueError): dispatch('run', c['source_id'], c['id'])
                self.assertTrue(c['how_to_unblock'])
        with self.assertRaises(ValueError): dispatch('run', 'nba-elo', 'D85-C')

    def test_series_temporal_selection_and_clustering_control(self):
        raw, m = load('nba-elo'); d, *_ = prepare('nba-elo', raw, m)
        previous = json.loads((BASE/'evidence/pilot_runs/nba-elo.json').read_text())
        tables, claims = ANALYSES['nba-elo'](d, raw, previous)
        self.assertEqual(len(tables['series']), 15)
        self.assertTrue(tables['series'].winner_wins.eq(4).all())
        for row in tables['series'].itertuples():
            first = d[d.game_id.eq(row.first_game)].iloc[0]
            self.assertEqual(row.favorite, first.team_id if first.elo_i > first.opp_elo_i else first.opp_id)
        raw, m = load('bob-ross-elementos'); d, *_ = prepare('bob-ross-elementos', raw, m)
        previous = json.loads((BASE/'evidence/pilot_runs/bob-ross-elementos.json').read_text())
        tables, claims = ANALYSES['bob-ross-elementos'](d, raw, previous)
        self.assertEqual(claims['D85-E']['sensitivity'][0]['ARI_vs_clean_euclidean'], 1)
        self.assertEqual(len(claims['D85-C']['permuted_marginals_silhouettes']), 30)
        self.assertEqual(len(tables['selection']), 12)
        self.assertTrue(tables['selection'].EPISODE.is_unique)


if __name__=='__main__': unittest.main()
