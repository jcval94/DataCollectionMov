"""Bob Ross entry-pack contract tests (static, offline, no model execution).

The 14-question Question Forge V2 bank supersedes the historical 12-arc
QUESTION_BANK/question_graph. Historical intake artifacts remain readable;
this suite deliberately tests only the canonical entry-pack contract.
"""
import csv
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "entry_pack"
DATA = ROOT / "data" / "elements-by-episode.csv"
SHA256 = "42045c8b8aaa8296095d6b294927fb9d0f73a57259f59b560c375844c0fe01cf"


def read_json(name):
    return json.loads((PACK / name).read_text(encoding="utf-8"))


class EntryPackTests(unittest.TestCase):
    def test_original_snapshot_metadata(self):
        md = read_json("metadata.json")
        self.assertEqual(hashlib.sha256(DATA.read_bytes()).hexdigest(), SHA256)
        self.assertEqual(md["sha256"], SHA256)
        self.assertEqual(md["rows"], 403)
        self.assertEqual(md["columns"], 69)
        self.assertEqual(md["binary_columns"], 67)
        self.assertEqual(md["host_rows"] + md["guest_rows"], 403)
        self.assertEqual(md["research_approval"], "PENDING")
        self.assertEqual(md["storytelling_approval"], "BLOCKED")
        self.assertEqual(md["video_approval"], "BLOCKED")

    def test_samples_are_real_subsets_with_matching_ids(self):
        with DATA.open(newline="", encoding="utf-8") as f:
            original = list(csv.DictReader(f))
        with (PACK / "sample_raw.csv").open(newline="", encoding="utf-8") as f:
            sample = list(csv.DictReader(f))
        with (PACK / "sample_features.csv").open(newline="", encoding="utf-8") as f:
            features = list(csv.DictReader(f))
        self.assertEqual(len(original), 403)
        self.assertEqual(len(sample), len(features))
        self.assertEqual(len(sample), read_json("metadata.json")["sample_rows"])
        self.assertEqual(len(sample[0]), 69)
        self.assertEqual(len(features[0]), 16)
        lookup = {row["EPISODE"]: row for row in original}
        self.assertEqual(len(lookup), 403)
        self.assertEqual(len({row["EPISODE"] for row in sample}), len(sample))
        for row in sample:
            self.assertIn(row["EPISODE"], lookup)
            self.assertEqual(row, lookup[row["EPISODE"]])
        self.assertEqual(
            {row["EPISODE"] for row in sample},
            {row["EPISODE"] for row in features},
        )
        self.assertTrue(any(int(row["GUEST"]) for row in sample))
        self.assertTrue(any(not int(row["GUEST"]) for row in sample))

    def test_canonical_bank_has_14_complete_conditional_arcs(self):
        bank = read_json("questions_master.json")
        questions = bank["questions"]
        self.assertEqual(len(questions), 14)
        self.assertEqual(
            [q["id"] for q in questions],
            [f"BR-{i:02d}" for i in range(1, 15)],
        )
        models = set(re.findall(
            r"^\\|\\s*(M\\d{2})\\s*\\|",
            (PACK / "MODEL_SET.md").read_text(encoding="utf-8"),
            re.M,
        ))
        self.assertEqual(len(models), 24)
        master = (PACK / "QUESTIONS_MASTER.md").read_text(encoding="utf-8")
        self.assertEqual(master.count("### BR-"), len(questions))
        for q in questions:
            for key in (
                "title", "root", "o1", "o2", "o3", "o2_trigger",
                "o3_trigger", "rival_hypothesis", "model_name", "model_why",
                "model_where", "model_baseline", "model_validation",
                "stat", "stat_why", "stat_where", "data", "visual",
            ):
                self.assertTrue(q.get(key), f"{q['id']} missing {key}")
            self.assertTrue(q["o2_trigger"].startswith("CONDICIONAL:"))
            self.assertTrue(q["o3_trigger"].startswith("CONDICIONAL:"))
            self.assertEqual(q["design_status"], "PLAN_ONLY")
            self.assertIn(q["model"], models)
            for key in ("grain", "population", "measure", "denominator", "time_basis"):
                self.assertTrue(q["estimand"].get(key), f"{q['id']} {key}")
            self.assertIn(f"### {q['id']} ·", master)

    def test_single_question_section_and_no_audiovisual(self):
        html = (ROOT / "research_guide.html").read_text(encoding="utf-8")
        self.assertEqual(html.count('id="preguntas"'), 1)
        self.assertNotIn('id="investigaciones"', html)
        self.assertNotIn('02B /', html)
        self.assertEqual(html.count('class="story-arc"'), 14)
        for number in range(1, 15):
            self.assertIn(f'id="br-{number:02d}"', html)
        self.assertIn("PENDIENTE DE APROBACIÓN", html)
        self.assertIn("linfoma", html.lower())

    def test_legacy_intake_retained_without_becoming_canonical(self):
        self.assertTrue((PACK / "QUESTION_BANK.md").exists())
        self.assertTrue((ROOT / "intake" / "qa_intake.cjs").exists())
        self.assertTrue((PACK / "skills" / "research-question-architect" / "SKILL.md").exists())
        self.assertTrue((PACK / "skills" / "question-forge" / "SKILL.md").exists())


if __name__ == "__main__":
    unittest.main()
