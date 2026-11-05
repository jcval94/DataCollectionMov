# Tests: Educación

[Todas las pruebas](../../README.md) · [Catálogo](../../../docs/CATALOGO_DATASETS_REALES.md)

Resultados y ejemplos de las peticiones indicadas. Las imágenes se comprueban por separado; un portal accesible no equivale a datos ingeridos.

### sep-cct

**Catálogo de Centros de Trabajo** — `DOC_ONLY`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

**Prueba 1: `DOC_ONLY`** · [html](https://siged.sep.gob.mx/SIGED/datos_abiertos.html) · HTTP `200`.

Captura UTC: `2026-11-05T00:07:55+00:00`; duración: 3.762 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

Contenido: `text/html`; 18,651 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 |
| --- | --- |
| page_title | SEP &#124; SIGED |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "page_title": "SEP | SIGED"
  }
]
```

</details>

### sep-formato-911

**Formato 911: alumnado, docentes y escuelas** — `BLOCKED`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

**Prueba 1: `BLOCKED`** · [html](https://www.datos.gob.mx/dataset/registro_alumnado_personal_docente_educacion_basica_media_superior_formato_911) · HTTP `403`.

Captura UTC: `2026-11-05T00:07:55+00:00`; duración: 3.123 s.

HTTP 403: Forbidden. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

### anuies-anuario

**Anuario Estadístico de Educación Superior** — `DOC_ONLY`.

Sólo se confirma la capa descrita por cada prueba; no se generaliza disponibilidad o calidad.

**Prueba 1: `DOC_ONLY`** · [html](https://anuario.anuies.mx/) · HTTP `200`.

Captura UTC: `2026-11-05T00:07:55+00:00`; duración: 4.07 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

Contenido: `text/html; charset=UTF-8`; 311,474 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 |
| --- | --- |
| page_title | Anuarios ANUIES |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "page_title": "Anuarios ANUIES"
  }
]
```

</details>

