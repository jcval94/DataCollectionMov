# Dirección visual del primer documento científico — no storyboard de video

**Objetivo:** figuras poderosas que expliquen datos, no que adornen una conclusión. Todas deben mostrar fuente, unidad, período, filtro, denominador y sus límites. Diseño responsive, accesible, SVG/HTML exportable e inspeccionado en navegador real.

## Siete figuras prioritarias

1. **Historia de los 403 episodios:** timeline con 31 temporadas y, en carril separado, fechas de emisión e hitos biográficos documentados, con intervalos de incertidumbre. Evitar superponer fecha de diagnóstico sobre fecha inventada de pintura.
2. **La textura de once años:** heatmap 31 temporadas × 12 familias de motivos, celdas como proporciones dentro de temporada, con n. Hover/foco muestra conteos exactos y el denominador. Color con escala fija y paleta accesible.
3. **Las temporadas atípicas:** distribución de scores de rareza por temporada y por episodio, con controles de multiplicidad y n=13; resaltar un punto solo tras contrastarlo con un modelo nulo.
4. **El universo de los paisajes:** red de coocurrencia de motivos con umbral justificado, comparada con prevalencias marginales. Separar rareza de una relación inesperada.
5. **El recuerdo de los árboles:** una matriz de puntos por episodio con filtros de árboles, invitados, temporada y paisaje sin árboles. Revelar contraejemplos, no eliminar sus etiquetas.
6. **Cuatro salas, cuatro interpretaciones:** comparación visual entre particiones Jaccard/Euclídea, alluvial solo si sus enlaces son legibles, ARI y ejemplos en frontera. No llamar «estilos» a los grupos arbitrarios.
7. **La sombra del dataset:** diagrama de universo real documentado → episodios emitidos → episodios etiquetados → familias usadas → poblaciones excluidas. La ausencia de datos debe ser visible.

## Interacción con pinturas en hover / focus / tap

**Gran idea, con puerta jurídica.** El HTML podría mostrar la obra asociada a cada episodio al pasar el cursor sobre un punto de cluster o usar focus con teclado/tap en móvil.

Propuesta de UI:
- Punto de cluster con identificador `SnnEnn`, temporada, distancia/cluster, motivos y n; el tooltip es accesible.
- Si `image_join_audit.csv` indica `license_status=AUTHORIZED_FOR_DISPLAY`, mostrar un thumbnail de la obra con fuente, atribución y texto alternativo.
- Cuando el permiso sea desconocido: panel textual, motivo en SVG abstracto original y enlace externo a la ficha oficial; **no cargar automáticamente la imagen ni copiarla al repositorio**.
- Si el recurso requiere red, informar que es opcional y garantizar un fallback offline.
- Evitar popovers que se oculten al mover cursor, navegación solo hover, controles táctiles inaccesibles o thumbnails no autorizados.
- Obra, fotografía, iconografía, nombre, voz y video están sujetos a derechos diferentes de los CSV.

## Verificación visual

- Revisar pixel-perfect en escritorio 1440×900 y móvil 390×844.
- Gráficos en 16:9 para proyección, pero leyendas y textos no se deben truncar en móvil.
- Separar gráficos exploratorios de conclusiones confirmadas.
- Contrastar etiquetas y n/N con tablas Gold; herramienta de QA automática para detectar discrepancias.
- Exportar SVG/PNG solo con autorización para imágenes integradas.
- Figuras accesibles con título, texto alternativo, foco visible, reducción de movimiento.
- No incluir gráficos «cinematográficos» que inventen evolución, conexiones o agrupamientos por estética.

## Galería de ejemplos de diseño (referencias conceptuales)

- Scrollytelling editorial de datos: una secuencia de preguntas que cambia el mismo gráfico para revelar un aspecto distinto.
- Small multiples con comparaciones justas.
- Zoom multiescala episodio → temporada → era.
- Inspector de puntos del cluster con modos «motivos», «datos», «fuente» y, condicionado a derechos, «obra».

Estas son **especificaciones técnicas y editoriales para el informe HTML de Fase 1**, no un storyboard de la Fase 2 de video.
