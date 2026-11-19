"""Bounded, offline Bob Ross analysis. Never executes arbitrary user Python."""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from time import perf_counter

ROOT = Path(__file__).resolve().parents[2]
CASE = ROOT / "examples" / "bob_ross_clustering"
RAW = CASE / "data" / "elements-by-episode.csv"
MANIFEST = CASE / "data" / "manifest.json"
REFERENCE = CASE / "reference" / "report.json"
DATA_MAX_BYTES = 1_048_576
ASSET_BASE = (
    "https://github.com/jcval94/DataCollectionMov/blob/main/"
    "examples/bob_ross_clustering"
)


def _inputs():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    raw = RAW.read_bytes()
    if len(raw) > DATA_MAX_BYTES or len(raw) != manifest["bytes"]:
        raise ValueError("Dataset missing or size differs from pinned manifest.")
    digest = hashlib.sha256(raw).hexdigest()
    if digest != manifest["sha256"]:
        raise ValueError("Pinned Bob Ross dataset SHA-256 mismatch.")
    return manifest


def _reference():
    _inputs()
    report = json.loads(REFERENCE.read_text(encoding="utf-8"))
    if report["source_sha256"] != json.loads(MANIFEST.read_text())["sha256"]:
        raise ValueError("Reference and data hashes disagree.")
    return report


def dataset_overview():
    """Read the pinned dataset contract and population without network requests."""
    manifest = _inputs()
    report = _reference()
    return {
        "dataset": "Bob Ross, elements-by-episode",
        "source": manifest["source_url"],
        "license": manifest["license"],
        "sha256": manifest["sha256"],
        "raw_episodes": report["population"]["raw_episodes"],
        "non_guest_episodes": report["population"]["included_episodes"],
        "excluded_guest": report["population"]["excluded_guest"],
        "feature_families": list(report["feature_mapping"]),
        "scope": "Human-coded painting elements; not pixels, aesthetic quality, or popularity.",
        "provenance_verified": True,
    }


def reference_summary():
    """Return the committed and verified K-Means classroom reference; no retraining."""
    result = _reference()
    return {
        "status": "committed_reference_not_live_comparison",
        "source_sha256": result["source_sha256"],
        "population": result["population"],
        "model": result["model"],
        "silhouette_euclidean": result["diagnostics"]["silhouette_k4"],
        "rooms": [
            {"room": r["room"], "size": r["size"],
             "top_motifs": sorted(r["frequencies"], key=r["frequencies"].get, reverse=True)[:4],
             "representative": r["medoid"]}
            for r in result["rooms"]
        ],
        "sensitivity": result["sensitivity"],
        "warning": result["interpretation"],
    }


def compare_models(k: int = 4, exclude_guests: bool = True):
    """Actually fit three predefined clustering approaches on the same pinned data.

    Uses the same twelve binary motifs, population, k and Euclidean silhouette.
    No user-provided paths, executable code, arbitrary URLs or hyperparameter grids.
    """
    if type(k) is not int or not 2 <= k <= 6:
        raise ValueError("k must be an integer between 2 and 6.")
    if type(exclude_guests) is not bool:
        raise ValueError("exclude_guests must be a boolean.")
    manifest = _inputs()

    import sys
    import numpy as np
    from sklearn.cluster import AgglomerativeClustering, KMeans
    from sklearn.metrics import silhouette_score
    from threadpoolctl import threadpool_limits

    # Existing audited transformation contract is the single source of truth.
    if str(CASE) not in sys.path:
        sys.path.insert(0, str(CASE))
    import run as reference_case

    raw = reference_case.load_data()
    rows, X = reference_case.prepare(raw, exclude_guests=exclude_guests)
    values = X.to_numpy(dtype=np.float64)
    candidates = (
        ("kmeans_euclidean", KMeans(n_clusters=k, random_state=42, n_init=50, algorithm="lloyd")),
        ("agglomerative_ward", AgglomerativeClustering(n_clusters=k, linkage="ward", metric="euclidean")),
        ("agglomerative_average_hamming", AgglomerativeClustering(n_clusters=k, linkage="average", metric="hamming")),
    )
    min_size = max(10, math.ceil(len(rows) * 0.05))
    measurements = []
    with threadpool_limits(limits=1):
        for name, model in candidates:
            start = perf_counter()
            labels = model.fit_predict(values)
            elapsed = round(perf_counter() - start, 4)
            sizes = np.bincount(labels, minlength=k).tolist()
            centroids = np.vstack([values[labels == group].mean(axis=0) for group in range(k)])
            within_ss = float(np.square(values - centroids[labels]).sum())
            score = float(silhouette_score(values, labels, metric="euclidean"))
            measurements.append({
                "algorithm": name,
                "silhouette_euclidean": round(score, 6),
                "within_cluster_ss": round(within_ss, 5),
                "group_sizes": sizes,
                "smallest_group": min(sizes),
                "eligible": min(sizes) >= min_size,
                "fit_seconds_observed": elapsed,
            })
    eligible = sorted(
        (m for m in measurements if m["eligible"]),
        key=lambda item: (-item["silhouette_euclidean"], -item["smallest_group"], item["algorithm"]),
    )
    winner = eligible[0]["algorithm"] if eligible else None
    return {
        "execution": "live_cpu_comparison",
        "source_sha256": manifest["sha256"],
        "episodes": len(rows),
        "exclude_guests": exclude_guests,
        "k": k,
        "motif_features": list(X.columns),
        "common_evaluation": "Euclidean silhouette on the same twelve binary motif families",
        "minimum_acceptable_group_size": min_size,
        "results": measurements,
        "preferred_by_predeclared_rule": winner,
        "decision_rule": "Highest common-space silhouette among methods with every group >= 5% of episodes (minimum 10).",
        "interpretation": (
            "Exploratory model choice, not proven true clusters. The four-room constraint is educational. "
            "Silhouette is an internal, in-sample clustering metric, not predictive accuracy or causal evidence. "
            "Hamming clustering is scored in the same Euclidean space only for comparability. "
            "Review interpretability, stability and human-labeled examples before adopting any grouping."
        ),
        "assets": visualization_links(),
    }


def visualization_links():
    """Existing source-backed charts; links do not imply newly generated figures."""
    _inputs()
    return {
        "room_profiles": f"{ASSET_BASE}/reference/profiles.svg",
        "k_diagnostics": f"{ASSET_BASE}/reference/k_diagnostics.svg",
        "metadata_leakage_trap": f"{ASSET_BASE}/reference/metadata_trap.svg",
        "interactive_classroom_demo": f"{ASSET_BASE}/demo.html",
        "teacher_guide": f"{ASSET_BASE}/DOCENTE.md",
    }


def storyboard():
    """Six evidence-based story beats suitable for a short classroom video."""
    result = _reference()
    sizes = [r["size"] for r in result["rooms"]]
    return {
        "title": "¿Puede una IA organizar el universo de Bob Ross?",
        "scenes": [
            {"scene": 1, "beat": "Hook: un museo tiene solo cuatro salas, ¿cómo clasificar 403 episodios?"},
            {"scene": 2, "beat": "Dataset: etiquetas binarias de elementos pintados; 22 episodios invitados excluidos."},
            {"scene": 3, "beat": f"Primera propuesta: K-Means divide 381 episodios en {sizes}."},
            {"scene": 4, "beat": "La trampa: añadir el orden de episodio como variable puede dar grupos nítidos pero irrelevantes."},
            {"scene": 5, "beat": "Contrasta alternativas con una métrica común y revisa tamaños, estabilidad e interpretación."},
            {"scene": 6, "beat": "Cierre: un puntaje alto no decide por nosotros; importa la pregunta y la evidencia."},
        ],
        "rules": [
            "Do not attribute artistic intent or causality.",
            "Do not label the historical K-Means result as the winner of an unexecuted comparison.",
            "Use licensed data charts; do not redistribute copyrighted paintings.",
        ],
    }
