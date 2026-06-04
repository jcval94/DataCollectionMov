from __future__ import annotations

import json
import shutil
from datetime import date, datetime
from pathlib import Path
from typing import Any

import pandas as pd

from .config import TableConfig, load_config


def parse_run_date(run_date: str | None = None) -> date:
    if run_date:
        return date.fromisoformat(run_date)
    return date.today()


def make_snapshot_id() -> str:
    return datetime.utcnow().replace(microsecond=0).strftime("%Y%m%dT%H%M%SZ")


def save_tables(
    tables: dict[str, pd.DataFrame],
    *,
    source: str,
    config_path: str | Path,
    run_date: str | None = None,
    snapshot_id: str | None = None,
) -> list[dict[str, Any]]:
    config = load_config(config_path)
    snapshot_date = parse_run_date(run_date)
    snapshot_id = snapshot_id or make_snapshot_id()
    manifest_rows: list[dict[str, Any]] = []

    for name, frame in sorted(tables.items()):
        table_config = config.tables.get(
            name,
            TableConfig(
                name=name,
                enabled=True,
                cadence=config.default_cadence,
                description="",
                source=source,
                owner="",
                primary_key=[],
                columns={},
                notes=[],
            ),
        )
        if not table_config.enabled:
            continue
        manifest_rows.append(
            save_table(
                name=name,
                frame=frame,
                source=source,
                snapshot_date=snapshot_date,
                snapshot_id=snapshot_id,
                cadence=table_config.cadence,
            )
        )

    write_manifest(source, snapshot_date, snapshot_id, manifest_rows)
    return manifest_rows


def save_table(
    *,
    name: str,
    frame: pd.DataFrame,
    source: str,
    snapshot_date: date,
    snapshot_id: str,
    cadence: str,
) -> dict[str, Any]:
    if frame is None:
        frame = pd.DataFrame()

    normalized = frame.copy()
    for column, value in [
        ("_snapshot_id", snapshot_id),
        ("_snapshot_date", snapshot_date.isoformat()),
        ("_extracted_at_utc", datetime.utcnow().replace(microsecond=0).isoformat() + "Z"),
        ("_source_table", name),
        ("_source_system", source),
    ]:
        if column not in normalized.columns:
            normalized.insert(0, column, value)

    current_dir = Path("data/current")
    history_dir = Path("data/history") / name
    current_dir.mkdir(parents=True, exist_ok=True)
    history_dir.mkdir(parents=True, exist_ok=True)

    current_path = current_dir / f"{name}.csv"
    snapshot_path = history_dir / f"{snapshot_id}.csv"

    normalized.to_csv(current_path, index=False, encoding="utf-8")
    normalized.to_csv(snapshot_path, index=False, encoding="utf-8")

    return {
        "table": name,
        "source": source,
        "snapshot_id": snapshot_id,
        "snapshot_date": snapshot_date.isoformat(),
        "rows": int(len(normalized)),
        "columns": int(len(normalized.columns)),
        "cadence": cadence,
        "current_path": str(current_path).replace("\\", "/"),
        "snapshot_path": str(snapshot_path).replace("\\", "/"),
    }


def save_artifact(
    *,
    name: str,
    suffix: str,
    content: str | bytes,
    source: str,
    run_date: str | None = None,
    snapshot_id: str | None = None,
) -> dict[str, Any]:
    snapshot_date = parse_run_date(run_date)
    snapshot_id = snapshot_id or make_snapshot_id()
    current_dir = Path("data/artifacts/current")
    history_dir = Path("data/artifacts/history") / name
    current_dir.mkdir(parents=True, exist_ok=True)
    history_dir.mkdir(parents=True, exist_ok=True)

    current_path = current_dir / f"{name}.{suffix}"
    snapshot_path = history_dir / f"{snapshot_id}.{suffix}"

    mode = "wb" if isinstance(content, bytes) else "w"
    kwargs = {} if isinstance(content, bytes) else {"encoding": "utf-8"}
    with open(current_path, mode, **kwargs) as f:
        f.write(content)
    shutil.copyfile(current_path, snapshot_path)

    row = {
        "artifact": name,
        "source": source,
        "snapshot_id": snapshot_id,
        "snapshot_date": snapshot_date.isoformat(),
        "current_path": str(current_path).replace("\\", "/"),
        "snapshot_path": str(snapshot_path).replace("\\", "/"),
    }
    append_artifact_manifest(source, snapshot_date, snapshot_id, row)
    return row


def write_manifest(
    source: str,
    snapshot_date: date,
    snapshot_id: str,
    rows: list[dict[str, Any]],
) -> None:
    manifest_dir = Path("data/manifests")
    manifest_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = manifest_dir / f"{snapshot_id}_{source}.json"
    manifest_path.write_text(
        json.dumps(
            {
                "generated_at": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
                "source": source,
                "snapshot_id": snapshot_id,
                "snapshot_date": snapshot_date.isoformat(),
                "tables": rows,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def append_artifact_manifest(
    source: str,
    snapshot_date: date,
    snapshot_id: str,
    row: dict[str, Any],
) -> None:
    manifest_dir = Path("data/manifests")
    manifest_dir.mkdir(parents=True, exist_ok=True)
    path = manifest_dir / f"{snapshot_id}_{source}_artifacts.json"
    payload = {
        "generated_at": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "source": source,
        "snapshot_id": snapshot_id,
        "snapshot_date": snapshot_date.isoformat(),
        "artifacts": [row],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_current_table(name: str) -> pd.DataFrame:
    path = Path("data/current") / f"{name}.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, low_memory=False)
