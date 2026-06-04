from __future__ import annotations

from pathlib import Path

import pandas as pd

from .config import TableConfig, load_config


def build_docs(config_path: str | Path) -> None:
    config = load_config(config_path)
    docs_dir = Path("docs")
    docs_dir.mkdir(parents=True, exist_ok=True)
    output = docs_dir / "tablas.md"

    lines: list[str] = [
        "# Documentacion de tablas",
        "",
        "Este archivo se regenera a partir de `configs/tables.yml` y de los CSV en `data/current`.",
        "Complete en el catalogo los significados de columnas cuando el valor aparezca como pendiente.",
        "",
    ]

    current_dir = Path("data/current")
    csv_paths = sorted(current_dir.glob("*.csv")) if current_dir.exists() else []
    configured_names = sorted(config.tables)
    names = sorted(set(configured_names) | {path.stem for path in csv_paths})

    if not names:
        lines.extend(
            [
                "Aun no hay tablas generadas.",
                "",
                "Ejecute `python -m historico_api run --notebook Get_Datos_API.ipynb --config configs/tables.yml --force`.",
                "",
            ]
        )
    for name in names:
        table_config = config.tables.get(
            name,
            TableConfig(name, True, config.default_cadence, "", "", "", [], {}, []),
        )
        lines.extend(_render_table_section(name, table_config, current_dir / f"{name}.csv"))

    output.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _render_table_section(name: str, table_config: TableConfig, csv_path: Path) -> list[str]:
    lines = [
        f"## `{name}`",
        "",
        f"- **Estado:** {'activa' if table_config.enabled else 'deshabilitada'}",
        f"- **Periodicidad:** `{table_config.cadence}`",
        f"- **Fuente:** {table_config.source or 'Pendiente de documentar'}",
        f"- **Responsable:** {table_config.owner or 'Pendiente de documentar'}",
        f"- **Descripcion:** {table_config.description or 'Pendiente de documentar'}",
    ]
    if table_config.primary_key:
        lines.append(f"- **Llave primaria sugerida:** `{', '.join(table_config.primary_key)}`")
    lines.append("")

    if not csv_path.exists():
        lines.extend(["No existe snapshot actual para esta tabla.", ""])
        if table_config.columns:
            lines.extend(
                [
                    "| Columna | Tipo inferido | Significado | Ejemplo |",
                    "| --- | --- | --- | --- |",
                ]
            )
            for column, col_config in table_config.columns.items():
                lines.append(
                    f"| `{column}` | `pendiente` | {col_config.get('meaning', 'Pendiente de documentar')} | `{_escape_cell(col_config.get('example', ''))}` |"
                )
            lines.append("")
        return lines

    frame = pd.read_csv(csv_path, nrows=25)
    lines.extend(
        [
            "| Columna | Tipo inferido | Significado | Ejemplo |",
            "| --- | --- | --- | --- |",
        ]
    )
    for column in frame.columns:
        col_config = table_config.columns.get(column, {})
        example = col_config.get("example") or _first_example(frame[column])
        meaning = col_config.get("meaning") or "Pendiente de documentar"
        lines.append(
            f"| `{column}` | `{frame[column].dtype}` | {meaning} | `{_escape_cell(example)}` |"
        )
    lines.append("")

    if table_config.notes:
        lines.append("Notas:")
        for note in table_config.notes:
            lines.append(f"- {note}")
        lines.append("")

    return lines


def _first_example(series: pd.Series) -> str:
    values = series.dropna()
    if values.empty:
        return ""
    return str(values.iloc[0])


def _escape_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")[:120]
