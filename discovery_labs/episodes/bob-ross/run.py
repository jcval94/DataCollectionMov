#!/usr/bin/env python3
"""Bob Ross Discovery Episode: offline data validation, cleaning, analyses and SVGs.

No pip dependencies, no network, no writes outside this episode directory.
Dataset: FiveThirtyEight/data (CC BY 4.0), fixed upstream commit/hash.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "elements-by-episode.csv"
OUTPUT = ROOT / "output"
EXPECTED_SHA = "42045c8b8aaa8296095d6b294927fb9d0f73a57259f59b560c375844c0fe01cf"
FEATURES = {
    "arboles": ("TREE", "TREES"),
    "montanas": ("MOUNTAIN", "MOUNTAINS", "SNOWY_MOUNTAIN"),
    "lagos": ("LAKE", "LAKES"),
    "rios": ("RIVER",),
    "mar": ("OCEAN",),
    "nieve": ("SNOW", "SNOWY_MOUNTAIN"),
    "cascadas": ("WATERFALL",),
    "estructuras": ("STRUCTURE",),
    "nubes": ("CLOUDS",),
    "rocas": ("ROCKS",),
    "sol": ("SUN",),
    "flores": ("FLOWERS",),
}
PALETTE = ("#d45b37", "#467f86", "#dbac64", "#826ba7", "#6b9767")
LABELS = list(FEATURES)


def load(path: Path = RAW, verify_hash: bool = True):
    source = path.read_bytes()
    observed_hash = hashlib.sha256(source).hexdigest()
    if verify_hash and observed_hash != EXPECTED_SHA:
        raise ValueError(f"Snapshot alterado: {observed_hash} != {EXPECTED_SHA}")
    text = source.decode("utf-8-sig")
    reader = csv.DictReader(text.splitlines())
    if not reader.fieldnames or len(reader.fieldnames) != 69:
        raise ValueError("Se esperaban 69 columnas: EPISODE, TITLE y 67 etiquetas.")
    if reader.fieldnames[:2] != ["EPISODE", "TITLE"] or "GUEST" not in reader.fieldnames:
        raise ValueError("Esquema original incompatible.")
    labels = reader.fieldnames[2:]
    rows = []
    seen = set()
    for item in reader:
        ident = item["EPISODE"]
        if not re.fullmatch(r"S\d{2}E\d{2}", ident) or ident in seen:
            raise ValueError(f"ID no válido o duplicado: {ident}")
        seen.add(ident)
        if not item["TITLE"].strip():
            raise ValueError(f"Falta título para {ident}")
        if any(item[c] not in ("0", "1") for c in labels):
            raise ValueError(f"Etiqueta no binaria o ausente: {ident}")
        flags = {c: int(item[c]) for c in labels}
        derived = {name: int(any(flags[c] for c in columns))
                   for name, columns in FEATURES.items()}
        rows.append({
            "id": ident, "title": item["TITLE"].strip('"'),
            "season": int(ident[1:3]), "guest": flags["GUEST"],
            "flags": flags, "motifs": derived,
        })
    if not rows:
        raise ValueError("El dataset está vacío.")
    return rows, observed_hash


def ratio(num, den):
    return round(num / den, 6) if den else None


def study(rows, observed_hash):
    host = [r for r in rows if not r["guest"]]
    guest = [r for r in rows if r["guest"]]
    tree = lambda r: r["motifs"]["arboles"] == 1
    mountain = lambda r: r["motifs"]["montanas"] == 1
    snow = lambda r: r["motifs"]["nieve"] == 1
    mountains = [r for r in host if mountain(r)]
    by_season = []
    for season in sorted({r["season"] for r in host}):
        season_rows = [r for r in host if r["season"] == season]
        by_season.append({
            "season": season, "n": len(season_rows),
            "trees": sum(map(tree, season_rows)),
            "mountains": sum(map(mountain, season_rows)),
        })
    motif_counts = {name: sum(r["motifs"][name] for r in host)
                    for name in FEATURES}
    no_trees = [r for r in host if not tree(r)]
    no_snow_mountains = [r for r in mountains if not snow(r)]
    profiles = Counter(tuple(r["motifs"][name] for name in LABELS) for r in host)
    # A deliberately simple, auditable "museum operations" allocation:
    # the priority order creates four disjoint rooms, not a learned taxonomy.
    def room(r):
        m = r["motifs"]
        if m["mar"] or m["cascadas"]:
            return "Agua y costa"
        if m["montanas"]:
            return "Montañas"
        if m["arboles"]:
            return "Bosques"
        return "Otros paisajes"
    allocation = Counter(room(r) for r in host)
    result = {
        "metadata": {
            "source": "FiveThirtyEight / Walt Hickey",
            "sha256": observed_hash, "rows": len(rows), "columns": 69,
            "binary_labels": 67, "unit": "episodio etiquetado",
            "rights": "CC BY 4.0 para etiquetas; no pinturas ni vídeos",
            "raw_no_cleaning": True,
        },
        "cleaning": {
            "original": len(rows), "host": len(host), "guest": len(guest),
            "removed_for_primary_analysis": len(guest),
            "missing_labels": 0, "duplicate_episode_ids": 0,
            "feature_note": "OR de columnas binarias: cuenta presencia, no objetos",
        },
        "host": {
            "n": len(host), "with_trees": sum(map(tree, host)),
            "without_trees": len(no_trees),
            "tree_rate": ratio(sum(map(tree, host)), len(host)),
            "mountains": len(mountains),
            "mountains_without_snow": len(no_snow_mountains),
            "mountain_snow_rate": ratio(len(mountains)-len(no_snow_mountains), len(mountains)),
            "unique_12_motif_profiles": len(profiles),
            "all_zero_profiles": profiles.get(tuple([0]*len(LABELS)), 0),
        },
        "guest": {
            "n": len(guest), "with_trees": sum(map(tree, guest)),
            "tree_rate": ratio(sum(map(tree, guest)), len(guest)),
        },
        "motif_counts_host": motif_counts,
        "by_season_host": by_season,
        "counterexamples": {
            "host_without_trees": [r["id"] for r in no_trees[:12]],
            "host_mountain_without_snow": [r["id"] for r in no_snow_mountains[:12]],
        },
        "museum_scenario": {
            "status": "hipotético, sin costes ni ingresos observados",
            "algorithm": "Reglas explícitas en orden: mar/cascadas, montañas, árboles, otros",
            "room_sizes": {name: allocation[name] for name in
                           ("Agua y costa", "Montañas", "Bosques", "Otros paisajes")},
            "interpretation": "Balance operativo descriptivo, no rentabilidad ni clustering",
        },
        "quality": {
            "inferences_forbidden": [
                "calidad artística", "popularidad", "recaudación",
                "número real de árboles", "discriminación causal", "estilos naturales",
            ],
            "warning": "Las etiquetas humanas no son imágenes ni preferencias de audiencia.",
        },
    }
    return result, host


def svg_bar(result):
    counts = result["motif_counts_host"]
    values = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    max_val = max(counts.values())
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 615" role="img" aria-labelledby="t d">',
        '<title id="t">Frecuencia de doce familias de motivos entre 381 episodios del anfitrión</title>',
        '<desc id="d">Barras horizontales en orden decreciente con conteo y porcentaje por episodio; categorías no excluyentes.</desc>',
        '<rect width="960" height="615" fill="#0e1926"/>',
        '<text x="35" y="50" fill="#f8f4e8" font-size="27" font-family="sans-serif" font-weight="700">¿Qué aparece en los cuadros?</text>',
        '<text x="35" y="78" fill="#acc0cf" font-size="15" font-family="sans-serif">Motivos codificados · anfitrión · n=381</text>',
    ]
    for i, (name, val) in enumerate(values):
        y = 110 + i * 39
        width = int(655 * val/max_val)
        parts.extend([
            f'<text x="34" y="{y+20}" fill="#dfebee" font-size="17" font-family="sans-serif">{html.escape(name.title())}</text>',
            f'<rect x="178" y="{y+2}" width="655" height="25" rx="6" fill="#243544"/>',
            f'<rect x="178" y="{y+2}" width="{width}" height="25" rx="6" fill="{PALETTE[i%len(PALETTE)]}"/>',
            f'<text x="853" y="{y+21}" fill="#f6f1e5" font-size="16" font-family="sans-serif">{val} ({val/381:.0%})</text>'
        ])
    parts.append('<text x="35" y="593" fill="#acc0cf" font-family="sans-serif" font-size="13">FiveThirtyEight · presencia registrada, no cantidad de elementos; las barras pueden superponerse</text></svg>')
    return "\n".join(parts)


def svg_seasons(result):
    seasons = result["by_season_host"]
    left, right = 65, 923
    sx = (right-left)/(len(seasons)-1)
    def points(key):
        return " ".join(f"{left+i*sx:.2f},{382-260*(s[key]/s['n']):.2f}" for i,s in enumerate(seasons))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 480" role="img" aria-labelledby="t d">
<title id="t">Árboles y montañas por temporada</title><desc id="d">Proporción de episodios con etiquetas de árboles y montañas según temporada, excluyendo invitados.</desc>
<rect width="960" height="480" fill="#0e1926"/>
<text x="35" y="52" fill="#f8f4e8" font-size="27" font-family="sans-serif" font-weight="700">¿El paisaje cambia con las temporadas?</text>
<text x="35" y="80" fill="#acc0cf" font-size="15" font-family="sans-serif">Porcentaje de episodios del anfitrión por temporada; tamaños por temporada no siempre iguales</text>
<line x1="65" y1="382" x2="923" y2="382" stroke="#6e8495"/><line x1="65" y1="252" x2="923" y2="252" stroke="#314657"/><line x1="65" y1="122" x2="923" y2="122" stroke="#314657"/>
<text x="22" y="386" fill="#acc0cf" font-size="13" font-family="sans-serif">0%</text><text x="13" y="256" fill="#acc0cf" font-size="13" font-family="sans-serif">50%</text><text x="6" y="126" fill="#acc0cf" font-size="13" font-family="sans-serif">100%</text>
<polyline fill="none" stroke="#74c7ac" stroke-width="4" stroke-linejoin="round" points="{points('trees')}"/>
<polyline fill="none" stroke="#ebb17d" stroke-width="4" stroke-linejoin="round" points="{points('mountains')}"/>
<text x="80" y="435" fill="#acc0cf" font-size="14" font-family="sans-serif">Temporada 1</text><text x="817" y="435" fill="#acc0cf" font-size="14" font-family="sans-serif">Temporada 31</text>
<circle cx="665" cy="80" r="7" fill="#74c7ac"/><text x="679" y="86" fill="#f8f4e8" font-size="16" font-family="sans-serif">Árboles</text>
<circle cx="788" cy="80" r="7" fill="#ebb17d"/><text x="802" y="86" fill="#f8f4e8" font-size="16" font-family="sans-serif">Montañas</text>
</svg>'''


def svg_compare(result):
    host, guest = result["host"], result["guest"]
    n_mount = host["mountains"]
    yes = n_mount - host["mountains_without_snow"]
    groups = [
        ("Árboles: anfitrión", host["with_trees"], host["n"], PALETTE[1]),
        ("Árboles: invitados", guest["with_trees"], guest["n"], PALETTE[0]),
        ("Nieve entre episodios con montañas", yes, n_mount, PALETTE[2]),
    ]
    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 430" role="img" aria-labelledby="t d">',
        '<title id="t">Tres proporciones y sus denominadores</title>',
        '<desc id="d">Porcentaje con árboles entre episodios de anfitrión e invitados, y porcentaje con nieve entre los de montañas del anfitrión.</desc>',
        '<rect width="960" height="430" fill="#0e1926"/>',
        '<text x="35" y="52" fill="#f8f4e8" font-size="27" font-family="sans-serif" font-weight="700">Una afirmación, tres denominadores</text>'
    ]
    for i, (label, value, n, color) in enumerate(groups):
        y = 115+i*96
        w = int(750 * (value/n)) if n else 0
        out.extend([
            f'<text x="35" y="{y}" fill="#f2f3e9" font-family="sans-serif" font-size="17">{html.escape(label)}</text>',
            f'<rect x="35" y="{y+14}" width="750" height="30" rx="8" fill="#243544"/>',
            f'<rect x="35" y="{y+14}" width="{w}" height="30" rx="8" fill="{color}"/>',
            f'<text x="802" y="{y+37}" fill="#f8f4e8" font-family="sans-serif" font-size="17">{value}/{n} ({value/n:.1%})</text>'
        ])
    out.append('<text x="35" y="408" fill="#acc0cf" font-family="sans-serif" font-size="13">Descriptivo; invitados n=22. No inferir intención, preferencias ni causalidad.</text></svg>')
    return "\n".join(out)


def write_outputs(rows, result):
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT/"results.json").write_text(json.dumps(result, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    with (OUTPUT/"silver_motifs.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["episode", "season", "guest", *LABELS])
        for r in rows:
            writer.writerow([r["id"],r["season"],r["guest"],*[r["motifs"][k] for k in LABELS]])
    (OUTPUT/"01-motivos.svg").write_text(svg_bar(result), encoding="utf-8")
    (OUTPUT/"02-temporadas.svg").write_text(svg_seasons(result), encoding="utf-8")
    (OUTPUT/"03-denominadores.svg").write_text(svg_compare(result), encoding="utf-8")
    return len(list(OUTPUT.glob("*")))


def checks(result):
    assert result["metadata"]["rows"] == 403
    assert result["metadata"]["binary_labels"] == 67
    assert result["host"]["n"] == 381 and result["guest"]["n"] == 22
    assert result["host"]["without_trees"] == 36
    assert result["host"]["mountains"] == 150
    assert result["host"]["mountains_without_snow"] == 48
    assert sum(result["museum_scenario"]["room_sizes"].values()) == 381
    assert len(result["by_season_host"]) == 31
    assert all(x["trees"]<=x["n"] and x["mountains"]<=x["n"]
               for x in result["by_season_host"])
    assert result["cleaning"]["duplicate_episode_ids"] == 0
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validar y comprobar resultados sin escribir archivos")
    parser.add_argument("--write", action="store_true", help="Generar resultados, silver y tres SVG dentro de output/")
    args = parser.parse_args()
    rows, digest = load()
    result, _ = study(rows, digest)
    checks(result)
    if args.write:
        write_outputs(rows, result)
    print(json.dumps({
        "PASS": True, "source_sha256": digest, "episodes": len(rows),
        "host": result["host"], "guest": result["guest"],
        "outputs": str(OUTPUT) if args.write else "sin escrituras",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
