#!/usr/bin/env python3
"""Validate the portable Question Forge entry pack, with no model execution.

Usage: python discovery_labs/episodes/bob-ross/entry_pack/validate_pack.py
Only reads files in the Bob Ross episode; no network, pip or generated outputs.
"""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EPISODE = ROOT.parent
REQUIRED = [
    "START_HERE_NEW_CHAT.md", "README.md", "EPISODE_TEMPLATE.md",
    "skills/question-forge/SKILL.md", "QUESTIONS_MASTER.md",
    "questions_master.json", "MODEL_SET.md", "DEEP_RESEARCH_PROMPTS.md",
    "CONTEXT_CLAIMS.md", "RESEARCH_PLAN.md", "VISUAL_DESIGN.md",
    "PROMPT_FASE1_V2.md", "metadata.json", "sample_raw.csv", "sample_features.csv",
]
def main():
    for name in REQUIRED:
        assert (ROOT / name).is_file(), f"Missing entry file: {name}"

    bank = json.loads((ROOT / "questions_master.json").read_text(encoding="utf-8"))
    questions = bank["questions"]
    ids = [q["id"] for q in questions]
    assert len(questions) >= 12 and len(set(ids)) == len(ids)
    assert ids[0] == "BR-01" and ids[-1] == "BR-14"
    assert all(re.fullmatch(r"BR-\d{2}", qid) for qid in ids)

    text = (ROOT / "QUESTIONS_MASTER.md").read_text(encoding="utf-8")
    model_text = (ROOT / "MODEL_SET.md").read_text(encoding="utf-8")
    models = set(re.findall(r"^\|\s*(M\d{2})\s*\|", model_text, re.M))
    assert len(models) >= 20, "Model catalog unexpectedly small"
    for q in questions:
        for attr in ("title", "root", "o1", "o2", "o3", "model",
                     "model_name", "model_why", "model_where", "stat",
                     "data", "visual", "note", "status"):
            assert isinstance(q.get(attr), str) and q[attr].strip(), f"{q['id']} lacks {attr}"
        for attr in ("o2_trigger", "o3_trigger", "rival_hypothesis", "model_baseline",
                     "model_validation", "stat_why", "stat_where", "design_status"):
            assert isinstance(q.get(attr), str) and len(q[attr].strip()) > 15, f"{q['id']} lacks methodological field {attr}"
        assert q["design_status"] == "PLAN_ONLY", f"{q['id']} must remain unexecuted"
        estimand = q.get("estimand", {})
        for attr in ("grain", "population", "measure", "denominator", "time_basis"):
            assert isinstance(estimand.get(attr), str) and estimand[attr].strip(), f"{q['id']} lacks estimand.{attr}"
        assert q["model_baseline"] != q["stat_why"]
        assert q["model"] in models, f"{q['id']} references missing model"
        assert f"### {q['id']}" in text, f"Question missing from canonical markdown: {q['id']}"
    assert text.count("### BR-") == len(questions)
    assert text.count("**Contrato metodológico adicional (sin ejecutar):**") == len(questions)
    assert "LSTM" in model_text and "Optuna" in model_text and "refuerzo" in model_text.lower()

    metadata = json.loads((ROOT / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["rows"] == 403 and metadata["columns"] == 69
    with (ROOT / "sample_raw.csv").open(newline="", encoding="utf-8") as f:
        raw = list(csv.DictReader(f))
    with (ROOT / "sample_features.csv").open(newline="", encoding="utf-8") as f:
        feat = list(csv.DictReader(f))
    assert len(raw) == len(feat) == 13
    assert set(x["EPISODE"] for x in raw) == set(x["EPISODE"] for x in feat)
    assert len(raw[0]) == 69 and len(feat[0]) == 16
    assert any(int(x["GUEST"]) for x in raw)

    skill = (ROOT / "skills/question-forge/SKILL.md").read_text(encoding="utf-8")
    assert "version: 2.0.0" in skill
    assert "único bloque" in skill.lower() or "un único bloque" in skill.lower()
    assert "ejercicio estadístico" in skill
    assert "NO" in (ROOT / "CONTEXT_CLAIMS.md").read_text(encoding="utf-8")
    guide = (EPISODE / "research_guide.html").read_text(encoding="utf-8")
    assert guide.count('id="preguntas"') == 1
    assert 'id="investigaciones"' not in guide
    assert "02B /" not in guide
    assert all(f'id="{qid.lower()}"' in guide for qid in ids)
    assert guide.count('class="story-arc"') == len(questions)
    assert "linfoma" in guide.lower()
    assert "modelo propuesto" in guide.lower()
    assert "estadístico" in guide.lower()
    assert "PENDIENTE DE APROBACIÓN" in guide
    print(json.dumps({
        "status": "PASS", "questions": len(questions), "models": len(models),
        "statistical_exercises": len(questions), "sample_raw_rows": len(raw),
        "one_html_question_section": True,
        "research_guide_status": "PENDING_HUMAN_APPROVAL",
        "note": "Static package validation only; no models/trials trained or external sources verified in this run."
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
