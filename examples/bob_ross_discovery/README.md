# Piloto: ¿qué suele acompañar a una montaña en Bob Ross?

Este ejemplo ya está **calculado** sobre el CSV completo recuperado. Las demás propuestas de la guía siguen siendo preguntas de investigación. No se ejecutó un modelo para producir estos conteos.

Fuente: [FiveThirtyEight](https://raw.githubusercontent.com/fivethirtyeight/data/master/bob-ross/elements-by-episode.csv). Captura UTC: `2026-11-05T00:52:56+00:00`. Hash SHA-256 completo en [metrics.json](metrics.json).

Definimos árboles como `TREE OR TREES` y montañas como `MOUNTAIN OR MOUNTAINS`; cada episodio se cuenta una vez. No se interpreta `TREES` como una cantidad de árboles.

| Medida descriptiva | Resultado |
| --- | ---: |
| Episodios | 403 |
| Con árbol(es) | 361 |
| Con montaña(s) | 161 |
| Con ambos | 157 |
| Árboles entre episodios con montañas | 157 / 161 = 97.5% |
| Árboles entre episodios sin montañas | 204 / 242 = 84.3% |

La pregunta útil es si la coocurrencia aporta información adicional, dado que los árboles ya son muy frecuentes en el conjunto. La tabla describe esta edición del dataset; no demuestra que una montaña cause la elección de árboles.

Como comprobación de sensibilidad, al excluir episodios marcados `GUEST`, quedan 381 episodios y la frecuencia de árboles entre los que tienen montañas es 97.3%. El detalle conserva numeradores y denominadores.

Verificaciones: identificadores de episodio únicos y variables seleccionadas binarias, sin faltantes. La codificación visual procede de terceros; no se volvió a revisar cada episodio ni se hizo una búsqueda de todas las asociaciones posibles.

Siguiente trabajo con IA: contrastar una muestra de etiquetas con las imágenes de los mismos episodios, conservar desacuerdos y revisar si el patrón depende de estación, paisaje o codificador. Esa revisión visual está pendiente.

Reproducir desde la raíz:

```bash
python scripts/analyze_bob_ross_pilot.py
```

<!-- VISUAL_EXAMPLE:START -->
## Ejemplo visual de la fuente

La imagen siguiente procede del dataset de **paletas**. El cálculo de coocurrencias de este piloto usa el dataset de **elementos** de FiveThirtyEight; son fuentes distintas. Ver la imagen no constituye una nueva auditoría de las etiquetas del piloto.

<a href="https://www.twoinchbrush.com/painting/a-walk-in-the-woods"><img src="https://www.twoinchbrush.com/images/painting282.webp" alt="A Walk in the Woods — Bob Ross, temporada 1, episodio 1" width="420"></a>

**A Walk in the Woods — Bob Ross, temporada 1, episodio 1**. Bob Ross; imagen enlazada por Two Inch Brush, referencia en el CSV de jwilber. [Ficha original](https://www.twoinchbrush.com/painting/a-walk-in-the-woods) · [Licencia y condiciones](https://www.twoinchbrush.com/): Derechos de sus titulares; imagen remota, sin licencia abierta confirmada.

Prueba de imagen: **`IMAGE_DECODED`**, HTTP `200`, `WEBP`, **450 × 337 px**, 21,240 bytes. Captura UTC: `2026-11-05T03:19:54+00:00`.

Ilustración enlazada desde el CSV de paletas. No se redistribuye el archivo de la pintura ni se afirma haber validado sus etiquetas con visión artificial.

Imagen incrustada desde el proveedor; su visualización depende de que esa URL siga disponible.

GET completo y decodificación de píxeles comprobados. SHA-256 completo: `d3aa6c9f407ce8de32cf94f9dbccd05e0b319f17686bf24036b8fc74aab67b49`. [Metadatos de origen](https://raw.githubusercontent.com/jwilber/Bob_Ross_Paintings/master/data/bob_ross_paintings.csv).
<!-- VISUAL_EXAMPLE:END -->

## Continuación para el aula

La [demo de clustering Cuatro salas para Bob Ross](../bob_ross_clustering/README.md) usa una edición fijada del mismo CSV de motivos, con otra pregunta: organizar una exposición y comprobar cómo las variables cambian los grupos. Incluye material del alumno, guía docente, presentación HTML, resultados calculados y tests. No reemplaza los conteos de coocurrencia de este piloto.
