"""Portable smoke/contract tests of shared entry-pack validation.

Run from repo root:
  python -m unittest discover -s discovery_labs/shared/validators/tests -v
No external packages or network.
"""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

VALIDATOR = Path(__file__).resolve().parents[1] / "validate_entry_pack.py"
spec = importlib.util.spec_from_file_location("entry_validation", VALIDATOR)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class EntryPackContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.entry = self.root / "episode" / "entry_pack"
        self.entry.mkdir(parents=True)
        self.catalog = self.root / "MODEL_SET.md"
        self.catalog.write_text(
            "# Models\n| ID | Name |\n|---|---|\n| M01 | GLM |\n",
            encoding="utf-8",
        )
        self.guide = self.entry.parent / "research_guide.html"
        self.guide.write_text(
            '<section id="preguntas"><article id="ex-01"></article>'
            'PENDIENTE DE APROBACIÓN</section>',
            encoding="utf-8",
        )
        self.question = {
            "id": "EX-01", "root": "How could the effect change?",
            "o1": "Measure a distribution",
            "o2": "If an outlier exists, investigate its group",
            "o3": "If it persists, test explanations",
            "o2_trigger": "CONDITIONAL: after observed O1",
            "o3_trigger": "CONDITIONAL: after observed O2",
            "model": "M01", "model_why": "interpetable baseline",
            "model_where": "Gold to Research",
            "stat": "permutation test on group difference",
            "data": "genuine tabular source", "visual": "annotated rate chart",
        }
        for item in mod.REQUIRED:
            file = self.entry / item
            file.parent.mkdir(parents=True, exist_ok=True)
            if not file.exists():
                file.write_text("Template\n", encoding="utf-8")
        self.write_bank([self.question])
        (self.entry / "QUESTIONS_MASTER.md").write_text(
            "### EX-01\n", encoding="utf-8"
        )
        (self.entry / "metadata.json").write_text(
            json.dumps({"rows": 3, "columns": 2}), encoding="utf-8"
        )
        (self.entry / "sample_raw.csv").write_text(
            "episode,val\nA,1\nB,0\nC,1\n", encoding="utf-8"
        )

    def tearDown(self):
        self.tmp.cleanup()

    def write_bank(self, questions):
        (self.entry / "questions_master.json").write_text(
            json.dumps({"questions": questions}), encoding="utf-8"
        )

    def test_valid_minimal_entry_pack(self):
        report, issues = mod.validate(self.entry, self.catalog, self.guide)
        self.assertEqual([], issues)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["questions"], 1)

    def test_missing_statistical_exercise(self):
        question = dict(self.question, stat="")
        self.write_bank([question])
        _, issues = mod.validate(self.entry, self.catalog, self.guide)
        self.assertTrue(any("MISSING_STATISTICAL_EXERCISE" in item for item in issues))

    def test_nonexistent_model(self):
        question = dict(self.question, model="M99")
        self.write_bank([question])
        _, issues = mod.validate(self.entry, self.catalog, self.guide)
        self.assertTrue(any("MODEL_NOT_IN_CATALOG" in item for item in issues))

    def test_second_question_block_fails(self):
        self.guide.write_text(
            '<section id="preguntas"><article id="ex-01"></article></section>'
            '<section id="investigaciones">02B /</section>'
            'PENDIENTE DE APROBACIÓN', encoding="utf-8",
        )
        _, issues = mod.validate(self.entry, self.catalog, self.guide)
        self.assertTrue(any("GUIDE_LEGACY_SECOND" in item for item in issues))

    def test_mismatched_sample_schema(self):
        (self.entry / "sample_raw.csv").write_text(
            "episode,val,extra\nA,1,x\n", encoding="utf-8"
        )
        _, issues = mod.validate(self.entry, self.catalog)
        self.assertIn("SAMPLE_RAW_COLUMN_MISMATCH", issues)

    def test_duplicate_question_id(self):
        self.write_bank([self.question, dict(self.question)])
        _, issues = mod.validate(self.entry, self.catalog)
        self.assertIn("DUPLICATE_OR_MISSING_QUESTION_ID", issues)


if __name__ == "__main__":
    unittest.main()
