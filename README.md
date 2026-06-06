# Historico de APIs de movilidad CDMX

Este repositorio genera historicos versionados de tablas provenientes de Metrobús, TomTom, ECOBICI, DENUE/INEGI y Google Maps Routes API. GitHub Actions ejecuta cada fuente con la periodicidad adecuada, guarda CSVs consultables en el repositorio y hace commits recurrentes con la nueva informacion.

## Estructura de datos

| Ruta | Uso |
| --- | --- |
| `data/current/<tabla>.csv` | Ultimo snapshot disponible de cada tabla. |
| `data/history/<tabla>/<snapshot_id>.csv` | Historico completo por tabla. |
| `data/manifests/*.json` | Manifiestos por corrida: fuente, snapshot, filas, columnas y rutas. |
| `data/artifacts/current/*.html` | Ultimo artefacto visual HTML, por ejemplo mapas. |
| `data/artifacts/history/<artefacto>/` | Historico de artefactos visuales. |
| `configs/tables.yml` | Catalogo de tablas, fuentes, periodicidad y columnas clave. |
| `docs/README_LECTURA_TABLAS.md` | Guia para consultar cada tabla. |
| `docs/periodicidad.md` | Criterio de programacion y schedules de GitHub Actions. |
| `docs/tablas.md` | Diccionario de tablas y columnas. |

## Fuentes cubiertas

| Fuente | Tablas principales | Workflow |
| --- | --- | --- |
| Metrobús GTFS-Realtime | `metrobus_vehicle_positions`, `metrobus_trip_updates`, `metrobus_alerts`, `metrobus_vehicle_positions_enriched` | `.github/workflows/metrobus-realtime.yml` |
| Metrobús GTFS estatico | `metrobus_gtfs_static_*` | `.github/workflows/metrobus-static.yml` |
| TomTom Traffic | `tomtom_cdmx_incidents`, `tomtom_cdmx_flow` | `.github/workflows/tomtom-traffic.yml` y campaña limitada `.github/workflows/tomtom-one-month-history.yml` |
| ECOBICI GBFS realtime | `ecobici_gbfs_station_status`, `ecobici_realtime_stations` | `.github/workflows/ecobici-realtime.yml` |
| ECOBICI catalogo | `ecobici_gbfs_feed_urls`, `ecobici_gbfs_station_information` | `.github/workflows/ecobici-catalog.yml` |
| ECOBICI historicos | `ecobici_historico_raw`, `ecobici_historico_normalizado`, `ecobici_summary_*`, metadatos | `.github/workflows/ecobici-historical.yml` |
| DENUE/INEGI | `campus_cdmx_base`, `denue_*` | `.github/workflows/denue.yml` |
| Google Routes API | `routes_api_*` | `.github/workflows/google-routes.yml` |

## Secrets requeridos

Configure estos secrets en `Settings > Secrets and variables > Actions`:

| Secret | Usado por |
| --- | --- |
| `METROBUS_USER` | Metrobús realtime y estatico. |
| `METROBUS_PASS` | Metrobús realtime y estatico. |
| `TOMTOM` | TomTom Traffic y campaña de 1 mes. |
| `INEGI_DENUE_TOKEN` | DENUE/INEGI. |
| `GOOGLE_MAPS_API_KEY` | Google Routes API. |
| `MAPS` | Alternativa aceptada para Google Routes API. |

No deje llaves ni usuarios dentro de notebooks o codigo versionado.

## Puesta en marcha

1. Suba este repositorio a GitHub.
2. Configure los secrets listados arriba.
3. En `Settings > Actions > General`, habilite `Read and write permissions`.
4. Ejecute manualmente estos workflows una vez para poblar `data/current`:
   `Metrobus GTFS static`, `ECOBICI catalog`, `DENUE INEGI`, `ECOBICI historical`, `Google Routes`.
5. Luego ejecute `Metrobus realtime`, `ECOBICI realtime` y `TomTom traffic` para crear los primeros snapshots dinamicos.

## Campaña TomTom de 1 mes

Para recolectar un historico acotado de TomTom sin saturar la API, use el workflow `TomTom one-month history` (`.github/workflows/tomtom-one-month-history.yml`). Este workflow consulta TomTom 5 veces al dia en horario operativo aproximado de CDMX y comparte el mismo grupo de concurrencia que `tomtom-traffic.yml`, por lo que no ejecuta dos extracciones TomTom en paralelo.

Pasos recomendados:

1. Configure el secret `TOMTOM`.
2. Cree estas repository variables en `Settings > Secrets and variables > Actions > Variables`:
   - `TOMTOM_HISTORY_ENABLED=true`
   - `TOMTOM_HISTORY_START_DATE=YYYY-MM-DD`
   - `TOMTOM_HISTORY_END_DATE=YYYY-MM-DD` (por ejemplo, 30 dias despues del inicio).
3. Si quiere evitar duplicar capturas con el workflow permanente, deshabilite temporalmente `TomTom traffic` mientras dure la campaña.
4. Ejecute manualmente `TomTom one-month history` para probar una captura o deje activo el schedule hasta la fecha final.

El schedule no corre si faltan las variables de inicio/fin o si `TOMTOM_HISTORY_ENABLED` no es `true`; esto evita corridas indefinidas por accidente.

## Ejecucion local

```bash
pip install -e .
python -m historico_api source ecobici_realtime --config configs/tables.yml
python -m historico_api docs --config configs/tables.yml
```

Comandos disponibles:

```bash
python -m historico_api source metrobus_realtime --config configs/tables.yml
python -m historico_api source metrobus_static --config configs/tables.yml
python -m historico_api source tomtom --config configs/tables.yml
python -m historico_api source ecobici_realtime --config configs/tables.yml
python -m historico_api source ecobici_catalog --config configs/tables.yml
python -m historico_api source ecobici_historical --config configs/tables.yml --start-month 2025-01 --end-month 2025-01
python -m historico_api source denue --config configs/tables.yml
python -m historico_api source google_routes --config configs/tables.yml
```

## Consulta rapida

Para leer la ultima version:

```python
import pandas as pd

df = pd.read_csv("data/current/ecobici_realtime_stations.csv")
```

Para leer todo el historico de una tabla:

```python
from pathlib import Path
import pandas as pd

paths = sorted(Path("data/history/tomtom_cdmx_flow").glob("*.csv"))
historico = pd.concat((pd.read_csv(path) for path in paths), ignore_index=True)
```

La guia completa de lectura por tabla esta en `docs/README_LECTURA_TABLAS.md`.
