from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
APPSCRIPT_DIR = ROOT / "appscript"

POLICE_TYPES = {
    "Amenazas",
    "Daño a la propiedad",
    "Delitos sexuales",
    "Fraude y extorsión",
    "Homicidio",
    "Lesiones",
    "Narcomenudeo",
    "Otros incidentes",
    "Otros robos",
    "Robo a casa habitación",
    "Robo a negocio",
    "Robo a transeúnte",
    "Robo de vehículo",
    "Robo en transporte",
    "Secuestro",
    "Violencia familiar",
}


def main() -> int:
    APPSCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    routes = pd.read_csv(DATA_DIR / "routes_google_gallery_summary.csv", dtype={"codigo_postal": str})
    fire = pd.read_csv(DATA_DIR / "routes_bomberos_summary.csv", dtype={"codigo_postal": str})
    centroids = pd.read_csv(DATA_DIR / "centroids_df.csv", dtype={"codigo_postal": str, "d_codigo": str})

    app_data = {
        "generatedAtUtc": pd.Timestamp.utcnow().replace(microsecond=0).isoformat(),
        "scenarios": {
            "fire": compact_routes(fire),
            "health": compact_routes(routes[routes["resolver_category"] == "hospital"]),
            "security": compact_routes(routes[routes["resolver_category"] == "police"]),
        },
        "securityCpOptions": security_cp_options(centroids),
    }
    security_centroids = compact_security_centroids_by_cp(centroids)

    data_gs = (
        "// Auto-generado por scripts/build_appscript_data.py. No editar a mano.\n"
        f"const APP_DATA = {json.dumps(app_data, ensure_ascii=False, separators=(',', ':'))};\n"
        f"const SECURITY_CENTROIDS_BY_CP = {json.dumps(security_centroids, ensure_ascii=False, separators=(',', ':'))};\n"
    )
    (APPSCRIPT_DIR / "Data.gs").write_text(data_gs, encoding="utf-8")

    return 0


def compact_routes(df: pd.DataFrame) -> list[dict[str, Any]]:
    rows = []
    sort_cols = [col for col in ["n_events", "duration_minutes"] if col in df.columns]
    df = df.sort_values(sort_cols, ascending=[False, True][: len(sort_cols)]) if sort_cols else df
    for _, row in df.iterrows():
        rows.append(
            {
                "id": str(row["incident_key"]),
                "cp": str(row["codigo_postal"]),
                "type": str(row["crime_type"]),
                "events": int(row["n_events"]),
                "unit": str(row["resolver_name"]),
                "category": str(row["resolver_category"]),
                "origin": [round_float(row["resolver_lat"]), round_float(row["resolver_lon"])],
                "destination": [round_float(row["centroid_lat"]), round_float(row["centroid_lon"])],
                "distanceKm": round_float(float(row["distance_meters"]) / 1000, 3),
                "durationMin": round_float(float(row["duration_minutes"]), 2),
                "encodedPolyline": None if pd.isna(row.get("encoded_polyline")) else str(row["encoded_polyline"]),
            }
        )
    return rows


def security_cp_options(centroids: pd.DataFrame) -> list[dict[str, Any]]:
    security = normalize_centroids(centroids)
    grouped = (
        security.groupby("codigo_postal")
        .agg(centroids=("centroid_id", "count"), events=("n_events", "sum"))
        .reset_index()
        .sort_values(["events", "centroids", "codigo_postal"], ascending=[False, False, True])
    )
    return [
        {"cp": str(row.codigo_postal), "centroids": int(row.centroids), "events": int(row.events)}
        for row in grouped.itertuples(index=False)
    ]


def compact_security_centroids_by_cp(centroids: pd.DataFrame) -> dict[str, list[dict[str, Any]]]:
    security = normalize_centroids(centroids)
    by_cp: dict[str, list[dict[str, Any]]] = {}
    for cp, group in security.groupby("codigo_postal"):
        ordered = group.sort_values(["n_events", "crime_type", "centroid_id"], ascending=[False, True, True])
        by_cp[str(cp)] = [
            {
                "id": int(row.centroid_id),
                "type": str(row.crime_type),
                "lat": round_float(row.centroid_lat),
                "lng": round_float(row.centroid_lon),
                "events": int(row.n_events),
            }
            for row in ordered.itertuples(index=False)
        ]
    return by_cp


def normalize_centroids(centroids: pd.DataFrame) -> pd.DataFrame:
    df = centroids.copy()
    df["crime_type"] = df["crime_type"].astype(str)
    df = df[df["crime_type"].isin(POLICE_TYPES)]
    df["centroid_lat"] = pd.to_numeric(df["centroid_lat"], errors="coerce")
    df["centroid_lon"] = pd.to_numeric(df["centroid_lon"], errors="coerce")
    df["n_events"] = pd.to_numeric(df["n_events"], errors="coerce").fillna(0).astype(int)
    df["centroid_id"] = pd.to_numeric(df["centroid_id"], errors="coerce").fillna(0).astype(int)
    df = df.dropna(subset=["centroid_lat", "centroid_lon", "codigo_postal"])
    return df[["codigo_postal", "crime_type", "centroid_id", "centroid_lat", "centroid_lon", "n_events"]]


def round_float(value: Any, digits: int = 6) -> float:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return 0.0
    return round(float(value), digits)


if __name__ == "__main__":
    raise SystemExit(main())
