# Tests: Arte, pintura y Bob Ross

[Todas las pruebas](../../README.md) · [Catálogo](../../../docs/CATALOGO_DATASETS_REALES.md)

Resultados y ejemplos de las peticiones indicadas. Las imágenes se comprueban por separado; un portal accesible no equivale a datos ingeridos.

### artic-pintura

**Obras, textos e imágenes del Art Institute of Chicago** — `BLOCKED`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

**Prueba 1: `BLOCKED`** · [json](https://api.artic.edu/api/v1/artworks/search?q=Monet&fields=id,title,artist_title,date_display,image_id,is_public_domain&limit=3) · HTTP `403`.

Captura UTC: `2026-11-05T00:52:01+00:00`; duración: 2.934 s.

HTTP 403: Forbidden. No se sorteó el bloqueo ni se usaron credenciales personales.

Sin registros o ejemplos recuperados para esta prueba.

### bob-ross-elementos

**Elementos que aparecen en los cuadros de Bob Ross** — `DATA_SAMPLE`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

**Prueba 1: `DATA_SAMPLE`** · [csv](https://raw.githubusercontent.com/fivethirtyeight/data/master/bob-ross/elements-by-episode.csv) · HTTP `200`.

Captura UTC: `2026-11-05T00:52:08+00:00`; duración: 3.885 s.

Primeras filas completas del archivo; no se contó el total ni se comprobaron llaves globales.

Contenido: `text/plain; charset=utf-8`; 65,536 bytes leídos; alcance del hash: `response_prefix`.

| Campo | Ejemplo 1 | Ejemplo 2 |
| --- | --- | --- |
| EPISODE | S01E01 | S01E02 |
| TITLE | &quot;A WALK IN THE WOODS&quot; | &quot;MT. MCKINLEY&quot; |
| TREE | 1 | 1 |
| TREES | 1 | 1 |
| MOUNTAIN | 0 | 1 |
| MOUNTAINS | 0 | 0 |
| CLOUDS | 0 | 1 |
| GUEST | 0 | 0 |

<details>
<summary>Ver los registros exactos en JSON</summary>

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

</details>

### bob-ross-paletas

**Cuadros, paletas y episodios de Bob Ross** — `DATA_SAMPLE`.

Ampliación para descubrimiento: los ejemplos verifican acceso/formato; la pregunta de investigación sigue siendo una hipótesis salvo resultado calculado explícito.

**Prueba 1: `DATA_SAMPLE`** · [csv](https://raw.githubusercontent.com/jwilber/Bob_Ross_Paintings/master/data/bob_ross_paintings.csv) · HTTP `200`.

Captura UTC: `2026-11-05T03:21:35+00:00`; duración: 3.831 s.

Primeras filas completas del archivo; no se contó el total ni se comprobaron llaves globales.

Contenido: `text/plain; charset=utf-8`; 65,536 bytes leídos; alcance del hash: `response_prefix`.

| Campo | Ejemplo 1 | Ejemplo 2 |
| --- | --- | --- |
| painting_index | 282 | 283 |
| painting_title | A Walk in the Woods | Mt. McKinley |
| season | 1 | 1 |
| episode | 1 | 2 |
| num_colors | 8 | 8 |
| colors | [&quot;Alizarin Crimson&quot;, &quot;Bright Red&quot;, &quot;Cadmium Yellow&quot;, &quot;Phthalo Green&quot;, &quot;Prussian Blue&quot;, &quot;Sap Green&quot;, &quot;Titanium White&quot;, &quot;Van Dyke Brown&quot;] | [&quot;Alizarin Crimson&quot;, &quot;Bright Red&quot;, &quot;Cadmium Yellow&quot;, &quot;Phthalo Green&quot;, &quot;Prussian Blue&quot;, &quot;Sap Green&quot;, &quot;Titanium White&quot;, &quot;Van Dyke Brown&quot;] |
| color_hex | [&quot;#4E1500&quot;, &quot;#DB0000&quot;, &quot;#FFEC00&quot;, &quot;#102E3C&quot;, &quot;#021E44&quot;, &quot;#0A3410&quot;, &quot;#FFFFFF&quot;, &quot;#221B15&quot;] | [&quot;#4E1500&quot;, &quot;#DB0000&quot;, &quot;#FFEC00&quot;, &quot;#102E3C&quot;, &quot;#021E44&quot;, &quot;#0A3410&quot;, &quot;#FFFFFF&quot;, &quot;#221B15&quot;] |
| img_src | https://www.twoinchbrush.com/images/painting282.webp | https://www.twoinchbrush.com/images/painting283.webp |

<details>
<summary>Ver los registros exactos en JSON</summary>

```json
[
  {
    "painting_index": "282",
    "painting_title": "A Walk in the Woods",
    "season": "1",
    "episode": "1",
    "num_colors": "8",
    "colors": [
      "Alizarin Crimson",
      "Bright Red",
      "Cadmium Yellow",
      "Phthalo Green",
      "Prussian Blue",
      "Sap Green",
      "Titanium White",
      "Van Dyke Brown"
    ],
    "color_hex": [
      "#4E1500",
      "#DB0000",
      "#FFEC00",
      "#102E3C",
      "#021E44",
      "#0A3410",
      "#FFFFFF",
      "#221B15"
    ],
    "img_src": "https://www.twoinchbrush.com/images/painting282.webp"
  },
  {
    "painting_index": "283",
    "painting_title": "Mt. McKinley",
    "season": "1",
    "episode": "2",
    "num_colors": "8",
    "colors": [
      "Alizarin Crimson",
      "Bright Red",
      "Cadmium Yellow",
      "Phthalo Green",
      "Prussian Blue",
      "Sap Green",
      "Titanium White",
      "Van Dyke Brown"
    ],
    "color_hex": [
      "#4E1500",
      "#DB0000",
      "#FFEC00",
      "#102E3C",
      "#021E44",
      "#0A3410",
      "#FFFFFF",
      "#221B15"
    ],
    "img_src": "https://www.twoinchbrush.com/images/painting283.webp"
  }
]
```

</details>

**Ejemplo visual y su test**

<a href="https://www.twoinchbrush.com/painting/a-walk-in-the-woods"><img src="https://www.twoinchbrush.com/images/painting282.webp" alt="A Walk in the Woods — Bob Ross, temporada 1, episodio 1" width="420"></a>

**A Walk in the Woods — Bob Ross, temporada 1, episodio 1**. Bob Ross; imagen enlazada por Two Inch Brush, referencia en el CSV de jwilber. [Ficha original](https://www.twoinchbrush.com/painting/a-walk-in-the-woods) · [Licencia y condiciones](https://www.twoinchbrush.com/): Derechos de sus titulares; imagen remota, sin licencia abierta confirmada.

Prueba de imagen: **`IMAGE_DECODED`**, HTTP `200`, `WEBP`, **450 × 337 px**, 21,240 bytes. Captura UTC: `2026-11-05T03:19:54+00:00`.

Ilustración enlazada desde el CSV de paletas. No se redistribuye el archivo de la pintura ni se afirma haber validado sus etiquetas con visión artificial.

Imagen incrustada desde el proveedor; su visualización depende de que esa URL siga disponible.

GET completo y decodificación de píxeles comprobados. SHA-256 completo: `d3aa6c9f407ce8de32cf94f9dbccd05e0b319f17686bf24036b8fc74aab67b49`. [Metadatos de origen](https://raw.githubusercontent.com/jwilber/Bob_Ross_Paintings/master/data/bob_ross_paintings.csv).

