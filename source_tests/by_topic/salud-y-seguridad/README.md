# Tests: Salud y seguridad

[Todas las pruebas](../../README.md) · [Catálogo](../../../docs/CATALOGO_DATASETS_REALES.md)

Resultados y ejemplos de las peticiones indicadas. Las imágenes se comprueban por separado; un portal accesible no equivale a datos ingeridos.

### salud-clues

**CLUES: establecimientos de salud** — `HTTP_ERROR`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

**Prueba 1: `HTTP_ERROR`** · [xlsx](https://gobi.salud.gob.mx/historico_clues/ESTABLECIMIENTO_SALUD_202609.xlsx?v=1.1) · HTTP `503`.

Captura UTC: `2026-11-05T00:08:11+00:00`; duración: 8.294 s.

HTTP 503: Service Unavailable. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

### cdmx-fgj-carpetas

**Carpetas de investigación FGJ CDMX** — `HTTP_ERROR`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

**Prueba 1: `HTTP_ERROR`** · [html](https://datos.cdmx.gob.mx/dataset/carpetas-de-investigacion-fgj-de-la-ciudad-de-mexico) · HTTP `503`.

Captura UTC: `2026-11-05T00:08:12+00:00`; duración: 9.02 s.

HTTP 503: Service Unavailable. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

**Prueba 2: `HTTP_ERROR`** · [ckan](https://datos.cdmx.gob.mx/api/3/action/package_show?id=carpetas-de-investigacion-fgj-de-la-ciudad-de-mexico) · HTTP `503`.

Captura UTC: `2026-11-05T00:08:21+00:00`; duración: 8.201 s.

HTTP 503: Service Unavailable. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

### inegi-atus

**ATUS: accidentes de tránsito urbanos y suburbanos** — `DOC_ONLY`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

**Prueba 1: `DOC_ONLY`** · [html](https://www.inegi.org.mx/programas/accidentes/default.html) · HTTP `200`.

Captura UTC: `2026-11-05T00:08:16+00:00`; duración: 3.089 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

Contenido: `text/html`; 3,876 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 |
| --- | --- |
| page_title | Accidentes de Tránsito Terrestre en Zonas Urbanas y Suburbanas (ATUS) |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "page_title": "Accidentes de Tránsito Terrestre en Zonas Urbanas y Suburbanas (ATUS)"
  }
]
```

</details>

