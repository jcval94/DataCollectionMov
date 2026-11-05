# Tests: INEGI y contexto

[Todas las pruebas](../../README.md) · [Catálogo](../../../docs/CATALOGO_DATASETS_REALES.md)

Resultados y ejemplos de las peticiones indicadas. Las imágenes se comprueban por separado; un portal accesible no equivale a datos ingeridos.

### inegi-indicadores-api

**API del Banco de Indicadores** — `DOC_ONLY`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

**Prueba 1: `DOC_ONLY`** · [html](https://www.inegi.org.mx/servicios/api-indicadores/) · HTTP `200`.

Captura UTC: `2026-11-05T00:07:41+00:00`; duración: 3.625 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

Contenido: `text/html`; 153,586 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 |
| --- | --- |
| page_title | API del Banco de Indicadores |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "page_title": "API del Banco de Indicadores"
  }
]
```

</details>

### inegi-denue

**DENUE: establecimientos y actividad económica** — `CACHED_SAMPLE`.

La muestra es el CSV público ya recolectado; no se prueba la API autenticada en vivo.

**Prueba 1: `DOC_ONLY`** · [html](https://www.inegi.org.mx/servicios/api-denue/) · HTTP `200`.

Captura UTC: `2026-11-05T00:07:45+00:00`; duración: 3.558 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

Contenido: `text/html`; 100,446 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 |
| --- | --- |
| page_title | API del DENUE |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "page_title": "API del DENUE"
  }
]
```

</details>

**Prueba 2: `CACHED_SAMPLE`** · [csv](https://raw.githubusercontent.com/jcval94/DataCollectionMov/main/data/current/denue_cdmx_sector_61_servicios_educativos.csv) · HTTP `200`.

Captura UTC: `2026-11-05T00:07:48+00:00`; duración: 3.971 s.

Primeras filas completas del archivo; no se contó el total ni se comprobaron llaves globales.

Contenido: `text/plain; charset=utf-8`; 65,536 bytes leídos; alcance del hash: `response_prefix`.

| Campo | Ejemplo 1 | Ejemplo 2 |
| --- | --- | --- |
| id_establecimiento | 9496872 | 824823 |
| clee | 09005611621001441000000000U9 | 09007611122001343002000000U2 |
| nombre | 12 ROUNDS | 24 DE FEBRERO TURNO MATUTINO PRIMARIA CCT 09DPR2087X |
| cp | 07500 | 09510 |
| latitud | 19.48014404 | 19.36841162 |
| longitud | -99.06501588 | -99.01300142 |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "id_establecimiento": "9496872",
    "clee": "09005611621001441000000000U9",
    "nombre": "12 ROUNDS",
    "cp": "07500",
    "latitud": "19.48014404",
    "longitud": "-99.06501588"
  },
  {
    "id_establecimiento": "824823",
    "clee": "09007611122001343002000000U2",
    "nombre": "24 DE FEBRERO TURNO MATUTINO PRIMARIA CCT 09DPR2087X",
    "cp": "09510",
    "latitud": "19.36841162",
    "longitud": "-99.01300142"
  }
]
```

</details>

### inegi-censo-2020-ageb

**Censo 2020: indicadores por AGEB y manzana urbana** — `DOC_ONLY`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

**Prueba 1: `DOC_ONLY`** · [html](https://www.inegi.org.mx/programas/ccpv/2020/) · HTTP `200`.

Captura UTC: `2026-11-05T00:07:45+00:00`; duración: 3.293 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

Contenido: `text/html`; 5,163 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 |
| --- | --- |
| page_title | Censo de Población y Vivienda (CPV) 2020 |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "page_title": "Censo de Población y Vivienda (CPV) 2020"
  }
]
```

</details>

### inegi-marco-geoestadistico

**Marco Geoestadístico y equivalencias** — `DOC_ONLY`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

**Prueba 1: `DOC_ONLY`** · [html](https://www.inegi.org.mx/temas/mg/) · HTTP `200`.

Captura UTC: `2026-11-05T00:07:45+00:00`; duración: 3.301 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

Contenido: `text/html`; 4,265 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 |
| --- | --- |
| page_title | Marco Geoestadístico |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "page_title": "Marco Geoestadístico"
  }
]
```

</details>

### inegi-entorno-urbano-2020

**Características del entorno urbano 2020** — `DOC_ONLY`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

**Prueba 1: `DOC_ONLY`** · [html](https://www.inegi.org.mx/rnm/index.php/catalog/941/related-materials) · HTTP `200`.

Captura UTC: `2026-11-05T00:07:45+00:00`; duración: 3.149 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

Contenido: `text/html; charset=UTF-8`; 273,272 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 |
| --- | --- |
| page_title | Mexico - Características de las Localidades y del Entorno Urbano 2020 |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "page_title": "Mexico - Características de las Localidades y del Entorno Urbano 2020"
  }
]
```

</details>

### inegi-enigh-2024

**ENIGH 2024: ingresos y gastos del hogar** — `DOC_ONLY`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

**Prueba 1: `DOC_ONLY`** · [html](https://www.inegi.org.mx/programas/enigh/nc/2024/) · HTTP `200`.

Captura UTC: `2026-11-05T00:07:48+00:00`; duración: 3.315 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

Contenido: `text/html`; 3,918 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 |
| --- | --- |
| page_title | Encuesta Nacional de Ingresos y Gastos de los Hogares (ENIGH) 2024 |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "page_title": "Encuesta Nacional de Ingresos y Gastos de los Hogares (ENIGH) 2024"
  }
]
```

</details>

### inegi-enoe

**ENOE: empleo, ingresos laborales e informalidad** — `DOC_ONLY`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

**Prueba 1: `DOC_ONLY`** · [html](https://www.inegi.org.mx/programas/enoe/15ymas/) · HTTP `200`.

Captura UTC: `2026-11-05T00:07:48+00:00`; duración: 3.268 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

Contenido: `text/html`; 5,765 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 |
| --- | --- |
| page_title | Encuesta Nacional de Ocupación y Empleo (ENOE), población de 15 años y más de edad |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "page_title": "Encuesta Nacional de Ocupación y Empleo (ENOE), población de 15 años y más de edad"
  }
]
```

</details>

### inegi-eod-zmvm-2017

**Encuesta Origen Destino ZMVM 2017** — `DOC_ONLY`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

**Prueba 1: `DOC_ONLY`** · [html](https://www.inegi.org.mx/programas/eod/2017/default.html) · HTTP `200`.

Captura UTC: `2026-11-05T00:07:49+00:00`; duración: 2.92 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

Contenido: `text/html`; 5,164 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 |
| --- | --- |
| page_title | Encuesta Origen Destino en Hogares de la Zona Metropolitana del Valle de México (EOD) 2017 |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "page_title": "Encuesta Origen Destino en Hogares de la Zona Metropolitana del Valle de México (EOD) 2017"
  }
]
```

</details>

