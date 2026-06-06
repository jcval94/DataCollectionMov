# Periodicidad de extraccion

El objetivo es conservar informacion suficiente para analisis historico sin saturar APIs ni generar commits innecesarios.

## Schedules activos

| Workflow | Fuente | Periodicidad | Motivo |
| --- | --- | --- | --- |
| `metrobus-realtime.yml` | Metrobús GTFS-Realtime | Cada hora en horario operativo de lunes a viernes | Posiciones y trip updates son de vida corta. Una hora reduce carga y deja patron operativo. |
| `metrobus-static.yml` | Metrobús GTFS estatico | Semanal | Rutas, paradas y calendarios cambian poco, pero pueden actualizarse sin aviso. |
| `tomtom-traffic.yml` | TomTom incidentes y flow | Cada 2 horas en horario operativo de lunes a viernes | Trafico cambia rapido, pero TomTom tiene cuota/costo. |
| `tomtom-one-month-history.yml` | TomTom incidentes y flow | Campaña opcional de 5 capturas diarias por hasta 1 mes | Permite construir un historico acotado sin corridas indefinidas; requiere variables de inicio/fin y flag de activacion. |
| `ecobici-realtime.yml` | ECOBICI station_status | Cada 2 horas en horario operativo de lunes a viernes | GBFS es realtime; capturas moderadas permiten historico de disponibilidad. |
| `ecobici-catalog.yml` | ECOBICI station_information y feeds | Mensual | Catalogo de estaciones y URLs cambia poco. |
| `ecobici-historical.yml` | Historicos mensuales ECOBICI | Mensual, dia 6 | Los archivos historicos son mensuales; correr despues del inicio del mes evita buscar archivos aun no publicados. |
| `denue.yml` | DENUE/INEGI educativo | Mensual | DENUE es capa contextual, no realtime. |
| `google-routes.yml` | Google Routes API | Diario, lunes a viernes | Tiene costo/cuota; una captura diaria en hora pico es balance razonable. |

## Reglas por tipo de tabla

| Tipo | Ejemplos | Cadencia |
| --- | --- | --- |
| Realtime de transporte | `metrobus_vehicle_positions`, `metrobus_trip_updates` | Horaria en dias laborales. |
| Realtime de trafico | `tomtom_cdmx_incidents`, `tomtom_cdmx_flow` | Cada 2 horas en dias laborales. |
| Realtime de bicicletas | `ecobici_gbfs_station_status`, `ecobici_realtime_stations` | Cada 2 horas en dias laborales. |
| Catalogos operativos | `metrobus_gtfs_static_*`, `ecobici_gbfs_station_information` | Semanal o mensual. |
| Historicos publicados por mes | `ecobici_historico_*`, `ecobici_summary_*` | Mensual. |
| Capas contextuales | `denue_*`, `campus_cdmx_base` | Mensual o trimestral. |
| APIs con costo por consulta | `routes_api_*` | Diario en dias laborales; manual si hay restriccion presupuestal. |

## Horario

GitHub Actions usa UTC. Los cron fueron escritos para aproximar horario laboral de `America/Mexico_City`. Si se requiere otra ventana, ajuste las expresiones en `.github/workflows/*.yml`.


## Campañas acotadas de TomTom

El workflow `tomtom-one-month-history.yml` esta pensado para levantar un historico de aproximadamente un mes sin saturar la API:

- Ejecuta 5 capturas diarias aproximadas en horario operativo de CDMX (`06:35`, `10:35`, `14:35`, `18:35` y `22:35`, sujeto a UTC y a GitHub Actions).
- Requiere `TOMTOM_HISTORY_ENABLED=true`, `TOMTOM_HISTORY_START_DATE` y `TOMTOM_HISTORY_END_DATE` para que el schedule haga trabajo real.
- Sale sin consultar la API cuando falta la configuracion o cuando la fecha actual esta fuera de la ventana.
- Usa el mismo grupo de concurrencia que `tomtom-traffic.yml` para evitar extracciones TomTom simultaneas.
- Para minimizar duplicados y consumo de cuota, deshabilite `tomtom-traffic.yml` durante la campaña si no necesita ambos ritmos de captura.
