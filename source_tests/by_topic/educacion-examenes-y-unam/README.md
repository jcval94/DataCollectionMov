# Tests: Educación, exámenes y UNAM

[Todas las pruebas](../../README.md) · [Catálogo](../../../docs/CATALOGO_DATASETS_REALES.md)

Resultados y ejemplos de las peticiones indicadas. Las imágenes se comprueban por separado; un portal accesible no equivale a datos ingeridos.

### gsm8k-examenes

**GSM8K: problemas matemáticos con soluciones** — `DATA_SAMPLE`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

**Prueba 1: `DATA_SAMPLE`** · [gsm_jsonl](https://raw.githubusercontent.com/openai/grade-school-math/master/grade_school_math/data/test.jsonl) · HTTP `200`.

Captura UTC: `2026-11-05T00:51:55+00:00`; duración: 2.848 s.

Una línea JSONL real: fragmento breve de pregunta y respuesta final de referencia, sin ejecutar un modelo ni evaluar todo el benchmark.

Contenido: `text/plain; charset=utf-8`; 65,536 bytes leídos; alcance del hash: `response_prefix`.

| Campo | Ejemplo 1 |
| --- | --- |
| question_excerpt | Janet’s ducks lay 16 eggs per day. She eats three for breakfast every morning and bakes muffins for |
| answer_numeric | 18 |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "question_excerpt": "Janet’s ducks lay 16 eggs per day. She eats three for breakfast every morning and bakes muffins for",
    "answer_numeric": "18"
  }
]
```

</details>

### unam-colecciones

**Colecciones universitarias abiertas UNAM** — `HTTP_ERROR`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

**Prueba 1: `HTTP_ERROR`** · [html](https://datosabiertos.unam.mx/IBUNAM%3AMEXU%3A1210262) · HTTP `503`.

Captura UTC: `2026-11-05T00:51:57+00:00`; duración: 8.544 s.

HTTP 503: Service Unavailable. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

### unam-agenda-estadistica

**Agenda Estadística y numeralia UNAM** — `DOC_ONLY`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

**Prueba 1: `PARSE_ERROR`** · [html](https://estadistica.unam.mx/numeralia/) · HTTP `200`.

Captura UTC: `2026-11-05T00:53:47+00:00`; duración: 4.392 s.

ValueError: Página vacía sin título ni contenido suficiente

Contenido: `text/html; charset=UTF-8`; 76 bytes leídos; alcance del hash: `complete_response`.

Sin registros o ejemplos recuperados para esta prueba.

**Prueba 2: `DOC_ONLY`** · [html](https://web.planeacion.unam.mx/direccion-de-sistemas-de-informacion-estadistica/agenda/) · HTTP `200`.

Captura UTC: `2026-11-05T00:53:51+00:00`; duración: 5.66 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

Contenido: `text/html; charset=UTF-8`; 123,882 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 |
| --- | --- |
| page_title | Agenda Estadística – Coordinación de Planeación, Evaluación y Simplificación de la Gestión Institucional |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "page_title": "Agenda Estadística – Coordinación de Planeación, Evaluación y Simplificación de la Gestión Institucional"
  }
]
```

</details>

### unam-guias-examenes

**Guías públicas de exámenes extraordinarios CCH** — `DOCUMENT_SAMPLE`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

**Prueba 1: `DOCUMENT_SAMPLE`** · [pdf](https://portalacademico.cch.unam.mx/materiales/al/Guias_extras/Matematicas/cal1_ori.pdf) · HTTP `200`.

Captura UTC: `2026-11-05T00:51:57+00:00`; duración: 3.68 s.

Firma PDF y extracción de una página validadas; sin OCR ni auditoría de todas sus tablas.

Contenido: `application/pdf`; 332,663 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 |
| --- | --- |
| page | 1 |
| excerpt | UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO COLEGIO DE CIENCIAS Y HUMANIDADES PLANTEL ORIENTE GUÍA PARA EL EXAMEN EXTRAORDINARIO DE CÁLCULO DIFERENCIAL |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "page": 1,
    "excerpt": "UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO COLEGIO DE CIENCIAS Y HUMANIDADES PLANTEL ORIENTE GUÍA PARA EL EXAMEN EXTRAORDINARIO DE CÁLCULO DIFERENCIAL"
  }
]
```

</details>

