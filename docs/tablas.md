# Diccionario de tablas

La fuente de verdad operativa es `configs/tables.yml`. Este documento explica el uso de las tablas y las columnas principales. Cuando existan snapshots, `python -m historico_api docs --config configs/tables.yml` complementara tipos inferidos y ejemplos reales desde `data/current`.

## Convenciones

Cada tabla historizada incluye:

| Columna | Significado |
| --- | --- |
| `_snapshot_id` | Identificador unico de corrida en UTC. |
| `_snapshot_date` | Fecha logica de snapshot. |
| `_extracted_at_utc` | Momento UTC de escritura. |
| `_source_table` | Nombre canonico de tabla. |
| `_source_system` | Fuente del extractor. |

## Metrobús realtime

### `metrobus_vehicle_positions`

Una fila por vehiculo reportado en GTFS-Realtime.

| Columna | Significado |
| --- | --- |
| `entity_id` | Identificador de entidad GTFS-Realtime. |
| `trip_id` | Viaje GTFS asociado. |
| `route_id` | Ruta GTFS asociada. |
| `direction_id` | Sentido del viaje, si el feed lo entrega. |
| `vehicle_id` | Identificador de unidad. |
| `vehicle_label` | Etiqueta publica o interna de unidad. |
| `latitude`, `longitude` | Coordenadas reportadas. |
| `bearing` | Rumbo de la unidad. |
| `speed_mps`, `speed_kmh` | Velocidad reportada. |
| `stop_id` | Parada actual o proxima. |
| `current_status` | Estado GTFS de parada. |
| `timestamp_raw`, `timestamp_cdmx` | Timestamp original y convertido a CDMX. |
| `congestion_level`, `occupancy_status` | Estado de congestion/ocupacion si el feed lo entrega. |

### `metrobus_trip_updates`

Una fila por viaje-parada actualizada.

| Columna | Significado |
| --- | --- |
| `entity_id` | Entidad GTFS-Realtime. |
| `trip_id`, `route_id`, `direction_id` | Identificacion del viaje. |
| `vehicle_id`, `vehicle_label` | Vehiculo asociado. |
| `stop_sequence`, `stop_id` | Parada dentro del viaje. |
| `arrival_delay_sec`, `departure_delay_sec` | Retraso de llegada/salida en segundos. |
| `arrival_time_raw`, `departure_time_raw` | Timestamp original. |
| `arrival_time_cdmx`, `departure_time_cdmx` | Hora convertida a CDMX. |

### `metrobus_alerts`

Una fila por alerta de servicio.

| Columna | Significado |
| --- | --- |
| `entity_id` | Entidad de alerta. |
| `cause` | Causa GTFS-Realtime. |
| `effect` | Efecto en servicio. |
| `header_text` | Encabezado multilenguaje. |
| `description_text` | Descripcion multilenguaje. |
| `url` | URL informativa si existe. |

### `metrobus_vehicle_positions_enriched`

Extiende `metrobus_vehicle_positions` con columnas de `routes.txt` y `stops.txt`.

| Columna | Significado |
| --- | --- |
| `route_short_name`, `route_long_name` | Nombres de ruta. |
| `route_color`, `route_text_color` | Colores GTFS de ruta. |
| `stop_name`, `stop_lat`, `stop_lon` | Nombre y ubicacion de parada. |

## Metrobús GTFS estatico

Las tablas `metrobus_gtfs_static_*` preservan los archivos `.txt` publicados en el ZIP GTFS estatico. Las mas relevantes son:

| Tabla | Uso |
| --- | --- |
| `metrobus_gtfs_static_routes` | Catalogo de rutas; llave `route_id`. |
| `metrobus_gtfs_static_stops` | Catalogo de paradas; llave `stop_id`. |
| `metrobus_gtfs_static_trips` | Viajes programados; llave `trip_id`. |
| `metrobus_gtfs_static_stop_times` | Secuencia y horarios por viaje-parada. |
| `metrobus_gtfs_static_calendar` | Dias de servicio por `service_id`. |
| `metrobus_gtfs_static_calendar_dates` | Excepciones de calendario. |
| `metrobus_gtfs_static_shapes` | Geometrias de ruta por `shape_id`. |

## TomTom

### `tomtom_cdmx_incidents`

Una fila por incidente vial dentro del bounding box de CDMX.

| Columna | Significado |
| --- | --- |
| `extraction_timestamp` | Momento UTC de consulta a TomTom. |
| `incident_id` | Identificador del incidente. |
| `incident_type`, `geometry_type` | Tipo de entidad y geometria. |
| `lat`, `lon` | Punto representativo del incidente. |
| `icon_category`, `icon_category_desc` | Categoria numerica y legible. |
| `magnitude_of_delay`, `delay_seconds` | Severidad/retraso estimado. |
| `length_meters` | Longitud afectada. |
| `from`, `to`, `road_numbers` | Tramo vial afectado. |
| `start_time`, `end_time`, `last_report_time` | Temporalidad del incidente. |
| `event_descriptions`, `event_codes` | Eventos reportados. |
| `raw_geometry`, `raw_properties` | JSON crudo para auditoria. |

### `tomtom_cdmx_flow`

Una fila por punto estrategico de flujo.

| Columna | Significado |
| --- | --- |
| `point_name` | Punto consultado. |
| `input_lat`, `input_lon` | Coordenada solicitada. |
| `segment_lat`, `segment_lon` | Coordenada representativa del segmento devuelto. |
| `current_speed_kmph` | Velocidad actual. |
| `free_flow_speed_kmph` | Velocidad libre. |
| `speed_ratio` | Velocidad actual / velocidad libre. |
| `congestion_index` | `1 - speed_ratio`. |
| `current_travel_time_seconds`, `free_flow_travel_time_seconds` | Tiempo actual y libre. |
| `delay_seconds`, `delay_ratio` | Demora absoluta y relativa. |
| `confidence` | Confianza del dato TomTom. |
| `road_closure` | Indicador de cierre vial. |
| `traffic_status` | Clasificacion heuristica. |
| `raw_response` | JSON crudo para auditoria. |

## ECOBICI

### `ecobici_gbfs_feed_urls`

Feeds publicados por el indice GBFS.

| Columna | Significado |
| --- | --- |
| `feed_name` | Nombre de feed GBFS. |
| `url` | URL del feed. |

### `ecobici_gbfs_station_information`

Catalogo de cicloestaciones.

| Columna | Significado |
| --- | --- |
| `station_id` | Identificador de cicloestacion. |
| `station_name` | Nombre publico. |
| `lat`, `lon` | Ubicacion. |
| `capacity` | Capacidad aproximada. |

### `ecobici_gbfs_station_status`

Estado realtime de cicloestaciones.

| Columna | Significado |
| --- | --- |
| `station_id` | Identificador de cicloestacion. |
| `num_bikes_available` | Bicicletas disponibles. |
| `num_docks_available` | Espacios disponibles. |
| `num_bikes_disabled`, `num_docks_disabled` | Bicis/espacios deshabilitados. |
| `is_installed`, `is_renting`, `is_returning` | Estado operativo. |
| `last_reported`, `last_reported_datetime` | Ultimo reporte original y convertido. |

### `ecobici_realtime_stations`

Union de informacion y estado realtime.

| Columna | Significado |
| --- | --- |
| `station_id`, `station_name`, `lat`, `lon`, `capacity` | Identidad y ubicacion. |
| `num_bikes_available`, `num_docks_available` | Disponibilidad actual. |
| `bike_availability_pct`, `dock_availability_pct` | Disponibilidad relativa 0-1. |

### Historicos ECOBICI

| Tabla | Grano | Uso |
| --- | --- | --- |
| `ecobici_historical_links` | Un mes publicado. | Auditar disponibilidad de historicos. |
| `ecobici_historico_raw` | Un viaje historico sin normalizar. | Reproducibilidad frente al archivo original. |
| `ecobici_historico_normalizado` | Un viaje historico normalizado. | Analisis de demanda y patrones. |

Columnas clave de `ecobici_historico_normalizado`:

| Columna | Significado |
| --- | --- |
| `bike_id` | Bicicleta usada. |
| `user_gender`, `user_age` | Variables declaradas por usuario, si existen. |
| `start_station_id`, `end_station_id` | Estaciones de retiro y arribo. |
| `start_date`, `start_time`, `end_date`, `end_time` | Fecha/hora original. |
| `started_at`, `ended_at` | Timestamps normalizados. |
| `duration_minutes` | Duracion calculada. |
| `start_hour`, `start_date_only`, `start_weekday` | Variables temporales derivadas. |
| `_month`, `_source_url`, `_source_file` | Mes y archivo de origen. |

Resumenes derivados:

| Tabla | Uso |
| --- | --- |
| `ecobici_summary_trips_by_hour` | Viajes por hora de inicio. |
| `ecobici_summary_trips_by_date` | Viajes por fecha. |
| `ecobici_summary_top_start_stations` | Ranking de estaciones de retiro. |
| `ecobici_summary_top_end_stations` | Ranking de estaciones de arribo. |
| `ecobici_summary_top_od_flows` | Pares origen-destino mas frecuentes. |
| `ecobici_summary_duration_stats` | Estadisticos de duracion. |
| `ecobici_metadata_columns`, `ecobici_dataset_summary`, `ecobici_datetime_summary`, `ecobici_numeric_summary` | Metadatos y perfilado. |

## DENUE/INEGI

| Tabla | Grano | Uso |
| --- | --- | --- |
| `campus_cdmx_base` | Un campus estrategico. | Coordenadas base. |
| `denue_cdmx_sector_61_servicios_educativos` | Un establecimiento educativo. | Universo educativo de CDMX. |
| `denue_cdmx_educacion_superior_universitaria` | Establecimiento superior estimado. | Subset universitario. |
| `denue_establecimientos_alrededor_campus` | Establecimiento-campus-radio. | Presion educativa local. |
| `denue_resumen_zonas_universitarias` | Campus-radio. | Score de concentracion educativa. |
| `denue_resumen_por_nivel_educativo` | Campus-radio-nivel. | Distribucion por nivel educativo. |
| `denue_metadata_reporte` | Columna perfilada. | Metadatos de tablas DENUE. |

Columnas clave DENUE:

| Columna | Significado |
| --- | --- |
| `id_establecimiento`, `clee` | Identificadores DENUE. |
| `nombre`, `razon_social`, `clase_actividad` | Identidad y actividad economica. |
| `estrato` | Rango de personal ocupado. |
| `calle`, `colonia`, `cp`, `ubicacion` | Direccion. |
| `latitud`, `longitud` | Coordenadas. |
| `nivel_educativo_estimado` | Clasificacion heuristica. |
| `flag_universidad`, `flag_media_superior`, `flag_educacion_basica` | Flags derivados. |
| `campus_id`, `radio_m`, `distancia_campus_m` | Relacion con campus. |
| `score_concentracion_educativa_0_100` | Score relativo por campus-radio. |

## Google Routes API

| Tabla | Grano | Uso |
| --- | --- | --- |
| `routes_api_ejemplo_ruta` | Una ruta ejemplo. | Validacion de ruta y mapa. |
| `routes_api_comparacion_modos` | Un modo de transporte. | Comparacion DRIVE/WALK/BICYCLE/TRANSIT. |
| `routes_api_drive_pairs` | Un par origen-destino DRIVE. | Accesos vehiculares a campus. |
| `routes_api_matriz` | Un elemento de matriz OD. | Accesibilidad y congestion. |
| `routes_api_score` | Un elemento OD con score. | Priorizacion de criticidad. |

Columnas clave:

| Columna | Significado |
| --- | --- |
| `query_timestamp` | Momento UTC de consulta. |
| `origin`, `destination` | Par origen-destino. |
| `travel_mode` | Modo solicitado. |
| `route_found` | Indica si Google devolvio ruta. |
| `distance_meters` | Distancia estimada. |
| `duration_seconds`, `duration_minutes` | Duracion con condiciones actuales. |
| `static_duration_seconds`, `static_duration_minutes` | Duracion base. |
| `delay_seconds`, `delay_minutes` | Diferencia actual vs base. |
| `traffic_delay_pct` | Retraso relativo porcentual. |
| `encoded_polyline` | Geometria codificada para mapas. |
| `criticality_score_0_100`, `criticality_level` | Score relativo de criticidad. |
