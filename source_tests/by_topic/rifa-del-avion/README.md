# Tests: Rifa del avión

[Todas las pruebas](../../README.md) · [Catálogo](../../../docs/CATALOGO_DATASETS_REALES.md)

Resultados y ejemplos de las peticiones indicadas. Las imágenes se comprueban por separado; un portal accesible no equivale a datos ingeridos.

### rifa-235-premios

**GSE 235: lista oficial de premios** — `HTTP_ERROR`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

**Prueba 1: `HTTP_ERROR`** · [pdf](https://www.lotenal.gob.mx/Comercial/Listas/235.pdf) · HTTP `503`.

Captura UTC: `2026-11-05T00:07:41+00:00`; duración: 3.628 s.

HTTP 503: Service Unavailable. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

### rifa-235-reportes

**GSE 235: balance y beneficiarios publicados** — `BLOCKED`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

**Prueba 1: `BLOCKED`** · [html](https://www.gob.mx/lotenal/prensa/197193) · HTTP `403`.

Captura UTC: `2026-11-05T00:07:41+00:00`; duración: 4.167 s.

HTTP 403: Forbidden. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

### rifa-235-asf

**GSE 235: auditoría de gestión financiera** — `DOCUMENT_SAMPLE`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

**Prueba 1: `DOCUMENT_SAMPLE`** · [pdf](https://www.asf.gob.mx/Trans/Informes/IR2020c/Documentos/Auditorias/2020_0051_a.pdf) · HTTP `200`.

Captura UTC: `2026-11-05T00:07:41+00:00`; duración: 3.541 s.

Firma PDF y extracción de una página validadas; sin OCR ni auditoría de todas sus tablas.

Contenido: `application/pdf`; 541,919 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 |
| --- | --- |
| page | 28 |
| excerpt | Informe Individual del Resultado de la Fiscalización Superior de la Cuenta Pública 2020 28 Celebración del sorteo De conformidad con |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "page": 28,
    "excerpt": "Informe Individual del Resultado de la Fiscalización Superior de la Cuenta Pública 2020 28 Celebración del sorteo De conformidad con"
  }
]
```

</details>

