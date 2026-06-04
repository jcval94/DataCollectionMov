from __future__ import annotations

import io
import json
import os
import time
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from google.transit import gtfs_realtime_pb2

from ..storage import make_snapshot_id, read_current_table, save_artifact, save_tables


AUTH_URL = "https://metrobus-gtfs.sinopticoplus.com/gtfs-api/partnerValidation"
SOURCE = "metrobus"
CACHE_AUTH_PATH = Path("data/tmp/metrobus_auth_cache.json")


def run_metrobus_static(config_path: str, run_date: str | None = None) -> None:
    snapshot_id = make_snapshot_id()
    auth_data = authenticate()
    static_tables = download_static_gtfs(auth_data)
    save_tables(
        {f"metrobus_gtfs_static_{name}": df for name, df in static_tables.items()},
        source=SOURCE,
        config_path=config_path,
        run_date=run_date,
        snapshot_id=snapshot_id,
    )


def run_metrobus_realtime(config_path: str, run_date: str | None = None) -> None:
    snapshot_id = make_snapshot_id()
    auth_data = authenticate()
    feed = get_realtime_feed(auth_data)

    vehicle_positions = extract_vehicle_positions(feed)
    trip_updates = extract_trip_updates(feed)
    alerts = extract_alerts(feed)

    static_tables = load_static_tables_from_current()
    if not static_tables:
        static_tables = download_static_gtfs(auth_data)

    vehicle_positions_enriched = enrich_vehicle_positions(vehicle_positions, static_tables)

    tables = {
        "metrobus_vehicle_positions": vehicle_positions,
        "metrobus_trip_updates": trip_updates,
        "metrobus_alerts": alerts,
        "metrobus_vehicle_positions_enriched": vehicle_positions_enriched,
    }
    save_tables(tables, source=SOURCE, config_path=config_path, run_date=run_date, snapshot_id=snapshot_id)

    html = build_vehicle_map_html(vehicle_positions_enriched)
    if html:
        save_artifact(
            name="metrobus_vehicle_map",
            suffix="html",
            content=html,
            source=SOURCE,
            run_date=run_date,
            snapshot_id=snapshot_id,
        )


def authenticate() -> dict[str, Any]:
    usuario = os.getenv("METROBUS_USER", "").strip()
    senha = os.getenv("METROBUS_PASS", "").strip()
    if not usuario or not senha:
        raise ValueError("Configura secrets METROBUS_USER y METROBUS_PASS en GitHub Actions.")

    payload = {"usuario": usuario, "senha": senha}
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 GitHubActions GTFS Client",
    }
    try:
        response = request_with_retries("POST", AUTH_URL, json=payload, headers=headers, timeout=45)
        response.raise_for_status()
        data = response.json()
        missing = [key for key in ["urlRealTime", "urlStatic"] if key not in data]
        if missing:
            raise KeyError(f"Faltan campos de autenticacion: {missing}")
        CACHE_AUTH_PATH.parent.mkdir(parents=True, exist_ok=True)
        CACHE_AUTH_PATH.write_text(json.dumps(data), encoding="utf-8")
        return data
    except Exception:
        if CACHE_AUTH_PATH.exists():
            return json.loads(CACHE_AUTH_PATH.read_text(encoding="utf-8"))
        raise


def request_with_retries(method: str, url: str, max_retries: int = 4, **kwargs: Any) -> requests.Response:
    retry_statuses = {429, 500, 502, 503, 504}
    last_response: requests.Response | None = None
    last_exception: Exception | None = None

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.request(method, url, **kwargs)
            last_response = response
            if response.status_code not in retry_statuses:
                return response
        except requests.RequestException as exc:
            last_exception = exc
        if attempt < max_retries:
            time.sleep(2 ** attempt)

    if last_response is not None:
        return last_response
    if last_exception is not None:
        raise last_exception
    raise RuntimeError("Request fallido sin respuesta.")


def download_binary(url: str, timeout: int = 90) -> bytes:
    response = request_with_retries(
        "GET",
        url,
        headers={
            "Accept": "application/octet-stream, application/x-protobuf, application/zip, */*",
            "User-Agent": "Mozilla/5.0 GitHubActions GTFS Client",
        },
        timeout=timeout,
    )
    response.raise_for_status()
    if not response.content:
        raise ValueError("Descarga vacia.")
    return response.content


def get_realtime_feed(auth_data: dict[str, Any]) -> gtfs_realtime_pb2.FeedMessage:
    content = download_binary(auth_data["urlRealTime"])
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(content)
    return feed


def download_static_gtfs(auth_data: dict[str, Any]) -> dict[str, pd.DataFrame]:
    content = download_binary(auth_data["urlStatic"])
    tables: dict[str, pd.DataFrame] = {}
    with zipfile.ZipFile(io.BytesIO(content)) as z:
        for name in z.namelist():
            if not name.endswith(".txt"):
                continue
            table_name = Path(name).stem
            with z.open(name) as f:
                df = pd.read_csv(f, dtype=str, keep_default_na=False, na_values=[])
            for col in df.columns:
                df[col] = df[col].astype("string").str.strip()
            tables[table_name] = df
    return tables


def load_static_tables_from_current() -> dict[str, pd.DataFrame]:
    tables: dict[str, pd.DataFrame] = {}
    for name in ["routes", "stops"]:
        df = read_current_table(f"metrobus_gtfs_static_{name}")
        if not df.empty:
            tables[name] = df
    return tables


def ensure_string_key(df: pd.DataFrame, col: str) -> pd.DataFrame:
    if df.empty or col not in df.columns:
        return df
    out = df.copy()
    out[col] = out[col].astype("string").str.strip()
    return out


def gtfs_timestamp_to_datetime(ts: int | None) -> pd.Timestamp | None:
    if ts in [None, 0]:
        return None
    return pd.to_datetime(ts, unit="s", utc=True).tz_convert("America/Mexico_City")


def enum_name(enum_class: Any, value: Any) -> str | None:
    try:
        return enum_class.Name(value)
    except Exception:
        return None


def extract_vehicle_positions(feed: gtfs_realtime_pb2.FeedMessage) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for entity in feed.entity:
        if not entity.HasField("vehicle"):
            continue
        vehicle = entity.vehicle
        trip = vehicle.trip if vehicle.HasField("trip") else None
        position = vehicle.position if vehicle.HasField("position") else None
        descriptor = vehicle.vehicle if vehicle.HasField("vehicle") else None
        timestamp_raw = vehicle.timestamp if vehicle.HasField("timestamp") else None
        rows.append(
            {
                "entity_id": entity.id,
                "trip_id": trip.trip_id if trip and trip.HasField("trip_id") else None,
                "route_id": trip.route_id if trip and trip.HasField("route_id") else None,
                "direction_id": trip.direction_id if trip and trip.HasField("direction_id") else None,
                "start_time": trip.start_time if trip and trip.HasField("start_time") else None,
                "start_date": trip.start_date if trip and trip.HasField("start_date") else None,
                "vehicle_id": descriptor.id if descriptor and descriptor.HasField("id") else None,
                "vehicle_label": descriptor.label if descriptor and descriptor.HasField("label") else None,
                "license_plate": descriptor.license_plate if descriptor and descriptor.HasField("license_plate") else None,
                "latitude": position.latitude if position and position.HasField("latitude") else None,
                "longitude": position.longitude if position and position.HasField("longitude") else None,
                "bearing": position.bearing if position and position.HasField("bearing") else None,
                "speed_mps": position.speed if position and position.HasField("speed") else None,
                "speed_kmh": position.speed * 3.6 if position and position.HasField("speed") else None,
                "current_stop_sequence": vehicle.current_stop_sequence if vehicle.HasField("current_stop_sequence") else None,
                "stop_id": vehicle.stop_id if vehicle.HasField("stop_id") else None,
                "current_status": enum_name(gtfs_realtime_pb2.VehiclePosition.VehicleStopStatus, vehicle.current_status)
                if vehicle.HasField("current_status")
                else None,
                "timestamp_raw": timestamp_raw,
                "timestamp_cdmx": gtfs_timestamp_to_datetime(timestamp_raw),
                "congestion_level": enum_name(gtfs_realtime_pb2.VehiclePosition.CongestionLevel, vehicle.congestion_level)
                if vehicle.HasField("congestion_level")
                else None,
                "occupancy_status": enum_name(gtfs_realtime_pb2.VehiclePosition.OccupancyStatus, vehicle.occupancy_status)
                if vehicle.HasField("occupancy_status")
                else None,
            }
        )
    df = pd.DataFrame(rows)
    for col in ["route_id", "stop_id", "trip_id"]:
        df = ensure_string_key(df, col)
    return df


def extract_trip_updates(feed: gtfs_realtime_pb2.FeedMessage) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for entity in feed.entity:
        if not entity.HasField("trip_update"):
            continue
        trip_update = entity.trip_update
        trip = trip_update.trip
        vehicle = trip_update.vehicle if trip_update.HasField("vehicle") else None
        for stop_update in trip_update.stop_time_update:
            arrival = stop_update.arrival if stop_update.HasField("arrival") else None
            departure = stop_update.departure if stop_update.HasField("departure") else None
            rows.append(
                {
                    "entity_id": entity.id,
                    "trip_id": trip.trip_id if trip.HasField("trip_id") else None,
                    "route_id": trip.route_id if trip.HasField("route_id") else None,
                    "direction_id": trip.direction_id if trip.HasField("direction_id") else None,
                    "start_time": trip.start_time if trip.HasField("start_time") else None,
                    "start_date": trip.start_date if trip.HasField("start_date") else None,
                    "vehicle_id": vehicle.id if vehicle and vehicle.HasField("id") else None,
                    "vehicle_label": vehicle.label if vehicle and vehicle.HasField("label") else None,
                    "stop_sequence": stop_update.stop_sequence if stop_update.HasField("stop_sequence") else None,
                    "stop_id": stop_update.stop_id if stop_update.HasField("stop_id") else None,
                    "arrival_delay_sec": arrival.delay if arrival and arrival.HasField("delay") else None,
                    "arrival_time_raw": arrival.time if arrival and arrival.HasField("time") else None,
                    "arrival_time_cdmx": gtfs_timestamp_to_datetime(arrival.time if arrival and arrival.HasField("time") else None),
                    "departure_delay_sec": departure.delay if departure and departure.HasField("delay") else None,
                    "departure_time_raw": departure.time if departure and departure.HasField("time") else None,
                    "departure_time_cdmx": gtfs_timestamp_to_datetime(
                        departure.time if departure and departure.HasField("time") else None
                    ),
                }
            )
    df = pd.DataFrame(rows)
    for col in ["route_id", "stop_id", "trip_id"]:
        df = ensure_string_key(df, col)
    return df


def translated_string_to_text(obj: Any) -> str | None:
    try:
        values = []
        for translation in obj.translation:
            lang = translation.language if translation.HasField("language") else "und"
            values.append(f"[{lang}] {translation.text}")
        return " | ".join(values) if values else None
    except Exception:
        return None


def extract_alerts(feed: gtfs_realtime_pb2.FeedMessage) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for entity in feed.entity:
        if not entity.HasField("alert"):
            continue
        alert = entity.alert
        rows.append(
            {
                "entity_id": entity.id,
                "cause": enum_name(gtfs_realtime_pb2.Alert.Cause, alert.cause) if alert.HasField("cause") else None,
                "effect": enum_name(gtfs_realtime_pb2.Alert.Effect, alert.effect) if alert.HasField("effect") else None,
                "header_text": translated_string_to_text(alert.header_text) if alert.HasField("header_text") else None,
                "description_text": translated_string_to_text(alert.description_text) if alert.HasField("description_text") else None,
                "url": translated_string_to_text(alert.url) if alert.HasField("url") else None,
            }
        )
    return pd.DataFrame(rows)


def enrich_vehicle_positions(vehicle_df: pd.DataFrame, static_tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    if vehicle_df.empty:
        return vehicle_df.copy()

    df = vehicle_df.copy()
    routes = static_tables.get("routes")
    stops = static_tables.get("stops")

    if routes is not None and not routes.empty and "route_id" in df.columns and "route_id" in routes.columns:
        df = ensure_string_key(df, "route_id")
        routes = ensure_string_key(routes, "route_id")
        route_cols = [
            c
            for c in [
                "route_id",
                "route_short_name",
                "route_long_name",
                "route_desc",
                "route_type",
                "route_color",
                "route_text_color",
            ]
            if c in routes.columns
        ]
        df = df.merge(routes[route_cols].drop_duplicates("route_id"), on="route_id", how="left")

    if stops is not None and not stops.empty and "stop_id" in df.columns and "stop_id" in stops.columns:
        df = ensure_string_key(df, "stop_id")
        stops = ensure_string_key(stops, "stop_id")
        stop_cols = [
            c
            for c in ["stop_id", "stop_name", "stop_lat", "stop_lon", "zone_id", "location_type", "parent_station"]
            if c in stops.columns
        ]
        df = df.merge(stops[stop_cols].drop_duplicates("stop_id"), on="stop_id", how="left")

    return df


def build_vehicle_map_html(vehicle_df: pd.DataFrame) -> str | None:
    if vehicle_df.empty or not {"latitude", "longitude"}.issubset(vehicle_df.columns):
        return None
    try:
        import folium

        df = vehicle_df.copy()
        df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
        df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
        df = df.dropna(subset=["latitude", "longitude"])
        if df.empty:
            return None
        m = folium.Map(location=[df["latitude"].mean(), df["longitude"].mean()], zoom_start=11, tiles="CartoDB positron")
        for _, row in df.iterrows():
            popup = "<br>".join(
                [
                    f"vehicle_id: {row.get('vehicle_id')}",
                    f"route_id: {row.get('route_id')}",
                    f"route: {row.get('route_short_name')}",
                    f"stop: {row.get('stop_name')}",
                    f"speed_kmh: {row.get('speed_kmh')}",
                    f"timestamp: {row.get('timestamp_cdmx')}",
                ]
            )
            folium.CircleMarker(location=[row["latitude"], row["longitude"]], radius=4, popup=popup, fill=True).add_to(m)
        return m.get_root().render()
    except Exception:
        return None
