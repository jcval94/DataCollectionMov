# Diccionario, procedencia y contratos de calidad

## Grano y alcance

Cada fila representa **un episodio etiquetado** de *The Joy of Painting*: 403 IDs únicos con formato \`SnnEnn\` en 31 temporadas; no es una fila por obra original, espectador, compra o pincelada.

- \`EPISODE\`: clave única de episodio; **metadato**, nunca feature estética.
- \`TITLE\`: título proporcionado por FiveThirtyEight; útil para localizar el ejemplo, no como indicador de motivos.
- \`GUEST\`: etiqueta binaria de episodio con invitado. 22 registros con 1; análisis principal n=381 sin invitados.
- Otras 66 etiquetas binarias (67 contando \`GUEST\`): 1 presencia codificada, 0 ausencia registrada. **No son cantidades**.
- \`TREE\` y \`TREES\`, \`MOUNTAIN\` y \`MOUNTAINS\`, etc., son **etiquetas distintas**; agruparlas requiere documentar el OR.

## Doce familias derivadas (Silver)

| Variable | Columnas originales (OR) | Observación |
|---|---|---|
| arboles | TREE, TREES | Presencia, no cantidad |
| montanas | MOUNTAIN, MOUNTAINS, SNOWY_MOUNTAIN | Se cruza por construcción con nieve |
| lagos | LAKE, LAKES | Una o más etiquetas |
| rios | RIVER | No implica longitud ni caudal |
| mar | OCEAN | Motivo codificado |
| nieve | SNOW, SNOWY_MOUNTAIN | Solapa con montaña |
| cascadas | WATERFALL | Motivo codificado |
| estructuras | STRUCTURE | No agrupa todas las etiquetas de edificaciones |
| nubes | CLOUDS | No incluye automáticamente CIRRUS/CUMULUS |
| rocas | ROCKS | No incluye CLIFF por defecto |
| sol | SUN | Etiqueta original |
| flores | FLOWERS | Etiqueta original |

Las doce familias están seleccionadas para una explicación humana y coinciden con el ejemplo previo del repositorio. Algunas etiquetas de baja frecuencia pueden producir grupos inestables.

## Política Bronze → Silver → Gold

**Bronze:** los bytes originales \`data/elements-by-episode.csv\`, inmutables, con SHA-256 fijado y licencia de datos declarada.

**Silver:** \`output/silver_motifs.csv\`, reconstruido únicamente a partir de Bronze: ID, temporada derivada, GUEST y doce familias binarias. No borra ni reemplaza Bronze.

**Gold descriptivo:** \`output/results.json\`: frecuencias, denominadores, temporadas, contraejemplos y asignación ficticia por reglas. Los SVG son vistas reproducibles de Gold.

**Gold experimental:** \`output/clusters.json\` con k-medoids Jaccard y Euclídea, cuatro grupos impuestos, representantes reales y acuerdo entre particiones (ARI). \`output/04-salas.svg\` resume sus tamaños.

## Registros de calidad obligatorios

- SHA del archivo íntegro y tamaño.
- 69 columnas declaradas; 67 etiquetas binarias.
- 403 IDs no nulos, formato \`SxxExx\`, sin repetidos.
- Todas las etiquetas son literalmente 0 o 1: **no imputar**.
- Título presente; temporada extraída sólo de un ID válido.
- 381 anfitrión + 22 invitados = 403.
- 345 de 381 anfitrión con TREE o TREES; 36 sin ambos.
- 150 anfitrión con montaña; 48 de esos 150 sin nieve.
- Los campos ID, TITLE, GUEST y temporada se excluyen de la matriz de clustering principal.
- Los diseños con dinero necesitan datos externos de costos/demanda; no simular un ROI observado.

## Limitaciones que la narrativa NO puede ocultar

1. **Cobertura:** representa los episodios codificados en este archivo. No acredita la totalidad de las pinturas físicas ni dibujos no emitidos.
2. **Sesgo de codificación:** es la clasificación humana de FiveThirtyEight, no un detector visual validado.
3. **Independencia:** \`SNOWY_MOUNTAIN\` activa dos familias; algunos motivos tienen múltiples etiquetas cercanas.
4. **Causalidad:** no se puede concluir que invitar artistas cambió los motivos; el tamaño de invitados es pequeño.
5. **Métrica:** silhouette mide compacidad/separación en un espacio dado. ARI mide acuerdo de particiones, no exactitud ni calidad artística.
6. **Monetización:** no hay dinero, visitas, boletaje, marketing ni costos; solo escenario hipotético de gestión de cuatro salas.
7. **Derechos:** la licencia CC BY 4.0 aplica al dataset y exige atribución; no concede licencia abierta sobre cuadros o videos.

## Proveniencia

FiveThirtyEight/data, edición \`4c1ff5e3aef1816ae04af63218015066e186c147\`.

- https://github.com/fivethirtyeight/data/tree/4c1ff5e3aef1816ae04af63218015066e186c147/bob-ross
- https://github.com/fivethirtyeight/data/blob/4c1ff5e3aef1816ae04af63218015066e186c147/LICENSE
- \`data/manifest.json\` contiene el hash completo y fecha de recuperación del original.
