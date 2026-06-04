from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class TableConfig:
    name: str
    enabled: bool
    cadence: str
    description: str
    source: str
    owner: str
    primary_key: list[str]
    columns: dict[str, dict[str, Any]]
    notes: list[str]


@dataclass(frozen=True)
class CatalogConfig:
    default_cadence: str
    default_format: str
    timezone: str
    cadence_policy: dict[str, Any]
    tables: dict[str, TableConfig]


def load_config(path: str | Path) -> CatalogConfig:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    raw_tables = raw.get("tables") or {}
    tables: dict[str, TableConfig] = {}

    for name, item in raw_tables.items():
        if item is None:
            item = {}
        tables[name] = TableConfig(
            name=name,
            enabled=bool(item.get("enabled", True)),
            cadence=item.get("cadence", raw.get("default_cadence", "weekly")),
            description=item.get("description", ""),
            source=item.get("source", ""),
            owner=item.get("owner", ""),
            primary_key=list(item.get("primary_key") or []),
            columns=dict(item.get("columns") or {}),
            notes=list(item.get("notes") or []),
        )

    return CatalogConfig(
        default_cadence=raw.get("default_cadence", "weekly"),
        default_format=raw.get("default_format", "csv"),
        timezone=raw.get("timezone", "America/Mexico_City"),
        cadence_policy=dict(raw.get("cadence_policy") or {}),
        tables=tables,
    )
