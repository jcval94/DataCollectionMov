# Tests: Mapas e inmuebles

[Todas las pruebas](../../README.md) · [Catálogo](../../../docs/CATALOGO_DATASETS_REALES.md)

Resultados y ejemplos de las peticiones indicadas. Las imágenes se comprueban por separado; un portal accesible no equivale a datos ingeridos.

### osm-mapas-restaurantes

**OpenStreetMap / Overpass: lugares y mapas vivos** — `HTTP_ERROR`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

**Prueba 1: `HTTP_ERROR`** · [json](https://overpass-api.de/api/interpreter?data=%5Bout%3Ajson%5D%5Btimeout%3A15%5D%3Bnode%5Bamenity%3Drestaurant%5D%2819.42%2C-99.18%2C19.44%2C-99.15%29%3Bout%203%3B) · HTTP `502`.

Captura UTC: `2026-11-05T00:51:53+00:00`; duración: 3.666 s.

HTTP 502: Bad Gateway. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

### loc-mapas-historicos

**Mapas históricos digitalizados** — `METADATA_SAMPLE`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

**Prueba 1: `METADATA_SAMPLE`** · [json](https://www.loc.gov/maps/?fo=json&c=3) · HTTP `200`.

Captura UTC: `2026-11-05T00:51:54+00:00`; duración: 3.225 s.

Formato y campos de la muestra validados; no implica calidad de toda la fuente.

Contenido: `application/json`; 54,622 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 |
| --- | --- |
| id | http://www.loc.gov/item/sanborn03483_002/ |
| title | Sanborn Fire Insurance Map from Jonesport, Washington County, Maine. |
| date | 1895-09 |
| original_format | [&quot;map&quot;] |

<details>
<summary>Ver los registros exactos en JSON</summary>

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

</details>

**Ejemplo visual y su test**

<a href="https://www.loc.gov/item/sanborn03483_002/"><img src="../../assets/loc-jonesport-1895.jpg" alt="Mapa Sanborn de Jonesport, Maine — septiembre de 1895" width="420"></a>

**Mapa Sanborn de Jonesport, Maine — septiembre de 1895**. Library of Congress, Geography and Map Division, Sanborn Maps Collection. [Ficha original](https://www.loc.gov/item/sanborn03483_002/) · [Licencia y condiciones](https://www.loc.gov/collections/sanborn-maps/about-this-collection/rights-and-access/): Dominio público.

Prueba de imagen: **`IMAGE_DECODED`**, HTTP `200`, `JPEG`, **807 × 957 px**, 102,894 bytes. Captura UTC: `2026-11-05T03:19:49+00:00`.

Vista del recurso original; decodificación de imagen independiente de la prueba de registros.

Archivo de imagen conservado en el repo.

GET completo y decodificación de píxeles comprobados. SHA-256 completo: `57aed0aa7ecc19448dad7dbc63098719098e9dee46e7d3bd2a6d95f408187bca`. [Metadatos de origen](https://www.loc.gov/item/sanborn03483_002/?fo=json).

### ct-ventas-inmuebles

**Ventas inmobiliarias registradas en Connecticut** — `DATA_SAMPLE`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

**Prueba 1: `DATA_SAMPLE`** · [json](https://data.ct.gov/resource/5mzw-sjtu.json?$limit=3) · HTTP `200`.

Captura UTC: `2026-11-05T00:51:58+00:00`; duración: 3.717 s.

Formato y campos de la muestra validados; no implica calidad de toda la fuente.

Contenido: `application/json;charset=utf-8`; 765 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 | Ejemplo 2 |
| --- | --- | --- |
| serialnumber | 24079 | 240171 |
| listyear | 2024 | 2024 |
| daterecorded | 2025-09-26T00:00:00.000 | 2025-06-06T00:00:00.000 |
| town | Ashford | Berlin |
| assessedvalue | 54460 | 251400 |
| saleamount | 95000 | 350000 |
| salesratio | 0.5732 | 0.7182 |
| propertytype | Vacant Land | Commercial |
| nonusecode | null | 25 - Other |

<details>
<summary>Ver los registros exactos en JSON</summary>

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

</details>

