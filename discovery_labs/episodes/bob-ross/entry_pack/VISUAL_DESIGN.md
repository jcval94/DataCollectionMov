# Sistema visual Fase 1 — imágenes que demuestran, no decoran

El primer HTML es una **investigación visual autosuficiente**, no una presentación ni storyboard de video. Protagonista: historia documentada de Bob Ross, contraste entre intuición y evidencia, evolución del show y las limitaciones del corpus.

## Figuras prioritarias

| # | Mensaje que debe poder probar | Diseño | Cálculo, filtro y prueba adversarial |
|---|---|---|---|
| V1 | «¿Cuánto de Bob Ross está en la etiqueta de árbol?» | **Mosaico de los 403 episodios**, anfitrión/invitado distinguible; árboles/no árboles, hover/focus con código | OR TREE/TREES, denominador por grupo, 36 contraejemplos entre 381 anfitrión |
| V2 | «El paisaje tiene historia» | **Heatmap de 31 temporadas × 12 familias**, n por temporada visible, orden temporal ordinal | Cada celda n_con_motivo/n_de_esa_temporada, intervalos si pertinentes |
| V3 | «El patrón cambia según cuándo miramos» | Small multiples / series de motivos por temporada; eventos históricos en capa separada | Fecha de emisión/grabación SOLO si verificada; señalizar precisión temporal e incertidumbre |
| V4 | «Una anomalía no siempre es un error» | **Outliers multiescala**: episodio/temporada/era + mini-mapa de perfiles | Rareza con baseline, n, efecto de longitud del episodio y de la fuente; robustez a métrica |
| V5 | «Agrupar no equivale a descubrir estilos» | Explorador de clusters, doce motivos, comparativa Jaccard/Euclídea, transición alluvial | 381 episodios, representación idéntica, k=4 impuesto, ARI, tamaños, representantes |
| V6 | «Lo que no está en la tabla también importa» | Diagrama de cobertura: episodios emitidos, tres versiones del cuadro, preparación temporada 32 | Fuente NPR y AP; no sumar obras a las 403 filas como si fueran observaciones homogéneas |
| V7 | «Los rasgos aparecen juntos de manera no obvia» | Matriz de coocurrencias/lift con anotación de dependencia `SNOWY_MOUNTAIN` | Control de frecuencias base, múltiples comparaciones, no causalidad |
| V8 | «Cómo la métrica cambia la conclusión» | Comparativa de proporciones, incertidumbre y denominadores vs conteos absolutos | GUEST n=22, host n=381; mostrar tamaños del grupo y sensibilidad |

## Patrón visual del explorador de clusters

**Layout:** scatter/UMAP/PCA únicamente si dimensionalidad y proyecciones están justificadas; alternativamente lista de grupos y mosaico ordenado por medoid. Los puntos se identifican por episodio; color codifica grupo por un algoritmo y versión declarados. Los tamaños son constantes salvo variable cuantitativa verificable.

**Hover, focus de teclado y tap** sobre cada episodio:

1. Mostrar tarjeta `S09E02 · Surf's Up` con temporada, título tal como aparece en CSV, doce motivos, grupo (algoritmo/métrica), distancia al representante y un estado visible de QA.
2. **Pintura real si hay autorización comprobable**: preview con `source_url`, copyright/atribución, `permission_status=ALLOWED` y archivo local revisado. No descargar ni hotlinkear en un dominio propio solo porque exista `img_src` público.
3. **Si NO hay autorización:** miniatura abstracta codificada por motivos (claramente «diagrama de atributos», nunca «reproducción de la pintura») y enlace «Ver pintura en el sitio original», abierto por acción explícita. El hover no filtra secretos ni toca servidores.
4. Al cambiar distancia, animar membresía SOLO sobre asignaciones calculadas; conservar el ID, nombrar grupos como «Sala 1» etc., no «estilo natural».
5. Tooltip equivalente en teclado (`tabindex=0`, `focus`, `aria-describedby`) y selección mediante toque móvil. Evitar hover exclusivo; ofrecer panel persistente de selección.
6. Cuando no hay conectividad, mostrar fallback con ID/título/etiquetas verificadas; no inventar imágenes.
7. Permitir descargar tabla de puntos y asignaciones con el SHA de la fuente.

## QA de figuras

- Evidencia de fuente y hash en `data-source`, pie y enlace de metodología.
- Periodo, grano, denominador y unidad visibles cerca de la comparación.
- No usar barras sin base cero si no está justificado; paletas accesibles y no depender solo del color.
- Control responsivo 390px, 768px, 1440px; tooltip nunca fuera de pantalla; texto >= 12px visual.
- Export SVG/PNG con títulos, texto alternativo, leyendas sin cortar.
- Confirmar identidad exacta entre episodio del CSV y la imagen externa; inconsistencias de títulos se documentan.
- Variar k/métrica o filtro hace cambiar etiquetas y figuras desde resultados calculados, no usar números escritos a mano.
- No incorporar imágenes de terceros en PDF, HTML ni video sin permiso suficiente.
- Las historias subjetivas («más oscuro», «más triste») requieren definición computable o análisis cualitativo validado; no proyectar emociones sobre las pinturas.

## Guía de contraste científico

**Mal diseño:** «Bob Ross tenía más árboles en 1990» sin fechas verificadas por episodio.

**Mejor diseño:** «En temporadas ordinales 1 a 31, ¿cómo cambió la proporción de episodios con TREE o TREES? ¿Qué pasa al separar GUEST y controlar tamaños de temporadas?». Colocar eventos biográficos solo en una banda **separada**, con incertidumbre y advertencia contra causalidad.

**Mal diseño:** clusters con thumbnails descargados sin licencia ni procedencia.

**Mejor diseño:** clusters con representantes de episodio y tarjeta de atributos, y opción de pintura auténtica únicamente tras verificación de derechos, igualdad season+episode y permiso.

## Narrativa de la guía

Abrir con Bob Ross como persona y creador de un programa, no con 403 como dato aislado. Las figuras deben tener tensión dramática sin inventar giros: mito → evidencia → excepción → contextualización temporal → modelo que falla → límite del dataset → nueva pregunta. El HTML conserva un modo técnico con fórmulas, resultados y código reproducible.

**La narrativa del video y su intro siguen BLOQUEADAS** hasta aprobar el reporte científico Fase 1.
