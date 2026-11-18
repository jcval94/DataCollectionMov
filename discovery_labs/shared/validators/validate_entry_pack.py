#!/usr/bin/env python3
"""Validate any AI Discovery Labs entry pack without model training or network.

Usage from repository root:
  python discovery_labs/shared/validators/validate_entry_pack.py \
      --entry-pack discovery_labs/episodes/<slug>/entry_pack \
      --guide discovery_labs/episodes/<slug>/research_guide.html

The validator checks structure, question contracts, source metadata,
model references and optional one-block HTML integration. It does not
validate the scientific truth of outside claims or execute research.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

SHARED = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = SHARED / "model_catalog" / "MODEL_SET.md"
REQUIRED = (
    "START_HERE_NEW_CHAT.md",
    "README.md",
    "QUESTIONS_MASTER.md",
    "questions_master.json",
    "metadata.json",
    "sample_raw.csv",
    "DEEP_RESEARCH_PROMPTS.md",
    "RESEARCH_PLAN.md",
    "VISUAL_DESIGN.md",
)
MODEL_RE = re.compile(r"^\|\s*(M\d{2})\s*\|", re.MULTILINE)


def validate(entry_pack: Path, catalog: Path = DEFAULT_CATALOG, guide: Path | None = None):
    entry_pack = entry_pack.resolve()
    catalog = catalog.resolve()
    issues = []
    report = {"entry_pack": str(entry_pack), "catalog": str(catalog)}
    for file in REQUIRED:
        if not (entry_pack / file).is_file():
            issues.append("MISSING_FILE " + file)
    if not catalog.is_file():
        issues.append("MISSING_CATALOG " + str(catalog))
    if issues:
        return report, issues

    try:
        bank = json.loads((entry_pack / "questions_master.json").read_text(encoding="utf-8"))
        questions = bank["questions"]
        assert isinstance(questions, list) and questions, "questions must be nonempty"
        metadata = json.loads((entry_pack / "metadata.json").read_text(encoding="utf-8"))
    except (ValueError, KeyError, AssertionError) as exc:
        return report, ["SCHEMA " + str(exc)]

    ids = [str(q.get("id", "")).strip() for q in questions]
    if not all(ids) or len(ids) != len(set(ids)):
        issues.append("DUPLICATE_OR_MISSING_QUESTION_ID")
    report["questions"] = len(questions)
    md = (entry_pack / "QUESTIONS_MASTER.md").read_text(encoding="utf-8")
    missing_md = [qid for qid in ids if qid and qid not in md]
    if missing_md:
        issues.append("MARKDOWN_QUESTION_MISMATCH: " + ",".join(missing_md))

    catalog_text = catalog.read_text(encoding="utf-8")
    catalog_ids = set(MODEL_RE.findall(catalog_text))
    if not catalog_ids:
        issues.append("EMPTY_MODEL_CATALOG")
    report["model_families"] = len(catalog_ids)

    for q in questions:
        qid = str(q.get("id", "?"))
        for field in ("root", "o1", "o2", "o3"):
            if not str(q.get(field) or "").strip():
                issues.append(qid + ":MISSING_" + field.upper())
        model = q.get("model_primary_id") or q.get("model")
        if isinstance(model, dict):
            model = model.get("primary_id")
        if model not in catalog_ids:
            issues.append(qid + ":MODEL_NOT_IN_CATALOG")
        for field in ("model_why", "model_where"):
            if not str(q.get(field) or "").strip():
                issues.append(qid + ":MISSING_" + field.upper())
        stat = q.get("statistical_exercise") or q.get("stat")
        if isinstance(stat, dict):
            stat = stat.get("what")
        if not str(stat or "").strip():
            issues.append(qid + ":MISSING_STATISTICAL_EXERCISE")
        if not str(q.get("data") or q.get("required_data") or "").strip():
            issues.append(qid + ":MISSING_DATA_NEEDS")
        for fld, alt in (("o2_trigger", "trigger_from_O1"), ("o3_trigger", "trigger_from_O2")):
            if not str(q.get(fld) or q.get(alt) or "").strip():
                issues.append(qid + ":MISSING_" + fld.upper())
        if not str(q.get("visual") or "").strip():
            issues.append(qid + ":MISSING_VISUAL")
    report["model_plans"] = sum(bool(q.get("model") or q.get("model_primary_id")) for q in questions)
    report["statistical_plans"] = sum(bool(q.get("stat") or q.get("statistical_exercise")) for q in questions)

    for field in ("rows", "columns"):
        val = metadata.get(field)
        if not isinstance(val, int) or val <= 0:
            issues.append("BAD_METADATA_" + field.upper())
    with (entry_pack / "sample_raw.csv").open(encoding="utf-8", newline="") as file:
        sample = list(csv.DictReader(file))
    if not sample:
        issues.append("EMPTY_SAMPLE_RAW")
    else:
        report["sample_rows"] = len(sample)
        if sample[0].keys() and len(sample[0]) != metadata.get("columns"):
            issues.append("SAMPLE_RAW_COLUMN_MISMATCH")
    features = entry_pack / "sample_features.csv"
    if features.is_file():
        with features.open(encoding="utf-8", newline="") as file:
            transformed = list(csv.DictReader(file))
        if len(transformed) != len(sample):
            issues.append("SAMPLE_FEATURE_ROW_MISMATCH")

    if guide is not None:
        guide = guide.resolve()
        if not guide.is_file():
            issues.append("MISSING_GUIDE " + str(guide))
        else:
            html = guide.read_text(encoding="utf-8")
            if html.count('id="preguntas"') != 1:
                issues.append("GUIDE_QUESTIONS_NOT_SINGLE_BLOCK")
            if 'id="investigaciones"' in html or "02B /" in html:
                issues.append("GUIDE_LEGACY_SECOND_QUESTION_BLOCK")
            missing = [qid for qid in ids if ('id="' + qid.lower() + '"') not in html]
            if missing:
                issues.append("GUIDE_MISSING_QUESTION_IDS: " + ",".join(missing))
            if not any(s in html for s in ("PENDIENTE DE APROBACIÓN", "PENDIENTE_DE_APROBACION")):
                issues.append("GUIDE_MISSING_APPROVAL_STATUS")
            report["guide"] = str(guide)
    report["status"] = "PASS" if not issues else "FAIL"
    return report, issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entry-pack", required=True, type=Path)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--guide", type=Path)
    args = parser.parse_args()
    report, issues = validate(args.entry_pack, args.catalog, args.guide)
    report["issues"] = issues
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
