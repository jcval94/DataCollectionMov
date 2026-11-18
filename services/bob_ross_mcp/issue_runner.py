"""Owner-only GitHub Issue request -> bounded offline Bob Ross comparison.

Expected GitHub Issue title: Bob Ross: comparar modelos
Body (optional):
    k: 4
    include_guests: false
"""
from __future__ import annotations

import json
import os
import re

from core import compare_models


def parse(body: str):
    k = 4
    include_guests = False
    if len(body) > 2000:
        raise ValueError("Issue body exceeds 2000 characters.")
    for line in body.splitlines():
        line = line.strip()
        if not line:
            continue
        match = re.fullmatch(r"k:\s*([0-9]+)", line, re.IGNORECASE)
        if match:
            k = int(match.group(1))
            continue
        match = re.fullmatch(r"include_guests:\s*(true|false)", line, re.IGNORECASE)
        if match:
            include_guests = match.group(1).lower() == "true"
            continue
        raise ValueError("Only 'k: 2..6' and 'include_guests: true/false' are accepted.")
    if k not in range(2, 7):
        raise ValueError("k must be 2..6.")
    return k, include_guests


def report(result):
    lines = [
        "## Bob Ross: comparación de modelos terminada",
        "",
        f"**Datos:** {result['episodes']} episodios; k={result['k']}; invitados excluidos={result['exclude_guests']}.",
        f"**SHA-256 del dataset:** \`{result['source_sha256']}\`",
        "",
        "| Método | Silhouette (Euclid.) | WCSS | Grupo menor | Admisible |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for model in result["results"]:
        lines.append(
            f"| {model['algorithm']} | {model['silhouette_euclidean']:.6f} "
            f"| {model['within_cluster_ss']:.3f} | {model['smallest_group']} "
            f"| {'Sí' if model['eligible'] else 'No'} |"
        )
    winner = result["preferred_by_predeclared_rule"]
    lines.extend([
        "",
        f"**Preferido según regla fijada:** {winner or 'Ninguno satisface el tamaño mínimo de grupo'}.",
        "",
        f"**Regla:** {result['decision_rule']}",
        "",
        f"**Límites:** {result['interpretation']}",
        "",
        f"[Gráficos de referencia]({result['assets']['room_profiles']}) · "
        "[Demo para clase](" + result["assets"]["interactive_classroom_demo"] + ")",
        "",
        "La comparación se recalculó en GitHub Actions. El gráfico enlazado corresponde a la referencia previa, no a los nuevos métodos.",
    ])
    return "\n".join(lines) + "\n"


def main():
    k, include_guests = parse(os.getenv("ISSUE_BODY", ""))
    result = compare_models(k=k, exclude_guests=not include_guests)
    print(report(result))


if __name__ == "__main__":
    main()
