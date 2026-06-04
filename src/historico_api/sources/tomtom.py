from __future__ import annotations

import json
import os
import time
from datetime import datetime
from typing import Any

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..storage import make_snapshot_id, save_artifact, save_tables


SOURCE = "tomtom"
CDMX_BBOX = {
    "min_lon": -99.364924,
    "min_lat": 19.048237,
    "max_lon": -98.940302,
    "max_lat": 19.592757,
}
CDMX_CENTER = [19.432608, -99.133209]
TRAFFIC_POINTS = [
    {"name": "Centro Historico - Zocalo", "lat": 19.432608, "lon": -99.133209},
    {"name": "Paseo de la Reforma - Angel", "lat": 19.426978, "lon": -99.167665},
    {"name": "Insurgentes Sur - WTC", "lat": 19.393246, "lon": -99.173205},
    {"name": "Viaducto - Eje Central", "lat": 19.401836, "lon": -99.141978},
    {"name": "Periferico Sur - San Angel", "lat": 19.337458, "lon": -99.190733},
    {"name": "Circuito Interior - Aeropuerto", "lat": 19.436190, "lon": -99.082571},
    {"name": "Calzada de Tlalpan - Portales", "lat": 19.369956, "lon": -99.143641},
    {"name": "Miguel Angel de Quevedo - Coyoacan", "lat": 19.346658, "lon": -99.180880},
    {"name": "Universidad - CU", "lat": 19.324596, "lon": -99.184971},
    {"name": "Santa Fe - Vasco de Quiroga", "lat": 19.365729, "lon": -99.259145},
    {"name": "Polanco - Masaryk", "lat": 19.433905, "lon": -99.195116},
    {"name": "Condesa - Tamaulipas", "lat": 19.411803, "lon": -99.174294},
]
ICON_CATEGORY_MAP = {
    0: "Unknown",
    1: "Accident",
    2: "Fog",
    3: "Dangerous conditions",
    4: "Rain",
    5: "Ice",
    6: "Jam",
    7: "Lane closed",
    8: "Road closed",
    9: "Road works",
    10: "Wind",
    11: "Flooding",
    14: "Broken down vehicle",
}


def run_tomtom(config_path: str, run_date: str | None = None) -> None:
    snapshot_id = make_snapshot_id()
    key = os.getenv("TOMTOM", os.getenv("TOMTOM_KEY", "")).strip()
    if not key:
        raise ValueError("Configura secret TOMTOM o TOMTOM_KEY en GitHub Actions.")

    session = build_session()
    df_incidents, _ = get_tomtom_incidents(session, key)
    df_flow = get_flow_table(session, key)
    df_flow["traffic_status"] = df_flow.apply(
        lambda r: classify_congestion(r.get("speed_ratio"), r.get("road_closure")), axis=1
    )

    save_tables(
        {
            "tomtom_cdmx_incidents": df_incidents,
            "tomtom_cdmx_flow": df_flow,
        },
        source=SOURCE,
        config_path=config_path,
        run_date=run_date,
        snapshot_id=snapshot_id,
    )

    html = build_map_html(df_incidents, df_flow)
    save_artifact(
        name="tomtom_cdmx_traffic_map",
        suffix="html",
        content=html,
        source=SOURCE,
        run_date=run_date,
        snapshot_id=snapshot_id,
    )


def build_session() -> requests.Session:
    session = requests.Session()
    retry_strategy = Retry(
        total=5,
        connect=5,
        read=5,
        backoff_factor=1.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update({"User-Agent": "Mozilla/5.0 GitHubActions TomTom Traffic", "Accept": "application/json"})
    return session


def extract_geometry_point(geometry: dict[str, Any]) -> tuple[float | None, float | None]:
    if not geometry:
        return None, None
    geom_type = geometry.get("type")
    coords = geometry.get("coordinates")
    if not coords:
        return None, None
    if geom_type == "Point":
        lon, lat = coords[0], coords[1]
        return lat, lon
    if geom_type == "LineString":
        lon, lat = coords[len(coords) // 2][0], coords[len(coords) // 2][1]
        return lat, lon
    return None, None


def get_tomtom_incidents(session: requests.Session, key: str) -> tuple[pd.DataFrame, dict[str, Any]]:
    bbox_str = f"{CDMX_BBOX['min_lon']},{CDMX_BBOX['min_lat']},{CDMX_BBOX['max_lon']},{CDMX_BBOX['max_lat']}"
    url = "https://api.tomtom.com/traffic/services/5/incidentDetails"
    fields = (
        "{incidents{type,geometry{type,coordinates},properties{id,iconCategory,magnitudeOfDelay,"
        "events{description,code,iconCategory},startTime,endTime,from,to,length,delay,roadNumbers,"
        "timeValidity,probabilityOfOccurrence,numberOfReports,lastReportTime}}}"
    )
    params = {
        "key": key,
        "bbox": bbox_str,
        "fields": fields,
        "language": "es-ES",
        "timeValidityFilter": "present",
    }
    response = session.get(url, params=params, timeout=(20, 90))
    response.raise_for_status()
    data = response.json()
    rows: list[dict[str, Any]] = []
    for incident in data.get("incidents", []):
        geometry = incident.get("geometry", {})
        props = incident.get("properties", {})
        lat, lon = extract_geometry_point(geometry)
        events = props.get("events", [])
        icon_category = props.get("iconCategory")
        rows.append(
            {
                "extraction_timestamp": datetime.utcnow().isoformat(),
                "incident_id": props.get("id"),
                "incident_type": incident.get("type"),
                "geometry_type": geometry.get("type"),
                "lat": lat,
                "lon": lon,
                "icon_category": icon_category,
                "icon_category_desc": ICON_CATEGORY_MAP.get(icon_category, "Other / Unknown"),
                "magnitude_of_delay": props.get("magnitudeOfDelay"),
                "delay_seconds": props.get("delay"),
                "length_meters": props.get("length"),
                "from": props.get("from"),
                "to": props.get("to"),
                "road_numbers": ",".join(props.get("roadNumbers", [])) if props.get("roadNumbers") else None,
                "time_validity": props.get("timeValidity"),
                "probability": props.get("probabilityOfOccurrence"),
                "number_of_reports": props.get("numberOfReports"),
                "start_time": props.get("startTime"),
                "end_time": props.get("endTime"),
                "last_report_time": props.get("lastReportTime"),
                "event_descriptions": " | ".join([ev.get("description", "") for ev in events if ev.get("description")])
                or None,
                "event_codes": ",".join([str(ev.get("code")) for ev in events if ev.get("code") is not None]) or None,
                "raw_geometry": json.dumps(geometry, ensure_ascii=False),
                "raw_properties": json.dumps(props, ensure_ascii=False),
            }
        )
    return pd.DataFrame(rows), data


def safe_get(dct: dict[str, Any], path: list[str], default: Any = None) -> Any:
    current: Any = dct
    for key in path:
        if not isinstance(current, dict):
            return default
        current = current.get(key, default)
    return current


def get_flow_table(session: requests.Session, key: str) -> pd.DataFrame:
    rows = []
    for point in TRAFFIC_POINTS:
        rows.append(get_flow_segment(session, key, point["lat"], point["lon"], point["name"]))
        time.sleep(0.25)
    return pd.DataFrame(rows)


def get_flow_segment(session: requests.Session, key: str, lat: float, lon: float, point_name: str) -> dict[str, Any]:
    url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/15/json"
    params = {"key": key, "point": f"{lat},{lon}", "unit": "kmph", "openLr": "false"}
    response = session.get(url, params=params, timeout=(20, 90))
    if response.status_code != 200:
        return {
            "extraction_timestamp": datetime.utcnow().isoformat(),
            "point_name": point_name,
            "input_lat": lat,
            "input_lon": lon,
            "status_code": response.status_code,
            "error": response.text[:1000],
        }
    data = response.json()
    fsd = data.get("flowSegmentData", {})
    current_speed = fsd.get("currentSpeed")
    free_flow_speed = fsd.get("freeFlowSpeed")
    current_travel_time = fsd.get("currentTravelTime")
    free_flow_travel_time = fsd.get("freeFlowTravelTime")
    speed_ratio = current_speed / free_flow_speed if current_speed is not None and free_flow_speed not in [None, 0] else None
    delay_seconds = (
        current_travel_time - free_flow_travel_time
        if current_travel_time is not None and free_flow_travel_time is not None
        else None
    )
    delay_ratio = (
        current_travel_time / free_flow_travel_time
        if current_travel_time not in [None, 0] and free_flow_travel_time not in [None, 0]
        else None
    )
    coords = safe_get(fsd, ["coordinates", "coordinate"], default=[])
    segment_lat = segment_lon = None
    if isinstance(coords, list) and coords:
        mid = coords[len(coords) // 2]
        segment_lat = mid.get("latitude")
        segment_lon = mid.get("longitude")
    return {
        "extraction_timestamp": datetime.utcnow().isoformat(),
        "point_name": point_name,
        "input_lat": lat,
        "input_lon": lon,
        "segment_lat": segment_lat,
        "segment_lon": segment_lon,
        "frc": fsd.get("frc"),
        "current_speed_kmph": current_speed,
        "free_flow_speed_kmph": free_flow_speed,
        "speed_ratio": speed_ratio,
        "congestion_index": 1 - speed_ratio if speed_ratio is not None else None,
        "current_travel_time_seconds": current_travel_time,
        "free_flow_travel_time_seconds": free_flow_travel_time,
        "delay_seconds": delay_seconds,
        "delay_ratio": delay_ratio,
        "confidence": fsd.get("confidence"),
        "road_closure": fsd.get("roadClosure"),
        "status_code": response.status_code,
        "error": None,
        "raw_response": json.dumps(data, ensure_ascii=False),
    }


def classify_congestion(speed_ratio: Any, road_closure: Any = False) -> str:
    if road_closure is True:
        return "Cierre vial"
    if pd.isna(speed_ratio):
        return "Sin dato"
    if speed_ratio >= 0.85:
        return "Flujo normal"
    if speed_ratio >= 0.65:
        return "Congestion ligera"
    if speed_ratio >= 0.40:
        return "Congestion media"
    return "Congestion severa"


def build_map_html(df_incidents: pd.DataFrame, df_flow: pd.DataFrame) -> str:
    import folium

    m = folium.Map(location=CDMX_CENTER, zoom_start=11, tiles="CartoDB positron")
    folium.Rectangle(
        bounds=[[CDMX_BBOX["min_lat"], CDMX_BBOX["min_lon"]], [CDMX_BBOX["max_lat"], CDMX_BBOX["max_lon"]]],
        popup="Bounding box CDMX usado para incidentes",
        fill=False,
    ).add_to(m)

    if not df_incidents.empty:
        for _, row in df_incidents.dropna(subset=["lat", "lon"]).iterrows():
            popup = (
                f"<b>Incidente:</b> {row.get('icon_category_desc')}<br>"
                f"<b>De:</b> {row.get('from')}<br>"
                f"<b>A:</b> {row.get('to')}<br>"
                f"<b>Retraso:</b> {row.get('delay_seconds')} segundos<br>"
                f"<b>Longitud:</b> {row.get('length_meters')} metros<br>"
                f"<b>Descripcion:</b> {row.get('event_descriptions')}<br>"
                f"<b>Ultimo reporte:</b> {row.get('last_report_time')}"
            )
            folium.CircleMarker(location=[row["lat"], row["lon"]], radius=5, popup=popup, fill=True).add_to(m)

    for _, row in df_flow.iterrows():
        lat = row.get("segment_lat") if pd.notna(row.get("segment_lat")) else row.get("input_lat")
        lon = row.get("segment_lon") if pd.notna(row.get("segment_lon")) else row.get("input_lon")
        popup = (
            f"<b>Punto:</b> {row.get('point_name')}<br>"
            f"<b>Estado:</b> {row.get('traffic_status')}<br>"
            f"<b>Velocidad actual:</b> {row.get('current_speed_kmph')} km/h<br>"
            f"<b>Velocidad libre:</b> {row.get('free_flow_speed_kmph')} km/h<br>"
            f"<b>Speed ratio:</b> {row.get('speed_ratio')}<br>"
            f"<b>Delay:</b> {row.get('delay_seconds')} segundos<br>"
            f"<b>Confianza:</b> {row.get('confidence')}<br>"
            f"<b>Cierre:</b> {row.get('road_closure')}"
        )
        folium.Marker(location=[lat, lon], popup=popup, tooltip=row.get("point_name")).add_to(m)
    return m.get_root().render()
