from __future__ import annotations

import io
import re
import time
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

from ..storage import make_snapshot_id, save_tables


SOURCE = "ecobici"
GBFS_INDEX_URL = "https://gbfs.mex.lyftbikes.com/gbfs/gbfs.json"
ECOBICI_OPEN_DATA_URL = "https://ecobici.cdmx.gob.mx/datos-abiertos/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; EcobiciDataClient/1.0; +https://ecobici.cdmx.gob.mx/datos-abiertos/)"
}


def run_ecobici_realtime(config_path: str, run_date: str | None = None) -> None:
    snapshot_id = make_snapshot_id()
    station_info, station_status, realtime, feed_urls = get_ecobici_realtime()
    save_tables(
        {
            "ecobici_gbfs_station_status": station_status,
            "ecobici_realtime_stations": realtime,
        },
        source=SOURCE,
        config_path=config_path,
        run_date=run_date,
        snapshot_id=snapshot_id,
    )


def run_ecobici_catalog(config_path: str, run_date: str | None = None) -> None:
    snapshot_id = make_snapshot_id()
    station_info, _station_status, _realtime, feed_urls = get_ecobici_realtime()
    feed_urls_df = pd.DataFrame([{"feed_name": name, "url": url} for name, url in sorted(feed_urls.items())])
    save_tables(
        {
            "ecobici_gbfs_feed_urls": feed_urls_df,
            "ecobici_gbfs_station_information": station_info,
        },
        source=SOURCE,
        config_path=config_path,
        run_date=run_date,
        snapshot_id=snapshot_id,
    )


def run_ecobici_historical(
    config_path: str,
    run_date: str | None = None,
    start_month: str | None = None,
    end_month: str | None = None,
) -> None:
    snapshot_id = make_snapshot_id()
    links = discover_historical_csv_links()
    if start_month is None and end_month is None:
        end_month = str(links["month"].max())
        start_month = end_month
    elif start_month is None:
        start_month = end_month
    elif end_month is None:
        end_month = start_month

    assert start_month is not None and end_month is not None
    raw = download_historical_range(start_month, end_month, links)
    normalized = normalize_historical_columns(raw)
    summaries = summarize_historical_trips(normalized)
    metadata_tables = build_metadata_tables(
        {
            "ecobici_historical_links": links,
            "ecobici_historico_raw": raw,
            "ecobici_historico_normalizado": normalized,
            **{f"ecobici_summary_{name}": df for name, df in summaries.items()},
        }
    )

    tables = {
        "ecobici_historical_links": links,
        "ecobici_historico_raw": raw,
        "ecobici_historico_normalizado": normalized,
        **{f"ecobici_summary_{name}": df for name, df in summaries.items()},
        **metadata_tables,
    }
    save_tables(tables, source=SOURCE, config_path=config_path, run_date=run_date, snapshot_id=snapshot_id)


def get_json(url: str, timeout: int = 30, retries: int = 3) -> dict[str, Any]:
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(1.5)
    raise RuntimeError(f"No se pudo descargar JSON desde {url}. Ultimo error: {last_error}")


def get_bytes(url: str, timeout: int = 60, retries: int = 3) -> bytes:
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=timeout)
            response.raise_for_status()
            return response.content
        except Exception as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(1.5)
    raise RuntimeError(f"No se pudo descargar archivo desde {url}. Ultimo error: {last_error}")


def get_gbfs_feed_urls(index_url: str = GBFS_INDEX_URL) -> dict[str, str]:
    gbfs_index = get_json(index_url)
    feeds = gbfs_index.get("data", {}).get("en", {}).get("feeds", [])
    if not feeds:
        for language_data in gbfs_index.get("data", {}).values():
            feeds = language_data.get("feeds", [])
            if feeds:
                break
    feed_urls = {feed.get("name"): feed.get("url") for feed in feeds if feed.get("name") and feed.get("url")}
    if not feed_urls:
        raise ValueError("No se encontraron feeds dentro del indice GBFS.")
    return feed_urls


def fetch_gbfs_feed(feed_name: str, feed_urls: dict[str, str]) -> dict[str, Any]:
    if feed_name not in feed_urls:
        raise KeyError(f"Feed {feed_name} no encontrado. Feeds disponibles: {sorted(feed_urls)}")
    return get_json(feed_urls[feed_name])


def gbfs_station_information_to_df(payload: dict[str, Any]) -> pd.DataFrame:
    df = pd.json_normalize(payload.get("data", {}).get("stations", []))
    if not df.empty and "name" in df.columns:
        df = df.rename(columns={"name": "station_name"})
    return df


def gbfs_station_status_to_df(payload: dict[str, Any]) -> pd.DataFrame:
    df = pd.json_normalize(payload.get("data", {}).get("stations", []))
    expected_cols = [
        "station_id",
        "num_bikes_available",
        "num_docks_available",
        "num_bikes_disabled",
        "num_docks_disabled",
        "is_installed",
        "is_renting",
        "is_returning",
        "last_reported",
    ]
    for col in expected_cols:
        if col not in df.columns:
            df[col] = pd.NA
    if "last_reported" in df.columns:
        df["last_reported_datetime"] = pd.to_datetime(df["last_reported"], unit="s", errors="coerce")
    return df


def get_ecobici_realtime() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, str]]:
    feed_urls = get_gbfs_feed_urls()
    station_info = gbfs_station_information_to_df(fetch_gbfs_feed("station_information", feed_urls))
    station_status = gbfs_station_status_to_df(fetch_gbfs_feed("station_status", feed_urls))
    realtime = station_info.merge(station_status, on="station_id", how="left", suffixes=("_info", "_status"))
    if "capacity" in realtime.columns:
        realtime["capacity"] = pd.to_numeric(realtime["capacity"], errors="coerce")
    for col in ["num_bikes_available", "num_docks_available", "num_bikes_disabled", "num_docks_disabled"]:
        if col in realtime.columns:
            realtime[col] = pd.to_numeric(realtime[col], errors="coerce")
    if {"num_bikes_available", "capacity"}.issubset(realtime.columns):
        realtime["bike_availability_pct"] = (realtime["num_bikes_available"] / realtime["capacity"]).clip(lower=0, upper=1)
    if {"num_docks_available", "capacity"}.issubset(realtime.columns):
        realtime["dock_availability_pct"] = (realtime["num_docks_available"] / realtime["capacity"]).clip(lower=0, upper=1)
    return station_info, station_status, realtime, feed_urls


def discover_historical_csv_links(open_data_url: str = ECOBICI_OPEN_DATA_URL) -> pd.DataFrame:
    html = get_bytes(open_data_url, timeout=60).decode("utf-8", errors="replace")
    soup = BeautifulSoup(html, "html.parser")
    month_pattern = re.compile(r"^20\d{2}-\d{2}$")
    records = []
    for a in soup.find_all("a"):
        text = a.get_text(strip=True)
        href = a.get("href")
        if href and month_pattern.match(text):
            records.append({"month": text, "url": urljoin(open_data_url, href)})
    df_links = pd.DataFrame(records)
    if df_links.empty:
        raise ValueError("No se encontraron links historicos tipo YYYY-MM.")
    return df_links.drop_duplicates(subset=["month", "url"]).sort_values("month").reset_index(drop=True)


def read_csv_bytes_safely(file_bytes: bytes, source_url: str = "") -> pd.DataFrame:
    if zipfile.is_zipfile(io.BytesIO(file_bytes)):
        with zipfile.ZipFile(io.BytesIO(file_bytes)) as z:
            dfs = []
            for csv_name in [name for name in z.namelist() if name.lower().endswith(".csv")]:
                with z.open(csv_name) as f:
                    df_part = read_csv_bytes_safely(f.read(), f"{source_url}::{csv_name}")
                    df_part["_source_file"] = csv_name
                    dfs.append(df_part)
            if not dfs:
                raise ValueError(f"El ZIP no contiene CSVs: {source_url}")
            return pd.concat(dfs, ignore_index=True)

    last_error: Exception | None = None
    for encoding in ["utf-8", "utf-8-sig", "latin1", "cp1252"]:
        for sep in [",", ";", "\t"]:
            try:
                df = pd.read_csv(io.BytesIO(file_bytes), encoding=encoding, sep=sep, low_memory=False)
                if df.shape[1] >= 2:
                    return df
            except Exception as exc:
                last_error = exc
    raise RuntimeError(f"No se pudo leer CSV: {source_url}. Ultimo error: {last_error}")


def download_historical_range(start_month: str, end_month: str, links: pd.DataFrame) -> pd.DataFrame:
    selected = links.loc[(links["month"] >= start_month) & (links["month"] <= end_month)].copy()
    if selected.empty:
        raise ValueError(f"No hay meses disponibles entre {start_month} y {end_month}.")
    dfs = []
    for _, row in selected.iterrows():
        file_bytes = get_bytes(row["url"], timeout=120)
        df = read_csv_bytes_safely(file_bytes, source_url=row["url"])
        df["_month"] = row["month"]
        df["_source_url"] = row["url"]
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)


def normalize_historical_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    def clean_col(col: str) -> str:
        col = str(col).strip().lower()
        for source, target in [("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"), ("ñ", "n")]:
            col = col.replace(source, target)
        col = re.sub(r"[^a-z0-9]+", "_", col)
        return re.sub(r"_+", "_", col).strip("_")

    df.columns = [clean_col(col) for col in df.columns]
    renames = {
        "genero_usuario": "user_gender",
        "edad_usuario": "user_age",
        "bici": "bike_id",
        "ciclo_estacion_retiro": "start_station_id",
        "fecha_retiro": "start_date",
        "hora_retiro": "start_time",
        "ciclo_estacion_arribo": "end_station_id",
        "fecha_arribo": "end_date",
        "hora_arribo": "end_time",
    }
    df = df.rename(columns={key: value for key, value in renames.items() if key in df.columns})
    if {"start_date", "start_time"}.issubset(df.columns):
        df["started_at"] = pd.to_datetime(
            df["start_date"].astype(str) + " " + df["start_time"].astype(str), errors="coerce", dayfirst=True
        )
    if {"end_date", "end_time"}.issubset(df.columns):
        df["ended_at"] = pd.to_datetime(
            df["end_date"].astype(str) + " " + df["end_time"].astype(str), errors="coerce", dayfirst=True
        )
    if {"started_at", "ended_at"}.issubset(df.columns):
        df["duration_minutes"] = (df["ended_at"] - df["started_at"]).dt.total_seconds() / 60
    if "started_at" in df.columns:
        df["start_hour"] = df["started_at"].dt.hour
        df["start_date_only"] = df["started_at"].dt.date
        df["start_weekday"] = df["started_at"].dt.day_name()
    return df


def summarize_historical_trips(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    summaries: dict[str, pd.DataFrame] = {}
    if "start_hour" in df.columns:
        summaries["trips_by_hour"] = df.groupby("start_hour", dropna=False).size().reset_index(name="trips").sort_values("start_hour")
    if "start_date_only" in df.columns:
        summaries["trips_by_date"] = (
            df.groupby("start_date_only", dropna=False).size().reset_index(name="trips").sort_values("start_date_only")
        )
    if "start_station_id" in df.columns:
        summaries["top_start_stations"] = (
            df.groupby("start_station_id", dropna=False).size().reset_index(name="trips").sort_values("trips", ascending=False).head(30)
        )
    if "end_station_id" in df.columns:
        summaries["top_end_stations"] = (
            df.groupby("end_station_id", dropna=False).size().reset_index(name="trips").sort_values("trips", ascending=False).head(30)
        )
    if {"start_station_id", "end_station_id"}.issubset(df.columns):
        summaries["top_od_flows"] = (
            df.groupby(["start_station_id", "end_station_id"], dropna=False)
            .size()
            .reset_index(name="trips")
            .sort_values("trips", ascending=False)
            .head(50)
        )
    if "duration_minutes" in df.columns:
        summaries["duration_stats"] = pd.DataFrame(
            {
                "metric": ["count", "mean", "median", "p90", "p95", "max"],
                "value": [
                    df["duration_minutes"].count(),
                    df["duration_minutes"].mean(),
                    df["duration_minutes"].median(),
                    df["duration_minutes"].quantile(0.90),
                    df["duration_minutes"].quantile(0.95),
                    df["duration_minutes"].max(),
                ],
            }
        )
    return summaries


def metadata_report(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    rows = []
    for col in df.columns:
        sample_series = df[col].dropna()
        rows.append(
            {
                "table_name": table_name,
                "column": col,
                "dtype": str(df[col].dtype),
                "non_null_count": int(df[col].notna().sum()),
                "null_count": int(df[col].isna().sum()),
                "null_pct": round(float(df[col].isna().mean()), 4) if len(df) else 0,
                "unique_values": int(df[col].nunique(dropna=True)),
                "sample_value": None if sample_series.empty else str(sample_series.iloc[0])[:120],
            }
        )
    return pd.DataFrame(rows)


def dataset_summary(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "table_name": table_name,
                "rows": len(df),
                "columns": len(df.columns),
                "duplicated_rows": int(df.duplicated().sum()) if not df.empty else 0,
                "memory_mb": round(df.memory_usage(deep=True).sum() / 1024**2, 3),
            }
        ]
    )


def build_metadata_tables(tables: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    metadata = pd.concat([metadata_report(df, name) for name, df in tables.items()], ignore_index=True)
    dataset = pd.concat([dataset_summary(df, name) for name, df in tables.items()], ignore_index=True)
    datetime_frames = [datetime_summary(df, name) for name, df in tables.items()]
    datetime_frames = [df for df in datetime_frames if not df.empty]
    numeric_frames = [numeric_summary(df, name) for name, df in tables.items()]
    numeric_frames = [df for df in numeric_frames if not df.empty]
    return {
        "ecobici_metadata_columns": metadata,
        "ecobici_dataset_summary": dataset,
        "ecobici_datetime_summary": pd.concat(datetime_frames, ignore_index=True) if datetime_frames else pd.DataFrame(),
        "ecobici_numeric_summary": pd.concat(numeric_frames, ignore_index=True) if numeric_frames else pd.DataFrame(),
    }


def datetime_summary(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    rows = []
    for col in df.columns:
        series = pd.to_datetime(df[col], errors="coerce") if df[col].dtype == object else df[col]
        if pd.api.types.is_datetime64_any_dtype(series) and series.notna().sum() > 0:
            rows.append(
                {
                    "table_name": table_name,
                    "datetime_column": col,
                    "min_datetime": series.min(),
                    "max_datetime": series.max(),
                    "non_null_count": int(series.notna().sum()),
                }
            )
    return pd.DataFrame(rows)


def numeric_summary(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    num_cols = df.select_dtypes(include="number").columns.tolist()
    if not num_cols:
        return pd.DataFrame()
    summary = df[num_cols].describe(percentiles=[0.25, 0.5, 0.75, 0.9, 0.95]).T
    summary = summary.reset_index().rename(columns={"index": "column"})
    summary.insert(0, "table_name", table_name)
    return summary
