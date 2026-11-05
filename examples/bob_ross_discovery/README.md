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
