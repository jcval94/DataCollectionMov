# Tests: Música, baile y teatro

[Todas las pruebas](../../README.md) · [Catálogo](../../../docs/CATALOGO_DATASETS_REALES.md)

Resultados y ejemplos de las peticiones indicadas. Las imágenes se comprueban por separado; un portal accesible no equivale a datos ingeridos.

### musicbrainz-conciertos

**Eventos, artistas y lugares de conciertos** — `DOC_ONLY`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

**Prueba 1: `PARSE_ERROR`** · [json](https://musicbrainz.org/ws/2/event/?query=type:Concert&fmt=json&limit=3) · HTTP `200`.

Captura UTC: `2026-11-05T00:53:47+00:00`; duración: 3.49 s.

JSONDecodeError: Expecting value: line 1 column 1 (char 0)

Contenido: `text/html`; 195 bytes leídos; alcance del hash: `complete_response`.

Sin registros o ejemplos recuperados para esta prueba.

**Prueba 2: `DOC_ONLY`** · [html](https://musicbrainz.org/doc/MusicBrainz_API) · HTTP `200`.

Captura UTC: `2026-11-05T00:53:50+00:00`; duración: 4.701 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

Contenido: `text/html`; 195 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 |
| --- | --- |
| page_title | Site Unavailable |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "page_title": "Site Unavailable"
  }
]
```

</details>

### setlist-conciertos

**Repertorios y orden de canciones en conciertos** — `DOC_ONLY`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

**Prueba 1: `DOC_ONLY`** · [html](https://api.setlist.fm/docs/1.0/index.html) · HTTP `200`.

Captura UTC: `2026-11-05T00:51:53+00:00`; duración: 4.019 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

Contenido: `text/html`; 25,681 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 |
| --- | --- |
| page_title | setlist.fm API |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "page_title": "setlist.fm API"
  }
]
```

</details>

### cmu-movimiento-baile

**Movimiento humano y secuencias de baile CMU MoCap** — `HTTP_ERROR`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

**Prueba 1: `HTTP_ERROR`** · [amc](https://mocap.cs.cmu.edu/subjects/05/05_02.amc) · HTTP `503`.

Captura UTC: `2026-11-05T00:52:00+00:00`; duración: 3.788 s.

HTTP 503: Service Unavailable. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

### aist-dance

**AIST++: baile, música y movimiento 3D** — `DOC_ONLY`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

**Prueba 1: `DOC_ONLY`** · [html](https://google.github.io/aistplusplus_dataset/factsfigures.html) · HTTP `200`.

Captura UTC: `2026-11-05T00:52:01+00:00`; duración: 4.482 s.

Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.

Contenido: `text/html; charset=utf-8`; 9,192 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 |
| --- | --- |
| page_title | AIST++ Dataset - Description |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "page_title": "AIST++ Dataset - Description"
  }
]
```

</details>

### dracor-teatro

**DraCor: teatro, personajes y redes de diálogo** — `DATA_SAMPLE`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

**Prueba 1: `DATA_SAMPLE`** · [json](https://dracor.org/api/v1/corpora/ger/plays/goethe-faust-eine-tragoedie) · HTTP `200`.

Captura UTC: `2026-11-05T00:52:04+00:00`; duración: 4.592 s.

Formato y campos de la muestra validados; no implica calidad de toda la fuente.

Contenido: `application/json;charset=utf-8`; 18,424 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 |
| --- | --- |
| id | ger000243 |
| title | Faust |
| name | goethe-faust-eine-tragoedie |
| allInSegment | 28 |
| segments | [{&quot;type&quot;: &quot;scene&quot;, &quot;title&quot;: &quot;Zueignung.&quot;, &quot;number&quot;: 1}, {&quot;type&quot;: &quot;scene&quot;, &quot;title&quot;: &quot;Vorspiel auf dem Theater.&quot;, &quot;speakers&quot;: [&quot;direktor&quot;, &quot;dichter&quot;, &quot;lustige_person&quot;], &quot;number&quot;: 2}, {&quot;type&quot;: &quot;scene&quot;, &quot;title&quot;: &quot;Prolog im Himmel.&quot;, &quot;speakers&quot;: [&quot;raphael&quot;, &quot;gabriel&quot;, &quot;michael&quot;, &quot;mephistopheles&quot;, &quot;der_herr&quot;], &quot;number&quot;: 3}, {&quot;type&quot;: &quot;scene&quot;, &quot;title&quot;: &quot;Nacht.&quot;, &quot;speakers&quot;: [&quot;faust&quot;, &quot;geist&quot;, &quot;wagner&quot;, &quot;chor_der_engel&quot;, &quot;chor_der_weiber&quot;, &quot;chor_der_juenger&quot;], &quot;number&quot;: 4}, {&quot;type&quot;: &quot;scene&quot;, &quot;title&quot;: &quot;Vor dem Tor.&quot;, &quot;speakers&quot;: [&quot;einige_handwerksburschen&quot;, &quot;andre_handwerksburschen&quot;, &quot;ein_handwerksbursch&quot;, &quot;zweiter_handwerksbursch&quot;, &quot;ein_dritter_handwerksbursch&quot;, &quot;vierter_handwerksbursch&quot;, &quot;fuenfter_h… [ver JSON completo debajo] |

<details>
<summary>Ver los registros exactos en JSON</summary>

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

</details>

**Prueba 2: `DOCUMENT_SAMPLE`** · [tei](https://dracor.org/api/v1/corpora/ger/plays/goethe-faust-eine-tragoedie/tei) · HTTP `200`.

Captura UTC: `2026-11-05T00:52:09+00:00`; duración: 3.941 s.

Documento TEI con título e intervenciones; no se calculó todavía la red completa de personajes.

Contenido: `application/xml; charset=UTF-8`; 398,630 bytes leídos; alcance del hash: `complete_response`.

| Campo | Ejemplo 1 |
| --- | --- |
| title | Faust |
| speaker_examples | [&quot;Direktor.&quot;, &quot;Dichter.&quot;] |
| passage_excerpt | Im Elend! Verzweifelnd! Erbärmlich auf der Erde lange verirrt und nun gefangen! Als Missetäterin im Kerker zu entsetzlichen Qualen eingesperrt |

<details>
<summary>Ver los registros exactos en JSON</summary>

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

</details>

