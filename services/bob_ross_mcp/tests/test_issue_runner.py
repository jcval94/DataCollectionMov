import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from issue_runner import parse, report


class IssueBridgeTests(unittest.TestCase):
    def test_defaults_and_bounded_values(self):
        self.assertEqual(parse(""), (4, False))
        self.assertEqual(parse("k: 5\ninclude_guests: true"), (5, True))

    def test_does_not_accept_arbitrary_commands(self):
        for body in ["k: 99", "script: rm -rf /", "include_guests: yes", "k: 3\nURL: http://evil"]:
            with self.subTest(body=body), self.assertRaises(ValueError):
                parse(body)

    def test_report_labels_metric_and_reference(self):
        example = {
            "episodes": 381, "k": 4, "exclude_guests": True,
            "source_sha256": "abcdef",
            "results": [{"algorithm": "kmeans_euclidean", "silhouette_euclidean": .22,
                         "within_cluster_ss": 430, "smallest_group": 39, "eligible": True}],
            "preferred_by_predeclared_rule": "kmeans_euclidean",
            "decision_rule": "Highest silhouette",
            "interpretation": "Non-causal exploratory result",
            "assets": {"room_profiles": "https://example.org/profiles.svg",
                       "interactive_classroom_demo": "https://example.org/demo.html"},
        }
        result = report(example)
        self.assertIn("kmeans_euclidean", result)
        self.assertIn("referencia previa", result)


if __name__ == "__main__":
    unittest.main()
