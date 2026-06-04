from __future__ import annotations

import os
import re
import time
from datetime import datetime
from typing import Any

import numpy as np
import pandas as pd
import requests

from ..storage import make_snapshot_id, save_artifact, save_tables


SOURCE = "google_routes"
COMPUTE_ROUTES_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"
COMPUTE_MATRIX_URL = "https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix"

PLACES = {
    "Metro Universidad": {"lat": 19.324353, "lng": -99.174770},
    "Metro Copilco": {"lat": 19.335720, "lng": -99.176595},
    "Rectoria UNAM": {"lat": 19.332242, "lng": -99.187276},
    "Facultad de Medicina UNAM": {"lat": 19.334324, "lng": -99.184510},
    "Estadio Olimpico Universitario": {"lat": 19.331872, "lng": -99.192310},
    "Metro Indios Verdes": {"lat": 19.495483, "lng": -99.119686},
    "IPN Zacatenco": {"lat": 19.500818, "lng": -99.139321},
    "UAM Xochimilco": {"lat": 19.305305, "lng": -99.103608},
    "Universidad Iberoamericana": {"lat": 19.370557, "lng": -99.264731},
    "Tec CCM": {"lat": 19.284546, "lng": -99.135983},
    "Zocalo": {"lat": 19.432608, "lng": -99.133209},
    "Angel de la Independencia": {"lat": 19.426978, "lng": -99.167665},
    "WTC": {"lat": 19.393246, "lng": -99.173205},
}


def run_google_routes(config_path: str, run_date: str | None = None) -> None:
    key = os.getenv("MAPS", os.getenv("GOOGLE_MAPS_API_KEY", "")).strip()
    if not key:
        raise ValueError("Configura secret MAPS o GOOGLE_MAPS_API_KEY en GitHub Actions.")

    snapshot_id = make_snapshot_id()
    client = RoutesClient(key)
    summary_drive, _ = client.compute_route("Metro Universidad", "Rectoria UNAM", "DRIVE")
    df_example_drive = pd.DataFrame([summary_drive])
    df_modes = compare_modes(client, "Metro Universidad", "Rectoria UNAM", ["DRIVE", "WALK", "BICYCLE", "TRANSIT"])
    df_drive_pairs = compute_drive_pairs(client)
    df_matrix, _ = client.compute_route_matrix(
        origin_names=["Metro Universidad", "Metro Copilco", "Zocalo", "Angel de la Independencia", "WTC", "Metro Indios Verdes"],
        destination_names=["Rectoria UNAM", "Facultad de Medicina UNAM", "IPN Zacatenco"],
        travel_mode="DRIVE",
    )
    df_scored = build_accessibility_score(df_matrix)

    save_tables(
        {
            "routes_api_ejemplo_ruta": df_example_drive,
            "routes_api_comparacion_modos": df_modes,
            "routes_api_drive_pairs": df_drive_pairs,
            "routes_api_matriz": df_matrix,
            "routes_api_score": df_scored,
        },
        source=SOURCE,
        config_path=config_path,
        run_date=run_date,
        snapshot_id=snapshot_id,
    )

    html = map_route_html(summary_drive, "Metro Universidad", "Rectoria UNAM")
    save_artifact(
        name="routes_api_mapa",
        suffix="html",
        content=html,
        source=SOURCE,
        run_date=run_date,
        snapshot_id=snapshot_id,
    )


class RoutesClient:
    def __init__(self, key: str) -> None:
        self.headers_routes = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": key,
            "X-Goog-FieldMask": (
                "routes.duration,routes.staticDuration,routes.distanceMeters,routes.polyline.encodedPolyline,"
                "routes.description,routes.routeLabels,routes.legs.duration,routes.legs.staticDuration,routes.legs.distanceMeters"
            ),
        }
        self.headers_matrix = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": key,
            "X-Goog-FieldMask": "originIndex,destinationIndex,status,condition,duration,staticDuration,distanceMeters",
        }

    def compute_route(
        self,
        origin_name: str,
        destination_name: str,
        travel_mode: str = "DRIVE",
        routing_preference: str = "TRAFFIC_AWARE",
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        origin = PLACES[origin_name]
        destination = PLACES[destination_name]
        body: dict[str, Any] = {
            "origin": waypoint_from_latlng(origin["lat"], origin["lng"]),
            "destination": waypoint_from_latlng(destination["lat"], destination["lng"]),
            "travelMode": travel_mode,
            "computeAlternativeRoutes": False,
            "languageCode": "es-MX",
            "units": "METRIC",
        }
        if travel_mode == "DRIVE":
            body["routingPreference"] = routing_preference
        response = requests.post(COMPUTE_ROUTES_URL, headers=self.headers_routes, json=body, timeout=60)
        response.raise_for_status()
        data = response.json()
        return extract_route_summary(data, origin_name, destination_name, travel_mode), data

    def compute_route_matrix(
        self,
        origin_names: list[str],
        destination_names: list[str],
        travel_mode: str = "DRIVE",
        routing_preference: str = "TRAFFIC_AWARE",
    ) -> tuple[pd.DataFrame, Any]:
        origins = [{"waypoint": waypoint_from_latlng(PLACES[name]["lat"], PLACES[name]["lng"])} for name in origin_names]
        destinations = [
            {"waypoint": waypoint_from_latlng(PLACES[name]["lat"], PLACES[name]["lng"])} for name in destination_names
        ]
        body: dict[str, Any] = {"origins": origins, "destinations": destinations, "travelMode": travel_mode}
        if travel_mode == "DRIVE":
            body["routingPreference"] = routing_preference
        response = requests.post(COMPUTE_MATRIX_URL, headers=self.headers_matrix, json=body, timeout=90)
        response.raise_for_status()
        data = response.json()
        elements = data.get("routeMatrixElements", []) if isinstance(data, dict) else data
        rows = []
        for element in elements:
            origin_idx = element.get("originIndex")
            destination_idx = element.get("destinationIndex")
            duration_seconds = parse_google_duration(element.get("duration"))
            static_duration_seconds = parse_google_duration(element.get("staticDuration"))
            delay_seconds = duration_seconds - static_duration_seconds
            if pd.isna(delay_seconds):
                delay_seconds = np.nan
            traffic_delay_pct = np.nan
            if not pd.isna(duration_seconds) and not pd.isna(static_duration_seconds) and static_duration_seconds > 0:
                traffic_delay_pct = (duration_seconds / static_duration_seconds - 1) * 100
            rows.append(
                {
                    "query_timestamp": datetime.utcnow().isoformat(),
                    "origin_index": origin_idx,
                    "destination_index": destination_idx,
                    "origin": origin_names[origin_idx] if origin_idx is not None else None,
                    "destination": destination_names[destination_idx] if destination_idx is not None else None,
                    "travel_mode": travel_mode,
                    "status": element.get("status", {}),
                    "condition": element.get("condition"),
                    "distance_meters": element.get("distanceMeters"),
                    "duration_seconds": duration_seconds,
                    "static_duration_seconds": static_duration_seconds,
                    "duration_minutes": seconds_to_min(duration_seconds),
                    "static_duration_minutes": seconds_to_min(static_duration_seconds),
                    "delay_seconds": delay_seconds,
                    "delay_minutes": seconds_to_min(delay_seconds),
                    "traffic_delay_pct": traffic_delay_pct,
                }
            )
        return pd.DataFrame(rows), data


def waypoint_from_latlng(lat: float, lng: float) -> dict[str, Any]:
    return {"location": {"latLng": {"latitude": lat, "longitude": lng}}}


def parse_google_duration(duration_str: Any) -> float:
    if not duration_str or not isinstance(duration_str, str):
        return np.nan
    match = re.match(r"^(\d+(\.\d+)?)s$", duration_str)
    return float(match.group(1)) if match else np.nan


def seconds_to_min(seconds: Any) -> float:
    if pd.isna(seconds):
        return np.nan
    return float(seconds) / 60


def extract_route_summary(response_json: dict[str, Any], origin_name: str, destination_name: str, travel_mode: str) -> dict[str, Any]:
    routes = response_json.get("routes", [])
    if not routes:
        return {
            "query_timestamp": datetime.utcnow().isoformat(),
            "origin": origin_name,
            "destination": destination_name,
            "travel_mode": travel_mode,
            "route_found": False,
        }
    route = routes[0]
    duration_seconds = parse_google_duration(route.get("duration"))
    static_duration_seconds = parse_google_duration(route.get("staticDuration"))
    delay_seconds = duration_seconds - static_duration_seconds
    traffic_delay_pct = np.nan
    if not pd.isna(duration_seconds) and not pd.isna(static_duration_seconds) and static_duration_seconds > 0:
        traffic_delay_pct = (duration_seconds / static_duration_seconds - 1) * 100
    return {
        "query_timestamp": datetime.utcnow().isoformat(),
        "origin": origin_name,
        "destination": destination_name,
        "travel_mode": travel_mode,
        "route_found": True,
        "distance_meters": route.get("distanceMeters"),
        "duration_seconds": duration_seconds,
        "static_duration_seconds": static_duration_seconds,
        "duration_minutes": seconds_to_min(duration_seconds),
        "static_duration_minutes": seconds_to_min(static_duration_seconds),
        "delay_seconds": delay_seconds,
        "delay_minutes": seconds_to_min(delay_seconds),
        "traffic_delay_pct": traffic_delay_pct,
        "encoded_polyline": route.get("polyline", {}).get("encodedPolyline"),
        "description": route.get("description"),
        "route_labels": ",".join(route.get("routeLabels", [])) if route.get("routeLabels") else None,
    }


def compare_modes(client: RoutesClient, origin_name: str, destination_name: str, modes: list[str]) -> pd.DataFrame:
    rows = []
    for mode in modes:
        try:
            summary, _ = client.compute_route(origin_name, destination_name, mode)
            rows.append(summary)
            time.sleep(0.2)
        except Exception as exc:
            rows.append(
                {
                    "query_timestamp": datetime.utcnow().isoformat(),
                    "origin": origin_name,
                    "destination": destination_name,
                    "travel_mode": mode,
                    "route_found": False,
                    "error": str(exc),
                }
            )
    return pd.DataFrame(rows)


def compute_drive_pairs(client: RoutesClient) -> pd.DataFrame:
    pairs = [
        ("Metro Universidad", "Rectoria UNAM"),
        ("Metro Copilco", "Rectoria UNAM"),
        ("Metro Universidad", "Facultad de Medicina UNAM"),
        ("Metro Copilco", "Facultad de Medicina UNAM"),
        ("Metro Indios Verdes", "IPN Zacatenco"),
        ("Zocalo", "Rectoria UNAM"),
        ("Angel de la Independencia", "Rectoria UNAM"),
        ("WTC", "Rectoria UNAM"),
    ]
    rows = []
    for origin_name, destination_name in pairs:
        try:
            summary, _ = client.compute_route(origin_name, destination_name, "DRIVE")
            rows.append(summary)
            time.sleep(0.2)
        except Exception as exc:
            rows.append(
                {
                    "query_timestamp": datetime.utcnow().isoformat(),
                    "origin": origin_name,
                    "destination": destination_name,
                    "travel_mode": "DRIVE",
                    "route_found": False,
                    "error": str(exc),
                }
            )
    return pd.DataFrame(rows)


def build_accessibility_score(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in ["duration_minutes", "delay_minutes", "traffic_delay_pct"]:
        if col not in out.columns:
            out[col] = np.nan

    def minmax(series: pd.Series) -> pd.Series:
        numeric = pd.to_numeric(series, errors="coerce")
        if numeric.notna().sum() == 0 or numeric.max() == numeric.min():
            return pd.Series([0.0] * len(numeric), index=numeric.index)
        return (numeric - numeric.min()) / (numeric.max() - numeric.min())

    out["duration_score"] = minmax(out["duration_minutes"])
    out["delay_score"] = minmax(out["delay_minutes"].fillna(0))
    out["traffic_pct_score"] = minmax(out["traffic_delay_pct"].fillna(0))
    out["criticality_score_0_100"] = (
        0.45 * out["duration_score"] + 0.35 * out["delay_score"] + 0.20 * out["traffic_pct_score"]
    ) * 100
    out["criticality_level"] = pd.cut(
        out["criticality_score_0_100"], bins=[-1, 25, 50, 75, 100], labels=["Baja", "Media", "Alta", "Critica"]
    )
    return out


def decode_polyline(polyline_str: str) -> list[list[float]]:
    index = lat = lng = 0
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
        lng += ~(result >> 1) if result & 1 else result >> 1
        coordinates.append([lat * 1e-5, lng * 1e-5])
    return coordinates


def map_route_html(summary: dict[str, Any], origin_name: str, destination_name: str) -> str:
    import folium

    origin = PLACES[origin_name]
    destination = PLACES[destination_name]
    m = folium.Map(
        location=[(origin["lat"] + destination["lat"]) / 2, (origin["lng"] + destination["lng"]) / 2],
        zoom_start=15,
        tiles="CartoDB positron",
    )
    folium.Marker([origin["lat"], origin["lng"]], tooltip=f"Origen: {origin_name}").add_to(m)
    folium.Marker([destination["lat"], destination["lng"]], tooltip=f"Destino: {destination_name}").add_to(m)
    encoded_polyline = summary.get("encoded_polyline")
    if encoded_polyline:
        folium.PolyLine(decode_polyline(encoded_polyline), weight=5, opacity=0.8).add_to(m)
    return m.get_root().render()
