# Tests: Código postal y territorio

[Todas las pruebas](../../README.md) · [Catálogo](../../../docs/CATALOGO_DATASETS_REALES.md)

Resultados y ejemplos de las peticiones indicadas. Las imágenes se comprueban por separado; un portal accesible no equivale a datos ingeridos.

### sepomex-codigos-postales

**Catálogo Nacional de Códigos Postales** — `DOC_ONLY`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

**Prueba 1: `DOC_ONLY`** · [html](https://www.correosdemexico.gob.mx/SSLServicios/ConsultaCP/CodigoPostal_Exportar.aspx) · HTTP `200`.

Captura UTC: `2026-11-05T00:07:51+00:00`; duración: 3.039 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

Contenido: `text/html; charset=iso-8859-1`; 16,842 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 |
| --- | --- |
| page_title | Descarga de Códigos Postales |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "page_title": "Descarga de Códigos Postales"
  }
]
```

</details>

### cdmx-codigos-postales-poligonos

**Códigos postales CDMX: capa geográfica** — `HTTP_ERROR`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

**Prueba 1: `HTTP_ERROR`** · [html](https://www.datos.cdmx.gob.mx/es_AR/dataset/codigos-postales) · HTTP `503`.

Captura UTC: `2026-11-05T00:07:51+00:00`; duración: 8.096 s.

HTTP 503: Service Unavailable. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

**Prueba 2: `HTTP_ERROR`** · [ckan](https://datos.cdmx.gob.mx/api/3/action/package_show?id=codigos-postales) · HTTP `503`.

Captura UTC: `2026-11-05T00:08:00+00:00`; duración: 8.37 s.

HTTP 503: Service Unavailable. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

