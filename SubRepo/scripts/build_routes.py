from __future__ import annotations

import argparse
import html
import json
import math
import os
import re
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import requests

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover - optional local convenience
    load_dotenv = None


GOOGLE_ROUTES_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"
OVERPASS_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]
SUBREPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CENTROIDS = SUBREPO_ROOT / "data" / "centroids_df.csv"
DEFAULT_OUTPUT_DIR = SUBREPO_ROOT / "dist" / "routes"

CRIME_RESPONSE_RULES = {
    "Amenazas": ["police"],
    "Daño a la propiedad": ["fire_station", "police"],
    "Delitos sexuales": ["police", "hospital"],
    "Fraude y extorsión": ["police"],
    "Homicidio": ["police", "hospital"],
    "Lesiones": ["hospital", "police"],
    "Narcomenudeo": ["police"],
    "Otros incidentes": ["police", "fire_station", "hospital"],
    "Otros robos": ["police"],
    "Robo a casa habitación": ["police"],
    "Robo a negocio": ["police"],
    "Robo a transeúnte": ["police"],
    "Robo de vehículo": ["police"],
    "Robo en transporte": ["police"],
    "Secuestro": ["police"],
    "Violencia familiar": ["police", "hospital"],
}

CATEGORY_LABELS = {
    "police": "Seguridad / vigilancia",
    "fire_station": "Bomberos / proteccion civil",
    "hospital": "Salud / emergencia medica",
}

ROUTE_COLORS = {
    "police": "#2563eb",
    "fire_station": "#dc2626",
    "hospital": "#059669",
    "mixed": "#7c3aed",
}

FALLBACK_UNITS = [
    {"unit_id": "fallback_police_centro", "name": "Base de seguridad Centro", "category": "police", "lat": 19.4326, "lon": -99.1332},
    {"unit_id": "fallback_police_norte", "name": "Base de seguridad Norte", "category": "police", "lat": 19.5008, "lon": -99.1466},
    {"unit_id": "fallback_police_sur", "name": "Base de seguridad Sur", "category": "police", "lat": 19.3048, "lon": -99.1030},
    {"unit_id": "fallback_police_poniente", "name": "Base de seguridad Poniente", "category": "police", "lat": 19.3677, "lon": -99.2634},
    {"unit_id": "fallback_fire_centro", "name": "Base de bomberos Centro", "category": "fire_station", "lat": 19.4270, "lon": -99.1450},
    {"unit_id": "fallback_fire_oriente", "name": "Base de bomberos Oriente", "category": "fire_station", "lat": 19.3605, "lon": -99.0738},
    {"unit_id": "fallback_fire_sur", "name": "Base de bomberos Sur", "category": "fire_station", "lat": 19.2839, "lon": -99.1353},
    {"unit_id": "fallback_hospital_centro", "name": "Base medica Centro", "category": "hospital", "lat": 19.4137, "lon": -99.1520},
    {"unit_id": "fallback_hospital_norte", "name": "Base medica Norte", "category": "hospital", "lat": 19.4895, "lon": -99.1170},
    {"unit_id": "fallback_hospital_sur", "name": "Base medica Sur", "category": "hospital", "lat": 19.3180, "lon": -99.1740},
]


def main() -> int:
    if load_dotenv:
        load_dotenv()

    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    centroids = load_centroids(Path(args.centroids_csv), args.max_centroids_per_type)
    units = load_response_units(centroids, Path(args.units_csv) if args.units_csv else None)
    routes = build_routes(
        centroids=centroids,
        units=units,
        google_key=os.getenv("MAPS", os.getenv("GOOGLE_MAPS_API_KEY", "")).strip(),
        max_google_routes=args.max_google_routes,
        candidate_units=args.candidate_units,
        sleep_seconds=args.google_sleep_seconds,
    )

    write_outputs(output_dir, routes, units)
    build_maps(output_dir, routes, units)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genera GeoJSON/JSON y mapas Folium con rutas desde unidades de respuesta hacia centroides de incidentes."
    )
    parser.add_argument("--centroids-csv", default=str(DEFAULT_CENTROIDS), help="CSV con centroides por CP y tipo de delito.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Carpeta destino de JSONs e HTMLs.")
    parser.add_argument("--units-csv", default=None, help="CSV opcional de unidades resolutoras con columnas name, category, lat, lon.")
    parser.add_argument(
        "--max-google-routes",
        type=int,
        default=250,
        help="Maximo de llamadas a Google Routes. Use -1 para intentar todas; 0 fuerza fallback sin llamadas.",
    )
    parser.add_argument("--candidate-units", type=int, default=3, help="Candidatas cercanas evaluadas por centroide.")
    parser.add_argument("--google-sleep-seconds", type=float, default=0.05, help="Pausa entre llamadas Google para cuidar cuota.")
    parser.add_argument("--max-centroids-per-type", type=int, default=None, help="Muestreo opcional por tipo para pruebas rapidas.")
    return parser.parse_args()


def load_centroids(path: Path, max_per_type: int | None) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"No existe el CSV de centroides: {path}")
    df = pd.read_csv(path, dtype={"codigo_postal": str, "d_codigo": str})
    required = {"codigo_postal", "crime_type", "centroid_id", "centroid_lat", "centroid_lon", "n_events"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Faltan columnas requeridas en centroides: {missing}")
    df = df.copy()
    df["centroid_lat"] = pd.to_numeric(df["centroid_lat"], errors="coerce")
    df["centroid_lon"] = pd.to_numeric(df["centroid_lon"], errors="coerce")
    df["n_events"] = pd.to_numeric(df["n_events"], errors="coerce").fillna(0).astype(int)
    df = df.dropna(subset=["centroid_lat", "centroid_lon", "crime_type"])
    df = df[(df["centroid_lat"].between(18.8, 20.0)) & (df["centroid_lon"].between(-100.0, -98.5))]
    df["incident_key"] = df.apply(
        lambda row: f"{row['codigo_postal']}_{slugify(row['crime_type'])}_{int(row['centroid_id'])}",
        axis=1,
    )
    if max_per_type:
        df = (
            df.sort_values(["crime_type", "n_events"], ascending=[True, False])
            .groupby("crime_type", as_index=False, group_keys=False)
            .head(max_per_type)
            .reset_index(drop=True)
        )
    return df.reset_index(drop=True)


def load_response_units(centroids: pd.DataFrame, units_csv: Path | None) -> pd.DataFrame:
    if units_csv and units_csv.exists():
        units = pd.read_csv(units_csv)
    else:
        units = fetch_osm_response_units(centroids)
        if units.empty:
            units = pd.DataFrame(FALLBACK_UNITS)
            units["source"] = "fallback_seed"
        else:
            units["source"] = "openstreetmap_overpass"
    for col in ["name", "category", "lat", "lon"]:
        if col not in units.columns:
            raise ValueError(f"El catalogo de unidades no tiene columna requerida: {col}")
    units = units.copy()
    units["lat"] = pd.to_numeric(units["lat"], errors="coerce")
    units["lon"] = pd.to_numeric(units["lon"], errors="coerce")
    units = units.dropna(subset=["lat", "lon", "category"])
    units = units[units["category"].isin(CATEGORY_LABELS)]
    if "unit_id" not in units.columns:
        units["unit_id"] = [f"unit_{i:05d}" for i in range(len(units))]
    units["category_label"] = units["category"].map(CATEGORY_LABELS)
    return units.drop_duplicates(subset=["unit_id"]).reset_index(drop=True)


def fetch_osm_response_units(centroids: pd.DataFrame) -> pd.DataFrame:
    min_lat = max(float(centroids["centroid_lat"].min()) - 0.06, 18.8)
    max_lat = min(float(centroids["centroid_lat"].max()) + 0.06, 20.0)
    min_lon = max(float(centroids["centroid_lon"].min()) - 0.06, -100.0)
    max_lon = min(float(centroids["centroid_lon"].max()) + 0.06, -98.5)
    query = f"""[out:json][timeout:35];
(
  node["amenity"="police"]({min_lat},{min_lon},{max_lat},{max_lon});
  way["amenity"="police"]({min_lat},{min_lon},{max_lat},{max_lon});
  node["amenity"="fire_station"]({min_lat},{min_lon},{max_lat},{max_lon});
  way["amenity"="fire_station"]({min_lat},{min_lon},{max_lat},{max_lon});
  node["amenity"="hospital"]({min_lat},{min_lon},{max_lat},{max_lon});
  way["amenity"="hospital"]({min_lat},{min_lon},{max_lat},{max_lon});
);
out center tags 500;"""
    data = None
    last_error: Exception | None = None
    for url in OVERPASS_URLS:
        try:
            response = requests.post(
                url,
                data=query.encode("utf-8"),
                headers={"Content-Type": "text/plain", "User-Agent": "DataCollectionMov incident-response-routes"},
                timeout=75,
            )
            response.raise_for_status()
            data = response.json()
            break
        except Exception as exc:
            last_error = exc
    if data is None:
        print(f"WARNING: no se pudo consultar Overpass; se usara fallback. Detalle: {last_error}")
        return pd.DataFrame()

    rows = []
    for element in data.get("elements", []):
        tags = element.get("tags", {})
        category = tags.get("amenity")
        lat = element.get("lat") or element.get("center", {}).get("lat")
        lon = element.get("lon") or element.get("center", {}).get("lon")
        if not lat or not lon or category not in CATEGORY_LABELS:
            continue
        rows.append(
            {
                "unit_id": f"osm_{element.get('type')}_{element.get('id')}",
                "name": tags.get("name") or CATEGORY_LABELS[category],
                "category": category,
                "lat": lat,
                "lon": lon,
                "operator": tags.get("operator"),
                "osm_type": element.get("type"),
                "osm_id": element.get("id"),
            }
        )
    return pd.DataFrame(rows)


def build_routes(
    centroids: pd.DataFrame,
    units: pd.DataFrame,
    google_key: str,
    max_google_routes: int,
    candidate_units: int,
    sleep_seconds: float,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    google_calls = 0
    google_available = bool(google_key) and max_google_routes != 0
    route_cache: dict[str, dict[str, Any]] = {}

    for idx, centroid in centroids.iterrows():
        allowed_categories = CRIME_RESPONSE_RULES.get(str(centroid["crime_type"]), ["police", "fire_station", "hospital"])
        candidates = nearest_units(centroid, units, allowed_categories, max(candidate_units, 1))
        best_row: dict[str, Any] | None = None

        for candidate in candidates:
            can_call_google = google_available and (max_google_routes < 0 or google_calls < max_google_routes)
            route = None
            if can_call_google:
                route = compute_google_route(centroid, candidate, google_key, route_cache)
                google_calls += 1
                time.sleep(max(sleep_seconds, 0))
            if not route:
                route = fallback_route(centroid, candidate, "fallback_no_google_key" if not google_key else "fallback_google_unavailable")

            row = route_record(centroid, candidate, route, allowed_categories)
            if best_row is None or route_sort_key(row) < route_sort_key(best_row):
                best_row = row

        if best_row:
            rows.append(best_row)
        if idx and idx % 1000 == 0:
            print(f"Procesados {idx:,} centroides; rutas Google usadas: {google_calls:,}")

    return pd.DataFrame(rows)


def nearest_units(centroid: pd.Series, units: pd.DataFrame, categories: list[str], limit: int) -> list[pd.Series]:
    subset = units[units["category"].isin(categories)].copy()
    if subset.empty:
        subset = units.copy()
    subset["haversine_m"] = subset.apply(
        lambda row: haversine_m(centroid["centroid_lat"], centroid["centroid_lon"], row["lat"], row["lon"]),
        axis=1,
    )
    return [row for _, row in subset.nsmallest(limit, "haversine_m").iterrows()]


def compute_google_route(
    centroid: pd.Series,
    unit: pd.Series,
    google_key: str,
    route_cache: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    cache_key = f"{unit['unit_id']}|{centroid['incident_key']}"
    if cache_key in route_cache:
        return route_cache[cache_key]
    body = {
        "origin": waypoint(float(unit["lat"]), float(unit["lon"])),
        "destination": waypoint(float(centroid["centroid_lat"]), float(centroid["centroid_lon"])),
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
        "computeAlternativeRoutes": False,
        "languageCode": "es-MX",
        "units": "METRIC",
    }
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": google_key,
        "X-Goog-FieldMask": "routes.duration,routes.staticDuration,routes.distanceMeters,routes.polyline.encodedPolyline,routes.description",
    }
    try:
        response = requests.post(GOOGLE_ROUTES_URL, headers=headers, json=body, timeout=45)
        response.raise_for_status()
        data = response.json()
        routes = data.get("routes", [])
        if not routes:
            return None
        route = routes[0]
        encoded = route.get("polyline", {}).get("encodedPolyline")
        coords_latlon = decode_polyline(encoded) if encoded else [[unit["lat"], unit["lon"]], [centroid["centroid_lat"], centroid["centroid_lon"]]]
        result = {
            "route_source": "google_routes",
            "routing_status": "ok",
            "distance_meters": route.get("distanceMeters"),
            "duration_seconds": parse_duration_seconds(route.get("duration")),
            "static_duration_seconds": parse_duration_seconds(route.get("staticDuration")),
            "encoded_polyline": encoded,
            "description": route.get("description"),
            "coordinates_latlon": coords_latlon,
        }
        route_cache[cache_key] = result
        return result
    except Exception as exc:
        route_cache[cache_key] = {"route_source": "google_routes", "routing_status": f"error: {str(exc)[:180]}"}
        return None


def fallback_route(centroid: pd.Series, unit: pd.Series, status: str) -> dict[str, Any]:
    distance = haversine_m(unit["lat"], unit["lon"], centroid["centroid_lat"], centroid["centroid_lon"])
    return {
        "route_source": "fallback_haversine_direct",
        "routing_status": status,
        "distance_meters": distance,
        "duration_seconds": distance / (28_000 / 3600),
        "static_duration_seconds": distance / (35_000 / 3600),
        "encoded_polyline": None,
        "description": "Linea directa entre unidad resolutora y centroide; no representa geometria vial.",
        "coordinates_latlon": [[float(unit["lat"]), float(unit["lon"])], [float(centroid["centroid_lat"]), float(centroid["centroid_lon"])]],
    }


def route_record(centroid: pd.Series, unit: pd.Series, route: dict[str, Any], allowed_categories: list[str]) -> dict[str, Any]:
    duration = route.get("duration_seconds")
    static_duration = route.get("static_duration_seconds")
    return {
        "incident_key": centroid["incident_key"],
        "codigo_postal": centroid["codigo_postal"],
        "crime_type": centroid["crime_type"],
        "centroid_id": int(centroid["centroid_id"]),
        "centroid_lat": float(centroid["centroid_lat"]),
        "centroid_lon": float(centroid["centroid_lon"]),
        "n_events": int(centroid["n_events"]),
        "resolver_unit_id": unit["unit_id"],
        "resolver_name": unit["name"],
        "resolver_category": unit["category"],
        "resolver_category_label": CATEGORY_LABELS.get(unit["category"], unit["category"]),
        "resolver_lat": float(unit["lat"]),
        "resolver_lon": float(unit["lon"]),
        "allowed_resolver_categories": ",".join(allowed_categories),
        "route_source": route.get("route_source"),
        "routing_status": route.get("routing_status"),
        "distance_meters": float(route["distance_meters"]) if route.get("distance_meters") is not None else None,
        "duration_seconds": float(duration) if duration is not None else None,
        "duration_minutes": float(duration) / 60 if duration is not None else None,
        "static_duration_seconds": float(static_duration) if static_duration is not None else None,
        "delay_seconds": float(duration) - float(static_duration) if duration is not None and static_duration is not None else None,
        "encoded_polyline": route.get("encoded_polyline"),
        "route_description": route.get("description"),
        "geometry": route.get("coordinates_latlon"),
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }


def route_sort_key(row: dict[str, Any]) -> tuple[int, float, float]:
    google_rank = 0 if row.get("route_source") == "google_routes" and row.get("routing_status") == "ok" else 1
    duration = row.get("duration_seconds")
    distance = row.get("distance_meters")
    return (google_rank, float(duration or math.inf), float(distance or math.inf))


def write_outputs(output_dir: Path, routes: pd.DataFrame, units: pd.DataFrame) -> None:
    routes_csv = routes.drop(columns=["geometry"], errors="ignore")
    routes_csv.to_csv(output_dir / "incident_response_routes_summary.csv", index=False, encoding="utf-8")
    units.to_csv(output_dir / "response_units.csv", index=False, encoding="utf-8")

    write_json(output_dir / "response_units.json", units_to_geojson(units))
    write_json(output_dir / "incident_response_routes_all.geojson", routes_to_geojson(routes))
    write_json(output_dir / "incident_response_summary.json", build_summary_payload(routes, units))

    for crime_type, group in routes.groupby("crime_type"):
        write_json(output_dir / f"routes_{slugify(crime_type)}.geojson", routes_to_geojson(group))


def build_maps(output_dir: Path, routes: pd.DataFrame, units: pd.DataFrame) -> None:
    import folium
    from folium.plugins import MarkerCluster

    index_links = []
    for crime_type, group in routes.groupby("crime_type"):
        filename = f"map_{slugify(crime_type)}.html"
        map_obj = build_type_map(folium, MarkerCluster, crime_type, group, units)
        map_obj.save(output_dir / filename)
        add_map_link(index_links, "Por tipo de incidente", crime_type, filename, group)

        top_group = group.sort_values("n_events", ascending=False).head(60).copy()
        filename = f"map_top_demanda_{slugify(crime_type)}.html"
        map_obj = build_type_map(folium, MarkerCluster, f"Top demanda: {crime_type}", top_group, units)
        map_obj.save(output_dir / filename)
        add_map_link(index_links, "Top demanda por tipo", f"Top demanda: {crime_type}", filename, top_group)

    for category, label in CATEGORY_LABELS.items():
        group = routes[routes["resolver_category"] == category].copy()
        if group.empty:
            continue
        filename = f"map_unidades_{slugify(label)}.html"
        map_obj = build_type_map(folium, MarkerCluster, f"Rutas atendidas por {label}", group, units, max_lines=2500)
        map_obj.save(output_dir / filename)
        add_map_link(index_links, "Por tipo de unidad resolutora", label, filename, group)

    high_demand = routes.sort_values("n_events", ascending=False).head(250).copy()
    filename = "map_alta_demanda_top_250.html"
    build_type_map(folium, MarkerCluster, "Top 250 centroides por volumen de eventos", high_demand, units).save(output_dir / filename)
    add_map_link(index_links, "Escenarios operativos", "Top 250 por volumen", filename, high_demand)

    long_duration = routes.sort_values("duration_minutes", ascending=False).head(250).copy()
    filename = "map_mayor_tiempo_respuesta_top_250.html"
    build_type_map(folium, MarkerCluster, "Top 250 por mayor tiempo estimado de respuesta", long_duration, units).save(output_dir / filename)
    add_map_link(index_links, "Escenarios operativos", "Top 250 por tiempo", filename, long_duration)

    google_routes = routes[(routes["route_source"] == "google_routes") & (routes["routing_status"] == "ok")].copy()
    if not google_routes.empty:
        filename = "map_rutas_google_maps.html"
        build_type_map(folium, MarkerCluster, "Rutas calculadas con Google Maps", google_routes, units).save(output_dir / filename)
        add_map_link(index_links, "Escenarios operativos", "Solo rutas Google Maps", filename, google_routes)

    fallback_routes = routes[routes["route_source"] != "google_routes"].copy()
    if not fallback_routes.empty:
        filename = "map_rutas_fallback.html"
        build_type_map(folium, MarkerCluster, "Rutas fallback sin geometria vial", fallback_routes, units, max_lines=2500).save(output_dir / filename)
        add_map_link(index_links, "Escenarios operativos", "Solo rutas fallback", filename, fallback_routes)

    for zone_name, group in split_city_zones(routes).items():
        if group.empty:
            continue
        filename = f"map_zona_{slugify(zone_name)}.html"
        build_type_map(folium, MarkerCluster, f"Zona {zone_name}", group, units, max_lines=2500).save(output_dir / filename)
        add_map_link(index_links, "Zonas de la ciudad", f"Zona {zone_name}", filename, group)

    all_map = build_type_map(folium, MarkerCluster, "Todos los tipos de incidentes", routes, units, max_lines=3500)
    all_map.save(output_dir / "map_all_incidents.html")
    add_map_link(index_links, "General", "Mapa general", "map_all_incidents.html", routes)
    write_index(output_dir / "index.html", index_links)


def add_map_link(index_links: list[dict[str, Any]], section: str, title: str, filename: str, routes: pd.DataFrame) -> None:
    index_links.append(
        {
            "section": section,
            "title": title,
            "filename": filename,
            "routes": int(len(routes)),
            "events": int(routes["n_events"].sum()) if "n_events" in routes.columns and not routes.empty else 0,
        }
    )


def split_city_zones(routes: pd.DataFrame) -> dict[str, pd.DataFrame]:
    lat_mid = float(routes["centroid_lat"].median()) if not routes.empty else 19.4326
    lon_mid = float(routes["centroid_lon"].median()) if not routes.empty else -99.1332
    return {
        "Norte": routes[routes["centroid_lat"] >= lat_mid].copy(),
        "Sur": routes[routes["centroid_lat"] < lat_mid].copy(),
        "Oriente": routes[routes["centroid_lon"] >= lon_mid].copy(),
        "Poniente": routes[routes["centroid_lon"] < lon_mid].copy(),
    }


def build_type_map(
    folium: Any,
    marker_cluster_cls: Any,
    title: str,
    routes: pd.DataFrame,
    units: pd.DataFrame,
    max_lines: int | None = None,
) -> Any:
    center_lat = float(routes["centroid_lat"].mean()) if not routes.empty else 19.4326
    center_lon = float(routes["centroid_lon"].mean()) if not routes.empty else -99.1332
    map_obj = folium.Map(location=[center_lat, center_lon], zoom_start=11, tiles="CartoDB positron", control_scale=True)

    unit_ids = set(routes["resolver_unit_id"].dropna().astype(str))
    unit_cluster = marker_cluster_cls(name="Unidades resolutoras").add_to(map_obj)
    for _, unit in units[units["unit_id"].astype(str).isin(unit_ids)].iterrows():
        folium.Marker(
            location=[unit["lat"], unit["lon"]],
            tooltip=f"{unit['name']} ({CATEGORY_LABELS.get(unit['category'], unit['category'])})",
            popup=popup_html(
                [
                    ("Unidad", unit["name"]),
                    ("Categoria", CATEGORY_LABELS.get(unit["category"], unit["category"])),
                    ("Fuente", unit.get("source", "")),
                ]
            ),
            icon=folium.Icon(color=marker_color(unit["category"]), icon=marker_icon(unit["category"]), prefix="fa"),
        ).add_to(unit_cluster)

    if max_lines and len(routes) > max_lines:
        plot_routes = routes.sort_values("n_events", ascending=False).head(max_lines).copy()
    else:
        plot_routes = routes.copy()

    for _, row in plot_routes.iterrows():
        color = ROUTE_COLORS.get(row["resolver_category"], ROUTE_COLORS["mixed"])
        coords = row["geometry"]
        if not coords:
            continue
        folium.PolyLine(
            coords,
            color=color,
            weight=route_weight(row.get("n_events", 1)),
            opacity=0.48,
            tooltip=f"{row['crime_type']} CP {row['codigo_postal']} -> {row['resolver_name']}",
            popup=popup_html(
                [
                    ("Tipo", row["crime_type"]),
                    ("CP", row["codigo_postal"]),
                    ("Eventos", row["n_events"]),
                    ("Unidad", row["resolver_name"]),
                    ("Categoria", row["resolver_category_label"]),
                    ("Distancia km", round((row.get("distance_meters") or 0) / 1000, 2)),
                    ("Duracion min", round(row.get("duration_minutes") or 0, 1)),
                    ("Fuente ruta", row["route_source"]),
                    ("Estado", row["routing_status"]),
                ]
            ),
        ).add_to(map_obj)
        folium.CircleMarker(
            location=[row["centroid_lat"], row["centroid_lon"]],
            radius=max(3, min(11, math.sqrt(max(row["n_events"], 1)) / 1.8)),
            color=color,
            fill=True,
            fill_opacity=0.72,
            weight=1,
            tooltip=f"{row['crime_type']} CP {row['codigo_postal']} ({row['n_events']} eventos)",
        ).add_to(map_obj)

    add_title(map_obj, title, len(routes), int(routes["n_events"].sum()), len(plot_routes))
    folium.LayerControl().add_to(map_obj)
    return map_obj


def routes_to_geojson(routes: pd.DataFrame) -> dict[str, Any]:
    features = []
    for _, row in routes.iterrows():
        coords = [[lon, lat] for lat, lon in row["geometry"]]
        props = row.drop(labels=["geometry"]).where(pd.notna(row.drop(labels=["geometry"])), None).to_dict()
        features.append({"type": "Feature", "geometry": {"type": "LineString", "coordinates": coords}, "properties": props})
    return {"type": "FeatureCollection", "features": features}


def units_to_geojson(units: pd.DataFrame) -> dict[str, Any]:
    features = []
    for _, row in units.iterrows():
        props = row.drop(labels=["lat", "lon"], errors="ignore").where(pd.notna(row.drop(labels=["lat", "lon"], errors="ignore")), None).to_dict()
        features.append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [float(row["lon"]), float(row["lat"])]},
                "properties": props,
            }
        )
    return {"type": "FeatureCollection", "features": features}


def build_summary_payload(routes: pd.DataFrame, units: pd.DataFrame) -> dict[str, Any]:
    by_type = []
    for crime_type, group in routes.groupby("crime_type"):
        by_type.append(
            {
                "crime_type": crime_type,
                "centroids": int(len(group)),
                "events": int(group["n_events"].sum()),
                "avg_distance_km": round(float(group["distance_meters"].mean()) / 1000, 3),
                "avg_duration_min": round(float(group["duration_minutes"].mean()), 2),
                "route_sources": group["route_source"].value_counts(dropna=False).to_dict(),
                "resolver_categories": group["resolver_category"].value_counts(dropna=False).to_dict(),
            }
        )
    return {
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "routes": int(len(routes)),
        "response_units": int(len(units)),
        "crime_types": int(routes["crime_type"].nunique()) if not routes.empty else 0,
        "summary_by_type": by_type,
    }


def write_index(path: Path, links: list[dict[str, Any]]) -> None:
    sections = []
    for section in sorted({item["section"] for item in links}):
        rows = [item for item in links if item["section"] == section]
        items = "\n".join(
            f'<li><a href="{html.escape(item["filename"])}">{html.escape(item["title"])}</a> '
            f'<span>{item["routes"]:,} rutas, {item["events"]:,} eventos</span></li>'
            for item in sorted(rows, key=lambda row: row["title"])
        )
        sections.append(f"<section><h2>{html.escape(section)}</h2><ul>{items}</ul></section>")
    path.write_text(
        f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Galeria de rutas de atencion por incidente</title>
  <style>
    body {{ font-family: system-ui, -apple-system, Segoe UI, sans-serif; margin: 32px; color: #172033; }}
    a {{ color: #0f5bd7; text-decoration: none; }}
    li {{ margin: 10px 0; }}
    h2 {{ margin-top: 28px; }}
    span {{ color: #596579; margin-left: 8px; }}
  </style>
</head>
<body>
  <h1>Galeria de rutas de atencion por incidente</h1>
  <p>{len(links):,} mapas HTML generados con rutas y unidades resolutoras.</p>
  {''.join(sections)}
</body>
</html>
""",
        encoding="utf-8",
    )


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(to_jsonable(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def waypoint(lat: float, lon: float) -> dict[str, Any]:
    return {"location": {"latLng": {"latitude": lat, "longitude": lon}}}


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius = 6_371_000
    phi1 = math.radians(float(lat1))
    phi2 = math.radians(float(lat2))
    dphi = math.radians(float(lat2) - float(lat1))
    dlambda = math.radians(float(lon2) - float(lon1))
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return radius * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def parse_duration_seconds(value: Any) -> float | None:
    if not isinstance(value, str):
        return None
    match = re.match(r"^(\d+(\.\d+)?)s$", value)
    return float(match.group(1)) if match else None


def decode_polyline(polyline_str: str) -> list[list[float]]:
    index = lat = lon = 0
    coordinates = []
    while index < len(polyline_str):
        result = 1
        shift = 0
        while True:
            b = ord(polyline_str[index]) - 63 - 1
            index += 1
            result += b << shift
            shift += 5
            if b < 0x1F:
                break
        lat += ~(result >> 1) if result & 1 else result >> 1
        result = 1
        shift = 0
        while True:
            b = ord(polyline_str[index]) - 63 - 1
            index += 1
            result += b << shift
            shift += 5
            if b < 0x1F:
                break
        lon += ~(result >> 1) if result & 1 else result >> 1
        coordinates.append([lat * 1e-5, lon * 1e-5])
    return coordinates


def route_weight(events: Any) -> float:
    try:
        return max(1.3, min(6.5, math.sqrt(float(events)) / 2.5))
    except Exception:
        return 2.0


def marker_color(category: str) -> str:
    return {"police": "blue", "fire_station": "red", "hospital": "green"}.get(category, "gray")


def marker_icon(category: str) -> str:
    return {"police": "shield", "fire_station": "fire-extinguisher", "hospital": "plus"}.get(category, "map-marker")


def popup_html(rows: list[tuple[str, Any]]) -> str:
    return "<br>".join(f"<b>{html.escape(str(key))}:</b> {html.escape(str(value))}" for key, value in rows)


def add_title(map_obj: Any, title: str, routes_count: int, events_count: int, plotted_count: int) -> None:
    from branca.element import Element

    title_html = f"""
    <div style="
      position: fixed; top: 12px; left: 50px; z-index: 9999;
      background: white; padding: 10px 12px; border: 1px solid #cbd5e1;
      border-radius: 6px; box-shadow: 0 1px 6px rgba(15,23,42,.14);
      font-family: Arial, sans-serif; font-size: 13px;">
      <strong>{html.escape(title)}</strong><br>
      {routes_count:,} rutas / {events_count:,} eventos / {plotted_count:,} lineas visibles
    </div>
    """
    map_obj.get_root().html.add_child(Element(title_html))


def to_jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [to_jsonable(item) for item in value]
    if isinstance(value, tuple):
        return [to_jsonable(item) for item in value]
    if pd.isna(value) if not isinstance(value, (dict, list, tuple)) else False:
        return None
    if hasattr(value, "item"):
        try:
            return value.item()
        except Exception:
            pass
    return value


def slugify(text: Any) -> str:
    normalized = unicodedata.normalize("NFD", str(text))
    ascii_text = "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")
    return re.sub(r"[^a-z0-9]+", "_", ascii_text.lower()).strip("_")


if __name__ == "__main__":
    raise SystemExit(main())
