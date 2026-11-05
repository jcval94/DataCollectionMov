# Tests: Historia, diarios y literatura

[Todas las pruebas](../../README.md) · [Catálogo](../../../docs/CATALOGO_DATASETS_REALES.md)

Resultados y ejemplos de las peticiones indicadas. Las imágenes se comprueban por separado; un portal accesible no equivale a datos ingeridos.

### napoleonica-cartas

**Correspondencia general de Napoleón** — `DOC_ONLY`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

**Prueba 1: `DOC_ONLY`** · [html](https://www.napoleonica.org/collection/9457) · HTTP `200`.

Captura UTC: `2026-11-05T00:51:49+00:00`; duración: 5.716 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

Contenido: `text/html;charset=UTF-8`; 167,335 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 |
| --- | --- |
| page_title | correspondance (Napoleonica les archives) |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "page_title": "correspondance (Napoleonica les archives)"
  }
]
```

</details>

### gallica-napoleon

**Gallica: libros históricos sobre Napoleón y su correspondencia** — `BLOCKED`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

**Prueba 1: `BLOCKED`** · [sru](https://gallica.bnf.fr/SRU?version=1.2&operation=searchRetrieve&query=dc.title%20all%20%22correspondance%20Napoleon%22&maximumRecords=3) · HTTP `403`.

Captura UTC: `2026-11-05T00:51:49+00:00`; duración: 3.887 s.

HTTP 403: Forbidden. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

### pepys-diarios

**Diario de Samuel Pepys: vida cotidiana, enfermedad y ciudad** — `DOCUMENT_SAMPLE`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

**Prueba 1: `DOCUMENT_SAMPLE`** · [text](https://www.gutenberg.org/cache/epub/4184/pg4184.txt) · HTTP `200`.

Captura UTC: `2026-11-05T00:51:50+00:00`; duración: 3.255 s.

Prefijo de documento real; no se descargó el corpus completo.

Contenido: `text/plain; charset=utf-8`; 65,536 bytes leídos; alcance del hash: `response_prefix`.

| Campo | Ejemplo 1 |
| --- | --- |
| excerpt | The Project Gutenberg eBook of Diary of Samuel Pepys — Complete 1667 N.S. This eBook is for the use of anyone anywhere in the United States and most other parts of the world at no cost and with almost no restrictions whatsoever. You may copy it, give it away or re-use it under the terms of the Project Gutenberg License |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "excerpt": "The Project Gutenberg eBook of Diary of Samuel Pepys — Complete 1667 N.S. This eBook is for the use of anyone anywhere in the United States and most other parts of the world at no cost and with almost no restrictions whatsoever. You may copy it, give it away or re-use it under the terms of the Project Gutenberg License"
  }
]
```

</details>

