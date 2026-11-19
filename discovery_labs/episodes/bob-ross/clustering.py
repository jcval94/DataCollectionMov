#!/usr/bin/env python3
"""Exploratory four-room clustering of human-coded Bob Ross motifs.

Pure Python; intentionally compare Jaccard and Euclidean for binary features.
Four rooms is a *fictional museum constraint*, never a proven taxonomy of art.
"""
from __future__ import annotations
import argparse
import json
import math
from collections import Counter
from pathlib import Path
from run import FEATURES, OUTPUT, ROOT, load, study

K = 4
NAMES = list(FEATURES)


def distance(a, b, metric="jaccard"):
    if metric == "jaccard":
        union = sum(bool(x or y) for x, y in zip(a, b))
        return 1 - sum(bool(x and y) for x, y in zip(a, b))/union if union else 0.0
    if metric == "euclidean":
        return math.sqrt(sum((x-y)**2 for x, y in zip(a, b)))
    raise ValueError(f"Distancia no soportada: {metric}")


def matrix(points, metric):
    return [[distance(a, b, metric) for b in points] for a in points]


def medoids(dist, k=K, max_iter=40):
    n = len(dist)
    if k < 2 or k >= n or any(len(row) != n for row in dist):
        raise ValueError("Matriz de distancias o k inválidos.")
    centers = [min(range(n), key=lambda i: (sum(dist[i]), i))]
    while len(centers) < k:
        choices = [i for i in range(n) if i not in centers]
        centers.append(max(choices, key=lambda i: (min(dist[i][c] for c in centers), -i)))
    for _ in range(max_iter):
        labels = [min(range(k), key=lambda g: (dist[i][centers[g]], g)) for i in range(n)]
        revised = []
        for group in range(k):
            members = [i for i, label in enumerate(labels) if label == group]
            if not members:
                taken = centers + revised
                pick = max((i for i in range(n) if i not in taken),
                           key=lambda i: (min(dist[i][c] for c in taken), -i))
            else:
                pick = min(members, key=lambda i: (sum(dist[i][j] for j in members), i))
            revised.append(pick)
        if revised == centers:
            break
        centers = revised
    labels = [min(range(k), key=lambda g: (dist[i][centers[g]], g)) for i in range(n)]
    order = sorted(range(k), key=lambda g: (-labels.count(g), centers[g]))
    remap = {group: idx for idx, group in enumerate(order)}
    labels = [remap[g] for g in labels]
    centers = [centers[g] for g in order]
    return labels, centers


def silhouette(dist, labels):
    buckets = {g: [i for i, label in enumerate(labels) if label == g]
               for g in set(labels)}
    scores = []
    for i, group in enumerate(labels):
        own = buckets[group]
        if len(own) <= 1:
            scores.append(0.0)
            continue
        a = sum(dist[i][j] for j in own if j != i) / (len(own)-1)
        b = min(sum(dist[i][j] for j in members)/len(members)
                for other, members in buckets.items() if other != group and members)
        scores.append((b-a)/max(a,b) if max(a,b) else 0.0)
    return sum(scores)/len(scores)


def ari(a, b):
    if len(a) != len(b):
        raise ValueError("ARI requiere los mismos episodios.")
    n = len(a)
    choose2 = lambda x: x*(x-1)//2
    contingency = Counter(zip(a,b))
    aa, bb = Counter(a), Counter(b)
    index = sum(choose2(x) for x in contingency.values())
    sa = sum(choose2(x) for x in aa.values())
    sb = sum(choose2(x) for x in bb.values())
    expected = sa*sb/choose2(n) if n > 1 else 0
    maximum = (sa+sb)/2
    return (index-expected)/(maximum-expected) if maximum != expected else 1.0


def analyse():
    rows, source_hash = load()
    _, host = study(rows, source_hash)
    points = [tuple(r["motifs"][key] for key in NAMES) for r in host]
    dj = matrix(points, "jaccard")
    de = matrix(points, "euclidean")
    lj, cj = medoids(dj)
    le, ce = medoids(de)
    # For this same host population, compare partitions; not artistic truth.
    by_group = []
    for g, center in enumerate(cj):
        members = [i for i, label in enumerate(lj) if label == g]
        by_group.append({
            "room": g+1, "n": len(members),
            "representative": {"episode": host[center]["id"], "title": host[center]["title"]},
            "motif_rates": {name: round(sum(points[i][j] for i in members)/len(members),4)
                            for j,name in enumerate(NAMES)},
        })
    no_trees_points = [point[1:] for point in points]
    no_trees_dist = matrix(no_trees_points, "jaccard")
    without_trees, _ = medoids(no_trees_dist)
    return {
        "source_sha256": source_hash, "n": len(host), "features": NAMES, "k": K,
        "why_k": "Cuatro salas de museo ficticias; no cuatro estilos reales.",
        "algorithm": "k-medoids desde centros por cobertura con refinamiento determinista",
        "primary_distance": "jaccard binaria", "secondary_distance": "euclidean binaria",
        "jaccard": {"sizes": [lj.count(g) for g in range(K)],
                    "silhouette_in_jaccard_space": round(silhouette(dj, lj),5)},
        "euclidean": {"sizes": [le.count(g) for g in range(K)],
                      "silhouette_in_euclidean_space": round(silhouette(de, le),5)},
        "adjusted_rand_between_partitions": round(ari(lj,le),5),
        "adjusted_rand_without_tree_feature": round(ari(lj,without_trees),5),
        "rooms": by_group,
        "warning": "Silhouette de métricas distintas no es una escala común. ARI es acuerdo, no exactitud.",
    }


def svg_rooms(report):
    colors = ["#d45b37","#467f86","#dbac64","#826ba7"]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 550" role="img" aria-labelledby="t d">',
        '<title id="t">Cuatro salas según k-medoids y distancia de Jaccard</title>',
        '<desc id="d">Tamaños de salas y frecuencia de doce motivos. Los grupos son exploratorios, no estilos artísticos validados.</desc>',
        '<rect width="960" height="550" fill="#0e1926"/>',
        '<text x="35" y="52" fill="#f8f4e8" font-size="27" font-family="sans-serif" font-weight="700">¿Hay cuatro estilos de Bob Ross?</text>',
        '<text x="35" y="80" fill="#acc0cf" font-size="15" font-family="sans-serif">Cuatro salas impuestas · k-medoids con Jaccard · 381 episodios</text>'
    ]
    for i, r in enumerate(report["rooms"]):
        y = 125 + i * 99
        sz = r["n"]
        width = max(3,int(sz*2))
        parts.extend([
            f'<text x="35" y="{y}" fill="#f8f4e8" font-family="sans-serif" font-size="19">Sala {i+1}: {sz} episodios</text>',
            f'<rect x="35" y="{y+12}" width="810" height="25" rx="6" fill="#263748"/>',
            f'<rect x="35" y="{y+12}" width="{min(width,810)}" height="25" rx="6" fill="{colors[i]}"/>',
            f'<text x="35" y="{y+62}" fill="#acc0cf" font-family="sans-serif" font-size="15">Representante real: {r["representative"]["episode"]}</text>'
        ])
    parts.append('<text x="35" y="525" fill="#acc0cf" font-family="sans-serif" font-size="13">Las distancias y reglas de agrupación alteran el resultado. La calidad del arte no se midió.</text></svg>')
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    result = analyse()
    assert sum(result["jaccard"]["sizes"]) == 381
    assert sum(result["euclidean"]["sizes"]) == 381
    if args.write:
        OUTPUT.mkdir(parents=True, exist_ok=True)
        (OUTPUT/"clusters.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        (OUTPUT/"04-salas.svg").write_text(svg_rooms(result), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
