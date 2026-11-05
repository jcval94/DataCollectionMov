# Tests: Comida, viajes y aplicaciones

[Todas las pruebas](../../README.md) · [Catálogo](../../../docs/CATALOGO_DATASETS_REALES.md)

Resultados y ejemplos de las peticiones indicadas. Las imágenes se comprueban por separado; un portal accesible no equivale a datos ingeridos.

### nyc-restaurantes

**Inspecciones de restaurantes de Nueva York** — `DATA_SAMPLE`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

**Prueba 1: `DATA_SAMPLE`** · [json](https://data.cityofnewyork.us/resource/43nn-pn8j.json?$limit=3) · HTTP `200`.

Captura UTC: `2026-11-05T00:51:41+00:00`; duración: 9.964 s.

Formato y campos de la muestra validados; no implica calidad de toda la fuente.

Contenido: `application/json;charset=utf-8`; 2,033 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 | Ejemplo 2 |
| --- | --- | --- |
| camis | 50160418 | 50177284 |
| dba | MAMAS CHICKEN SHACK HAPPY DUMPLING COCOA CABIN COCOA CABIN | WORLD SPA ENTERTAINMENT LLC |
| boro | Manhattan | Brooklyn |
| zipcode | 10036 | 11230 |
| inspection_date | 1900-01-01T00:00:00.000 | 1900-01-01T00:00:00.000 |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "camis": "50160418",
    "dba": "MAMAS CHICKEN SHACK HAPPY DUMPLING COCOA CABIN COCOA CABIN",
    "boro": "Manhattan",
    "zipcode": "10036",
    "inspection_date": "1900-01-01T00:00:00.000"
  },
  {
    "camis": "50177284",
    "dba": "WORLD SPA ENTERTAINMENT LLC",
    "boro": "Brooklyn",
    "zipcode": "11230",
    "inspection_date": "1900-01-01T00:00:00.000"
  }
]
```

</details>

### openflights-red-aerea

**Aeropuertos, aerolíneas, aviones y rutas históricas** — `DATA_SAMPLE`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

**Prueba 1: `DATA_SAMPLE`** · [csv](https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat) · HTTP `200`.

Captura UTC: `2026-11-05T00:51:41+00:00`; duración: 5.231 s.

Primeras filas completas del archivo; no se contó el total ni se comprobaron llaves globales.

Contenido: `text/plain; charset=utf-8`; 65,536 bytes leídos; alcance del hash: `response_prefix`.

| Campo | Ejemplo 1 | Ejemplo 2 |
| --- | --- | --- |
| airport_id | 1 | 2 |
| name | Goroka Airport | Madang Airport |
| country | Papua New Guinea | Papua New Guinea |
| iata | GKA | MAG |
| latitude | -6.081689834590001 | -5.20707988739 |
| longitude | 145.391998291 | 145.789001465 |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "airport_id": "1",
    "name": "Goroka Airport",
    "country": "Papua New Guinea",
    "iata": "GKA",
    "latitude": "-6.081689834590001",
    "longitude": "145.391998291"
  },
  {
    "airport_id": "2",
    "name": "Madang Airport",
    "country": "Papua New Guinea",
    "iata": "MAG",
    "latitude": "-5.20707988739",
    "longitude": "145.789001465"
  }
]
```

</details>

**Prueba 2: `DATA_SAMPLE`** · [csv](https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat) · HTTP `200`.

Captura UTC: `2026-11-05T00:51:46+00:00`; duración: 3.454 s.

Primeras filas completas del archivo; no se contó el total ni se comprobaron llaves globales.

Contenido: `text/plain; charset=utf-8`; 65,536 bytes leídos; alcance del hash: `response_prefix`.

| Campo | Ejemplo 1 | Ejemplo 2 |
| --- | --- | --- |
| airline | 2B | 2B |
| airline_id | 410 | 410 |
| source_airport | AER | ASF |
| source_id | 2965 | 2966 |
| dest_airport | KZN | KZN |
| dest_id | 2990 | 2990 |
| codeshare |  |  |
| stops | 0 | 0 |
| equipment | CR2 | CR2 |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "airline": "2B",
    "airline_id": "410",
    "source_airport": "AER",
    "source_id": "2965",
    "dest_airport": "KZN",
    "dest_id": "2990",
    "codeshare": "",
    "stops": "0",
    "equipment": "CR2"
  },
  {
    "airline": "2B",
    "airline_id": "410",
    "source_airport": "ASF",
    "source_id": "2966",
    "dest_airport": "KZN",
    "dest_id": "2990",
    "codeshare": "",
    "stops": "0",
    "equipment": "CR2"
  }
]
```

</details>

### bts-puntualidad-vuelos

**Puntualidad, cancelaciones y demoras aéreas** — `DOC_ONLY`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

**Prueba 1: `DOC_ONLY`** · [html](https://transtats.bts.gov/ONTIME/) · HTTP `200`.

Captura UTC: `2026-11-05T00:51:41+00:00`; duración: 4.982 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

Contenido: `text/html; charset=utf-8`; 59,532 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 |
| --- | --- |
| page_title | On-Time Index pageLockU.S. Department of TransportationUnited States Department of Transportation |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "page_title": "On-Time Index pageLockU.S. Department of TransportationUnited States Department of Transportation"
  }
]
```

</details>

### apple-apps

**Catálogo público de apps de Apple** — `DATA_SAMPLE`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

**Prueba 1: `DATA_SAMPLE`** · [json](https://itunes.apple.com/search?term=travel&entity=software&country=mx&limit=3) · HTTP `200`.

Captura UTC: `2026-11-05T00:51:41+00:00`; duración: 4.707 s.

Formato y campos de la muestra validados; no implica calidad de toda la fuente.

Contenido: `text/javascript; charset=utf-8`; 33,441 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 | Ejemplo 2 |
| --- | --- | --- |
| trackId | 912390687 | 427916203 |
| trackName | TREBEL Music - Download Songs | Expedia: hoteles y vuelos |
| primaryGenreName | Music | Travel |
| price | 0.0 | 0.0 |
| currency | MXN | MXN |
| averageUserRating | 4.70673 | 4.852 |
| userRatingCount | 470548 | 371599 |
| version | 7.9.9 | 2026.44 |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "trackId": 912390687,
    "trackName": "TREBEL Music - Download Songs",
    "primaryGenreName": "Music",
    "price": 0.0,
    "currency": "MXN",
    "averageUserRating": 4.70673,
    "userRatingCount": 470548,
    "version": "7.9.9"
  },
  {
    "trackId": 427916203,
    "trackName": "Expedia: hoteles y vuelos",
    "primaryGenreName": "Travel",
    "price": 0.0,
    "currency": "MXN",
    "averageUserRating": 4.852,
    "userRatingCount": 371599,
    "version": "2026.44"
  }
]
```

</details>

**Ejemplo visual y su test**

<a href="https://apps.apple.com/mx/app/trebel-music-download-songs/id912390687"><img src="https://is1-ssl.mzstatic.com/image/thumb/Purple211/v4/a0/14/42/a01442bd-26bc-26cf-f816-efc7c7c2a3eb/AppIcon-0-0-1x_U007emarketing-0-8-0-85-220.png/100x100bb.jpg" alt="Icono de TREBEL Music — ficha de App Store México" width="420"></a>

**Icono de TREBEL Music — ficha de App Store México**. TREBEL Music; icono servido por Apple App Store. [Ficha original](https://apps.apple.com/mx/app/trebel-music-download-songs/id912390687) · [Licencia y condiciones](https://www.apple.com/legal/internet-services/itunes/): Derechos de sus titulares; icono remoto, sin licencia abierta confirmada.

Prueba de imagen: **`IMAGE_DECODED`**, HTTP `200`, `JPEG`, **100 × 100 px**, 2,857 bytes. Captura UTC: `2026-11-05T03:19:59+00:00`.

Icono de la ficha recuperada; no acredita instalaciones, usuarios activos ni acceso al código de la app.

Imagen incrustada desde el proveedor; su visualización depende de que esa URL siga disponible.

GET completo y decodificación de píxeles comprobados. SHA-256 completo: `348aeb47032c868a5115d3f766756af5d1348d990daca71b4c8815087e2b9625`. [Metadatos de origen](https://itunes.apple.com/lookup?id=912390687&country=mx).

### apple-resenas-apps

**Reseñas públicas de apps por tienda** — `DATA_SAMPLE`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

**Prueba 1: `DATA_SAMPLE`** · [json](https://itunes.apple.com/mx/rss/customerreviews/id=310633997/sortBy=mostRecent/json) · HTTP `200`.

Captura UTC: `2026-11-05T00:51:45+00:00`; duración: 3.811 s.

Formato y campos de la muestra validados; no implica calidad de toda la fuente.

Contenido: `text/javascript; charset=UTF-8`; 38,785 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 |
| --- | --- |
| id.label | 14746272762 |
| im:rating.label | 1 |
| im:version.label | 26.43.75 |
| title.label | Hackean |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "id.label": "14746272762",
    "im:rating.label": "1",
    "im:version.label": "26.43.75",
    "title.label": "Hackean"
  }
]
```

</details>

### insideairbnb-cdmx

**Alojamiento turístico: Inside Airbnb CDMX** — `DATA_SAMPLE`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

**Prueba 1: `DATA_SAMPLE`** · [csv](https://data.insideairbnb.com/mexico/df/mexico-city/2026-09-23/visualisations/listings.csv) · HTTP `200`.

Captura UTC: `2026-11-05T00:51:46+00:00`; duración: 4.238 s.

Primeras filas completas del archivo; no se contó el total ni se comprobaron llaves globales.

Contenido: `application/csv`; 65,536 bytes leídos; alcance del hash: `response_prefix`.

| Campo | Ejemplo 1 | Ejemplo 2 |
| --- | --- | --- |
| id | 35797 | 44616 |
| neighbourhood | Cuajimalpa de Morelos | Cuauhtémoc |
| room_type | Private room | Entire home/apt |
| price | 8874 | 21950 |
| minimum_nights | 1 | 1 |
| number_of_reviews | 0 | 67 |
| availability_365 | 363 | 361 |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "id": "35797",
    "neighbourhood": "Cuajimalpa de Morelos",
    "room_type": "Private room",
    "price": "8874",
    "minimum_nights": "1",
    "number_of_reviews": "0",
    "availability_365": "363"
  },
  {
    "id": "44616",
    "neighbourhood": "Cuauhtémoc",
    "room_type": "Entire home/apt",
    "price": "21950",
    "minimum_nights": "1",
    "number_of_reviews": "67",
    "availability_365": "361"
  }
]
```

</details>

