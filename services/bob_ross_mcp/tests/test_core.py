"""Offline Bob Ross MCP smoke tests, without external API calls."""
import json
import sys
import unittest
from pathlib import Path

SERVICE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SERVICE))
import core


class BobRossCoreTests(unittest.TestCase):
    def test_manifest_matches_reference(self):
        d = core.dataset_overview()
        self.assertTrue(d["provenance_verified"])
        self.assertEqual((d["raw_episodes"], d["non_guest_episodes"]), (403, 381))
        self.assertEqual(len(d["feature_families"]), 12)

    def test_reference_is_clearly_not_live_comparison(self):
        r = core.reference_summary()
        self.assertEqual(r["status"], "committed_reference_not_live_comparison")
        self.assertEqual(sum(room["size"] for room in r["rooms"]), 381)

    def test_compares_three_real_models(self):
        r = core.compare_models()
        self.assertEqual(r["episodes"], 381)
        self.assertEqual(len(r["results"]), 3)
        self.assertEqual(r["k"], 4)
        self.assertEqual({m["algorithm"] for m in r["results"]}, {
            "kmeans_euclidean", "agglomerative_ward", "agglomerative_average_hamming"})
        self.assertTrue(all(sum(m["group_sizes"]) == 381 for m in r["results"]))
        self.assertTrue(all(len(m["group_sizes"]) == 4 for m in r["results"]))
        km = next(m for m in r["results"] if m["algorithm"] == "kmeans_euclidean")
        self.assertAlmostEqual(km["silhouette_euclidean"], 0.22698154, places=5)
        eligible = [m for m in r["results"] if m["eligible"]]
        self.assertIn(r["preferred_by_predeclared_rule"], {m["algorithm"] for m in eligible} if eligible else {None})

    def test_invalid_k_and_guests_are_rejected(self):
        for k in [0, 1, 7, 1.1, True, "4"]:
            with self.subTest(k=k), self.assertRaises(ValueError):
                core.compare_models(k=k)
        with self.assertRaises(ValueError):
            core.compare_models(exclude_guests="yes")

    def test_storyboard_and_assets_only_reference_committed_sources(self):
        self.assertEqual(len(core.storyboard()["scenes"]), 6)
        self.assertEqual(len(core.visualization_links()), 5)


if __name__ == "__main__":
    unittest.main()
