#!/usr/bin/env python3
"""Validate a versioned AI Discovery Labs human-feedback checkpoint.

Offline, standard-library-only quality gate. It checks structure, provenance,
summary-first presentation, chart evidence, human approval and publication QA.
It does not assess the scientific truth of the underlying evidence.

Usage:
  python discovery_labs/shared/validators/validate_human_feedback.py \
    --checkpoint discovery_labs/episodes/bob-ross/human_feedback/HF-00/v01 \
    --ready
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

CHECKPOINTS = {f"HF-{i:02d}" for i in range(6)}
HUMAN_GATES = {
    "HF-00": "ORIENTATION",
    "HF-01": "RESEARCH_FEEDBACK",
    "HF-02": "O2_PRIORITY_DECISION",
    "HF-03": "SCIENTIFIC_FEEDBACK",
    "HF-04": "RESEARCH_APPROVAL",
    "HF-05": "STORY_APPROVAL",
}
QA_FIELDS = (
    "summary_first",
    "chart_provenance_checked",
    "uncertainty_checked",
    "mobile_checked",
    "desktop_checked",
    "keyboard_checked",
    "references_resolve",
    "has_adversarial_review",
    "no_unverified_surprise",
)
SUMMARY_FIELDS = ("summary", "delta", "surprise", "recommendation", "limitation")
CHART_FIELDS = (
    "chart_id", "title", "question_id", "type", "chart_path",
    "data_source", "evidence_ref", "code_ref", "population", "n",
    "denominator", "unit", "baseline", "uncertainty", "alt_text",
    "rights_status", "mobile_checked", "desktop_checked",
)
VALID_STATUS = {"DRAFT", "READY_FOR_FEEDBACK", "BLOCKED", "REVISED", "CLOSED"}
VALID_DECISIONS = {"PENDING", "APPROVED", "CHANGES_REQUESTED", "DEFERRED", "REJECTED"}
PLACEHOLDER_RE = re.compile(r"\{\{[^{}]+\}\}")
SUMMARY_RE = re.compile(r'id\s*=\s*["\']summary-title["\']', re.I)
FIRST_FIGURE_RE = re.compile(r"<figure(?:\s|>)", re.I)
FIRST_TABLE_RE = re.compile(r"<table(?:\s|>)", re.I)


def _str(value):
    return isinstance(value, str) and bool(value.strip())


def _required_fields(value, fields, prefix, issues):
    if not isinstance(value, dict):
        issues.append(f"INVALID_OBJECT {prefix}")
        return False
    for name in fields:
        if name not in value:
            issues.append(f"MISSING_FIELD {prefix}.{name}")
    return True


def validate(checkpoint: Path, ready: bool = False) -> list[str]:
    """Return diagnostics, empty list means structural/QA pass."""
    checkpoint = checkpoint.resolve()
    problems: list[str] = []
    meta_path = checkpoint / "checkpoint.json"
    html_path = checkpoint / "report.html"
    feedback_path = checkpoint / "feedback.md"

    for file in (meta_path, html_path, feedback_path):
        if not file.is_file():
            problems.append(f"MISSING_FILE {file.name}")
    if problems:
        return problems

    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError) as exc:
        return [f"INVALID_JSON checkpoint.json: {exc}"]
    if not isinstance(meta, dict):
        return ["INVALID_JSON_ROOT expected object"]

    required = (
        "schema_version", "checkpoint_id", "dataset_id", "version",
        "created_at", "phase", "status", "source_commit",
        "previous_checkpoint", "report_path", "executive_summary",
        "changes_since_prior", "insights", "charts", "user_questions",
        "recommendation", "human_gate", "decision_status", "qa",
    )
    _required_fields(meta, required, "checkpoint", problems)
    if meta.get("schema_version") != "human-feedback-checkpoint-1.0":
        problems.append("INVALID_SCHEMA_VERSION")
    ident = meta.get("checkpoint_id")
    if ident not in CHECKPOINTS:
        problems.append("INVALID_CHECKPOINT_ID")
    if ident != checkpoint.parent.name:
        problems.append("CHECKPOINT_PATH_ID_MISMATCH")
    version = meta.get("version")
    if not isinstance(version, int) or isinstance(version, bool) or version < 1:
        problems.append("INVALID_VERSION")
    elif checkpoint.name != f"v{version:02d}":
        problems.append("CHECKPOINT_PATH_VERSION_MISMATCH")
    if meta.get("human_gate") != HUMAN_GATES.get(ident):
        problems.append("HUMAN_GATE_MISMATCH")
    if meta.get("status") not in VALID_STATUS:
        problems.append("INVALID_STATUS")
    if meta.get("decision_status") not in VALID_DECISIONS:
        problems.append("INVALID_DECISION_STATUS")
    for field in ("dataset_id", "phase", "source_commit", "report_path"):
        if not _str(meta.get(field)):
            problems.append(f"MISSING_VALUE {field}")
    if meta.get("report_path") and Path(str(meta["report_path"])).name != "report.html":
        problems.append("REPORT_PATH_NOT_HTML")
    if meta.get("report_starts_with_summary") is not True:
        problems.append("SUMMARY_FIRST_FLAG_MISSING")
    if ident != "HF-00" and not _str(meta.get("previous_checkpoint")):
        problems.append("PREVIOUS_CHECKPOINT_REQUIRED")

    summary = meta.get("executive_summary")
    if _required_fields(summary, SUMMARY_FIELDS, "executive_summary", problems):
        for key in SUMMARY_FIELDS:
            if not _str(summary.get(key)):
                problems.append(f"EMPTY_SUMMARY_FIELD {key}")

    html = html_path.read_text(encoding="utf-8")
    heading = html.find("<h1")
    summary_match = SUMMARY_RE.search(html)
    figure = FIRST_FIGURE_RE.search(html)
    table = FIRST_TABLE_RE.search(html)
    if heading < 0 or not summary_match:
        problems.append("MISSING_TITLE_OR_SUMMARY")
    elif summary_match.start() < heading:
        problems.append("SUMMARY_BEFORE_TITLE")
    if summary_match and figure and summary_match.start() > figure.start():
        problems.append("SUMMARY_AFTER_CHART")
    if summary_match and table and summary_match.start() > table.start():
        problems.append("SUMMARY_AFTER_TABLE")
    if "Resumen ejecutivo" not in html:
        problems.append("SUMMARY_HEADING_NOT_VISIBLE")

    changes = meta.get("changes_since_prior")
    if not isinstance(changes, list):
        problems.append("INVALID_CHANGES")
    elif ident != "HF-00" and not changes:
        problems.append("NO_COMPARISON_WITH_PREVIOUS")
    insights = meta.get("insights")
    if not isinstance(insights, list):
        problems.append("INVALID_INSIGHTS")
    else:
        for i, insight in enumerate(insights):
            if not isinstance(insight, dict):
                problems.append(f"INVALID_INSIGHT {i}")
                continue
            if insight.get("status") == "VERIFIED" and not insight.get("evidence_refs"):
                problems.append(f"UNSUPPORTED_VERIFIED_INSIGHT {i}")
            if insight.get("surprising") and insight.get("status") != "VERIFIED":
                problems.append(f"UNVERIFIED_SURPRISE {i}")
    charts = meta.get("charts")
    if not isinstance(charts, list):
        problems.append("INVALID_CHARTS")
        charts = []
    ids = []
    for i, chart in enumerate(charts):
        if not _required_fields(chart, CHART_FIELDS, f"charts[{i}]", problems):
            continue
        ids.append(chart.get("chart_id"))
        for field in CHART_FIELDS:
            if field in ("n", "mobile_checked", "desktop_checked"):
                continue
            if not _str(chart.get(field)):
                problems.append(f"EMPTY_CHART_FIELD charts[{i}].{field}")
        if not isinstance(chart.get("n"), int) or isinstance(chart.get("n"), bool) or chart["n"] < 0:
            problems.append(f"INVALID_CHART_N {i}")
        if chart.get("rights_status") == "BLOCKED":
            problems.append(f"BLOCKED_IMAGE_IN_REPORT {i}")
        chart_path = chart.get("chart_path")
        if _str(chart_path) and not chart_path.startswith(("https://", "http://")):
            target = (checkpoint / chart_path).resolve()
            if not target.is_relative_to(checkpoint):
                problems.append(f"CHART_PATH_ESCAPE {i}")
            elif not target.is_file():
                problems.append(f"CHART_FILE_MISSING {i}")
        if ready and (chart.get("mobile_checked") is not True or chart.get("desktop_checked") is not True):
            problems.append(f"CHART_VISUAL_QA_INCOMPLETE {i}")
    if len(ids) != len(set(map(str, ids))):
        problems.append("DUPLICATE_CHART_ID")

    questions = meta.get("user_questions")
    if not isinstance(questions, list):
        problems.append("INVALID_USER_QUESTIONS")
    elif len(questions) > 3:
        problems.append("TOO_MANY_HUMAN_QUESTIONS")
    elif ready:
        for i, q in enumerate(questions):
            if not isinstance(q, dict) or not all(
                _str(q.get(f)) for f in ("id", "question", "recommended_option", "reason", "impact_if_postponed")
            ):
                problems.append(f"INCOMPLETE_HUMAN_QUESTION {i}")
    approval = meta.get("human_approval_ref")
    if meta.get("decision_status") == "APPROVED":
        if not _str(approval):
            problems.append("APPROVAL_WITHOUT_HUMAN_REFERENCE")
        if ident == "HF-04" and (not _str(approval) or not approval.startswith("RESEARCH_APPROVED:")):
            problems.append("MISSING_RESEARCH_APPROVAL_COMMIT")
        if ident == "HF-05" and (not _str(approval) or not approval.startswith("STORY_APPROVED:")):
            problems.append("MISSING_STORY_APPROVAL_COMMIT")

    if ready:
        if meta.get("status") not in {"READY_FOR_FEEDBACK", "CLOSED"}:
            problems.append("NOT_READY_FOR_PUBLICATION")
        if PLACEHOLDER_RE.search(html):
            problems.append("UNRESOLVED_HTML_PLACEHOLDERS")
        if not charts:
            problems.append("NO_EVIDENCE_CHARTS")
        if len(charts) > len(FIRST_FIGURE_RE.findall(html)):
            problems.append("CHART_METADATA_WITHOUT_VISIBLE_FIGURE")
        qa = meta.get("qa")
        if not isinstance(qa, dict):
            problems.append("INVALID_QA")
        else:
            for key in QA_FIELDS:
                if qa.get(key) is not True:
                    problems.append(f"QA_NOT_PASSED {key}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, required=True, help="HF-XX/vNN directory")
    parser.add_argument("--ready", action="store_true", help="enforce ready-to-publish report/chart/QA checks")
    args = parser.parse_args()
    errors = validate(args.checkpoint, ready=args.ready)
    if errors:
        print("\n".join(f"FAIL {item}" for item in errors))
        return 1
    print(f"PASS Human Feedback checkpoint: {args.checkpoint} ({'ready' if args.ready else 'draft'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
