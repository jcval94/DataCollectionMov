# Diccionario del snapshot Bob Ross

Unidad: episodio de The Joy of Painting. 403 filas y 69 columnas: EPISODE, TITLE y 67 indicadores binarios humanos. El snapshot mantiene los episodios de invitados; la ruta principal usa GUEST=0 (381 episodios) y los invitados se estudian por separado.

| Campo o familia | Significado y límite |
| --- | --- |
| EPISODE | ID SxxExx, único y obligatorio. Se usa para localizar episodios, nunca como rasgo de una pintura. |
| TITLE | Título registrado. Se conserva para localizar contraejemplos; no participa del clustering. |
| GUEST | Marca de invitado según la codificación del productor; no es verificación independiente de autoría. |
| TREE / TREES | Indicadores nominales de motivos. El contraste de árboles usa OR entre ambos, no suma de cantidades de árboles. |
| MOUNTAIN / MOUNTAINS | El contraste de montañas usa OR entre ambos. |
| SNOW / SNOWY_MOUNTAIN | El contraste de nieve usa OR. SNOWY_MOUNTAIN introduce solapamiento semántico entre nieve y montaña; no asumir independencia. |
| LAKE, RIVER, OCEAN, CLOUDS, ROCKS, FLOWERS | Motivos binarios elegidos junto con los anteriores para el clustering del piloto. |
| Otros indicadores | Se preservan en el original, pero no participan en ese clustering. Un cero no equivale a cuadro vacío ni a ausencia de todo lo que no está etiquetado. |

La representación de clustering contiene doce columnas originales seleccionadas, con redundancias semánticas explícitas. Jaccard ignora coincidencias de ausencia; Euclídea trata de otra manera esa representación. Se comparan distancias y se informa su desacuerdo. Cuatro grupos es una restricción narrativa, no un resultado que pruebe cuatro estilos naturales. Para inferir sobre imágenes se requerirían las imágenes, permiso y otra medición.

Un episodio válido sin TREE ni TREES refuta la versión universal dentro del archivo de etiquetas. No demuestra que ninguna reproducción del cuadro contenga un árbol. Las etiquetas, el material visual y el corpus de todas las pinturas son objetos distintos.

Fuente, atribución y SHA256: data/manifest.json. Licencia de las etiquetas: CC BY 4.0; no extiende permiso a pinturas, audio o vídeo.
