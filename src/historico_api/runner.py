from __future__ import annotations

import hashlib
import json
import os
import sys
import types
from datetime import date, datetime
from pathlib import Path
from typing import Any

import nbformat
import pandas as pd

from .config import TableConfig, load_config
from .storage import make_snapshot_id


def run_notebook(
    notebook_path: str | Path,
    config_path: str | Path,
    run_date: str | None = None,
    force: bool = False,
) -> None:
    process_date = _parse_date(run_date)
    config = load_config(config_path)
    namespace = _execute_notebook(notebook_path)
    frames = _discover_frames(namespace)
    snapshot_id = make_snapshot_id()

    manifest_rows: list[dict[str, Any]] = []
    for name, frame in sorted(frames.items()):
        table_config = config.tables.get(
            name,
            TableConfig(
                name=name,
                enabled=True,
                cadence=config.default_cadence,
                description="",
                source="",
                owner="",
                primary_key=[],
                columns={},
                notes=[],
            ),
        )
        if not table_config.enabled:
            continue
        if not force and not _is_due(table_config.cadence, process_date, config.cadence_policy):
            continue

        manifest_rows.append(_save_frame(name, frame, table_config, process_date, snapshot_id))

    _write_manifest(manifest_rows, process_date, snapshot_id)


def _execute_notebook(notebook_path: str | Path) -> dict[str, Any]:
    notebook = nbformat.read(notebook_path, as_version=4)
    content_dir = Path("data/tmp/content")
    content_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("GOOGLE_MAPS_API_KEY", os.environ.get("GOOGLE_API_KEY", ""))
    _install_colab_shim()

    namespace: dict[str, Any] = {
        "__name__": "__historico_notebook__",
        "RUNNING_HISTORICO": True,
        "CONTENT_DIR": str(content_dir),
        "display": lambda *_args, **_kwargs: None,
        "get_ipython": lambda: None,
    }

    for index, cell in enumerate(notebook.cells):
        if cell.get("cell_type") != "code":
            continue
        source = _clean_source(cell.get("source", ""))
        if not source.strip():
            continue
        code = compile(source, f"{notebook_path}:cell_{index}", "exec")
        exec(code, namespace)

    return namespace


def _install_colab_shim() -> None:
    try:
        import google as google_pkg  # type: ignore
    except Exception:
        google_pkg = types.ModuleType("google")
        google_pkg.__path__ = []  # type: ignore[attr-defined]
        sys.modules["google"] = google_pkg

    colab_module = types.ModuleType("google.colab")

    class _UserData:
        @staticmethod
        def get(key: str) -> str:
            return os.environ.get(key, "")

    class _Drive:
        @staticmethod
        def mount(*_args: Any, **_kwargs: Any) -> None:
            return None

    class _Files:
        @staticmethod
        def download(*_args: Any, **_kwargs: Any) -> None:
            return None

    colab_module.userdata = _UserData()
    colab_module.drive = _Drive()
    colab_module.files = _Files()
    setattr(google_pkg, "colab", colab_module)
    sys.modules["google.colab"] = colab_module


def _clean_source(source: str) -> str:
    cleaned_lines: list[str] = []
    for line in source.splitlines():
        stripped = line.strip()
        if (
            stripped.startswith("%")
            or stripped.startswith("!")
            or stripped.startswith("pip install")
            or stripped.startswith("pip3 install")
            or stripped.startswith("apt install")
            or stripped.startswith("apt-get install")
            or stripped.startswith("get_ipython().system")
            or stripped.startswith("get_ipython().run_line_magic")
            or stripped.startswith("get_ipython().run_cell_magic")
        ):
            continue
        if "/content/" in line:
            line = line.replace("/content/", "data/tmp/content/")
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)


def _discover_frames(namespace: dict[str, Any]) -> dict[str, pd.DataFrame]:
    frames: dict[str, pd.DataFrame] = {}
    for name, value in namespace.items():
        if name.startswith("_"):
            continue
        if isinstance(value, pd.DataFrame):
            frames[name] = value.copy()
    return frames


def _save_frame(
    name: str,
    frame: pd.DataFrame,
    table_config: TableConfig,
    process_date: date,
    snapshot_id: str,
) -> dict[str, Any]:
    normalized = frame.copy()
    normalized.insert(0, "_snapshot_id", snapshot_id)
    normalized.insert(1, "_snapshot_date", process_date.isoformat())
    normalized.insert(2, "_source_table", name)

    current_dir = Path("data/current")
    history_dir = Path("data/history") / name
    current_dir.mkdir(parents=True, exist_ok=True)
    history_dir.mkdir(parents=True, exist_ok=True)

    current_path = current_dir / f"{name}.csv"
    snapshot_path = history_dir / f"{snapshot_id}.csv"

    normalized.to_csv(current_path, index=False)
    normalized.to_csv(snapshot_path, index=False)

    content_hash = hashlib.sha256(snapshot_path.read_bytes()).hexdigest()
    return {
        "table": name,
        "snapshot_id": snapshot_id,
        "snapshot_date": process_date.isoformat(),
        "rows": int(len(normalized)),
        "columns": int(len(normalized.columns)),
        "cadence": table_config.cadence,
        "hash_sha256": content_hash,
        "current_path": str(current_path).replace("\\", "/"),
        "snapshot_path": str(snapshot_path).replace("\\", "/"),
    }


def _write_manifest(rows: list[dict[str, Any]], process_date: date, snapshot_id: str) -> None:
    manifest_dir = Path("data/manifests")
    manifest_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = manifest_dir / f"{snapshot_id}_notebook.json"
    manifest_path.write_text(
        json.dumps(
            {
                "generated_at": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
                "snapshot_id": snapshot_id,
                "snapshot_date": process_date.isoformat(),
                "tables": rows,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def _parse_date(run_date: str | None) -> date:
    if run_date:
        return date.fromisoformat(run_date)
    return date.today()


def _is_due(cadence: str, process_date: date, policy: dict[str, Any]) -> bool:
    if cadence in {"hourly_weekdays", "every_2_hours_weekdays", "daily", "daily_weekdays"}:
        return True
    if cadence == "weekly":
        weekday = int(policy.get("weekly", {}).get("weekday", 1))
        return process_date.isoweekday() == weekday
    if cadence == "monthly":
        day = int(policy.get("monthly", {}).get("day_of_month", 1))
        return process_date.day == day
    if cadence == "quarterly":
        return process_date.day == 1 and process_date.month in {1, 4, 7, 10}
    raise ValueError(f"Periodicidad no soportada: {cadence}")
