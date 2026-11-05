# Prueba de acceso y muestras de fuentes

Ejecución: **2026-11-04T18:07:41-06:00** (America/Mexico_City). Fin UTC: `2026-11-05T00:53:57+00:00`.

Se probaron **72 fuentes** del catálogo mediante GET públicos, con timeout de 18 s por operación, 4 fuentes en paralelo y un límite de 8388608 bytes para documentos completos. CSV/TXT se muestrean por prefijo de 64 KiB.

**Qué comprueba:** acceso desde este entorno, formato, campos mínimos y ejemplos recuperados. **Qué no comprueba:** disponibilidad futura, calidad estadística completa, autenticación de APIs protegidas, decodificación/reproducción integral de multimedia, ni salud de los workflows existentes. Una página HTTP 200 no se cuenta como un dataset recuperado.

Los ejemplos se tomaron de las respuestas; los datos no disponibles no se sustituyen por filas inventadas. `CACHED_SAMPLE` identifica CSVs ya publicados por el repo, separados de las APIs en vivo. `METADATA_SAMPLE` prueba un catálogo/manifiesto, no los eventos u observaciones que referencia.

## Alcance de este informe acumulado

Se conservan las **45 fuentes** comprobadas en la entrega anterior y se añaden **27** pruebas nuevas. Las anteriores no se volvieron a solicitar por la ampliación del catálogo. La corrida nueva comenzó en `2026-11-04T18:51:41-06:00`; se recomprobaron selectivamente los dos portales con respuestas incompletas para añadir sus páginas oficiales de documentación. Los errores de la capa de datos se conservan en cada ficha.

`results.json` conserva la corrida anterior, su recomprobación de Xeno-canto, la nueva corrida en `extensions`, los resultados anteriores de las dos fichas recomprobadas y el hash del programa/definiciones por captura. El título de resultado muestra la capa más útil recuperada; la columna de fallos y el detalle conservan las capas que fallaron.

Además del acceso, se ejecutó un [piloto descriptivo con Bob Ross](../examples/bob_ross_discovery/README.md). La [guía de descubrimientos](../docs/GUIA_DESCUBRIMIENTOS_IA.md) distingue preguntas abiertas y resultados ya medidos.

## Resultados

| Resultado | Fuentes |
| --- | ---: |
| BLOCKED: Acceso bloqueado | 6 |
| CACHED_SAMPLE: Registros del repo | 2 |
| DATA_SAMPLE: Registros recuperados | 22 |
| DOCUMENT_SAMPLE: Documento recuperado | 5 |
| DOC_ONLY: Sólo portal/documentación | 22 |
| HTTP_ERROR: Error HTTP | 10 |
| METADATA_SAMPLE: Sólo catálogo/manifiesto | 5 |

## Índice de las pruebas

| Fuente | Resultado más útil | Capas con fallo o límite |
| --- | --- | --- |
| [rifa-235-premios](#rifa-235-premios) | HTTP_ERROR | HTTP_ERROR |
| [rifa-235-reportes](#rifa-235-reportes) | BLOCKED | BLOCKED |
| [rifa-235-asf](#rifa-235-asf) | DOCUMENT_SAMPLE | — |
| [inegi-indicadores-api](#inegi-indicadores-api) | DOC_ONLY | — |
| [inegi-denue](#inegi-denue) | CACHED_SAMPLE | — |
| [inegi-censo-2020-ageb](#inegi-censo-2020-ageb) | DOC_ONLY | — |
| [inegi-marco-geoestadistico](#inegi-marco-geoestadistico) | DOC_ONLY | — |
| [inegi-entorno-urbano-2020](#inegi-entorno-urbano-2020) | DOC_ONLY | — |
| [inegi-enigh-2024](#inegi-enigh-2024) | DOC_ONLY | — |
| [inegi-enoe](#inegi-enoe) | DOC_ONLY | — |
| [inegi-eod-zmvm-2017](#inegi-eod-zmvm-2017) | DOC_ONLY | — |
| [sepomex-codigos-postales](#sepomex-codigos-postales) | DOC_ONLY | — |
| [cdmx-codigos-postales-poligonos](#cdmx-codigos-postales-poligonos) | HTTP_ERROR | HTTP_ERROR, HTTP_ERROR |
| [shcp-pef](#shcp-pef) | BLOCKED | BLOCKED |
| [shcp-cuenta-publica](#shcp-cuenta-publica) | HTTP_ERROR | HTTP_ERROR |
| [shcp-srft](#shcp-srft) | HTTP_ERROR | HTTP_ERROR |
| [sep-cct](#sep-cct) | DOC_ONLY | — |
| [sep-formato-911](#sep-formato-911) | BLOCKED | BLOCKED |
| [anuies-anuario](#anuies-anuario) | DOC_ONLY | — |
| [ceey-emovi-2023](#ceey-emovi-2023) | DOC_ONLY | BLOCKED |
| [ceey-emovi-2017](#ceey-emovi-2017) | DOC_ONLY | BLOCKED |
| [inegi-mmsi-2016](#inegi-mmsi-2016) | DOC_ONLY | — |
| [coneval-pobreza-municipal](#coneval-pobreza-municipal) | DOC_ONLY | — |
| [conapo-marginacion-2020](#conapo-marginacion-2020) | BLOCKED | BLOCKED |
| [metrobus-gtfs](#metrobus-gtfs) | CACHED_SAMPLE | — |
| [ecobici-viajes](#ecobici-viajes) | DATA_SAMPLE | — |
| [ecobici-gbfs](#ecobici-gbfs) | DATA_SAMPLE | — |
| [salud-clues](#salud-clues) | HTTP_ERROR | HTTP_ERROR |
| [cdmx-fgj-carpetas](#cdmx-fgj-carpetas) | HTTP_ERROR | HTTP_ERROR, HTTP_ERROR |
| [inegi-atus](#inegi-atus) | DOC_ONLY | — |
| [dof-publicaciones](#dof-publicaciones) | DOCUMENT_SAMPLE | — |
| [usgs-sismos](#usgs-sismos) | DATA_SAMPLE | — |
| [nasa-exoplanetas](#nasa-exoplanetas) | DATA_SAMPLE | — |
| [gwosc-ondas-gravitacionales](#gwosc-ondas-gravitacionales) | HTTP_ERROR | HTTP_ERROR |
| [noaa-ghcn](#noaa-ghcn) | METADATA_SAMPLE | — |
| [gbif-biodiversidad](#gbif-biodiversidad) | DATA_SAMPLE | — |
| [xeno-canto-audio](#xeno-canto-audio) | DATA_SAMPLE | — |
| [met-arte](#met-arte) | DATA_SAMPLE | — |
| [loc-prensa-historica](#loc-prensa-historica) | METADATA_SAMPLE | — |
| [gutenberg-quijote](#gutenberg-quijote) | DOCUMENT_SAMPLE | — |
| [openfoodfacts-alimentos](#openfoodfacts-alimentos) | DATA_SAMPLE | — |
| [nuforc-ovnis](#nuforc-ovnis) | DOC_ONLY | — |
| [gdelt-noticias](#gdelt-noticias) | METADATA_SAMPLE | — |
| [nasa-bolidos](#nasa-bolidos) | DATA_SAMPLE | — |
| [nyc-ratas](#nyc-ratas) | DATA_SAMPLE | — |
| [nyc-restaurantes](#nyc-restaurantes) | DATA_SAMPLE | — |
| [openflights-red-aerea](#openflights-red-aerea) | DATA_SAMPLE | — |
| [bts-puntualidad-vuelos](#bts-puntualidad-vuelos) | DOC_ONLY | — |
| [apple-apps](#apple-apps) | DATA_SAMPLE | — |
| [apple-resenas-apps](#apple-resenas-apps) | DATA_SAMPLE | — |
| [insideairbnb-cdmx](#insideairbnb-cdmx) | DATA_SAMPLE | — |
| [napoleonica-cartas](#napoleonica-cartas) | DOC_ONLY | — |
| [gallica-napoleon](#gallica-napoleon) | BLOCKED | BLOCKED |
| [pepys-diarios](#pepys-diarios) | DOCUMENT_SAMPLE | — |
| [musicbrainz-conciertos](#musicbrainz-conciertos) | DOC_ONLY | PARSE_ERROR |
| [setlist-conciertos](#setlist-conciertos) | DOC_ONLY | — |
| [osm-mapas-restaurantes](#osm-mapas-restaurantes) | HTTP_ERROR | HTTP_ERROR |
| [loc-mapas-historicos](#loc-mapas-historicos) | METADATA_SAMPLE | — |
| [gsm8k-examenes](#gsm8k-examenes) | DATA_SAMPLE | — |
| [unam-colecciones](#unam-colecciones) | HTTP_ERROR | HTTP_ERROR |
| [unam-agenda-estadistica](#unam-agenda-estadistica) | DOC_ONLY | PARSE_ERROR |
| [unam-guias-examenes](#unam-guias-examenes) | DOCUMENT_SAMPLE | — |
| [ct-ventas-inmuebles](#ct-ventas-inmuebles) | DATA_SAMPLE | — |
| [cmu-movimiento-baile](#cmu-movimiento-baile) | HTTP_ERROR | HTTP_ERROR |
| [aist-dance](#aist-dance) | DOC_ONLY | — |
| [artic-pintura](#artic-pintura) | BLOCKED | BLOCKED |
| [dracor-teatro](#dracor-teatro) | DATA_SAMPLE | — |
| [uci-retail](#uci-retail) | DATA_SAMPLE | — |
| [openfda-etiquetas](#openfda-etiquetas) | DATA_SAMPLE | — |
| [wellcome-medicina-antigua](#wellcome-medicina-antigua) | METADATA_SAMPLE | — |
| [bob-ross-elementos](#bob-ross-elementos) | DATA_SAMPLE | — |
| [bob-ross-paletas](#bob-ross-paletas) | DATA_SAMPLE | — |

## Interpretación y siguientes correcciones

- Registros recuperados permiten comenzar una exploración de esa muestra; no prueban representatividad ni unicidad global.
- Portales, índices y documentación requieren un segundo paso para obtener la base. Consultar cada ficha para autenticación, licencia y unidad de análisis.
- Un bloqueo/error queda registrado con URL, código y hora. Reintentar sólo esa fuente desde otro momento o entorno autorizado; no afirmar que el sitio está caído globalmente.
- Las muestras por prefijo no dan un conteo total ni una muestra aleatoria. Un hash de prefijo no identifica el archivo completo.
- En fuentes mixtas se indica la capa probada. Una URL de imagen o audio presente no demuestra descarga o reproducción del medio.
- Para citar resultados científicos, de encuestas o territoriales, añadir una validación del diseño, calidad y cobertura antes de inferir conclusiones.

## Reproducir

Desde la raíz del repo (Python 3.10+; `pypdf` y `openpyxl` son lectores opcionales):

```bash
python -m pip install pypdf openpyxl
python scripts/probe_catalog_sources.py
python scripts/probe_catalog_sources.py --only dof-publicaciones usgs-sismos
```

No lee secrets ni activa tareas programadas. Sin `--strict`, el código de salida 0 significa que el informe se produjo; los fallos permanecen visibles. Con `--strict` devuelve 1 si falla cualquier comprobación definida, incluidos recursos enlazados. Un `DOC_ONLY` válido pasa su comprobación de página, pero sigue sin acreditar ingesta de registros.

La selección `--only` guarda resultados en un subdirectorio `selected/` para conservar la última corrida completa. Se puede cambiar con `--output`. El informe y results.json se generan juntos.

## Ejemplos y evidencia por fuente

### rifa-235-premios

**GSE 235: lista oficial de premios** — `HTTP_ERROR`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [pdf](https://www.lotenal.gob.mx/Comercial/Listas/235.pdf) — `HTTP_ERROR`; HTTP `503`; 3.628 s.

HTTP 503: Service Unavailable. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

### rifa-235-reportes

**GSE 235: balance y beneficiarios publicados** — `BLOCKED`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [html](https://www.gob.mx/lotenal/prensa/197193) — `BLOCKED`; HTTP `403`; 4.167 s.

HTTP 403: Forbidden. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

### rifa-235-asf

**GSE 235: auditoría de gestión financiera** — `DOCUMENT_SAMPLE`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [pdf](https://www.asf.gob.mx/Trans/Informes/IR2020c/Documentos/Auditorias/2020_0051_a.pdf) — `DOCUMENT_SAMPLE`; HTTP `200`; 3.541 s.

Firma PDF y extracción de una página validadas; sin OCR ni auditoría de todas sus tablas.

```json
[
  {
    "page": 28,
    "excerpt": "Informe Individual del Resultado de la Fiscalización Superior de la Cuenta Pública 2020 28 Celebración del sorteo De conformidad con"
  }
]
```

### inegi-indicadores-api

**API del Banco de Indicadores** — `DOC_ONLY`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [html](https://www.inegi.org.mx/servicios/api-indicadores/) — `DOC_ONLY`; HTTP `200`; 3.625 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

```json
[
  {
    "page_title": "API del Banco de Indicadores"
  }
]
```

### inegi-denue

**DENUE: establecimientos y actividad económica** — `CACHED_SAMPLE`.

La muestra es el CSV público ya recolectado; no se prueba la API autenticada en vivo.

Prueba 1: [html](https://www.inegi.org.mx/servicios/api-denue/) — `DOC_ONLY`; HTTP `200`; 3.558 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

```json
[
  {
    "page_title": "API del DENUE"
  }
]
```

Prueba 2: [csv](https://raw.githubusercontent.com/jcval94/DataCollectionMov/main/data/current/denue_cdmx_sector_61_servicios_educativos.csv) — `CACHED_SAMPLE`; HTTP `200`; 3.971 s.

Primeras filas completas del archivo; no se contó el total ni se comprobaron llaves globales.

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

### inegi-censo-2020-ageb

**Censo 2020: indicadores por AGEB y manzana urbana** — `DOC_ONLY`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [html](https://www.inegi.org.mx/programas/ccpv/2020/) — `DOC_ONLY`; HTTP `200`; 3.293 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

```json
[
  {
    "page_title": "Censo de Población y Vivienda (CPV) 2020"
  }
]
```

### inegi-marco-geoestadistico

**Marco Geoestadístico y equivalencias** — `DOC_ONLY`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [html](https://www.inegi.org.mx/temas/mg/) — `DOC_ONLY`; HTTP `200`; 3.301 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

```json
[
  {
    "page_title": "Marco Geoestadístico"
  }
]
```

### inegi-entorno-urbano-2020

**Características del entorno urbano 2020** — `DOC_ONLY`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [html](https://www.inegi.org.mx/rnm/index.php/catalog/941/related-materials) — `DOC_ONLY`; HTTP `200`; 3.149 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

```json
[
  {
    "page_title": "Mexico - Características de las Localidades y del Entorno Urbano 2020"
  }
]
```

### inegi-enigh-2024

**ENIGH 2024: ingresos y gastos del hogar** — `DOC_ONLY`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [html](https://www.inegi.org.mx/programas/enigh/nc/2024/) — `DOC_ONLY`; HTTP `200`; 3.315 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

```json
[
  {
    "page_title": "Encuesta Nacional de Ingresos y Gastos de los Hogares (ENIGH) 2024"
  }
]
```

### inegi-enoe

**ENOE: empleo, ingresos laborales e informalidad** — `DOC_ONLY`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [html](https://www.inegi.org.mx/programas/enoe/15ymas/) — `DOC_ONLY`; HTTP `200`; 3.268 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

```json
[
  {
    "page_title": "Encuesta Nacional de Ocupación y Empleo (ENOE), población de 15 años y más de edad"
  }
]
```

### inegi-eod-zmvm-2017

**Encuesta Origen Destino ZMVM 2017** — `DOC_ONLY`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [html](https://www.inegi.org.mx/programas/eod/2017/default.html) — `DOC_ONLY`; HTTP `200`; 2.92 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

```json
[
  {
    "page_title": "Encuesta Origen Destino en Hogares de la Zona Metropolitana del Valle de México (EOD) 2017"
  }
]
```

### sepomex-codigos-postales

**Catálogo Nacional de Códigos Postales** — `DOC_ONLY`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [html](https://www.correosdemexico.gob.mx/SSLServicios/ConsultaCP/CodigoPostal_Exportar.aspx) — `DOC_ONLY`; HTTP `200`; 3.039 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

```json
[
  {
    "page_title": "Descarga de Códigos Postales"
  }
]
```

### cdmx-codigos-postales-poligonos

**Códigos postales CDMX: capa geográfica** — `HTTP_ERROR`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [html](https://www.datos.cdmx.gob.mx/es_AR/dataset/codigos-postales) — `HTTP_ERROR`; HTTP `503`; 8.096 s.

HTTP 503: Service Unavailable. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

Prueba 2: [ckan](https://datos.cdmx.gob.mx/api/3/action/package_show?id=codigos-postales) — `HTTP_ERROR`; HTTP `503`; 8.37 s.

HTTP 503: Service Unavailable. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

### shcp-pef

**Presupuesto de Egresos de la Federación aprobado** — `BLOCKED`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [html](https://www.datos.gob.mx/dataset/presupuesto_egresos_federacion_pef) — `BLOCKED`; HTTP `403`; 3.445 s.

HTTP 403: Forbidden. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

### shcp-cuenta-publica

**Cuenta Pública: gasto al cierre** — `HTTP_ERROR`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [html](https://www.transparenciapresupuestaria.gob.mx/es/PTP/Cuenta_Publica_2025) — `HTTP_ERROR`; HTTP `503`; 3.065 s.

HTTP 503: Service Unavailable. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

### shcp-srft

**SRFT: ejercicio y destino del gasto federalizado** — `HTTP_ERROR`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [html](https://www.transparenciapresupuestaria.gob.mx/Entidades-Federativas) — `HTTP_ERROR`; HTTP `503`; 0.941 s.

HTTP 503: Service Unavailable. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

### sep-cct

**Catálogo de Centros de Trabajo** — `DOC_ONLY`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [html](https://siged.sep.gob.mx/SIGED/datos_abiertos.html) — `DOC_ONLY`; HTTP `200`; 3.762 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

```json
[
  {
    "page_title": "SEP | SIGED"
  }
]
```

### sep-formato-911

**Formato 911: alumnado, docentes y escuelas** — `BLOCKED`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [html](https://www.datos.gob.mx/dataset/registro_alumnado_personal_docente_educacion_basica_media_superior_formato_911) — `BLOCKED`; HTTP `403`; 3.123 s.

HTTP 403: Forbidden. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

### anuies-anuario

**Anuario Estadístico de Educación Superior** — `DOC_ONLY`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [html](https://anuario.anuies.mx/) — `DOC_ONLY`; HTTP `200`; 4.07 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

```json
[
  {
    "page_title": "Anuarios ANUIES"
  }
]
```

### ceey-emovi-2023

**ESRU–EMOVI 2023** — `DOC_ONLY`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [html](https://ceey.org.mx/contenido/que-hacemos/emovi/) — `DOC_ONLY`; HTTP `200`; 3.972 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

```json
[
  {
    "page_title": "ESRU – EMOVI – Centro de Estudios Espinosa Yglesias"
  }
]
```

Prueba 2: [html](https://drive.google.com/file/d/1r736z5vok0ss68cIW11SnZ5_MR0bUiDC/view?usp=drive_link) — `BLOCKED`; HTTP `429`; 7.045 s.

HTTP 429: Too Many Requests. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

### ceey-emovi-2017

**ESRU–EMOVI 2017** — `DOC_ONLY`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [html](https://ceey.org.mx/contenido/que-hacemos/emovi/) — `DOC_ONLY`; HTTP `200`; 3.828 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

```json
[
  {
    "page_title": "ESRU – EMOVI – Centro de Estudios Espinosa Yglesias"
  }
]
```

Prueba 2: [html](https://drive.google.com/file/d/1hko58nfnlexpw5kiB1K0kqeXlOPAaGyr/view?usp=sharing) — `BLOCKED`; HTTP `429`; 7.003 s.

HTTP 429: Too Many Requests. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

### inegi-mmsi-2016

**Módulo de Movilidad Social Intergeneracional 2016** — `DOC_ONLY`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [html](https://www.inegi.org.mx/programas/mmsi/2016/) — `DOC_ONLY`; HTTP `200`; 3.917 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

```json
[
  {
    "page_title": "Módulo de Movilidad Social Intergeneracional (MMSI) 2016"
  }
]
```

### coneval-pobreza-municipal

**Pobreza municipal 2010–2020** — `DOC_ONLY`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [html](https://www.coneval.org.mx/Medicion/Paginas/Programas_BD_municipal_2010_2020.aspx) — `DOC_ONLY`; HTTP `200`; 3.808 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

```json
[
  {
    "page_title": "Bases de datos y programas de cálculo pobreza municipal 2010-2020"
  }
]
```

### conapo-marginacion-2020

**Índices de marginación 2020** — `BLOCKED`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [html](https://www.gob.mx/conapo/documentos/indices-de-marginacion-2020-284372) — `BLOCKED`; HTTP `403`; 5.113 s.

HTTP 403: Forbidden. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

### metrobus-gtfs

**Metrobús: GTFS estático y tiempo real** — `CACHED_SAMPLE`.

Snapshot público del repo; no demuestra respuesta actual del feed autenticado ni todas las tablas GTFS.

Prueba 1: [csv](https://raw.githubusercontent.com/jcval94/DataCollectionMov/main/data/current/metrobus_vehicle_positions.csv) — `CACHED_SAMPLE`; HTTP `200`; 3.448 s.

Primeras filas completas del archivo; no se contó el total ni se comprobaron llaves globales.

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

### ecobici-viajes

**ECOBICI: viajes históricos** — `DATA_SAMPLE`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [discover_csv](https://ecobici.cdmx.gob.mx/datos-abiertos/) — `DATA_SAMPLE`; HTTP `200`; 7.613 s.

Descarga CSV descubierta en página oficial, muestreo por prefijo.

Recurso enlazado: [csv](https://ecobici.cdmx.gob.mx/wp-content/uploads/2026/10/public_data_web_2026-09.csv) — `DATA_SAMPLE`, HTTP `200`.

Primeras filas completas del archivo; no se contó el total ni se comprobaron llaves globales.

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

### ecobici-gbfs

**ECOBICI: catálogo y disponibilidad GBFS** — `DATA_SAMPLE`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [gbfs](https://gbfs.mex.lyftbikes.com/gbfs/gbfs.json) — `DATA_SAMPLE`; HTTP `200`; 6.769 s.

Descubrimiento GBFS y validación del catálogo de estaciones.

Recurso enlazado: [json](https://gbfs.mex.lyftbikes.com/gbfs/en/station_information.json) — `DATA_SAMPLE`, HTTP `200`.

Formato y campos de la muestra validados; no implica calidad de toda la fuente.

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

### salud-clues

**CLUES: establecimientos de salud** — `HTTP_ERROR`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [xlsx](https://gobi.salud.gob.mx/historico_clues/ESTABLECIMIENTO_SALUD_202609.xlsx?v=1.1) — `HTTP_ERROR`; HTTP `503`; 8.294 s.

HTTP 503: Service Unavailable. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

### cdmx-fgj-carpetas

**Carpetas de investigación FGJ CDMX** — `HTTP_ERROR`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [html](https://datos.cdmx.gob.mx/dataset/carpetas-de-investigacion-fgj-de-la-ciudad-de-mexico) — `HTTP_ERROR`; HTTP `503`; 9.02 s.

HTTP 503: Service Unavailable. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

Prueba 2: [ckan](https://datos.cdmx.gob.mx/api/3/action/package_show?id=carpetas-de-investigacion-fgj-de-la-ciudad-de-mexico) — `HTTP_ERROR`; HTTP `503`; 8.201 s.

HTTP 503: Service Unavailable. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

### inegi-atus

**ATUS: accidentes de tránsito urbanos y suburbanos** — `DOC_ONLY`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [html](https://www.inegi.org.mx/programas/accidentes/default.html) — `DOC_ONLY`; HTTP `200`; 3.089 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

```json
[
  {
    "page_title": "Accidentes de Tránsito Terrestre en Zonas Urbanas y Suburbanas (ATUS)"
  }
]
```

### dof-publicaciones

**DOF/SIDOF: publicaciones y reformas para explicar Git** — `DOCUMENT_SAMPLE`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [html](https://sidof.segob.gob.mx/datos_abiertos) — `DOC_ONLY`; HTTP `200`; 4.835 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

```json
[
  {
    "page_title": "Diario Oficial de la Federación || Datos abiertos"
  }
]
```

Prueba 2: [dof](https://sidof.segob.gob.mx/notas/docFuente/5675889) — `DOCUMENT_SAMPLE`; HTTP `200`; 3.921 s.

Texto real de nota histórica; campos extraídos/normalizados para la demostración.

```json
[
  {
    "codigo": "5675889",
    "titulo": "Decreto de reforma de los artículos 76 y 78 de la LFT",
    "publicacion": "2022-12-27",
    "nuevo_minimo_dias": 12,
    "entrada_vigor": "2023-01-01"
  }
]
```

### usgs-sismos

**Terremotos del último día y sus revisiones** — `DATA_SAMPLE`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [geojson](https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson) — `DATA_SAMPLE`; HTTP `200`; 3.331 s.

Formato y campos de la muestra validados; no implica calidad de toda la fuente.

```json
[
  {
    "id": "ci41358519",
    "properties.title": "M 0.8 - 10 km SW of Idyllwild, CA",
    "properties.mag": 0.83,
    "properties.time": 1793837018700,
    "properties.updated": 1793837221405,
    "geometry.coordinates": [
      -116.780666666667,
      33.6643333333333,
      13.53
    ]
  },
  {
    "id": "ci41358511",
    "properties.title": "M 0.9 - 13 km SE of Tehachapi, CA",
    "properties.mag": 0.92,
    "properties.time": 1793835466310,
    "properties.updated": 1793835679040,
    "geometry.coordinates": [
      -118.332666666667,
      35.0611666666667,
      1.7
    ]
  }
]
```

### nasa-exoplanetas

**Planetas fuera del Sistema Solar** — `DATA_SAMPLE`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [csv](https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+top+3+pl_name,hostname,discoverymethod,disc_year,pl_orbper+from+pscomppars&format=csv) — `DATA_SAMPLE`; HTTP `200`; 4.195 s.

Primeras filas completas del archivo; no se contó el total ni se comprobaron llaves globales.

```json
[
  {
    "pl_name": "55 Cnc b",
    "hostname": "55 Cnc",
    "discoverymethod": "Radial Velocity",
    "disc_year": "1996",
    "pl_orbper": "14.65155200000"
  },
  {
    "pl_name": "55 Cnc c",
    "hostname": "55 Cnc",
    "discoverymethod": "Radial Velocity",
    "disc_year": "2004",
    "pl_orbper": "44.39360000000"
  }
]
```

### gwosc-ondas-gravitacionales

**Colisiones de agujeros negros y ondas gravitacionales** — `HTTP_ERROR`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [json](https://gwosc.org/api/v2/catalogs?format=json) — `HTTP_ERROR`; HTTP `503`; 7.969 s.

HTTP 503: Service Unavailable. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

### noaa-ghcn

**El clima escrito por estaciones meteorológicas** — `METADATA_SAMPLE`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [noaa_fixed](https://www.ncei.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt) — `METADATA_SAMPLE`; HTTP `200`; 3.372 s.

Catálogo de estaciones de ancho fijo; observaciones meteorológicas no probadas.

```json
[
  {
    "station_id": "ACW00011604",
    "latitude": 17.1167,
    "longitude": -61.7833,
    "elevation_m": 10.1,
    "name": "ST JOHNS COOLIDGE FLD"
  },
  {
    "station_id": "ACW00011647",
    "latitude": 17.1333,
    "longitude": -61.7833,
    "elevation_m": 19.2,
    "name": "ST JOHNS"
  }
]
```

### gbif-biodiversidad

**Dónde se ha observado vida: especies y sesgo de muestreo** — `DATA_SAMPLE`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [json](https://api.gbif.org/v1/occurrence/search?country=MX&limit=3) — `DATA_SAMPLE`; HTTP `200`; 3.846 s.

Formato y campos de la muestra validados; no implica calidad de toda la fuente.

```json
[
  {
    "key": 5937748320,
    "scientificName": "Panthiades bathildis (R.F.C.Felder, 1865)",
    "countryCode": "MX",
    "eventDate": "2026-01-01",
    "basisOfRecord": "HUMAN_OBSERVATION",
    "license": "http://creativecommons.org/licenses/by-nc/4.0/legalcode"
  },
  {
    "key": 5937748335,
    "scientificName": "Urbanus dorantes (Stoll, 1790)",
    "countryCode": "MX",
    "eventDate": "2026-01-01",
    "basisOfRecord": "HUMAN_OBSERVATION",
    "license": "http://creativecommons.org/licenses/by-nc/4.0/legalcode"
  }
]
```

### xeno-canto-audio

**Cantos de aves, murciélagos e insectos** — `DATA_SAMPLE`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [html](https://xeno-canto.org/explore/api) — `DOC_ONLY`; HTTP `200`; 3.89 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

```json
[
  {
    "page_title": "API :: xeno-canto"
  }
]
```

Prueba 2: [json](https://xeno-canto.org/api/3/recordings?query=gen:larus+sp:fuscus&key=demo&per_page=2) — `DATA_SAMPLE`; HTTP `200`; 7.379 s.

Formato y campos de la muestra validados; no implica calidad de toda la fuente. Se probó además la cabecera del medio enlazado; ver resultado del recurso.

Recurso enlazado: [media](https://xeno-canto.org/1154497/download) — `MEDIA_SAMPLE`, HTTP `200`.

Sólo firma binaria y acceso al prefijo: no se decodificó, reprodujo ni validó el medio completo.

```json
[
  {
    "format": "WAV",
    "bytes_checked": 65536,
    "complete_file": false
  }
]
```

```json
[
  {
    "id": "1154497",
    "gen": "Larus",
    "sp": "fuscus",
    "cnt": "United Kingdom",
    "type": "alarm call",
    "length": "1:33",
    "file": "https://xeno-canto.org/1154497/download",
    "lic": "https://creativecommons.org/licenses/by-nc-sa/4.0/"
  },
  {
    "id": "1065457",
    "gen": "Larus",
    "sp": "fuscus",
    "cnt": "Italy",
    "type": "flight call",
    "length": "0:10",
    "file": "https://xeno-canto.org/1065457/download",
    "lic": "https://creativecommons.org/licenses/by-nc-sa/4.0/"
  }
]
```

### met-arte

**Arte, objetos e imágenes del Metropolitan Museum** — `DATA_SAMPLE`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [json](https://collectionapi.metmuseum.org/public/collection/v1/objects/436535) — `DATA_SAMPLE`; HTTP `200`; 7.528 s.

Formato y campos de la muestra validados; no implica calidad de toda la fuente. Se probó además la cabecera del medio enlazado; ver resultado del recurso.

Recurso enlazado: [media](https://images.metmuseum.org/CRDImages/ep/web-large/DP-42549-001.jpg) — `MEDIA_SAMPLE`, HTTP `200`.

Sólo firma binaria y acceso al prefijo: no se decodificó, reprodujo ni validó el medio completo.

```json
[
  {
    "format": "JPEG",
    "bytes_checked": 65536,
    "complete_file": false
  }
]
```

```json
[
  {
    "objectID": 436535,
    "title": "Wheat Field with Cypresses",
    "artistDisplayName": "Vincent van Gogh",
    "objectDate": "1889",
    "medium": "Oil on canvas",
    "isPublicDomain": true,
    "primaryImage": "https://images.metmuseum.org/CRDImages/ep/original/DP-42549-001.jpg"
  }
]
```

### loc-prensa-historica

**Periódicos antiguos: portadas, OCR y metadatos** — `METADATA_SAMPLE`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [json](https://www.loc.gov/newspapers/?fo=json&c=3) — `METADATA_SAMPLE`; HTTP `200`; 3.103 s.

Formato y campos de la muestra validados; no implica calidad de toda la fuente.

```json
[
  {
    "id": "http://www.loc.gov/item/2012218613/1882-04-12/ed-1/",
    "title": "The Fairfield news and herald (Winnsboro, S.C.), April 12, 1882",
    "date": "1882-04-12",
    "language": [
      "english"
    ],
    "original_format": [
      "newspaper"
    ],
    "url": "https://www.loc.gov/item/2012218613/1882-04-12/ed-1/"
  },
  {
    "id": "http://www.loc.gov/item/sn83045313/1949-10-25/ed-1/",
    "title": "Le messager (Lewiston, Me.), October 25, 1949",
    "date": "1949-10-25",
    "language": [
      "french",
      "english"
    ],
    "original_format": [
      "newspaper"
    ],
    "url": "https://www.loc.gov/item/sn83045313/1949-10-25/ed-1/"
  }
]
```

### gutenberg-quijote

**Don Quijote como corpus de lenguaje** — `DOCUMENT_SAMPLE`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [text](https://www.gutenberg.org/cache/epub/2000/pg2000.txt) — `DOCUMENT_SAMPLE`; HTTP `200`; 3.829 s.

Prefijo de documento real; no se descargó el corpus completo.

```json
[
  {
    "excerpt": "En un lugar de la Mancha, de cuyo nombre no quiero acordarme, no ha mucho tiempo que vivía un hidalgo de los de lanza en astillero, adarga antigua, rocín flaco y galgo corredor. Una olla de algo más vaca que carnero, salpicón las más noches, duelos y quebrantos los sábados, lantejas los viernes, algún palomino de añadidura los domingos, consumían"
  }
]
```

### openfoodfacts-alimentos

**Alimentos: ingredientes, nutrientes y fotos de etiquetas** — `DATA_SAMPLE`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [json](https://world.openfoodfacts.org/api/v2/product/3017620422003?fields=code,product_name,brands,nutriments,nutriscore_grade,image_url) — `DATA_SAMPLE`; HTTP `200`; 3.421 s.

Formato y campos de la muestra validados; no implica calidad de toda la fuente.

```json
[
  {
    "code": "3017620422003",
    "product_name": "Nutella",
    "brands": "Nutella, Ferrero",
    "nutriscore_grade": "unknown",
    "nutriments": {
      "added-sugars": 52.13,
      "added-sugars_100g": 52.13,
      "added-sugars_unit": "g",
      "added-sugars_value": 52.13,
      "carbohydrates": 57.5,
      "carbohydrates_100g": 57.5,
      "carbohydrates_unit": "g",
      "carbohydrates_value": 57.5,
      "energy": 2252,
      "energy-kcal": 539,
      "energy-kcal_100g": 539,
      "energy-kcal_unit": "kcal"
    },
    "image_url": "https://images.openfoodfacts.org/images/products/301/762/042/2003/front_en.879.400.jpg"
  }
]
```

### nuforc-ovnis

**Relatos de avistamientos de ovnis/UAP** — `DOC_ONLY`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [html](https://nuforc.org/databank/?id=latest) — `DOC_ONLY`; HTTP `200`; 4.593 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

```json
[
  {
    "page_title": "NUFORC Reports for State atest"
  }
]
```

### gdelt-noticias

**El mundo contado por noticias: eventos y menciones** — `METADATA_SAMPLE`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [gdelt_index](https://data.gdeltproject.org/gdeltv2/lastupdate.txt) — `METADATA_SAMPLE`; HTTP `200`; 3.522 s.

Manifiesto recuperado; archivos de eventos/mentions/GKG no descargados.

```json
[
  {
    "bytes": 131623,
    "md5": "8c1327fd003001080389187c21fbb939",
    "url": "http://data.gdeltproject.org/gdeltv2/20261105001500.export.CSV.zip"
  },
  {
    "bytes": 122069,
    "md5": "c27d37d8d98604efe7d9085d02db02d7",
    "url": "http://data.gdeltproject.org/gdeltv2/20261105001500.mentions.CSV.zip"
  },
  {
    "bytes": 5009186,
    "md5": "3b8c897d4d7173d767dfcb5ad99f2243",
    "url": "http://data.gdeltproject.org/gdeltv2/20261105001500.gkg.csv.zip"
  }
]
```

### nasa-bolidos

**Bólidos: entradas atmosféricas detectadas por sensores** — `DATA_SAMPLE`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [nasa_rows](https://ssd-api.jpl.nasa.gov/fireball.api?limit=3) — `DATA_SAMPLE`; HTTP `200`; 3.165 s.

Formato y campos de la muestra validados; no implica calidad de toda la fuente.

```json
[
  {
    "date": "2026-10-04 03:14:45",
    "energy": "5.4",
    "impact-e": "0.18",
    "lat": "41.8",
    "lat-dir": "S",
    "lon": "173.1",
    "lon-dir": "W",
    "alt": "26.9",
    "vel": "13.8"
  },
  {
    "date": "2026-09-15 11:26:13",
    "energy": "2.2",
    "impact-e": "0.079",
    "lat": "37.6",
    "lat-dir": "S",
    "lon": "161.6",
    "lon-dir": "W",
    "alt": "37.0"
  }
]
```

### nyc-ratas

**Inspecciones de ratas por predio en Nueva York** — `DATA_SAMPLE`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

Prueba 1: [json](https://data.cityofnewyork.us/resource/p937-wjvj.json?$limit=3) — `DATA_SAMPLE`; HTTP `200`; 3.143 s.

Formato y campos de la muestra validados; no implica calidad de toda la fuente.

```json
[
  {
    "job_id": "PC8178739",
    "inspection_date": "2023-09-21T10:54:00.000",
    "inspection_type": "Stoppage",
    "zip_code": "11216",
    "borough": "Brooklyn",
    "result": "Stoppage done"
  },
  {
    "job_id": "PC8129591",
    "inspection_date": "2023-06-25T15:20:41.000",
    "inspection_type": "Treatments",
    "zip_code": "11237",
    "borough": "Brooklyn",
    "result": "Bait applied"
  }
]
```

### nyc-restaurantes

**Inspecciones de restaurantes de Nueva York** — `DATA_SAMPLE`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

Prueba 1: [json](https://data.cityofnewyork.us/resource/43nn-pn8j.json?$limit=3) — `DATA_SAMPLE`; HTTP `200`; 9.964 s.

Formato y campos de la muestra validados; no implica calidad de toda la fuente.

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

### openflights-red-aerea

**Aeropuertos, aerolíneas, aviones y rutas históricas** — `DATA_SAMPLE`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

Prueba 1: [csv](https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat) — `DATA_SAMPLE`; HTTP `200`; 5.231 s.

Primeras filas completas del archivo; no se contó el total ni se comprobaron llaves globales.

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

Prueba 2: [csv](https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat) — `DATA_SAMPLE`; HTTP `200`; 3.454 s.

Primeras filas completas del archivo; no se contó el total ni se comprobaron llaves globales.

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

### bts-puntualidad-vuelos

**Puntualidad, cancelaciones y demoras aéreas** — `DOC_ONLY`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

Prueba 1: [html](https://transtats.bts.gov/ONTIME/) — `DOC_ONLY`; HTTP `200`; 4.982 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

```json
[
  {
    "page_title": "On-Time Index pageLockU.S. Department of TransportationUnited States Department of Transportation"
  }
]
```

### apple-apps

**Catálogo público de apps de Apple** — `DATA_SAMPLE`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

Prueba 1: [json](https://itunes.apple.com/search?term=travel&entity=software&country=mx&limit=3) — `DATA_SAMPLE`; HTTP `200`; 4.707 s.

Formato y campos de la muestra validados; no implica calidad de toda la fuente.

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

### apple-resenas-apps

**Reseñas públicas de apps por tienda** — `DATA_SAMPLE`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

Prueba 1: [json](https://itunes.apple.com/mx/rss/customerreviews/id=310633997/sortBy=mostRecent/json) — `DATA_SAMPLE`; HTTP `200`; 3.811 s.

Formato y campos de la muestra validados; no implica calidad de toda la fuente.

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

### insideairbnb-cdmx

**Alojamiento turístico: Inside Airbnb CDMX** — `DATA_SAMPLE`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

Prueba 1: [csv](https://data.insideairbnb.com/mexico/df/mexico-city/2026-09-23/visualisations/listings.csv) — `DATA_SAMPLE`; HTTP `200`; 4.238 s.

Primeras filas completas del archivo; no se contó el total ni se comprobaron llaves globales.

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

### napoleonica-cartas

**Correspondencia general de Napoleón** — `DOC_ONLY`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

Prueba 1: [html](https://www.napoleonica.org/collection/9457) — `DOC_ONLY`; HTTP `200`; 5.716 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

```json
[
  {
    "page_title": "correspondance (Napoleonica les archives)"
  }
]
```

### gallica-napoleon

**Gallica: libros históricos sobre Napoleón y su correspondencia** — `BLOCKED`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

Prueba 1: [sru](https://gallica.bnf.fr/SRU?version=1.2&operation=searchRetrieve&query=dc.title%20all%20%22correspondance%20Napoleon%22&maximumRecords=3) — `BLOCKED`; HTTP `403`; 3.887 s.

HTTP 403: Forbidden. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

### pepys-diarios

**Diario de Samuel Pepys: vida cotidiana, enfermedad y ciudad** — `DOCUMENT_SAMPLE`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

Prueba 1: [text](https://www.gutenberg.org/cache/epub/4184/pg4184.txt) — `DOCUMENT_SAMPLE`; HTTP `200`; 3.255 s.

Prefijo de documento real; no se descargó el corpus completo.

```json
[
  {
    "excerpt": "The Project Gutenberg eBook of Diary of Samuel Pepys — Complete 1667 N.S. This eBook is for the use of anyone anywhere in the United States and most other parts of the world at no cost and with almost no restrictions whatsoever. You may copy it, give it away or re-use it under the terms of the Project Gutenberg License"
  }
]
```

### musicbrainz-conciertos

**Eventos, artistas y lugares de conciertos** — `DOC_ONLY`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

Prueba 1: [json](https://musicbrainz.org/ws/2/event/?query=type:Concert&fmt=json&limit=3) — `PARSE_ERROR`; HTTP `200`; 3.49 s.

JSONDecodeError: Expecting value: line 1 column 1 (char 0)

Sin registros o ejemplos recuperados para esta prueba.

Prueba 2: [html](https://musicbrainz.org/doc/MusicBrainz_API) — `DOC_ONLY`; HTTP `200`; 4.701 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

```json
[
  {
    "page_title": "Site Unavailable"
  }
]
```

### setlist-conciertos

**Repertorios y orden de canciones en conciertos** — `DOC_ONLY`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

Prueba 1: [html](https://api.setlist.fm/docs/1.0/index.html) — `DOC_ONLY`; HTTP `200`; 4.019 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

```json
[
  {
    "page_title": "setlist.fm API"
  }
]
```

### osm-mapas-restaurantes

**OpenStreetMap / Overpass: lugares y mapas vivos** — `HTTP_ERROR`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

Prueba 1: [json](https://overpass-api.de/api/interpreter?data=%5Bout%3Ajson%5D%5Btimeout%3A15%5D%3Bnode%5Bamenity%3Drestaurant%5D%2819.42%2C-99.18%2C19.44%2C-99.15%29%3Bout%203%3B) — `HTTP_ERROR`; HTTP `502`; 3.666 s.

HTTP 502: Bad Gateway. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

### loc-mapas-historicos

**Mapas históricos digitalizados** — `METADATA_SAMPLE`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

Prueba 1: [json](https://www.loc.gov/maps/?fo=json&c=3) — `METADATA_SAMPLE`; HTTP `200`; 3.225 s.

Formato y campos de la muestra validados; no implica calidad de toda la fuente.

```json
[
  {
    "id": "http://www.loc.gov/item/sanborn03483_002/",
    "title": "Sanborn Fire Insurance Map from Jonesport, Washington County, Maine.",
    "date": "1895-09",
    "original_format": [
      "map"
    ]
  }
]
```

### gsm8k-examenes

**GSM8K: problemas matemáticos con soluciones** — `DATA_SAMPLE`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

Prueba 1: [gsm_jsonl](https://raw.githubusercontent.com/openai/grade-school-math/master/grade_school_math/data/test.jsonl) — `DATA_SAMPLE`; HTTP `200`; 2.848 s.

Una línea JSONL real: fragmento breve de pregunta y respuesta final de referencia, sin ejecutar un modelo ni evaluar todo el benchmark.

```json
[
  {
    "question_excerpt": "Janet’s ducks lay 16 eggs per day. She eats three for breakfast every morning and bakes muffins for",
    "answer_numeric": "18"
  }
]
```

### unam-colecciones

**Colecciones universitarias abiertas UNAM** — `HTTP_ERROR`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

Prueba 1: [html](https://datosabiertos.unam.mx/IBUNAM%3AMEXU%3A1210262) — `HTTP_ERROR`; HTTP `503`; 8.544 s.

HTTP 503: Service Unavailable. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

### unam-agenda-estadistica

**Agenda Estadística y numeralia UNAM** — `DOC_ONLY`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

Prueba 1: [html](https://estadistica.unam.mx/numeralia/) — `PARSE_ERROR`; HTTP `200`; 4.392 s.

ValueError: Página vacía sin título ni contenido suficiente

Sin registros o ejemplos recuperados para esta prueba.

Prueba 2: [html](https://web.planeacion.unam.mx/direccion-de-sistemas-de-informacion-estadistica/agenda/) — `DOC_ONLY`; HTTP `200`; 5.66 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

```json
[
  {
    "page_title": "Agenda Estadística – Coordinación de Planeación, Evaluación y Simplificación de la Gestión Institucional"
  }
]
```

### unam-guias-examenes

**Guías públicas de exámenes extraordinarios CCH** — `DOCUMENT_SAMPLE`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

Prueba 1: [pdf](https://portalacademico.cch.unam.mx/materiales/al/Guias_extras/Matematicas/cal1_ori.pdf) — `DOCUMENT_SAMPLE`; HTTP `200`; 3.68 s.

Firma PDF y extracción de una página validadas; sin OCR ni auditoría de todas sus tablas.

```json
[
  {
    "page": 1,
    "excerpt": "UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO COLEGIO DE CIENCIAS Y HUMANIDADES PLANTEL ORIENTE GUÍA PARA EL EXAMEN EXTRAORDINARIO DE CÁLCULO DIFERENCIAL"
  }
]
```

### ct-ventas-inmuebles

**Ventas inmobiliarias registradas en Connecticut** — `DATA_SAMPLE`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

Prueba 1: [json](https://data.ct.gov/resource/5mzw-sjtu.json?$limit=3) — `DATA_SAMPLE`; HTTP `200`; 3.717 s.

Formato y campos de la muestra validados; no implica calidad de toda la fuente.

```json
[
  {
    "serialnumber": "24079",
    "listyear": "2024",
    "daterecorded": "2025-09-26T00:00:00.000",
    "town": "Ashford",
    "assessedvalue": "54460",
    "saleamount": "95000",
    "salesratio": "0.5732",
    "propertytype": "Vacant Land"
  },
  {
    "serialnumber": "240171",
    "listyear": "2024",
    "daterecorded": "2025-06-06T00:00:00.000",
    "town": "Berlin",
    "assessedvalue": "251400",
    "saleamount": "350000",
    "salesratio": "0.7182",
    "propertytype": "Commercial",
    "nonusecode": "25 - Other"
  }
]
```

### cmu-movimiento-baile

**Movimiento humano y secuencias de baile CMU MoCap** — `HTTP_ERROR`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

Prueba 1: [amc](https://mocap.cs.cmu.edu/subjects/05/05_02.amc) — `HTTP_ERROR`; HTTP `503`; 3.788 s.

HTTP 503: Service Unavailable. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

### aist-dance

**AIST++: baile, música y movimiento 3D** — `DOC_ONLY`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

Prueba 1: [html](https://google.github.io/aistplusplus_dataset/factsfigures.html) — `DOC_ONLY`; HTTP `200`; 4.482 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

```json
[
  {
    "page_title": "AIST++ Dataset - Description"
  }
]
```

### artic-pintura

**Obras, textos e imágenes del Art Institute of Chicago** — `BLOCKED`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

Prueba 1: [json](https://api.artic.edu/api/v1/artworks/search?q=Monet&fields=id,title,artist_title,date_display,image_id,is_public_domain&limit=3) — `BLOCKED`; HTTP `403`; 2.934 s.

HTTP 403: Forbidden. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

### dracor-teatro

**DraCor: teatro, personajes y redes de diálogo** — `DATA_SAMPLE`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

Prueba 1: [json](https://dracor.org/api/v1/corpora/ger/plays/goethe-faust-eine-tragoedie) — `DATA_SAMPLE`; HTTP `200`; 4.592 s.

Formato y campos de la muestra validados; no implica calidad de toda la fuente.

```json
[
  {
    "id": "ger000243",
    "title": "Faust",
    "name": "goethe-faust-eine-tragoedie",
    "allInSegment": 28,
    "segments": [
      {
        "type": "scene",
        "title": "Zueignung.",
        "number": 1
      },
      {
        "type": "scene",
        "title": "Vorspiel auf dem Theater.",
        "speakers": [
          "direktor",
          "dichter",
          "lustige_person"
        ],
        "number": 2
      },
      {
        "type": "scene",
        "title": "Prolog im Himmel.",
        "speakers": [
          "raphael",
          "gabriel",
          "michael",
          "mephistopheles",
          "der_herr"
        ],
        "number": 3
      },
      {
        "type": "scene",
        "title": "Nacht.",
        "speakers": [
          "faust",
          "geist",
          "wagner",
          "chor_der_engel",
          "chor_der_weiber",
          "chor_der_juenger"
        ],
        "number": 4
      },
      {
        "type": "scene",
        "title": "Vor dem Tor.",
        "speakers": [
          "einige_handwerksburschen",
          "andre_handwerksburschen",
          "ein_handwerksbursch",
          "zweiter_handwerksbursch",
          "ein_dritter_handwerksbursch",
          "vierter_handwerksbursch",
          "fuenfter_handwerksbursch",
          "erstes_dienstmaedchen"
        ],
        "number": 5
      },
      {
        "type": "scene",
        "title": "Studierzimmer.",
        "speakers": [
          "faust",
          "geister",
          "mephistopheles"
        ],
        "number": 6
      },
      {
        "type": "scene",
        "title": "Studierzimmer.",
        "speakers": [
          "faust",
          "mephistopheles",
          "geisterchor",
          "schueler"
        ],
        "number": 7
      },
      {
        "type": "scene",
        "title": "Auerbachs Keller in Leipzig.",
        "speakers": [
          "frosch",
          "brander",
          "siebel",
          "altmayer",
          "mephistopheles",
          "faust"
        ],
        "number": 8
      }
    ]
  }
]
```

Prueba 2: [tei](https://dracor.org/api/v1/corpora/ger/plays/goethe-faust-eine-tragoedie/tei) — `DOCUMENT_SAMPLE`; HTTP `200`; 3.941 s.

Documento TEI con título e intervenciones; no se calculó todavía la red completa de personajes.

```json
[
  {
    "title": "Faust",
    "speaker_examples": [
      "Direktor.",
      "Dichter."
    ],
    "passage_excerpt": "Im Elend! Verzweifelnd! Erbärmlich auf der Erde lange verirrt und nun gefangen! Als Missetäterin im Kerker zu entsetzlichen Qualen eingesperrt"
  }
]
```

### uci-retail

**Online Retail: facturas y líneas de pedido reales** — `DATA_SAMPLE`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

Prueba 1: [csv](https://archive.ics.uci.edu/static/public/352/data.csv) — `DATA_SAMPLE`; HTTP `200`; 3.337 s.

Primeras filas completas del archivo; no se contó el total ni se comprobaron llaves globales.

```json
[
  {
    "InvoiceNo": "536365",
    "StockCode": "85123A",
    "Description": "WHITE HANGING HEART T-LIGHT HOLDER",
    "Quantity": "6",
    "InvoiceDate": "12/1/2010 8:26",
    "UnitPrice": "2.55",
    "CustomerID": "17850",
    "Country": "United Kingdom"
  },
  {
    "InvoiceNo": "536365",
    "StockCode": "71053",
    "Description": "WHITE METAL LANTERN",
    "Quantity": "6",
    "InvoiceDate": "12/1/2010 8:26",
    "UnitPrice": "3.39",
    "CustomerID": "17850",
    "Country": "United Kingdom"
  }
]
```

### openfda-etiquetas

**Etiquetas y documentación farmacéutica pública** — `DATA_SAMPLE`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

Prueba 1: [json](https://api.fda.gov/drug/label.json?limit=1) — `DATA_SAMPLE`; HTTP `200`; 3.58 s.

Formato y campos de la muestra validados; no implica calidad de toda la fuente.

```json
[
  {
    "id": "ca7bbcc8-2354-375c-e053-2995a90a72a0",
    "set_id": "0000025c-6dbf-4af7-a741-5cbacaed519a",
    "effective_time": "20210902",
    "openfda.brand_name": [
      "SILICEA"
    ],
    "openfda.generic_name": [
      "SILICEA"
    ]
  }
]
```

### wellcome-medicina-antigua

**Libros, archivos e ilustraciones de medicina histórica** — `METADATA_SAMPLE`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

Prueba 1: [json](https://api.wellcomecollection.org/catalogue/v2/works?query=sleep&production.dates.to=1900-01-01&pageSize=3&include=production,items) — `METADATA_SAMPLE`; HTTP `200`; 3.383 s.

Formato y campos de la muestra validados; no implica calidad de toda la fuente.

```json
[
  {
    "id": "gvybrs3w",
    "title": "Sleep and dreams.",
    "production": [
      {
        "label": "London : Longman, Brown, [1857]",
        "agents": [
          {
            "label": "Longman, Brown",
            "type": "Agent"
          }
        ],
        "dates": [
          {
            "label": "[1857]",
            "type": "Period"
          }
        ],
        "function": {
          "label": "Publication",
          "type": "Concept"
        },
        "type": "ProductionEvent",
        "places": [
          {
            "label": "London",
            "type": "Place"
          }
        ]
      }
    ],
    "workType": {
      "id": "a",
      "type": "Format",
      "label": "Books"
    }
  }
]
```

### bob-ross-elementos

**Elementos que aparecen en los cuadros de Bob Ross** — `DATA_SAMPLE`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

Prueba 1: [csv](https://raw.githubusercontent.com/fivethirtyeight/data/master/bob-ross/elements-by-episode.csv) — `DATA_SAMPLE`; HTTP `200`; 3.885 s.

Primeras filas completas del archivo; no se contó el total ni se comprobaron llaves globales.

```json
[
  {
    "EPISODE": "S01E01",
    "TITLE": "\"A WALK IN THE WOODS\"",
    "TREE": "1",
    "TREES": "1",
    "MOUNTAIN": "0",
    "MOUNTAINS": "0",
    "CLOUDS": "0",
    "GUEST": "0"
  },
  {
    "EPISODE": "S01E02",
    "TITLE": "\"MT. MCKINLEY\"",
    "TREE": "1",
    "TREES": "1",
    "MOUNTAIN": "1",
    "MOUNTAINS": "0",
    "CLOUDS": "1",
    "GUEST": "0"
  }
]
```

### bob-ross-paletas

**Cuadros, paletas y episodios de Bob Ross** — `DATA_SAMPLE`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

Prueba 1: [csv](https://raw.githubusercontent.com/jwilber/Bob_Ross_Paintings/master/data/bob_ross_paintings.csv) — `DATA_SAMPLE`; HTTP `200`; 2.773 s.

Primeras filas completas del archivo; no se contó el total ni se comprobaron llaves globales.

```json
[
  {
    "painting_index": "282",
    "painting_title": "A Walk in the Woods",
    "season": "1",
    "episode": "1",
    "num_colors": "8",
    "colors": "\"['Alizarin Crimson'",
    "color_hex": " 'Bright Red'"
  },
  {
    "painting_index": "283",
    "painting_title": "Mt. McKinley",
    "season": "1",
    "episode": "2",
    "num_colors": "8",
    "colors": "\"['Alizarin Crimson'",
    "color_hex": " 'Bright Red'"
  }
]
```

## Evidencia legible por máquina

[results.json](results.json) contiene cada petición y su timestamp; código HTTP, content-type, bytes, hash y su alcance cuando están disponibles; además de muestras y errores. [Definición de pruebas](../catalogs/source_probes.json). [Catálogo](../docs/CATALOGO_DATASETS_REALES.md).
