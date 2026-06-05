# Documentacion de tablas

Este archivo se regenera a partir de `configs/tables.yml` y de los CSV en `data/current`.
Complete en el catalogo los significados de columnas cuando el valor aparezca como pendiente.

## `campus_cdmx_base`

- **Estado:** activa
- **Periodicidad:** `quarterly`
- **Fuente:** Catalogo manual del repositorio
- **Responsable:** Movilidad universitaria
- **Descripcion:** Campus estrategicos CDMX usados como puntos de analisis.

No existe snapshot actual para esta tabla.

## `denue_cdmx_educacion_superior_universitaria`

- **Estado:** activa
- **Periodicidad:** `monthly`
- **Fuente:** Derivado de DENUE sector 61
- **Responsable:** Movilidad universitaria
- **Descripcion:** Subconjunto estimado de educacion superior/universitaria.

No existe snapshot actual para esta tabla.

## `denue_cdmx_sector_61_servicios_educativos`

- **Estado:** activa
- **Periodicidad:** `monthly`
- **Fuente:** INEGI DENUE API sector SCIAN 61
- **Responsable:** Movilidad universitaria
- **Descripcion:** Universo de establecimientos educativos de CDMX.

No existe snapshot actual para esta tabla.

## `denue_establecimientos_alrededor_campus`

- **Estado:** activa
- **Periodicidad:** `monthly`
- **Fuente:** INEGI DENUE API Buscar por punto
- **Responsable:** Movilidad universitaria
- **Descripcion:** Establecimientos educativos alrededor de campus y radios 500/1000/2000 m.

No existe snapshot actual para esta tabla.

## `denue_metadata_reporte`

- **Estado:** activa
- **Periodicidad:** `monthly`
- **Fuente:** Metadatos generados
- **Responsable:** Movilidad universitaria
- **Descripcion:** Perfil de columnas de tablas DENUE.

No existe snapshot actual para esta tabla.

## `denue_resumen_por_nivel_educativo`

- **Estado:** activa
- **Periodicidad:** `monthly`
- **Fuente:** Derivado de DENUE alrededor de campus
- **Responsable:** Movilidad universitaria
- **Descripcion:** Conteo por nivel educativo estimado, campus y radio.

No existe snapshot actual para esta tabla.

## `denue_resumen_zonas_universitarias`

- **Estado:** activa
- **Periodicidad:** `monthly`
- **Fuente:** Derivado de DENUE alrededor de campus
- **Responsable:** Movilidad universitaria
- **Descripcion:** Resumen por campus y radio con score de concentracion educativa.

No existe snapshot actual para esta tabla.

## `ecobici_dataset_summary`

- **Estado:** activa
- **Periodicidad:** `monthly`
- **Fuente:** Metadatos generados
- **Responsable:** Movilidad universitaria
- **Descripcion:** Resumen general de tablas ECOBICI.

No existe snapshot actual para esta tabla.

## `ecobici_datetime_summary`

- **Estado:** activa
- **Periodicidad:** `monthly`
- **Fuente:** Metadatos generados
- **Responsable:** Movilidad universitaria
- **Descripcion:** Rangos temporales de tablas ECOBICI.

No existe snapshot actual para esta tabla.

## `ecobici_gbfs_feed_urls`

- **Estado:** activa
- **Periodicidad:** `monthly`
- **Fuente:** ECOBICI GBFS index
- **Responsable:** Movilidad universitaria
- **Descripcion:** URLs de feeds GBFS disponibles.

| Columna | Tipo inferido | Significado | Ejemplo |
| --- | --- | --- | --- |
| `_source_system` | `str` | Pendiente de documentar | `ecobici` |
| `_source_table` | `str` | Pendiente de documentar | `ecobici_gbfs_feed_urls` |
| `_extracted_at_utc` | `str` | Pendiente de documentar | `2026-06-05T01:37:34Z` |
| `_snapshot_date` | `str` | Pendiente de documentar | `2026-06-05` |
| `_snapshot_id` | `str` | Pendiente de documentar | `20260605T013733Z` |
| `feed_name` | `str` | Pendiente de documentar | `free_bike_status` |
| `url` | `str` | Pendiente de documentar | `https://gbfs.mex.lyftbikes.com/gbfs/en/free_bike_status.json` |

## `ecobici_gbfs_station_information`

- **Estado:** activa
- **Periodicidad:** `monthly`
- **Fuente:** ECOBICI GBFS station_information
- **Responsable:** Movilidad universitaria
- **Descripcion:** Catalogo de cicloestaciones, ubicacion y capacidad.
- **Llave primaria sugerida:** `station_id`

| Columna | Tipo inferido | Significado | Ejemplo |
| --- | --- | --- | --- |
| `_source_system` | `str` | Pendiente de documentar | `ecobici` |
| `_source_table` | `str` | Pendiente de documentar | `ecobici_gbfs_station_information` |
| `_extracted_at_utc` | `str` | Pendiente de documentar | `2026-06-05T01:37:34Z` |
| `_snapshot_date` | `str` | Pendiente de documentar | `2026-06-05` |
| `_snapshot_id` | `str` | Pendiente de documentar | `20260605T013733Z` |
| `station_id` | `int64` | Pendiente de documentar | `1` |
| `external_id` | `str` | Pendiente de documentar | `e961269c-34c4-4b70-8e30-a51aa95a8429` |
| `station_name` | `str` | Pendiente de documentar | `CE-710 Molino del Rey - Glorieta de la Lealtad` |
| `short_name` | `int64` | Pendiente de documentar | `710` |
| `lat` | `float64` | Pendiente de documentar | `19.416795` |
| `lon` | `float64` | Pendiente de documentar | `-99.192508` |
| `rental_methods` | `str` | Pendiente de documentar | `['KEY', 'CREDITCARD']` |
| `capacity` | `int64` | Pendiente de documentar | `39` |
| `electric_bike_surcharge_waiver` | `bool` | Pendiente de documentar | `False` |
| `is_charging` | `bool` | Pendiente de documentar | `False` |
| `eightd_has_key_dispenser` | `bool` | Pendiente de documentar | `False` |
| `has_kiosk` | `bool` | Pendiente de documentar | `True` |

## `ecobici_gbfs_station_status`

- **Estado:** activa
- **Periodicidad:** `every_2_hours_weekdays`
- **Fuente:** ECOBICI GBFS station_status
- **Responsable:** Movilidad universitaria
- **Descripcion:** Disponibilidad realtime por cicloestacion.
- **Llave primaria sugerida:** `_snapshot_id, station_id`

| Columna | Tipo inferido | Significado | Ejemplo |
| --- | --- | --- | --- |
| `_source_system` | `str` | Pendiente de documentar | `ecobici` |
| `_source_table` | `str` | Pendiente de documentar | `ecobici_gbfs_station_status` |
| `_extracted_at_utc` | `str` | Pendiente de documentar | `2026-06-05T15:38:05Z` |
| `_snapshot_date` | `str` | Pendiente de documentar | `2026-06-05` |
| `_snapshot_id` | `str` | Pendiente de documentar | `20260605T153804Z` |
| `station_id` | `int64` | Pendiente de documentar | `1` |
| `num_bikes_available` | `int64` | Pendiente de documentar | `20` |
| `num_bikes_disabled` | `int64` | Pendiente de documentar | `3` |
| `num_docks_available` | `int64` | Pendiente de documentar | `16` |
| `num_docks_disabled` | `int64` | Pendiente de documentar | `0` |
| `is_installed` | `int64` | Pendiente de documentar | `1` |
| `is_renting` | `int64` | Pendiente de documentar | `1` |
| `is_returning` | `int64` | Pendiente de documentar | `1` |
| `last_reported` | `int64` | Pendiente de documentar | `1780673676` |
| `eightd_has_available_keys` | `bool` | Pendiente de documentar | `False` |
| `is_charging` | `bool` | Pendiente de documentar | `False` |
| `last_reported_datetime` | `str` | Pendiente de documentar | `2026-06-05 15:34:36` |

## `ecobici_historical_links`

- **Estado:** activa
- **Periodicidad:** `monthly`
- **Fuente:** ECOBICI datos abiertos
- **Responsable:** Movilidad universitaria
- **Descripcion:** Links mensuales detectados para historicos ECOBICI.

No existe snapshot actual para esta tabla.

## `ecobici_historico_normalizado`

- **Estado:** activa
- **Periodicidad:** `monthly`
- **Fuente:** ECOBICI historico raw normalizado
- **Responsable:** Movilidad universitaria
- **Descripcion:** Viajes historicos con nombres estandarizados y campos temporales derivados.

No existe snapshot actual para esta tabla.

| Columna | Tipo inferido | Significado | Ejemplo |
| --- | --- | --- | --- |
| `bike_id` | `pendiente` | Identificador de bicicleta. | `12345` |
| `user_gender` | `pendiente` | Genero reportado por usuario si existe. | `M` |
| `user_age` | `pendiente` | Edad reportada por usuario si existe. | `27` |
| `start_station_id` | `pendiente` | Cicloestacion de retiro. | `271` |
| `end_station_id` | `pendiente` | Cicloestacion de arribo. | `112` |
| `started_at` | `pendiente` | Timestamp de inicio de viaje. | `2025-01-15 08:30:00` |
| `ended_at` | `pendiente` | Timestamp de fin de viaje. | `2025-01-15 08:44:00` |
| `duration_minutes` | `pendiente` | Duracion del viaje en minutos. | `14` |

## `ecobici_historico_raw`

- **Estado:** activa
- **Periodicidad:** `monthly`
- **Fuente:** ECOBICI datos abiertos historicos mensuales
- **Responsable:** Movilidad universitaria
- **Descripcion:** Viajes historicos mensuales tal como se publican.

No existe snapshot actual para esta tabla.

## `ecobici_metadata_columns`

- **Estado:** activa
- **Periodicidad:** `monthly`
- **Fuente:** Metadatos generados
- **Responsable:** Movilidad universitaria
- **Descripcion:** Perfil de columnas de tablas ECOBICI.

No existe snapshot actual para esta tabla.

## `ecobici_numeric_summary`

- **Estado:** activa
- **Periodicidad:** `monthly`
- **Fuente:** Metadatos generados
- **Responsable:** Movilidad universitaria
- **Descripcion:** Estadisticos numericos de tablas ECOBICI.

No existe snapshot actual para esta tabla.

## `ecobici_realtime_stations`

- **Estado:** activa
- **Periodicidad:** `every_2_hours_weekdays`
- **Fuente:** ECOBICI GBFS station_information + station_status
- **Responsable:** Movilidad universitaria
- **Descripcion:** Tabla unificada de cicloestaciones con disponibilidad actual.
- **Llave primaria sugerida:** `_snapshot_id, station_id`

| Columna | Tipo inferido | Significado | Ejemplo |
| --- | --- | --- | --- |
| `_source_system` | `str` | Pendiente de documentar | `ecobici` |
| `_source_table` | `str` | Pendiente de documentar | `ecobici_realtime_stations` |
| `_extracted_at_utc` | `str` | Pendiente de documentar | `2026-06-05T15:38:05Z` |
| `_snapshot_date` | `str` | Pendiente de documentar | `2026-06-05` |
| `_snapshot_id` | `str` | Pendiente de documentar | `20260605T153804Z` |
| `station_id` | `int64` | Identificador de cicloestacion. | `271` |
| `external_id` | `str` | Pendiente de documentar | `e961269c-34c4-4b70-8e30-a51aa95a8429` |
| `station_name` | `str` | Nombre de cicloestacion. | `271 Reforma` |
| `short_name` | `int64` | Pendiente de documentar | `710` |
| `lat` | `float64` | Pendiente de documentar | `19.416795` |
| `lon` | `float64` | Pendiente de documentar | `-99.192508` |
| `rental_methods` | `str` | Pendiente de documentar | `['CREDITCARD', 'KEY']` |
| `capacity` | `int64` | Capacidad total aproximada. | `20` |
| `electric_bike_surcharge_waiver` | `bool` | Pendiente de documentar | `False` |
| `is_charging_info` | `bool` | Pendiente de documentar | `False` |
| `eightd_has_key_dispenser` | `bool` | Pendiente de documentar | `False` |
| `has_kiosk` | `bool` | Pendiente de documentar | `True` |
| `num_bikes_available` | `int64` | Bicicletas disponibles. | `8` |
| `num_bikes_disabled` | `int64` | Pendiente de documentar | `3` |
| `num_docks_available` | `int64` | Espacios libres para devolver bicicleta. | `12` |
| `num_docks_disabled` | `int64` | Pendiente de documentar | `0` |
| `is_installed` | `int64` | Pendiente de documentar | `1` |
| `is_renting` | `int64` | Pendiente de documentar | `1` |
| `is_returning` | `int64` | Pendiente de documentar | `1` |
| `last_reported` | `int64` | Pendiente de documentar | `1780673676` |
| `eightd_has_available_keys` | `bool` | Pendiente de documentar | `False` |
| `is_charging_status` | `bool` | Pendiente de documentar | `False` |
| `last_reported_datetime` | `str` | Pendiente de documentar | `2026-06-05 15:34:36` |
| `bike_availability_pct` | `float64` | Proporcion de bicicletas disponibles. | `0.4` |
| `dock_availability_pct` | `float64` | Proporcion de espacios disponibles. | `0.6` |

## `ecobici_summary_duration_stats`

- **Estado:** activa
- **Periodicidad:** `monthly`
- **Fuente:** Derivado de ecobici_historico_normalizado
- **Responsable:** Movilidad universitaria
- **Descripcion:** Estadisticos de duracion de viajes.

No existe snapshot actual para esta tabla.

## `ecobici_summary_top_end_stations`

- **Estado:** activa
- **Periodicidad:** `monthly`
- **Fuente:** Derivado de ecobici_historico_normalizado
- **Responsable:** Movilidad universitaria
- **Descripcion:** Top estaciones de destino por volumen mensual.

No existe snapshot actual para esta tabla.

## `ecobici_summary_top_od_flows`

- **Estado:** activa
- **Periodicidad:** `monthly`
- **Fuente:** Derivado de ecobici_historico_normalizado
- **Responsable:** Movilidad universitaria
- **Descripcion:** Top flujos origen-destino ECOBICI.

No existe snapshot actual para esta tabla.

## `ecobici_summary_top_start_stations`

- **Estado:** activa
- **Periodicidad:** `monthly`
- **Fuente:** Derivado de ecobici_historico_normalizado
- **Responsable:** Movilidad universitaria
- **Descripcion:** Top estaciones de origen por volumen mensual.

No existe snapshot actual para esta tabla.

## `ecobici_summary_trips_by_date`

- **Estado:** activa
- **Periodicidad:** `monthly`
- **Fuente:** Derivado de ecobici_historico_normalizado
- **Responsable:** Movilidad universitaria
- **Descripcion:** Conteo de viajes por fecha.

No existe snapshot actual para esta tabla.

## `ecobici_summary_trips_by_hour`

- **Estado:** activa
- **Periodicidad:** `monthly`
- **Fuente:** Derivado de ecobici_historico_normalizado
- **Responsable:** Movilidad universitaria
- **Descripcion:** Conteo de viajes por hora de inicio.

No existe snapshot actual para esta tabla.

## `metrobus_alerts`

- **Estado:** activa
- **Periodicidad:** `hourly_weekdays`
- **Fuente:** Metrobús CDMX GTFS-Realtime urlRealTime
- **Responsable:** Movilidad universitaria
- **Descripcion:** Alertas de servicio publicadas en el feed realtime.
- **Llave primaria sugerida:** `_snapshot_id, entity_id`

| Columna | Tipo inferido | Significado | Ejemplo |
| --- | --- | --- | --- |
| `_source_system` | `object` | Pendiente de documentar | `` |
| `_source_table` | `object` | Pendiente de documentar | `` |
| `_extracted_at_utc` | `object` | Pendiente de documentar | `` |
| `_snapshot_date` | `object` | Pendiente de documentar | `` |
| `_snapshot_id` | `object` | Pendiente de documentar | `` |

## `metrobus_gtfs_static_agency`

- **Estado:** activa
- **Periodicidad:** `weekly`
- **Fuente:** Metrobús CDMX GTFS estatico urlStatic
- **Responsable:** Movilidad universitaria
- **Descripcion:** Agencias del feed GTFS estatico.

No existe snapshot actual para esta tabla.

## `metrobus_gtfs_static_calendar`

- **Estado:** activa
- **Periodicidad:** `weekly`
- **Fuente:** Metrobús CDMX GTFS estatico urlStatic
- **Responsable:** Movilidad universitaria
- **Descripcion:** Calendario base de servicio.

No existe snapshot actual para esta tabla.

## `metrobus_gtfs_static_calendar_dates`

- **Estado:** activa
- **Periodicidad:** `weekly`
- **Fuente:** Metrobús CDMX GTFS estatico urlStatic
- **Responsable:** Movilidad universitaria
- **Descripcion:** Excepciones de calendario de servicio.

No existe snapshot actual para esta tabla.

## `metrobus_gtfs_static_feed_info`

- **Estado:** activa
- **Periodicidad:** `weekly`
- **Fuente:** Metrobús CDMX GTFS estatico urlStatic
- **Responsable:** Movilidad universitaria
- **Descripcion:** Metadatos del feed GTFS.

No existe snapshot actual para esta tabla.

## `metrobus_gtfs_static_frequencies`

- **Estado:** activa
- **Periodicidad:** `weekly`
- **Fuente:** Metrobús CDMX GTFS estatico urlStatic
- **Responsable:** Movilidad universitaria
- **Descripcion:** Frecuencias programadas si el feed las publica.

No existe snapshot actual para esta tabla.

## `metrobus_gtfs_static_routes`

- **Estado:** activa
- **Periodicidad:** `weekly`
- **Fuente:** Metrobús CDMX GTFS estatico urlStatic
- **Responsable:** Movilidad universitaria
- **Descripcion:** Catalogo de rutas de Metrobus.
- **Llave primaria sugerida:** `route_id`

No existe snapshot actual para esta tabla.

## `metrobus_gtfs_static_shapes`

- **Estado:** activa
- **Periodicidad:** `weekly`
- **Fuente:** Metrobús CDMX GTFS estatico urlStatic
- **Responsable:** Movilidad universitaria
- **Descripcion:** Geometrias de rutas GTFS.

No existe snapshot actual para esta tabla.

## `metrobus_gtfs_static_stop_times`

- **Estado:** activa
- **Periodicidad:** `weekly`
- **Fuente:** Metrobús CDMX GTFS estatico urlStatic
- **Responsable:** Movilidad universitaria
- **Descripcion:** Horarios programados por viaje y parada.

No existe snapshot actual para esta tabla.

## `metrobus_gtfs_static_stops`

- **Estado:** activa
- **Periodicidad:** `weekly`
- **Fuente:** Metrobús CDMX GTFS estatico urlStatic
- **Responsable:** Movilidad universitaria
- **Descripcion:** Catalogo de paradas y estaciones de Metrobus.
- **Llave primaria sugerida:** `stop_id`

No existe snapshot actual para esta tabla.

## `metrobus_gtfs_static_transfers`

- **Estado:** activa
- **Periodicidad:** `weekly`
- **Fuente:** Metrobús CDMX GTFS estatico urlStatic
- **Responsable:** Movilidad universitaria
- **Descripcion:** Reglas de transferencia GTFS, si existen.

No existe snapshot actual para esta tabla.

## `metrobus_gtfs_static_trips`

- **Estado:** activa
- **Periodicidad:** `weekly`
- **Fuente:** Metrobús CDMX GTFS estatico urlStatic
- **Responsable:** Movilidad universitaria
- **Descripcion:** Viajes programados del feed GTFS.

No existe snapshot actual para esta tabla.

## `metrobus_trip_updates`

- **Estado:** activa
- **Periodicidad:** `hourly_weekdays`
- **Fuente:** Metrobús CDMX GTFS-Realtime urlRealTime
- **Responsable:** Movilidad universitaria
- **Descripcion:** Actualizaciones realtime de viajes, paradas, llegadas y salidas.
- **Llave primaria sugerida:** `_snapshot_id, entity_id, trip_id, stop_sequence`

| Columna | Tipo inferido | Significado | Ejemplo |
| --- | --- | --- | --- |
| `_source_system` | `object` | Pendiente de documentar | `` |
| `_source_table` | `object` | Pendiente de documentar | `` |
| `_extracted_at_utc` | `object` | Pendiente de documentar | `` |
| `_snapshot_date` | `object` | Pendiente de documentar | `` |
| `_snapshot_id` | `object` | Pendiente de documentar | `` |

## `metrobus_vehicle_positions`

- **Estado:** activa
- **Periodicidad:** `hourly_weekdays`
- **Fuente:** Metrobús CDMX GTFS-Realtime urlRealTime
- **Responsable:** Movilidad universitaria
- **Descripcion:** Posicion realtime de unidades de Metrobus.
- **Llave primaria sugerida:** `_snapshot_id, entity_id`

| Columna | Tipo inferido | Significado | Ejemplo |
| --- | --- | --- | --- |
| `_source_system` | `str` | Pendiente de documentar | `metrobus` |
| `_source_table` | `str` | Pendiente de documentar | `metrobus_vehicle_positions` |
| `_extracted_at_utc` | `str` | Pendiente de documentar | `2026-06-05T06:42:53Z` |
| `_snapshot_date` | `str` | Pendiente de documentar | `2026-06-05` |
| `_snapshot_id` | `str` | Pendiente de documentar | `20260605T064250Z` |
| `entity_id` | `str` | Identificador de entidad GTFS-Realtime. | `vehicle_123` |
| `trip_id` | `float64` | Identificador del viaje GTFS asociado. | `trip_456` |
| `route_id` | `float64` | Identificador de ruta GTFS. | `1` |
| `direction_id` | `float64` | Pendiente de documentar | `0.0` |
| `start_time` | `str` | Pendiente de documentar | `06:20:51` |
| `start_date` | `float64` | Pendiente de documentar | `20260605.0` |
| `vehicle_id` | `int64` | Identificador de unidad. | `1234` |
| `vehicle_label` | `int64` | Pendiente de documentar | `2306` |
| `license_plate` | `str` | Pendiente de documentar | `1240002` |
| `latitude` | `float64` | Latitud reportada por la unidad. | `19.4326` |
| `longitude` | `float64` | Longitud reportada por la unidad. | `-99.1332` |
| `bearing` | `float64` | Pendiente de documentar | `159.0` |
| `speed_mps` | `float64` | Pendiente de documentar | `0.0` |
| `speed_kmh` | `float64` | Velocidad estimada en kilometros por hora. | `24.5` |
| `current_stop_sequence` | `float64` | Pendiente de documentar | `` |
| `stop_id` | `float64` | Pendiente de documentar | `` |
| `current_status` | `float64` | Pendiente de documentar | `` |
| `timestamp_raw` | `int64` | Pendiente de documentar | `1780641754` |
| `timestamp_cdmx` | `str` | Hora del reporte convertida a America/Mexico_City. | `2026-06-04 08:15:00-06:00` |
| `congestion_level` | `float64` | Pendiente de documentar | `` |
| `occupancy_status` | `float64` | Pendiente de documentar | `` |

## `metrobus_vehicle_positions_enriched`

- **Estado:** activa
- **Periodicidad:** `hourly_weekdays`
- **Fuente:** Metrobús realtime unido con GTFS estatico routes/stops
- **Responsable:** Movilidad universitaria
- **Descripcion:** Posiciones de unidades enriquecidas con nombres de ruta y parada.
- **Llave primaria sugerida:** `_snapshot_id, entity_id`

| Columna | Tipo inferido | Significado | Ejemplo |
| --- | --- | --- | --- |
| `_source_system` | `str` | Pendiente de documentar | `metrobus` |
| `_source_table` | `str` | Pendiente de documentar | `metrobus_vehicle_positions_enriched` |
| `_extracted_at_utc` | `str` | Pendiente de documentar | `2026-06-05T06:42:53Z` |
| `_snapshot_date` | `str` | Pendiente de documentar | `2026-06-05` |
| `_snapshot_id` | `str` | Pendiente de documentar | `20260605T064250Z` |
| `entity_id` | `str` | Pendiente de documentar | `b02ca729-27d2-4d21-9a4d-864f86b2e53b` |
| `trip_id` | `float64` | Pendiente de documentar | `` |
| `route_id` | `float64` | Pendiente de documentar | `19563.0` |
| `direction_id` | `float64` | Pendiente de documentar | `0.0` |
| `start_time` | `str` | Pendiente de documentar | `06:20:51` |
| `start_date` | `float64` | Pendiente de documentar | `20260605.0` |
| `vehicle_id` | `int64` | Pendiente de documentar | `69379` |
| `vehicle_label` | `int64` | Pendiente de documentar | `2306` |
| `license_plate` | `str` | Pendiente de documentar | `1240002` |
| `latitude` | `float64` | Pendiente de documentar | `19.478105545043945` |
| `longitude` | `float64` | Pendiente de documentar | `-99.06351470947266` |
| `bearing` | `float64` | Pendiente de documentar | `159.0` |
| `speed_mps` | `float64` | Pendiente de documentar | `0.0` |
| `speed_kmh` | `float64` | Pendiente de documentar | `0.0` |
| `current_stop_sequence` | `float64` | Pendiente de documentar | `` |
| `stop_id` | `float64` | Pendiente de documentar | `` |
| `current_status` | `float64` | Pendiente de documentar | `` |
| `timestamp_raw` | `int64` | Pendiente de documentar | `1780641754` |
| `timestamp_cdmx` | `str` | Pendiente de documentar | `2026-06-05 00:42:34-06:00` |
| `congestion_level` | `float64` | Pendiente de documentar | `` |
| `occupancy_status` | `float64` | Pendiente de documentar | `` |
| `route_short_name` | `float64` | Nombre corto de ruta proveniente de routes.txt. | `L1` |
| `route_long_name` | `str` | Nombre largo de ruta. | `Indios Verdes - El Caminero` |
| `route_desc` | `float64` | Pendiente de documentar | `` |
| `route_type` | `float64` | Pendiente de documentar | `3.0` |
| `route_color` | `str` | Pendiente de documentar | `8D1A96` |
| `route_text_color` | `str` | Pendiente de documentar | `FFFFFF` |
| `stop_name` | `float64` | Nombre de parada asociada. | `Buenavista` |
| `stop_lat` | `float64` | Pendiente de documentar | `` |
| `stop_lon` | `float64` | Pendiente de documentar | `` |
| `zone_id` | `float64` | Pendiente de documentar | `` |
| `location_type` | `float64` | Pendiente de documentar | `` |
| `parent_station` | `float64` | Pendiente de documentar | `` |

## `routes_api_comparacion_modos`

- **Estado:** activa
- **Periodicidad:** `daily_weekdays`
- **Fuente:** Google Maps Platform Routes API computeRoutes
- **Responsable:** Movilidad universitaria
- **Descripcion:** Comparacion multimodal para un par origen-destino.

| Columna | Tipo inferido | Significado | Ejemplo |
| --- | --- | --- | --- |
| `_source_system` | `str` | Pendiente de documentar | `google_routes` |
| `_source_table` | `str` | Pendiente de documentar | `routes_api_comparacion_modos` |
| `_extracted_at_utc` | `str` | Pendiente de documentar | `2026-06-05T16:14:04Z` |
| `_snapshot_date` | `str` | Pendiente de documentar | `2026-06-05` |
| `_snapshot_id` | `str` | Pendiente de documentar | `20260605T161400Z` |
| `query_timestamp` | `str` | Pendiente de documentar | `2026-06-05T16:14:00.576110` |
| `origin` | `str` | Pendiente de documentar | `Metro Universidad` |
| `destination` | `str` | Pendiente de documentar | `Rectoria UNAM` |
| `travel_mode` | `str` | Pendiente de documentar | `DRIVE` |
| `route_found` | `bool` | Pendiente de documentar | `True` |
| `distance_meters` | `int64` | Pendiente de documentar | `2330` |
| `duration_seconds` | `float64` | Pendiente de documentar | `416.0` |
| `static_duration_seconds` | `float64` | Pendiente de documentar | `426.0` |
| `duration_minutes` | `float64` | Pendiente de documentar | `6.933333333333334` |
| `static_duration_minutes` | `float64` | Pendiente de documentar | `7.1` |
| `delay_seconds` | `float64` | Pendiente de documentar | `-10.0` |
| `delay_minutes` | `float64` | Pendiente de documentar | `-0.1666666666666666` |
| `traffic_delay_pct` | `float64` | Pendiente de documentar | `-2.3474178403755874` |
| `encoded_polyline` | `str` | Pendiente de documentar | `mh}tBxai\|QwAIcDAuCGqDFkCLoBTk@NYPgDdDgGhDMPeBnHKTgCUIV@h@nBLDFf@Xf@`@tA`BN\HXDj@BfGDzDJtEDbFA`C`AtQU?I[KCgABQBSCYD` |
| `description` | `str` | Pendiente de documentar | `Investigación Científica y Escolar` |
| `route_labels` | `str` | Pendiente de documentar | `DEFAULT_ROUTE` |

## `routes_api_drive_pairs`

- **Estado:** activa
- **Periodicidad:** `daily_weekdays`
- **Fuente:** Google Maps Platform Routes API computeRoutes
- **Responsable:** Movilidad universitaria
- **Descripcion:** Rutas DRIVE para varios origenes hacia zonas universitarias.

| Columna | Tipo inferido | Significado | Ejemplo |
| --- | --- | --- | --- |
| `_source_system` | `str` | Pendiente de documentar | `google_routes` |
| `_source_table` | `str` | Pendiente de documentar | `routes_api_drive_pairs` |
| `_extracted_at_utc` | `str` | Pendiente de documentar | `2026-06-05T16:14:04Z` |
| `_snapshot_date` | `str` | Pendiente de documentar | `2026-06-05` |
| `_snapshot_id` | `str` | Pendiente de documentar | `20260605T161400Z` |
| `query_timestamp` | `str` | Pendiente de documentar | `2026-06-05T16:14:02.102876` |
| `origin` | `str` | Pendiente de documentar | `Metro Universidad` |
| `destination` | `str` | Pendiente de documentar | `Rectoria UNAM` |
| `travel_mode` | `str` | Pendiente de documentar | `DRIVE` |
| `route_found` | `bool` | Pendiente de documentar | `True` |
| `distance_meters` | `int64` | Pendiente de documentar | `2330` |
| `duration_seconds` | `float64` | Pendiente de documentar | `416.0` |
| `static_duration_seconds` | `float64` | Pendiente de documentar | `426.0` |
| `duration_minutes` | `float64` | Pendiente de documentar | `6.933333333333334` |
| `static_duration_minutes` | `float64` | Pendiente de documentar | `7.1` |
| `delay_seconds` | `float64` | Pendiente de documentar | `-10.0` |
| `delay_minutes` | `float64` | Pendiente de documentar | `-0.1666666666666666` |
| `traffic_delay_pct` | `float64` | Pendiente de documentar | `-2.3474178403755874` |
| `encoded_polyline` | `str` | Pendiente de documentar | `mh}tBxai\|QwAIcDAuCGqDFkCLoBTk@NYPgDdDgGhDMPeBnHKTgCUIV@h@nBLDFf@Xf@`@tA`BN\HXDj@BfGDzDJtEDbFA`C`AtQU?I[KCgABQBSCYD` |
| `description` | `str` | Pendiente de documentar | `Investigación Científica y Escolar` |
| `route_labels` | `str` | Pendiente de documentar | `DEFAULT_ROUTE` |

## `routes_api_ejemplo_ruta`

- **Estado:** activa
- **Periodicidad:** `daily_weekdays`
- **Fuente:** Google Maps Platform Routes API computeRoutes
- **Responsable:** Movilidad universitaria
- **Descripcion:** Ruta ejemplo Metro Universidad a Rectoria UNAM.

| Columna | Tipo inferido | Significado | Ejemplo |
| --- | --- | --- | --- |
| `_source_system` | `str` | Pendiente de documentar | `google_routes` |
| `_source_table` | `str` | Pendiente de documentar | `routes_api_ejemplo_ruta` |
| `_extracted_at_utc` | `str` | Pendiente de documentar | `2026-06-05T16:14:04Z` |
| `_snapshot_date` | `str` | Pendiente de documentar | `2026-06-05` |
| `_snapshot_id` | `str` | Pendiente de documentar | `20260605T161400Z` |
| `query_timestamp` | `str` | Pendiente de documentar | `2026-06-05T16:14:00.464380` |
| `origin` | `str` | Pendiente de documentar | `Metro Universidad` |
| `destination` | `str` | Pendiente de documentar | `Rectoria UNAM` |
| `travel_mode` | `str` | Pendiente de documentar | `DRIVE` |
| `route_found` | `bool` | Pendiente de documentar | `True` |
| `distance_meters` | `int64` | Pendiente de documentar | `2330` |
| `duration_seconds` | `float64` | Pendiente de documentar | `416.0` |
| `static_duration_seconds` | `float64` | Pendiente de documentar | `426.0` |
| `duration_minutes` | `float64` | Pendiente de documentar | `6.933333333333334` |
| `static_duration_minutes` | `float64` | Pendiente de documentar | `7.1` |
| `delay_seconds` | `float64` | Pendiente de documentar | `-10.0` |
| `delay_minutes` | `float64` | Pendiente de documentar | `-0.1666666666666666` |
| `traffic_delay_pct` | `float64` | Pendiente de documentar | `-2.3474178403755874` |
| `encoded_polyline` | `str` | Pendiente de documentar | `mh}tBxai\|QwAIcDAuCGqDFkCLoBTk@NYPgDdDgGhDMPeBnHKTgCUIV@h@nBLDFf@Xf@`@tA`BN\HXDj@BfGDzDJtEDbFA`C`AtQU?I[KCgABQBSCYD` |
| `description` | `str` | Pendiente de documentar | `Investigación Científica y Escolar` |
| `route_labels` | `str` | Pendiente de documentar | `DEFAULT_ROUTE` |

## `routes_api_matriz`

- **Estado:** activa
- **Periodicidad:** `daily_weekdays`
- **Fuente:** Google Maps Platform Routes API computeRouteMatrix
- **Responsable:** Movilidad universitaria
- **Descripcion:** Matriz origen-destino con trafico hacia universidades.

| Columna | Tipo inferido | Significado | Ejemplo |
| --- | --- | --- | --- |
| `_source_system` | `str` | Pendiente de documentar | `google_routes` |
| `_source_table` | `str` | Pendiente de documentar | `routes_api_matriz` |
| `_extracted_at_utc` | `str` | Pendiente de documentar | `2026-06-05T16:14:04Z` |
| `_snapshot_date` | `str` | Pendiente de documentar | `2026-06-05` |
| `_snapshot_id` | `str` | Pendiente de documentar | `20260605T161400Z` |
| `query_timestamp` | `str` | Pendiente de documentar | `2026-06-05T16:14:04.911030` |
| `origin_index` | `int64` | Pendiente de documentar | `0` |
| `destination_index` | `int64` | Pendiente de documentar | `0` |
| `origin` | `str` | Pendiente de documentar | `Metro Universidad` |
| `destination` | `str` | Pendiente de documentar | `Rectoria UNAM` |
| `travel_mode` | `str` | Pendiente de documentar | `DRIVE` |
| `status` | `str` | Pendiente de documentar | `{}` |
| `condition` | `str` | Pendiente de documentar | `ROUTE_EXISTS` |
| `distance_meters` | `int64` | Pendiente de documentar | `2330` |
| `duration_seconds` | `float64` | Pendiente de documentar | `416.0` |
| `static_duration_seconds` | `float64` | Pendiente de documentar | `427.0` |
| `duration_minutes` | `float64` | Pendiente de documentar | `6.933333333333334` |
| `static_duration_minutes` | `float64` | Pendiente de documentar | `7.116666666666666` |
| `delay_seconds` | `float64` | Pendiente de documentar | `-11.0` |
| `delay_minutes` | `float64` | Pendiente de documentar | `-0.1833333333333333` |
| `traffic_delay_pct` | `float64` | Pendiente de documentar | `-2.576112412177989` |

## `routes_api_score`

- **Estado:** activa
- **Periodicidad:** `daily_weekdays`
- **Fuente:** Derivado de routes_api_matriz
- **Responsable:** Movilidad universitaria
- **Descripcion:** Score relativo de criticidad por par origen-destino.

| Columna | Tipo inferido | Significado | Ejemplo |
| --- | --- | --- | --- |
| `_source_system` | `str` | Pendiente de documentar | `google_routes` |
| `_source_table` | `str` | Pendiente de documentar | `routes_api_score` |
| `_extracted_at_utc` | `str` | Pendiente de documentar | `2026-06-05T16:14:04Z` |
| `_snapshot_date` | `str` | Pendiente de documentar | `2026-06-05` |
| `_snapshot_id` | `str` | Pendiente de documentar | `20260605T161400Z` |
| `query_timestamp` | `str` | Pendiente de documentar | `2026-06-05T16:14:04.911030` |
| `origin_index` | `int64` | Pendiente de documentar | `0` |
| `destination_index` | `int64` | Pendiente de documentar | `0` |
| `origin` | `str` | Pendiente de documentar | `Metro Universidad` |
| `destination` | `str` | Pendiente de documentar | `Rectoria UNAM` |
| `travel_mode` | `str` | Pendiente de documentar | `DRIVE` |
| `status` | `str` | Pendiente de documentar | `{}` |
| `condition` | `str` | Pendiente de documentar | `ROUTE_EXISTS` |
| `distance_meters` | `int64` | Pendiente de documentar | `2330` |
| `duration_seconds` | `float64` | Pendiente de documentar | `416.0` |
| `static_duration_seconds` | `float64` | Pendiente de documentar | `427.0` |
| `duration_minutes` | `float64` | Pendiente de documentar | `6.933333333333334` |
| `static_duration_minutes` | `float64` | Pendiente de documentar | `7.116666666666666` |
| `delay_seconds` | `float64` | Pendiente de documentar | `-11.0` |
| `delay_minutes` | `float64` | Pendiente de documentar | `-0.1833333333333333` |
| `traffic_delay_pct` | `float64` | Pendiente de documentar | `-2.576112412177989` |
| `duration_score` | `float64` | Pendiente de documentar | `0.0326763485477178` |
| `delay_score` | `float64` | Pendiente de documentar | `0.037037037037037` |
| `traffic_pct_score` | `float64` | Pendiente de documentar | `0.1772611789243684` |
| `criticality_score_0_100` | `float64` | Pendiente de documentar | `6.311955559430968` |
| `criticality_level` | `str` | Pendiente de documentar | `Baja` |

## `tomtom_cdmx_flow`

- **Estado:** activa
- **Periodicidad:** `every_2_hours_weekdays`
- **Fuente:** TomTom Flow Segment Data
- **Responsable:** Movilidad universitaria
- **Descripcion:** Flujo de trafico en puntos estrategicos de CDMX.
- **Llave primaria sugerida:** `_snapshot_id, point_name`

| Columna | Tipo inferido | Significado | Ejemplo |
| --- | --- | --- | --- |
| `_source_system` | `str` | Pendiente de documentar | `tomtom` |
| `_source_table` | `str` | Pendiente de documentar | `tomtom_cdmx_flow` |
| `_extracted_at_utc` | `str` | Pendiente de documentar | `2026-06-05T15:32:19Z` |
| `_snapshot_date` | `str` | Pendiente de documentar | `2026-06-05` |
| `_snapshot_id` | `str` | Pendiente de documentar | `20260605T153215Z` |
| `extraction_timestamp` | `str` | Pendiente de documentar | `2026-06-05T15:32:15.962159` |
| `point_name` | `str` | Punto estrategico consultado. | `Universidad - CU` |
| `input_lat` | `float64` | Pendiente de documentar | `19.432608` |
| `input_lon` | `float64` | Pendiente de documentar | `-99.133209` |
| `segment_lat` | `float64` | Pendiente de documentar | `19.43135715602765` |
| `segment_lon` | `float64` | Pendiente de documentar | `-99.13658297600612` |
| `frc` | `str` | Pendiente de documentar | `FRC5` |
| `current_speed_kmph` | `int64` | Velocidad actual estimada. | `24` |
| `free_flow_speed_kmph` | `int64` | Velocidad esperada sin trafico. | `45` |
| `speed_ratio` | `float64` | current_speed_kmph / free_flow_speed_kmph. | `0.53` |
| `congestion_index` | `float64` | Indice heuristico 1 - speed_ratio. | `0.47` |
| `current_travel_time_seconds` | `int64` | Pendiente de documentar | `887` |
| `free_flow_travel_time_seconds` | `int64` | Pendiente de documentar | `488` |
| `delay_seconds` | `int64` | Diferencia entre tiempo actual y tiempo libre. | `120` |
| `delay_ratio` | `float64` | Pendiente de documentar | `1.817622950819672` |
| `confidence` | `float64` | Pendiente de documentar | `0.995378` |
| `road_closure` | `bool` | Pendiente de documentar | `False` |
| `status_code` | `int64` | Pendiente de documentar | `200` |
| `error` | `float64` | Pendiente de documentar | `` |
| `raw_response` | `str` | Pendiente de documentar | `{"flowSegmentData": {"frc": "FRC5", "currentSpeed": 11, "freeFlowSpeed": 20, "currentTravelTime": 887, "freeFlowTravelTi` |
| `traffic_status` | `str` | Clasificacion heuristica de congestion. | `Congestion media` |

## `tomtom_cdmx_incidents`

- **Estado:** activa
- **Periodicidad:** `every_2_hours_weekdays`
- **Fuente:** TomTom Traffic Incident Details v5
- **Responsable:** Movilidad universitaria
- **Descripcion:** Incidentes actuales de trafico dentro del bounding box de CDMX.
- **Llave primaria sugerida:** `_snapshot_id, incident_id`

| Columna | Tipo inferido | Significado | Ejemplo |
| --- | --- | --- | --- |
| `_source_system` | `str` | Pendiente de documentar | `tomtom` |
| `_source_table` | `str` | Pendiente de documentar | `tomtom_cdmx_incidents` |
| `_extracted_at_utc` | `str` | Pendiente de documentar | `2026-06-05T15:32:19Z` |
| `_snapshot_date` | `str` | Pendiente de documentar | `2026-06-05` |
| `_snapshot_id` | `str` | Pendiente de documentar | `20260605T153215Z` |
| `extraction_timestamp` | `str` | Pendiente de documentar | `2026-06-05T15:32:15.866118` |
| `incident_id` | `str` | Identificador de incidente reportado por TomTom. | `123456` |
| `incident_type` | `str` | Pendiente de documentar | `Feature` |
| `geometry_type` | `str` | Pendiente de documentar | `LineString` |
| `lat` | `float64` | Pendiente de documentar | `19.3613286582` |
| `lon` | `float64` | Pendiente de documentar | `-99.3521695489` |
| `icon_category` | `int64` | Pendiente de documentar | `6` |
| `icon_category_desc` | `str` | Categoria legible del incidente. | `Jam` |
| `magnitude_of_delay` | `int64` | Pendiente de documentar | `3` |
| `delay_seconds` | `float64` | Retraso estimado en segundos. | `420` |
| `length_meters` | `float64` | Longitud vial afectada. | `850` |
| `from` | `str` | Inicio textual del tramo afectado. | `Av. Insurgentes` |
| `to` | `str` | Fin textual del tramo afectado. | `Eje 5 Sur` |
| `road_numbers` | `str` | Pendiente de documentar | `MEX-15` |
| `time_validity` | `str` | Pendiente de documentar | `present` |
| `probability` | `str` | Pendiente de documentar | `certain` |
| `number_of_reports` | `float64` | Pendiente de documentar | `` |
| `start_time` | `str` | Pendiente de documentar | `2026-06-05T15:26:30Z` |
| `end_time` | `str` | Pendiente de documentar | `2026-06-05T15:50:30Z` |
| `last_report_time` | `float64` | Ultimo reporte del incidente segun TomTom. | `2026-06-04T13:30:00Z` |
| `event_descriptions` | `str` | Pendiente de documentar | `Tráfico parado` |
| `event_codes` | `str` | Pendiente de documentar | `101` |
| `raw_geometry` | `str` | Pendiente de documentar | `{"type": "LineString", "coordinates": [[-99.3519227857, 19.3616733622], [-99.3520327563, 19.3615405892], [-99.3520729894` |
| `raw_properties` | `str` | Pendiente de documentar | `{"id": "TTI-13f3ec6a-4ca6-44e3-a453-bf78cdebb43e-TTL24441700980014000", "iconCategory": 6, "magnitudeOfDelay": 3, "start` |
