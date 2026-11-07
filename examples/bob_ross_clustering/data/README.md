# Datos originales y contrato

`elements-by-episode.csv` conserva los 66,315 bytes originales de FiveThirtyEight. La edición está fijada al commit `4c1ff5e3aef1816ae04af63218015066e186c147`; URL, fecha UTC y SHA-256 completo están en [manifest.json](manifest.json). No se vuelve a descargar al ejecutar el análisis.

- **Unidad:** episodio de *The Joy of Painting*, identificado por `EPISODE`. 403 episodios y 69 columnas: identificador, título y 67 etiquetas binarias.
- **Semántica:** 1 indica presencia según la codificación humana del productor, 0 ausencia registrada. `TREES` no cuenta cuántos árboles hay. Las etiquetas no describen píxeles, pigmentos, calidad ni intención.
- **Población principal:** 381 episodios con `GUEST == 0`; 22 marcados `GUEST` se excluyen y se reincorporan en una comprobación de sensibilidad. La marca no es una nueva verificación independiente de autoría.
- **Variables:** [run.py](../run.py), constante `FEATURES`, documenta doce familias agregadas mediante OR. Nieve y montañas comparten `SNOWY_MOUNTAIN`: hay correlación deliberada entre familias, no independencia estadística.
- **Fuera del modelo:** título, ID, temporada, número de episodio, artista invitado, marcos, paletas e imágenes. No se aplica `StandardScaler`: cada familia binaria recibe el mismo peso; estandarizar alteraría ese peso, especialmente en motivos raros.
- **Ceros:** se conservan tres perfiles sin ninguno de estos doce motivos. No son datos ausentes ni cuadros vacíos. 381 episodios se reducen a 122 perfiles distintos: muchos cuadros son indistinguibles con esta representación.

## Atribución y uso

Fuente: [FiveThirtyEight, Bob Ross](https://github.com/fivethirtyeight/data/tree/4c1ff5e3aef1816ae04af63218015066e186c147/bob-ross), datos que acompañan el trabajo de Walt Hickey. Datos del repositorio bajo [CC BY 4.0](https://github.com/fivethirtyeight/data/blob/4c1ff5e3aef1816ae04af63218015066e186c147/LICENSE). Las transformaciones de esta demo son el filtro de invitados y la agregación de motivos; no se modificaron los bytes originales.

Esta licencia de datos no implica permiso sobre pinturas, vídeos o reproducciones. Las cuatro imágenes opcionales se enlazan al proveedor, sin copiar sus archivos. [gallery.json](../reference/gallery.json) conserva atribución, cruce de episodios y pruebas de descarga/decodificación. La segunda fuente sólo ilustra representantes; no alimenta el clustering ni acredita visualmente cada etiqueta.
