"""Self-contained checks for the Bob Ross discovery episode.

Run: python -m unittest discover -s discovery_labs/episodes/bob-ross/tests -v
No network or third-party dependencies.
"""
import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import run
import clustering


class InputAndResearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows, cls.hash = run.load()
        cls.result, cls.host = run.study(cls.rows, cls.hash)

    def test_exact_frozen_source(self):
        self.assertEqual(self.hash, run.EXPECTED_SHA)
        self.assertEqual(hashlib.sha256(run.RAW.read_bytes()).hexdigest(), self.hash)

    def test_columns_and_units(self):
        self.assertEqual(len(self.rows), 403)
        self.assertEqual(self.result["metadata"]["columns"], 69)
        self.assertEqual(len(run.FEATURES), 12)
        self.assertEqual(self.result["metadata"]["binary_labels"], 67)

    def test_unique_episode_ids(self):
        ids = [r["id"] for r in self.rows]
        self.assertEqual(len(ids), len(set(ids)))

    def test_binary_features_are_not_object_counts(self):
        self.assertTrue(all(set(r["motifs"].values()) <= {0,1} for r in self.rows))
        self.assertEqual(self.rows[0]["id"], "S01E01")

    def test_guest_filter_explicit(self):
        self.assertEqual(len(self.host), 381)
        self.assertEqual(sum(r["guest"] for r in self.rows), 22)

    def test_trees_claim_has_counterexamples(self):
        self.assertEqual(self.result["host"]["with_trees"], 345)
        self.assertEqual(self.result["host"]["without_trees"], 36)
        self.assertTrue(self.result["counterexamples"]["host_without_trees"])

    def test_mountain_snow_claim_has_counterexamples(self):
        self.assertEqual(self.result["host"]["mountains"], 150)
        self.assertEqual(self.result["host"]["mountains_without_snow"], 48)

    def test_guest_denominator_is_visible(self):
        self.assertEqual(self.result["guest"]["n"], 22)
        self.assertEqual(self.result["guest"]["with_trees"], 16)

    def test_operational_scenario_not_money(self):
        self.assertEqual(sum(self.result["museum_scenario"]["room_sizes"].values()), 381)
        self.assertIn("sin costes ni ingresos", self.result["museum_scenario"]["status"])

    def test_visualizations_are_accessible_svg(self):
        for figure in (run.svg_bar(self.result),
                       run.svg_seasons(self.result),
                       run.svg_compare(self.result)):
            self.assertIn("<title", figure)
            self.assertIn("<desc", figure)
            self.assertIn("<svg", figure)
            self.assertIn("</svg>", figure)

    def test_both_ways_to_represent_metadata(self):
        self.assertEqual(self.result["host"]["unique_12_motif_profiles"] > 1, True)
        self.assertEqual(len(self.result["by_season_host"]), 31)

    def test_qa_guardrail(self):
        self.assertTrue(run.checks(self.result))

    def test_six_question_contracts(self):
        obj = json.loads((ROOT / "questions.json").read_text(encoding="utf-8"))
        qs = obj["questions"]
        self.assertEqual(len(qs), 6)
        self.assertEqual(len({q["id"] for q in qs}), 6)
        self.assertEqual(set(q["id"] for q in qs),
                         {"D85-A","D85-B","D85-C","D85-D1","D85-D2","D85-E"})
        self.assertTrue(all(q.get("adversary") and q.get("metric") for q in qs))

    def test_interactive_page_is_offline_and_scoped(self):
        page = (ROOT/"episode.html").read_text(encoding="utf-8")
        self.assertIn('id="rows"', page)
        self.assertIn('id="questions"', page)
        self.assertIn('id="prediction"', page)
        self.assertIn('id="conclusion"', page)
        self.assertNotIn('<script src="https:', page)
        self.assertNotIn('fetch(', page)


class ClusteringUnitTests(unittest.TestCase):
    def test_jaccard_zeros(self):
        self.assertEqual(clustering.distance((0,0,0), (0,0,0)), 0)
        self.assertEqual(clustering.distance((1,0,0), (0,1,0)), 1)

    def test_distance_symmetry(self):
        a,b=(0,1,0,1),(1,0,0,1)
        for metric in ("jaccard", "euclidean"):
            self.assertAlmostEqual(clustering.distance(a,b,metric),
                                   clustering.distance(b,a,metric))

    def test_perfect_partition_ari(self):
        self.assertAlmostEqual(clustering.ari([0,0,1,1],[7,7,8,8]),1.0)

    def test_medoids_small_fixture(self):
        pts=[(0,0),(0,1),(1,0),(1,1),(1,1)]
        mat=clustering.matrix(pts,"jaccard")
        lab, centers=clustering.medoids(mat,k=2)
        self.assertEqual(len(lab), 5)
        self.assertEqual(len(centers), 2)
        self.assertEqual(sum(lab.count(k) for k in (0,1)), 5)


if __name__ == "__main__":
    unittest.main()
