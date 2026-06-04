from __future__ import annotations

import math
import os
import re
import time
import unicodedata
from typing import Any
from urllib.parse import quote

import pandas as pd
import requests

from ..storage import make_snapshot_id, save_artifact, save_tables


SOURCE = "denue"
BASE_URL = "https://www.inegi.org.mx/app/api/denue/v1/consulta"
CDMX_ENTIDAD = "09"
SECTOR_EDUCATIVO = "61"
RADIOS_METROS = [500, 1000, 2000]
CONDICION_ESCOLAR = "universidad,escuela,colegio,instituto,facultad,preparatoria,bachillerato,secundaria,primaria"
HEADERS = {"User-Agent": "Mozilla/5.0 denue-cdmx-educacion/1.0"}


CAMPUS_DATA = [
    {"campus_id": "unam_cu", "universidad": "UNAM", "campus": "Ciudad Universitaria", "lat": 19.3322, "lon": -99.1861, "tipo": "publica", "comentario": "Zona universitaria grande."},
    {"campus_id": "ipn_zacatenco", "universidad": "IPN", "campus": "Zacatenco", "lat": 19.5008, "lon": -99.1466, "tipo": "publica", "comentario": "Concentracion universitaria fuerte al norte de CDMX."},
    {"campus_id": "uam_xochimilco", "universidad": "UAM", "campus": "Xochimilco", "lat": 19.3048, "lon": -99.1030, "tipo": "publica", "comentario": "Campus relevante para conectividad sur-oriente."},
    {"campus_id": "uam_iztapalapa", "universidad": "UAM", "campus": "Iztapalapa", "lat": 19.3605, "lon": -99.0738, "tipo": "publica", "comentario": "Zona importante para movilidad en oriente."},
    {"campus_id": "uam_azcapotzalco", "universidad": "UAM", "campus": "Azcapotzalco", "lat": 19.5038, "lon": -99.1866, "tipo": "publica", "comentario": "Campus con entorno industrial y educativo."},
    {"campus_id": "ipn_upiicsa", "universidad": "IPN", "campus": "UPIICSA", "lat": 19.3957, "lon": -99.0925, "tipo": "publica", "comentario": "Zona de alta presion vial."},
    {"campus_id": "itesm_ccm", "universidad": "ITESM", "campus": "Campus Ciudad de Mexico", "lat": 19.2839, "lon": -99.1353, "tipo": "privada", "comentario": "Campus privado relevante al sur."},
    {"campus_id": "ibero_santa_fe", "universidad": "Universidad Iberoamericana", "campus": "Santa Fe", "lat": 19.3677, "lon": -99.2634, "tipo": "privada", "comentario": "Zona con dependencia fuerte de auto."},
    {"campus_id": "itam_rio_hondo", "universidad": "ITAM", "campus": "Rio Hondo", "lat": 19.3454, "lon": -99.1997, "tipo": "privada", "comentario": "Campus con presion vial local."},
    {"campus_id": "up_mixcoac", "universidad": "Universidad Panamericana", "campus": "Mixcoac", "lat": 19.3740, "lon": -99.1830, "tipo": "privada", "comentario": "Zona urbana densa."},
    {"campus_id": "uacm_san_lorenzo", "universidad": "UACM", "campus": "San Lorenzo Tezonco", "lat": 19.3066, "lon": -99.0639, "tipo": "publica", "comentario": "Movilidad escolar en periferia sur-oriente."},
    {"campus_id": "la_salle_condesa", "universidad": "Universidad La Salle", "campus": "Condesa", "lat": 19.4099, "lon": -99.1815, "tipo": "privada", "comentario": "Zona central y densa."},
]


def run_denue(config_path: str, run_date: str | None = None) -> None:
    token = os.getenv("INEGI_DENUE_TOKEN", "").strip()
    if not token:
        raise ValueError("Configura secret INEGI_DENUE_TOKEN en GitHub Actions.")

    snapshot_id = make_snapshot_id()
    df_campus = pd.DataFrame(CAMPUS_DATA)
    df_educacion = add_strategic_flags(
        paginate_buscar_area_act(token=token, entidad=CDMX_ENTIDAD, sector=SECTOR_EDUCATIVO)
    )
    if df_educacion.empty:
        df_superior = pd.DataFrame()
    else:
        df_superior = df_educacion[
            (df_educacion["nivel_educativo_estimado"] == "superior_universitaria")
            | (df_educacion["flag_universidad"] == True)
        ].copy()
    df_campus_establecimientos = query_campus_zones(df_campus, token, RADIOS_METROS)
    df_resumen_campus = summarize_campus_zones(df_campus_establecimientos)
    df_resumen_nivel = summarize_by_level(df_campus_establecimientos)
    df_metadata = pd.concat(
        [
            metadata_report(df, name)
            for name, df in {
                "campus_cdmx_base": df_campus,
                "denue_cdmx_sector_61_servicios_educativos": df_educacion,
                "denue_cdmx_educacion_superior_universitaria": df_superior,
                "denue_establecimientos_alrededor_campus": df_campus_establecimientos,
                "denue_resumen_zonas_universitarias": df_resumen_campus,
                "denue_resumen_por_nivel_educativo": df_resumen_nivel,
            }.items()
        ],
        ignore_index=True,
    )

    save_tables(
        {
            "campus_cdmx_base": df_campus,
            "denue_cdmx_sector_61_servicios_educativos": df_educacion,
            "denue_cdmx_educacion_superior_universitaria": df_superior,
            "denue_establecimientos_alrededor_campus": df_campus_establecimientos,
            "denue_resumen_zonas_universitarias": df_resumen_campus,
            "denue_resumen_por_nivel_educativo": df_resumen_nivel,
            "denue_metadata_reporte": df_metadata,
        },
        source=SOURCE,
        config_path=config_path,
        run_date=run_date,
        snapshot_id=snapshot_id,
    )

    html = create_map_html(df_campus, df_campus_establecimientos)
    save_artifact(
        name="mapa_denue_zonas_universitarias_cdmx",
        suffix="html",
        content=html,
        source=SOURCE,
        run_date=run_date,
        snapshot_id=snapshot_id,
    )


def strip_accents(text: Any) -> str:
    if pd.isna(text):
        return ""
    normalized = unicodedata.normalize("NFD", str(text))
    return "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")


def clean_text(text: Any) -> str:
    return re.sub(r"\s+", " ", strip_accents(text).lower().strip())


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius = 6371000
    phi1 = math.radians(float(lat1))
    phi2 = math.radians(float(lat2))
    dphi = math.radians(float(lat2) - float(lat1))
    dlambda = math.radians(float(lon2) - float(lon1))
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return radius * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def denue_get_json(url: str, timeout: int = 60, retries: int = 3) -> Any:
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, dict) and "Mensaje" in data:
                raise RuntimeError(f"Mensaje de API: {data}")
            return data
        except Exception as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(1.0)
    raise RuntimeError(f"No se pudo consultar DENUE. Ultimo error: {last_error}")


def normalize_denue_df(data: Any) -> pd.DataFrame:
    if not data:
        return pd.DataFrame()
    df = pd.DataFrame(data)
    if df.empty:
        return df
    rename_map = {
        "CLEE": "clee",
        "Id": "id_establecimiento",
        "Nombre": "nombre",
        "Razon_social": "razon_social",
        "Clase_actividad": "clase_actividad",
        "Estrato": "estrato",
        "Tipo_vialidad": "tipo_vialidad",
        "Calle": "calle",
        "Num_Exterior": "num_exterior",
        "Num_Interior": "num_interior",
        "Colonia": "colonia",
        "CP": "cp",
        "Ubicacion": "ubicacion",
        "Telefono": "telefono",
        "Correo_e": "correo_e",
        "Sitio_internet": "sitio_internet",
        "Tipo": "tipo_establecimiento",
        "Longitud": "longitud",
        "Latitud": "latitud",
        "CentroComercial": "centro_comercial",
        "TipoCentroComercial": "tipo_centro_comercial",
        "NumLocal": "num_local",
        "AGEB": "ageb",
        "Manzana": "manzana",
        "Edificio": "edificio",
        "Clase": "id_clase_actividad",
        "Sector": "id_sector",
        "Subsector": "id_subsector",
        "Rama": "id_rama",
        "Subrama": "id_subrama",
        "Fecha_Alta": "fecha_alta",
        "AreaGeo": "area_geo",
    }
    df = df.rename(columns={key: value for key, value in rename_map.items() if key in df.columns})
    for col in [
        "id_establecimiento",
        "nombre",
        "razon_social",
        "clase_actividad",
        "estrato",
        "calle",
        "colonia",
        "cp",
        "ubicacion",
        "longitud",
        "latitud",
    ]:
        if col not in df.columns:
            df[col] = pd.NA
    df["latitud"] = pd.to_numeric(df["latitud"], errors="coerce")
    df["longitud"] = pd.to_numeric(df["longitud"], errors="coerce")
    for col in ["nombre", "razon_social", "clase_actividad", "estrato", "colonia", "ubicacion"]:
        df[col + "_clean"] = df[col].apply(clean_text)
    return df


def buscar_por_punto(token: str, condicion: str, lat: float, lon: float, metros: int) -> pd.DataFrame:
    condicion_url = quote(str(condicion), safe=",")
    url = f"{BASE_URL}/Buscar/{condicion_url}/{lat},{lon}/{metros}/{token}"
    return normalize_denue_df(denue_get_json(url))


def buscar_area_act(
    token: str,
    entidad: str = "09",
    sector: str = "61",
    nombre: str = "0",
    inicio: int = 1,
    fin: int = 1000,
) -> pd.DataFrame:
    nombre_url = quote(str(nombre), safe=",")
    url = f"{BASE_URL}/BuscarAreaAct/{entidad}/0/0/0/0/{sector}/0/0/0/{nombre_url}/{inicio}/{fin}/0/{token}"
    return normalize_denue_df(denue_get_json(url))


def paginate_buscar_area_act(
    token: str,
    entidad: str = "09",
    sector: str = "61",
    page_size: int = 1000,
    max_pages: int = 80,
) -> pd.DataFrame:
    pages = []
    for page in range(max_pages):
        inicio = page * page_size + 1
        fin = (page + 1) * page_size
        df_page = buscar_area_act(token=token, entidad=entidad, sector=sector, inicio=inicio, fin=fin)
        if df_page.empty:
            break
        pages.append(df_page)
        if len(df_page) < page_size:
            break
        time.sleep(0.2)
    if not pages:
        return pd.DataFrame()
    df = pd.concat(pages, ignore_index=True)
    if "id_establecimiento" in df.columns:
        df = df.drop_duplicates(subset=["id_establecimiento"])
    return df


def classify_education_level(row: pd.Series) -> str:
    text = " ".join(
        [str(row.get("nombre_clean", "")), str(row.get("razon_social_clean", "")), str(row.get("clase_actividad_clean", ""))]
    )
    if any(x in text for x in ["universidad", "educacion superior", "facultad", "instituto tecnologico", "posgrado", "licenciatura", "centro de investigacion"]):
        return "superior_universitaria"
    if any(x in text for x in ["bachillerato", "preparatoria", "educacion media superior", "colegio de bachilleres", "conalep", "cch", "vocacional"]):
        return "media_superior"
    if "secundaria" in text:
        return "secundaria"
    if "primaria" in text:
        return "primaria"
    if any(x in text for x in ["preescolar", "kinder", "jardin de ninos"]):
        return "preescolar"
    if any(x in text for x in ["capacitacion", "academia", "idiomas", "computacion", "arte", "musica", "deporte", "regularizacion"]):
        return "capacitacion_otros"
    return "educativo_no_clasificado"


def add_strategic_flags(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    df = df.copy()
    for col in ["nombre_clean", "razon_social_clean", "clase_actividad_clean", "estrato_clean", "ubicacion_clean"]:
        if col not in df.columns:
            df[col] = ""
    df["nivel_educativo_estimado"] = df.apply(classify_education_level, axis=1)
    all_text = df["nombre_clean"].fillna("") + " " + df["razon_social_clean"].fillna("") + " " + df["clase_actividad_clean"].fillna("")
    df["flag_universidad"] = all_text.str.contains(
        "universidad|facultad|educacion superior|licenciatura|posgrado|instituto tecnologico", regex=True, na=False
    )
    df["flag_media_superior"] = all_text.str.contains(
        "bachillerato|preparatoria|media superior|vocacional|cch|conalep", regex=True, na=False
    )
    df["flag_educacion_basica"] = all_text.str.contains(
        "preescolar|primaria|secundaria|jardin de ninos", regex=True, na=False
    )
    df["estrato_ocupacion_estimado"] = df["estrato"].astype(str)
    return df


def query_campus_zones(df_campus: pd.DataFrame, token: str, radios: list[int]) -> pd.DataFrame:
    rows = []
    for _, campus in df_campus.iterrows():
        for radio in radios:
            try:
                df_zone = buscar_por_punto(token, CONDICION_ESCOLAR, campus["lat"], campus["lon"], radio)
                if df_zone.empty:
                    continue
                df_zone = add_strategic_flags(df_zone)
                df_zone["campus_id"] = campus["campus_id"]
                df_zone["universidad_base"] = campus["universidad"]
                df_zone["campus_base"] = campus["campus"]
                df_zone["campus_lat"] = campus["lat"]
                df_zone["campus_lon"] = campus["lon"]
                df_zone["radio_m"] = radio
                df_zone["campus_tipo"] = campus["tipo"]
                df_zone["distancia_campus_m"] = df_zone.apply(
                    lambda r: haversine_m(campus["lat"], campus["lon"], r["latitud"], r["longitud"])
                    if pd.notna(r["latitud"]) and pd.notna(r["longitud"])
                    else pd.NA,
                    axis=1,
                )
                rows.append(df_zone)
                time.sleep(0.2)
            except Exception:
                continue
    if not rows:
        return pd.DataFrame()
    df_all = pd.concat(rows, ignore_index=True)
    if {"campus_id", "radio_m", "id_establecimiento"}.issubset(df_all.columns):
        df_all = df_all.drop_duplicates(subset=["campus_id", "radio_m", "id_establecimiento"])
    return df_all


def summarize_campus_zones(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    summary = (
        df.groupby(["campus_id", "universidad_base", "campus_base", "campus_tipo", "radio_m"])
        .agg(
            establecimientos_educativos=("id_establecimiento", "nunique"),
            establecimientos_superior=("flag_universidad", "sum"),
            establecimientos_media_superior=("flag_media_superior", "sum"),
            establecimientos_basica=("flag_educacion_basica", "sum"),
            distancia_promedio_m=("distancia_campus_m", "mean"),
            distancia_min_m=("distancia_campus_m", "min"),
            distancia_max_m=("distancia_campus_m", "max"),
        )
        .reset_index()
    )
    summary["score_concentracion_educativa_raw"] = (
        summary["establecimientos_educativos"]
        + 2.0 * summary["establecimientos_superior"]
        + 1.5 * summary["establecimientos_media_superior"]
        + summary["establecimientos_basica"]
    )
    summary["score_concentracion_educativa_0_100"] = 0.0
    for radio in summary["radio_m"].unique():
        mask = summary["radio_m"] == radio
        x = summary.loc[mask, "score_concentracion_educativa_raw"]
        xmin, xmax = x.min(), x.max()
        summary.loc[mask, "score_concentracion_educativa_0_100"] = ((x - xmin) / (xmax - xmin) * 100) if xmax > xmin else 0
    summary["score_concentracion_educativa_0_100"] = summary["score_concentracion_educativa_0_100"].round(2)
    return summary.sort_values(["radio_m", "score_concentracion_educativa_0_100"], ascending=[True, False])


def summarize_by_level(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    return (
        df.groupby(["campus_id", "universidad_base", "campus_base", "radio_m", "nivel_educativo_estimado"])
        .agg(establecimientos=("id_establecimiento", "nunique"), distancia_promedio_m=("distancia_campus_m", "mean"))
        .reset_index()
        .sort_values(["campus_id", "radio_m", "establecimientos"], ascending=[True, True, False])
    )


def color_by_level(level: str) -> str:
    return {
        "superior_universitaria": "red",
        "media_superior": "orange",
        "primaria": "blue",
        "secundaria": "blue",
        "preescolar": "blue",
        "capacitacion_otros": "green",
    }.get(level, "gray")


def create_map_html(df_campus: pd.DataFrame, df_est: pd.DataFrame) -> str:
    import folium
    from folium.plugins import MarkerCluster

    m = folium.Map(location=[19.4326, -99.1332], zoom_start=11, tiles="CartoDB positron")
    for _, row in df_campus.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=f"<b>{row['universidad']}</b><br>Campus: {row['campus']}<br>Tipo: {row['tipo']}<br>{row['comentario']}",
            tooltip=f"{row['universidad']} - {row['campus']}",
            icon=folium.Icon(color="purple", icon="university", prefix="fa"),
        ).add_to(m)
        folium.Circle(location=[row["lat"], row["lon"]], radius=1000, color="purple", fill=False, weight=2, opacity=0.35).add_to(m)
    if not df_est.empty:
        cluster = MarkerCluster(name="Establecimientos educativos DENUE 1km").add_to(m)
        df_plot = df_est[df_est["radio_m"] == 1000].copy() if "radio_m" in df_est.columns else df_est
        for _, row in df_plot.iterrows():
            if pd.isna(row.get("latitud")) or pd.isna(row.get("longitud")):
                continue
            level = row.get("nivel_educativo_estimado", "educativo_no_clasificado")
            distance = row.get("distancia_campus_m", 0)
            distance_text = "" if pd.isna(distance) else f"{float(distance):.0f} m"
            popup = (
                f"<b>{row.get('nombre', '')}</b><br>"
                f"Clase: {row.get('clase_actividad', '')}<br>"
                f"Nivel estimado: {level}<br>"
                f"Campus cercano: {row.get('universidad_base', '')} - {row.get('campus_base', '')}<br>"
                f"Distancia campus: {distance_text}"
            )
            folium.CircleMarker(
                location=[row["latitud"], row["longitud"]],
                radius=4,
                color=color_by_level(level),
                fill=True,
                fill_opacity=0.65,
                popup=popup,
                tooltip=row.get("nombre", ""),
            ).add_to(cluster)
    folium.LayerControl().add_to(m)
    return m.get_root().render()


def metadata_report(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    rows = []
    for col in df.columns:
        sample = df[col].dropna()
        rows.append(
            {
                "table_name": table_name,
                "column": col,
                "dtype": str(df[col].dtype),
                "non_null": int(df[col].notna().sum()),
                "nulls": int(df[col].isna().sum()),
                "null_pct": round(float(df[col].isna().mean()), 4) if len(df) else 0,
                "unique_values": int(df[col].nunique(dropna=True)),
                "sample": None if sample.empty else str(sample.iloc[0])[:120],
            }
        )
    return pd.DataFrame(rows)
