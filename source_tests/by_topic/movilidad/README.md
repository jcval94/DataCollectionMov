# Tests: Movilidad

[Todas las pruebas](../../README.md) · [Catálogo](../../../docs/CATALOGO_DATASETS_REALES.md)

Resultados y ejemplos de las peticiones indicadas. Las imágenes se comprueban por separado; un portal accesible no equivale a datos ingeridos.

### metrobus-gtfs

**Metrobús: GTFS estático y tiempo real** — `CACHED_SAMPLE`.

Snapshot público del repo; no demuestra respuesta actual del feed autenticado ni todas las tablas GTFS.

**Prueba 1: `CACHED_SAMPLE`** · [csv](https://raw.githubusercontent.com/jcval94/DataCollectionMov/main/data/current/metrobus_vehicle_positions.csv) · HTTP `200`.

Captura UTC: `2026-11-05T00:08:08+00:00`; duración: 3.448 s.

Primeras filas completas del archivo; no se contó el total ni se comprobaron llaves globales.

Contenido: `text/plain; charset=utf-8`; 65,536 bytes leídos; alcance del hash: `response_prefix`.

| Campo | Ejemplo 1 | Ejemplo 2 |
| --- | --- | --- |
| entity_id | 3f98eff3-6ee2-4cfd-9455-8cd0763e8187 | 98cc1a26-2a7e-4e2b-9779-ca4cb9617b08 |
| route_id | 19472 | 19562 |
| trip_id |  |  |
| latitude | 19.491252899169922 | 19.406333923339844 |
| longitude | -99.13525390625 | -99.17977142333984 |
| timestamp_cdmx | 2026-11-04 13:48:53-06:00 | 2026-11-04 13:48:54-06:00 |
| _snapshot_id | 20261104T194911Z | 20261104T194911Z |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "entity_id": "3f98eff3-6ee2-4cfd-9455-8cd0763e8187",
    "route_id": "19472",
    "trip_id": "",
    "latitude": "19.491252899169922",
    "longitude": "-99.13525390625",
    "timestamp_cdmx": "2026-11-04 13:48:53-06:00",
    "_snapshot_id": "20261104T194911Z"
  },
  {
    "entity_id": "98cc1a26-2a7e-4e2b-9779-ca4cb9617b08",
    "route_id": "19562",
    "trip_id": "",
    "latitude": "19.406333923339844",
    "longitude": "-99.17977142333984",
    "timestamp_cdmx": "2026-11-04 13:48:54-06:00",
    "_snapshot_id": "20261104T194911Z"
  }
]
```

</details>

### ecobici-viajes

**ECOBICI: viajes históricos** — `DATA_SAMPLE`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

**Prueba 1: `DATA_SAMPLE`** · [discover_csv](https://ecobici.cdmx.gob.mx/datos-abiertos/) · HTTP `200`.

Captura UTC: `2026-11-05T00:08:09+00:00`; duración: 7.613 s.

Descarga CSV descubierta en página oficial, muestreo por prefijo.

Contenido: `text/html; charset=UTF-8`; 117,065 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 | Ejemplo 2 |
| --- | --- | --- |
| Genero_Usuario | M | F |
| Edad_Usuario | 30.0 | 33.0 |
| Bici | 6583322 | 4139655 |
| Ciclo_Estacion_Retiro | 028 | 030 |
| Fecha_Retiro | 31/08/2026 | 31/08/2026 |
| Hora_Retiro | 23:54:59 | 23:24:43 |
| Ciclo_EstacionArribo | 258 | 530 |
| Fecha_Arribo | 01/09/2026 | 01/09/2026 |
| Hora_Arribo | 00:00:03 | 00:00:04 |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "Genero_Usuario": "M",
    "Edad_Usuario": "30.0",
    "Bici": "6583322",
    "Ciclo_Estacion_Retiro": "028",
    "Fecha_Retiro": "31/08/2026",
    "Hora_Retiro": "23:54:59",
    "Ciclo_EstacionArribo": "258",
    "Fecha_Arribo": "01/09/2026",
    "Hora_Arribo": "00:00:03"
  },
  {
    "Genero_Usuario": "F",
    "Edad_Usuario": "33.0",
    "Bici": "4139655",
    "Ciclo_Estacion_Retiro": "030",
    "Fecha_Retiro": "31/08/2026",
    "Hora_Retiro": "23:24:43",
    "Ciclo_EstacionArribo": "530",
    "Fecha_Arribo": "01/09/2026",
    "Hora_Arribo": "00:00:04"
  }
]
```

</details>

**Recurso enlazado: comprobación independiente**

**Prueba 1.medio: `DATA_SAMPLE`** · [csv](https://ecobici.cdmx.gob.mx/wp-content/uploads/2026/10/public_data_web_2026-09.csv) · HTTP `200`.

Captura UTC: `2026-11-05T00:08:13+00:00`; duración: 3.676 s.

Primeras filas completas del archivo; no se contó el total ni se comprobaron llaves globales.

Contenido: `text/csv`; 65,536 bytes leídos; alcance del hash: `response_prefix`.

| Campo | Ejemplo 1 | Ejemplo 2 |
| --- | --- | --- |
| Genero_Usuario | M | F |
| Edad_Usuario | 30.0 | 33.0 |
| Bici | 6583322 | 4139655 |
| Ciclo_Estacion_Retiro | 028 | 030 |
| Fecha_Retiro | 31/08/2026 | 31/08/2026 |
| Hora_Retiro | 23:54:59 | 23:24:43 |
| Ciclo_EstacionArribo | 258 | 530 |
| Fecha_Arribo | 01/09/2026 | 01/09/2026 |
| Hora_Arribo | 00:00:03 | 00:00:04 |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "Genero_Usuario": "M",
    "Edad_Usuario": "30.0",
    "Bici": "6583322",
    "Ciclo_Estacion_Retiro": "028",
    "Fecha_Retiro": "31/08/2026",
    "Hora_Retiro": "23:54:59",
    "Ciclo_EstacionArribo": "258",
    "Fecha_Arribo": "01/09/2026",
    "Hora_Arribo": "00:00:03"
  },
  {
    "Genero_Usuario": "F",
    "Edad_Usuario": "33.0",
    "Bici": "4139655",
    "Ciclo_Estacion_Retiro": "030",
    "Fecha_Retiro": "31/08/2026",
    "Hora_Retiro": "23:24:43",
    "Ciclo_EstacionArribo": "530",
    "Fecha_Arribo": "01/09/2026",
    "Hora_Arribo": "00:00:04"
  }
]
```

</details>

### ecobici-gbfs

**ECOBICI: catálogo y disponibilidad GBFS** — `DATA_SAMPLE`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

**Prueba 1: `DATA_SAMPLE`** · [gbfs](https://gbfs.mex.lyftbikes.com/gbfs/gbfs.json) · HTTP `200`.

Captura UTC: `2026-11-05T00:08:09+00:00`; duración: 6.769 s.

Descubrimiento GBFS y validación del catálogo de estaciones.

Contenido: `text/plain; charset=UTF-8`; 1,049 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 | Ejemplo 2 |
| --- | --- | --- |
| station_id | 1 | 5 |
| name | CE-710 Molino del Rey - Glorieta de la Lealtad | CE-407  Prolongación Xochicalco-General Emiliano Zapata |
| lat | 19.416795 | 19.36726591257277 |
| lon | -99.192508 | -99.15865559132271 |
| capacity | 39 | 19 |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "station_id": "1",
    "name": "CE-710 Molino del Rey - Glorieta de la Lealtad",
    "lat": 19.416795,
    "lon": -99.192508,
    "capacity": 39
  },
  {
    "station_id": "5",
    "name": "CE-407  Prolongación Xochicalco-General Emiliano Zapata",
    "lat": 19.36726591257277,
    "lon": -99.15865559132271,
    "capacity": 19
  }
]
```

</details>

**Recurso enlazado: comprobación independiente**

**Prueba 1.medio: `DATA_SAMPLE`** · [json](https://gbfs.mex.lyftbikes.com/gbfs/en/station_information.json) · HTTP `200`.

Captura UTC: `2026-11-05T00:08:13+00:00`; duración: 3.316 s.

Formato y campos de la muestra validados; no implica calidad de toda la fuente.

Contenido: `text/plain; charset=UTF-8`; 226,314 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 | Ejemplo 2 |
| --- | --- | --- |
| station_id | 1 | 5 |
| name | CE-710 Molino del Rey - Glorieta de la Lealtad | CE-407  Prolongación Xochicalco-General Emiliano Zapata |
| lat | 19.416795 | 19.36726591257277 |
| lon | -99.192508 | -99.15865559132271 |
| capacity | 39 | 19 |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "station_id": "1",
    "name": "CE-710 Molino del Rey - Glorieta de la Lealtad",
    "lat": 19.416795,
    "lon": -99.192508,
    "capacity": 39
  },
  {
    "station_id": "5",
    "name": "CE-407  Prolongación Xochicalco-General Emiliano Zapata",
    "lat": 19.36726591257277,
    "lon": -99.15865559132271,
    "capacity": 19
  }
]
```

</details>

