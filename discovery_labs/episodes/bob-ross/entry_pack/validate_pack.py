#!/usr/bin/env python3
"""Validate Bob Ross against the canonical shared Question Forge contract.

No model fitting, statistical tests, network requests, or data transformations.
Usage: python discovery_labs/episodes/bob-ross/entry_pack/validate_pack.py
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EPISODE = ROOT.parent
SHARED = ROOT.parents[2] / "shared"
VALIDATOR = SHARED / "validators" / "validate_entry_pack.py"
CATALOG = SHARED / "model_catalog" / "MODEL_SET.md"
SKILL = SHARED / "skills" / "question-forge" / "SKILL.md"


def main() -> int:
    if not (VALIDATOR.exists() and CATALOG.exists() and SKILL.exists()):
        print("ERROR: shared core missing; integrate PR #11 before Bob Ross.", file=sys.stderr)
        return 2
    spec = importlib.util.spec_from_file_location("shared_entry_validation", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    report, issues = module.validate(ROOT, CATALOG, EPISODE / "research_guide.html")
    questions = json.loads((ROOT / "questions_master.json").read_text(encoding="utf-8"))["questions"]
    qids = [q["id"] for q in questions]
    if len(questions) != 14 or len(set(qids)) != 14:
        issues.append("BOB_ROSS_EXPECTED_14_UNIQUE_QUESTIONS")
    if "BR-01" not in qids:
        issues.append("BOB_ROSS_MISSING_BIOGRAPHICAL_QUESTION")
    for q in questions:
        qid = str(q.get("id", "?"))
        if not re.fullmatch(r"BR-\d{2}", qid):
            issues.append(qid + ":INVALID_ID")
        if q.get("design_status") != "PLAN_ONLY":
            issues.append(qid + ":NOT_PLANNING_ONLY")
        for name in ("o2_trigger", "o3_trigger"):
            if not str(q.get(name, "")).startswith("CONDICIONAL:"):
                issues.append(qid + ":MISSING_CONDITIONAL_" + name)
        for name in ("rival_hypothesis", "model_baseline", "model_validation", "stat_why", "stat_where"):
            if len(str(q.get(name, "")).strip()) < 16:
                issues.append(qid + ":MISSING_" + name)
        estimand = q.get("estimand") or {}
        if not all(str(estimand.get(k, "")).strip() for k in ("grain", "population", "measure", "denominator", "time_basis")):
            issues.append(qid + ":INCOMPLETE_ESTIMAND")
    guide = (EPISODE / "research_guide.html").read_text(encoding="utf-8")
    if guide.count('class="story-arc"') != 14 or "linfoma" not in guide.lower():
        issues.append("GUIDE_MISSING_14_QUESTIONS_OR_HEALTH_CONTEXT")
    if len(re.findall(r'\bid="preguntas"', guide)) != 1:
        issues.append("GUIDE_DUPLICATED_QUESTION_BLOCKS")
    report.update({
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "canonical_skill": str(SKILL),
        "canonical_catalog": str(CATALOG),
        "questions_with_model_and_statistical_plan": len(questions),
        "research_approval": "PENDING",
        "models_executed": 0,
    })
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
