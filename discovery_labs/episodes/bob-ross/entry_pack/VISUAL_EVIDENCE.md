# Brief de visualización — poderoso, interactivo y científicamente honesto

## Principio
La gráfica debe permitir responder **«¿qué cambió en mi interpretación?»**, no decorar un párrafo. Priorizar figuras inspeccionables y reproducibles en el primer HTML; las animaciones/video llegan después de aprobación.

## 1. Línea de vida + línea de datos
**Pregunta:** ¿qué ocurrió en la vida y carrera de Bob Ross y cómo cambian los motivos a lo largo del programa?
- Eje x doble validado: temporada S01–S31 y, sólo si se verifica la relación, fecha de emisión.
- Densidad de árbol/montaña/nieve y complejidad/entropía por temporada, con n.
- Marcadores para carrera, hitos de producción y salud con fecha/rango + certeza + fuente.
- Zona «fecha no verificada»: no poner un marcador exacto por intuición.
- Comparar tendencias y cortes placebo. Una coincidencia visual NO es prueba causal.
- CTA «ver cómo se midió», no CTA «la enfermedad cambió todo».

## 2. Anatomía de una temporada atípica
**Pregunta:** ¿qué hace diferente a una temporada y qué cambia con el nivel de agregación?
- Heatmap por temporada × motivo; tooltip con n/N, proporción y definición.
- Panel sincronizado de 13 episodios de temporada seleccionada; el punto destacado muestra sus motivos.
- Señalar valores extremos por episodio, luego por temporada y por bloque temporal, con agregación explicitada.
- Comparar leave-one-out para descubrir si un episodio extremo explica toda una temporada.
- Evitar colorear frecuencia con paleta perceptual donde 0 sea igual a faltante.

## 3. Laboratorio de agrupamientos + vista previa de obra
**Pregunta:** ¿qué representa un cluster, y qué obras podrían contradecir su nombre?
- 381 episodios GUEST=0, doce familias OR, k=4 impuesto por una exposición ficticia.
- Panel grande: scatter/embedding con ejes que indiquen que son coordenadas exploratorias (UMAP/PCA si se calculan y se justifican).
- Clusters coloreados con paleta apta para daltonismo, tamaño por muestra, medoids y casos frontera.
- Selector de distancia: Jaccard/Euclídea; mostrar transiciones de asignación y el ARI correspondiente.
- Al pasar cursor o enfocar con teclado un punto: **tarjeta de episodio** con SxxExx, título, temporada, motivos, cluster, distancia al medoid y enlace de procedencia.
- **Cuadro real en la tarjeta, únicamente si la URL y el permiso están verificados**. Si los derechos son inciertos, mostrar ficha y un enlace externo para abrir la obra, nunca alojar imagen ni simular una licencia. No descargar copias.
- En móvil: tap abre tarjeta fija; botón cerrar y navegación previa/siguiente; nunca depender únicamente de hover.
- Fallback offline: metadatos y mini-ilustración ORIGINAL genérica («sin vista previa autorizada»), no una pintura falsa.
- Se puede reutilizar el cruce season+episode de `jwilber/Bob_Ross_Paintings` y el manifiesto `examples/bob_ross_clustering/reference/gallery.json` como **pistas**, no como permiso de reproducción. Cuatro imágenes ya se probaron técnicamente en 2026-11-07; disponibilidad ≠ derechos.

## 4. La paradoja de medir estilo con etiquetas
- Seleccionar dos episodios con doce motivos idénticos o cercanos.
- Comparador de paletas y, solo si se autoriza, cuadros.
- Indicador de qué ignora la tabla: composición, trazo, cantidad de árboles, textura, color, calidad.
- Llamada editorial: «La misma fila conceptual no implica la misma imagen».
- Enlazar el cálculo de similitud al snapshot, no escribir porcentajes a mano.

## 5. Gráfico de ruptura y prueba adversarial
- Panel principal de serie temporal junto a gráfico con puntos de corte alternativos.
- Registrar cambio observado, pero también placebo/permutación, sensibilidad a GUEST, a rareza de motivos y a temporada.
- Incluir escenario sin cambio si las pruebas lo muestran: sigue siendo un descubrimiento válido.

## 6. Pirámide narrativa de evidencia
En cada sección de la guía HTML:
1. Afirmación en titular (precisa, sin hiperbole).
2. Figura explicativa.
3. Qué dato y denominador sostienen la frase.
4. Prueba de resistencia.
5. Qué no se puede afirmar y qué dataset hace falta.
6. Expansión técnica con código, versión, muestra, fuente y fecha.

## Política de interacción y QA
- `pointerenter`, `focusin`, `click`, `touch` equivalentes; teclado Escape/cerrar; aria-label descriptiva.
- No usar tooltip como único acceso a información importante; mantener tabla accesible y texto alternativo.
- Latencia aceptable en móvil sin bloquear el scroll; interacción progresiva, posibilidad de desactivar animación.
- SVG/Canvas debe mapear coordenadas a registros con IDs estables, no por índice de array tras filtros.
- Para reproducibilidad, cifras provienen de JSON/CSV generados por análisis, no se duplican en el DOM.
- Un gráfico de periodos muestra «temporada aproximada» cuando la fecha exacta se desconoce.
- Inspeccionar desktop 1440×900, móvil 390×844, navegación teclado, contraste, tooltip fuera de pantalla y textos recortados.

## Derechos de imagen
Verificar proveedor, autor/titular, condiciones de uso, hotlinking y atribución. Si el uso remoto es permitido, conservar URL y comprobación con fecha; si no, ofrecer enlace a catálogo y alternativa textual. Nunca asumir que CC BY 4.0 de FiveThirtyEight se aplica a cuadros o videos.

**Salida Fase 1:** visualizaciones y fichas dentro de `research_guide.html` con criterio científico. Este brief no autoriza producir guion de video, intro, voz ni MP4.
