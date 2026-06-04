# README de lectura de tablas

Todas las tablas se consultan igual:

- Ultima version: `data/current/<tabla>.csv`
- Historico: `data/history/<tabla>/*.csv`
- Manifiestos: `data/manifests/*.json`
- Mapas/HTML: `data/artifacts/current/*.html`

Ejemplo:

```python
from pathlib import Path
import pandas as pd

actual = pd.read_csv("data/current/routes_api_matriz.csv")
hist = pd.concat(
    (pd.read_csv(path) for path in sorted(Path("data/history/routes_api_matriz").glob("*.csv"))),
    ignore_index=True,
)
```

## Metadatos agregados

Cada CSV historizado incluye columnas tecnicas:

| Columna | Uso |
| --- | --- |
| `_snapshot_id` | Identificador unico de corrida, formato UTC `YYYYMMDDTHHMMSSZ`. |
| `_snapshot_date` | Fecha logica de snapshot. |
| `_extracted_at_utc` | Momento UTC de escritura en el repositorio. |
| `_source_table` | Nombre canonico de tabla. |
| `_source_system` | Fuente o extractor que genero la tabla. |

## Tablas

| Tabla | Grano | Cadencia | Como leerla |
| --- | --- | --- | --- |
| `metrobus_vehicle_positions` | Una fila por entidad vehiculo por snapshot. | Horaria laboral | Use `entity_id`, `vehicle_id`, `route_id`, `latitude`, `longitude`, `timestamp_cdmx`. |
| `metrobus_trip_updates` | Una fila por viaje-parada actualizada. | Horaria laboral | Use `trip_id`, `route_id`, `stop_id`, `arrival_delay_sec`, `departure_delay_sec`. |
| `metrobus_alerts` | Una fila por alerta GTFS-RT. | Horaria laboral | Use `cause`, `effect`, `header_text`, `description_text`. |
| `metrobus_vehicle_positions_enriched` | Vehiculo realtime con nombre de ruta/parada. | Horaria laboral | Preferible para mapas y analisis, porque agrega `route_short_name` y `stop_name`. |
| `metrobus_gtfs_static_agency` | Agencia GTFS. | Semanal | Catalogo de referencia. |
| `metrobus_gtfs_static_routes` | Una fila por ruta GTFS. | Semanal | Unir por `route_id`. |
| `metrobus_gtfs_static_stops` | Una fila por parada/estacion GTFS. | Semanal | Unir por `stop_id`. |
| `metrobus_gtfs_static_trips` | Una fila por viaje programado. | Semanal | Unir por `trip_id` y `route_id`. |
| `metrobus_gtfs_static_stop_times` | Una fila por parada dentro de viaje. | Semanal | Usar para horarios programados. |
| `metrobus_gtfs_static_calendar` | Servicio por dia de semana. | Semanal | Usar con `service_id`. |
| `metrobus_gtfs_static_calendar_dates` | Excepciones de calendario. | Semanal | Usar con `service_id` y fecha. |
| `metrobus_gtfs_static_shapes` | Puntos de geometria GTFS. | Semanal | Usar con `shape_id`. |
| `metrobus_gtfs_static_frequencies` | Frecuencias programadas. | Semanal | Puede estar vacia si el feed no publica frecuencias. |
| `metrobus_gtfs_static_feed_info` | Metadata del feed. | Semanal | Validar version o vigencia del feed. |
| `metrobus_gtfs_static_transfers` | Reglas de transbordo. | Semanal | Puede estar vacia si el feed no publica transfers. |
| `tomtom_cdmx_incidents` | Un incidente vial por snapshot. | Cada 2 horas laboral | Use `incident_id`, `icon_category_desc`, `delay_seconds`, `from`, `to`, `last_report_time`. |
| `tomtom_cdmx_flow` | Un punto estrategico por snapshot. | Cada 2 horas laboral | Use `point_name`, `current_speed_kmph`, `free_flow_speed_kmph`, `congestion_index`, `traffic_status`. |
| `ecobici_gbfs_feed_urls` | Un feed GBFS por fila. | Mensual | Sirve para auditar URLs de ECOBICI. |
| `ecobici_gbfs_station_information` | Una cicloestacion por fila. | Mensual | Catalogo de `station_id`, `station_name`, `lat`, `lon`, `capacity`. |
| `ecobici_gbfs_station_status` | Una cicloestacion por snapshot. | Cada 2 horas laboral | Disponibilidad realtime: `num_bikes_available`, `num_docks_available`. |
| `ecobici_realtime_stations` | Cicloestacion con ubicacion + disponibilidad. | Cada 2 horas laboral | Tabla recomendada para mapas y disponibilidad actual. |
| `ecobici_historical_links` | Un mes publicado por fila. | Mensual | Audita historicos disponibles en datos abiertos. |
| `ecobici_historico_raw` | Viaje historico ECOBICI sin normalizar. | Mensual | Usar cuando se requiere fidelidad al archivo original. |
| `ecobici_historico_normalizado` | Viaje historico normalizado. | Mensual | Tabla recomendada para analisis de demanda; usa `started_at`, `ended_at`, `duration_minutes`. |
| `ecobici_summary_trips_by_hour` | Una hora del dia por fila. | Mensual | Perfil horario de demanda. |
| `ecobici_summary_trips_by_date` | Una fecha por fila. | Mensual | Perfil diario de demanda. |
| `ecobici_summary_top_start_stations` | Top estaciones de origen. | Mensual | Ranking mensual de retiros. |
| `ecobici_summary_top_end_stations` | Top estaciones de destino. | Mensual | Ranking mensual de arribos. |
| `ecobici_summary_top_od_flows` | Top pares origen-destino. | Mensual | Flujo OD mensual. |
| `ecobici_summary_duration_stats` | Estadisticos de duracion. | Mensual | Media, mediana, percentiles y maximo. |
| `ecobici_metadata_columns` | Una columna perfilada por fila. | Mensual | Documentacion tecnica de columnas ECOBICI. |
| `ecobici_dataset_summary` | Una tabla perfilada por fila. | Mensual | Filas, columnas, duplicados y memoria. |
| `ecobici_datetime_summary` | Una columna temporal por fila. | Mensual | Rango minimo/maximo de fechas. |
| `ecobici_numeric_summary` | Una columna numerica por fila. | Mensual | Estadisticos descriptivos. |
| `campus_cdmx_base` | Un campus estrategico por fila. | Trimestral/mensual | Base de coordenadas para analisis de zonas universitarias. |
| `denue_cdmx_sector_61_servicios_educativos` | Un establecimiento educativo DENUE. | Mensual | Universo educativo CDMX sector SCIAN 61. |
| `denue_cdmx_educacion_superior_universitaria` | Establecimiento universitario estimado. | Mensual | Subset por heuristica de educacion superior. |
| `denue_establecimientos_alrededor_campus` | Establecimiento-campus-radio. | Mensual | Permite analizar entorno educativo a 500/1000/2000 m. |
| `denue_resumen_zonas_universitarias` | Campus-radio. | Mensual | Incluye `score_concentracion_educativa_0_100`. |
| `denue_resumen_por_nivel_educativo` | Campus-radio-nivel. | Mensual | Distribucion por nivel educativo estimado. |
| `denue_metadata_reporte` | Una columna perfilada por fila. | Mensual | Metadatos de tablas DENUE. |
| `routes_api_ejemplo_ruta` | Una ruta ejemplo por snapshot. | Diario laboral | Valida distancia, duracion y polyline. |
| `routes_api_comparacion_modos` | Un modo de transporte por fila. | Diario laboral | Compara DRIVE/WALK/BICYCLE/TRANSIT. |
| `routes_api_drive_pairs` | Un par origen-destino DRIVE por fila. | Diario laboral | Rutas vehiculares hacia zonas universitarias. |
| `routes_api_matriz` | Un par origen-destino de matriz. | Diario laboral | Tabla principal de accesibilidad/congestion Google. |
| `routes_api_score` | Un par origen-destino con score. | Diario laboral | Priorizacion relativa de criticidad. |

## Artefactos HTML

| Artefacto | Ruta actual |
| --- | --- |
| Mapa Metrobus | `data/artifacts/current/metrobus_vehicle_map.html` |
| Mapa TomTom | `data/artifacts/current/tomtom_cdmx_traffic_map.html` |
| Mapa DENUE | `data/artifacts/current/mapa_denue_zonas_universitarias_cdmx.html` |
| Mapa Google Routes | `data/artifacts/current/routes_api_mapa.html` |
