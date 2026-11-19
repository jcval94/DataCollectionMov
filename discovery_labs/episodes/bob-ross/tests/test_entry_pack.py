"""Phase-zero intake package contract. No network or third-party libraries required."""
import csv
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTAKE = ROOT / "entry_pack"


def read_json(name):
    return json.loads((INTAKE / name).read_text(encoding="utf-8"))


class EntryPackTests(unittest.TestCase):
    def test_original_snapshot_metadata(self):
        md = read_json("metadata.json")
        digest = hashlib.sha256((ROOT / "data/elements-by-episode.csv").read_bytes()).hexdigest()
        self.assertEqual(digest, md["sha256"])
        self.assertEqual(md["records"], 403)
        self.assertEqual(md["binary_columns"], 67)

    def test_sample_is_real_subset(self):
        with (ROOT / "data/elements-by-episode.csv").open(newline="", encoding="utf-8") as f:
            raw = list(csv.DictReader(f))
        with (INTAKE / "data_sample.csv").open(newline="", encoding="utf-8") as f:
            sample = list(csv.DictReader(f))
        ids = {r["EPISODE"] for r in raw}
        self.assertEqual(len(sample), read_json("metadata.json")["sample_rows"])
        self.assertTrue(all(r["episode"] in ids for r in sample))
        self.assertTrue(any(int(r["guest"]) == 1 for r in sample))
        self.assertTrue(any(int(r["guest"]) == 0 for r in sample))
        self.assertEqual(len({r["episode"] for r in sample}), len(sample))

    def test_question_trees_and_conditional_branches(self):
        graph = read_json("question_graph.json")
        self.assertGreaterEqual(len(graph["questions"]), 10)
        self.assertEqual(len({x["id"] for x in graph["questions"]}), len(graph["questions"]))
        for q in graph["questions"]:
            self.assertTrue(q["first_order"]["metric"])
            self.assertTrue(q["second_order"]["question"])
            self.assertGreaterEqual(len(q["second_order"]["branches"]), 2)
            self.assertNotEqual(q["second_order"]["branches"][0]["when"],
                                q["second_order"]["branches"][1]["when"])
            self.assertTrue(q["third_order"]["rival_explanation"])

    def test_prompts_and_skill_exist(self):
        self.assertIn("DR-1", (INTAKE / "DEEP_RESEARCH_PROMPTS.md").read_text(encoding="utf-8"))
        self.assertIn("DR-5", (INTAKE / "DEEP_RESEARCH_PROMPTS.md").read_text(encoding="utf-8"))
        self.assertTrue((INTAKE / "skills/research-question-architect/SKILL.md").exists())
        self.assertTrue((INTAKE / "VISUAL_EVIDENCE.md").exists())

    def test_video_stages_blocked(self):
        md = read_json("metadata.json")
        self.assertEqual(md["approval"]["phase2"], "BLOCKED")
        self.assertEqual(md["approval"]["phase3"], "BLOCKED")

    def test_image_rights_remain_unverified(self):
        sources = read_json("sources.json")["sources"]
        galleries = [s for s in sources if s["type"] == "gallery"]
        self.assertTrue(galleries)
        self.assertTrue(all("NOT_VERIFIED" in s["status"] for s in galleries))


if __name__ == "__main__":
    unittest.main()
