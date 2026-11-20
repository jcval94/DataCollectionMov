"""Offline tests for actual Human Feedback checkpoint publication gates.

Tests use *synthetic* report metadata and an SVG fixture; they are not
scientific Bob Ross results and must never be published as findings.
Run from repo root:
  python -m unittest discover -s discovery_labs/shared/validators/tests -v
"""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

VALIDATOR = Path(__file__).resolve().parents[1] / "validate_human_feedback.py"
spec = importlib.util.spec_from_file_location("human_feedback_validation", VALIDATOR)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

HTML = """<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
</head><body><main><h1>Checkpoint de prueba sintética</h1>
<section><h2 id="summary-title">Resumen ejecutivo</h2>
<p>Solo datos sintéticos para comprobar la estructura.</p></section>
<section><h2>Gráficas</h2><figure>
<img src="charts/coverage.svg" alt="Cobertura de prueba sintética">
<figcaption>n = 2; referencia sintética.</figcaption></figure></section>
</main></body></html>
"""


class HumanFeedbackValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.checkpoint = Path(self.temp.name) / "HF-00" / "v01"
        self.checkpoint.mkdir(parents=True)
        (self.checkpoint / "charts").mkdir()
        (self.checkpoint / "charts" / "coverage.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" role="img">'
            '<title>Datos sintéticos de prueba</title><rect width="2" height="2"/></svg>',
            encoding="utf-8",
        )
        (self.checkpoint / "report.html").write_text(HTML, encoding="utf-8")
        (self.checkpoint / "feedback.md").write_text(
            "# Feedback de prueba\n\nPENDING: sin aprobación humana.\n", encoding="utf-8"
        )
        self.meta = {
            "schema_version": "human-feedback-checkpoint-1.0",
            "checkpoint_id": "HF-00",
            "dataset_id": "synthetic-contract-test",
            "version": 1,
            "created_at": "2026-11-19",
            "phase": "data-audit",
            "status": "READY_FOR_FEEDBACK",
            "source_commit": "a" * 40,
            "previous_checkpoint": None,
            "report_path": "report.html",
            "report_starts_with_summary": True,
            "executive_summary": {
                "summary": "Cobertura ficticia de prueba, no hallazgo real",
                "delta": "Primer paquete, sin comparación",
                "surprise": "Aún no hay un insight sorprendente confirmado",
                "recommendation": "Validar datos reales antes de presentar hallazgos",
                "limitation": "Solo artefactos sintéticos",
            },
            "changes_since_prior": [],
            "insights": [],
            "charts": [
                {
                    "chart_id": "coverage-synthetic",
                    "title": "Gráfico de cobertura sintética",
                    "question_id": "QA-00",
                    "type": "svg",
                    "chart_path": "charts/coverage.svg",
                    "data_source": "sintético para tests",
                    "evidence_ref": "test fixture",
                    "code_ref": "shared/validators/tests/test_validate_human_feedback.py",
                    "population": "dos unidades artificiales",
                    "n": 2,
                    "denominator": "2 unidades de prueba",
                    "unit": "cuenta",
                    "baseline": "sin baseline empírico",
                    "uncertainty": "no aplica, test estático",
                    "alt_text": "cuadrado representando cobertura sintética",
                    "rights_status": "DATA_ONLY",
                    "mobile_checked": True,
                    "desktop_checked": True,
                },
            ],
            "user_questions": [
                {
                    "id": "q1",
                    "question": "¿Validar el archivo antes de analizar?",
                    "options": ["Sí", "No"],
                    "recommended_option": "Sí",
                    "reason": "Evita inferencias espurias",
                    "impact_if_postponed": "Bloquea investigación",
                }
            ],
            "recommendation": {
                "proposed_action": "Auditar los datos originales",
                "default_action": "Continuar auditoría",
                "next_action": "Calcular conteos",
                "prerequisites": [],
            },
            "human_gate": "ORIENTATION",
            "decision_status": "PENDING",
            "human_approval_ref": None,
            "qa": {field: True for field in mod.QA_FIELDS},
        }
        self.save()

    def tearDown(self):
        self.temp.cleanup()

    def save(self):
        (self.checkpoint / "checkpoint.json").write_text(
            json.dumps(self.meta, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def test_ready_checkpoint_with_summary_chart_and_pending_gate_passes(self):
        self.assertEqual(mod.validate(self.checkpoint, ready=True), [])

    def test_summary_must_precede_graphs(self):
        html = (self.checkpoint / "report.html").read_text(encoding="utf-8")
        html = html.replace("<section><h2 id=\"summary-title\">Resumen ejecutivo", "<figure></figure><section><h2 id=\"summary-title\">Resumen ejecutivo")
        (self.checkpoint / "report.html").write_text(html, encoding="utf-8")
        self.assertIn("SUMMARY_AFTER_CHART", mod.validate(self.checkpoint, ready=True))

    def test_unresolved_tokens_fail_ready_publication(self):
        (self.checkpoint / "report.html").write_text(HTML + "{{UNMEASURED_EFFECT}}", encoding="utf-8")
        self.assertIn("UNRESOLVED_HTML_PLACEHOLDERS", mod.validate(self.checkpoint, ready=True))

    def test_chart_asset_must_exist(self):
        self.meta["charts"][0]["chart_path"] = "charts/missing.svg"
        self.save()
        self.assertIn("CHART_FILE_MISSING 0", mod.validate(self.checkpoint, ready=True))

    def test_strong_unsupported_insight_rejected(self):
        self.meta["insights"] = [
            {"status": "HYPOTHESIS", "surprising": True, "evidence_refs": []}
        ]
        self.save()
        self.assertIn("UNVERIFIED_SURPRISE 0", mod.validate(self.checkpoint, ready=True))

    def test_quality_false_blocks_publication(self):
        self.meta["qa"]["keyboard_checked"] = False
        self.save()
        self.assertIn("QA_NOT_PASSED keyboard_checked", mod.validate(self.checkpoint, ready=True))

    def test_non_explicit_human_approval_rejected(self):
        self.meta["decision_status"] = "APPROVED"
        self.save()
        self.assertIn("APPROVAL_WITHOUT_HUMAN_REFERENCE", mod.validate(self.checkpoint, ready=True))

    def test_approval_for_research_needs_commit_reference(self):
        dest = self.checkpoint.parent.parent / "HF-04" / "v01"
        dest.parent.mkdir(parents=True, exist_ok=True)
        self.checkpoint.rename(dest)
        self.checkpoint = dest
        self.meta.update({
            "checkpoint_id": "HF-04",
            "human_gate": "RESEARCH_APPROVAL",
            "previous_checkpoint": "HF-03/v01",
            "changes_since_prior": [{
                "description": "Fase final",
                "previous": "Investigación pendiente",
                "current": "QA terminada",
                "impact": "Solicitar aprobación",
                "evidence_ref": "commit:a" * 1,
            }],
            "decision_status": "APPROVED",
            "human_approval_ref": "yes",
        })
        self.save()
        self.assertIn("MISSING_RESEARCH_APPROVAL_COMMIT", mod.validate(self.checkpoint, ready=True))

    def test_no_more_than_three_user_questions(self):
        self.meta["user_questions"] *= 4
        self.save()
        self.assertIn("TOO_MANY_HUMAN_QUESTIONS", mod.validate(self.checkpoint, ready=True))

    def test_bob_ross_report_is_not_accidentally_executed(self):
        """The index exists, but no synthetic report belongs in a real episode."""
        bob_index = Path(__file__).resolve().parents[3] / "episodes" / "bob-ross" / "human_feedback" / "README.md"
        self.assertTrue(bob_index.is_file())
        self.assertIn("NO ejecutados", bob_index.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
