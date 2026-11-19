# Banco histórico de preguntas — Bob Ross (LEGACY)

> **ARCHIVO HISTÓRICO; NO USAR COMO BANCO EDITORIAL VIGENTE.** Conservado del PR #5 para trazabilidad de las 12 candidatas iniciales. La única lista canónica de investigación es [`QUESTIONS_MASTER.md`](QUESTIONS_MASTER.md) + [`questions_master.json`](questions_master.json), con 14 preguntas O1/O2/O3 y modelo más estadística. Para toda guía nueva, utilizar Question Forge V2. No presentar el banco histórico como un segundo bloque.

> **12 investigaciones candidatas, no 12 hallazgos confirmados.** Cada árbol contiene observación inicial → segunda pregunta → contraste de tercer orden. No hay compromiso de responderlas todas en una clase de 45 minutos. Seleccionar una protagonista y una rama razonable; las seis perspectivas iniciales se conservan como rutas de votación, pero deben evolucionar.

## Por qué cambiamos el estándar

Una consulta como «¿cuántos cuadros tienen árboles?» solo sirve de primer indicio. Para convertirla en investigación debemos preguntar **cuándo cambia, qué significa, por qué podría parecer así, qué otra fuente necesitaríamos y qué prueba podría tumbar la interpretación**. Las preguntas sobre salud no deben afirmar relación causal; las imágenes no heredan la licencia del CSV.

## Árboles propuestos

### Q01 · ¿Sus últimos paisajes cuentan una historia diferente?

- **Familia generalizable:** CAMBIO_DE_RÉGIMEN (salud/contexto).
- **1.er orden:** ¿Cambian la diversidad y frecuencia de motivos durante las 31 temporadas, especialmente en los últimos episodios? **Métrica:** Entropía de combinaciones, 67 tags por episodio, prevalencias por temporada; excluir invitados.
- **2.º orden:** Si hay cambio, ¿se concentra en una ruptura temporal o ya existía la tendencia mucho antes? **Prueba:** Ajuste de tendencia segmentada con intervalos y cortes placebo; fechas reales externas.
- **3.er orden:** ¿Seguiría existiendo el cambio si no supiéramos nada de su enfermedad o si usáramos otra métrica de estilo? **Rival o límite:** Orden de emisión ≠ producción; cambios de producción, etiquetado o elección de motivos; biografía ≠ prueba causal.
- **Visualización de alto impacto:** Timeline con banda de fechas biográficas inciertas, distribuciones por periodos y robustez por cortes placebo.
- **Datos adicionales:** Fechas verificadas por episodio + enfermedad con precisión y fuentes; colores/estilo visual si se pretende hablar de estilo.
- **Estado:** HYPOTHESIS_NEEDS_EXTERNAL_DATA; NO afirmar resultados sin ejecutarlos.

### Q02 · ¿Bob Ross se repetía o experimentaba más de lo que recordamos?

- **Familia generalizable:** NOVEDAD_Y_REPETICIÓN (creencia compleja).
- **1.er orden:** ¿Cuánto se parecen los patrones de motivos entre temporadas y episodios próximos? **Métrica:** Jaccard entre episodios, novedad relativa vs episodios anteriores, tasa de combinaciones no vistas.
- **2.º orden:** Si algunas temporadas parecen repetitivas, ¿se debe a pocos motivos dominantes o a una reutilización estructurada de composiciones? **Prueba:** Comparar pares condicionados por número de elementos y mezcla de motivos.
- **3.er orden:** ¿La misma impresión persiste cuando cambiamos etiquetas por paletas de color e imágenes autorizadas? **Rival o límite:** Las etiquetas binarias no miden técnica, composición, luminosidad ni estilo.
- **Visualización de alto impacto:** Mosaico de temporadas con novedades y pequeñas múltiples de pares aparentemente iguales.
- **Datos adicionales:** Paletas jwilber y revisión de imágenes con permisos/atribución.
- **Estado:** TESTABLE_IN_LABELS_EXTERNAL_FOR_STYLE; NO afirmar resultados sin ejecutarlos.

### Q03 · La temporada atípica: ¿existe una verdadera excepción?

- **Familia generalizable:** OUTLIERS_MULTIESCALA (anomalías).
- **1.er orden:** ¿Qué episodio o temporada es más atípico según frecuencia de motivos y combinaciones? **Métrica:** Distancias Jaccard por episodio; desviación multivariante por temporada y tamaño de n.
- **2.º orden:** Si una temporada parece excepcional, ¿se concentra el desvío en dos episodios raros o afecta al conjunto? **Prueba:** Leave-one-out y análisis de influencia por episodio; por temporada y bloques históricos.
- **3.er orden:** ¿La anomalía sobrevive al excluir invitados, motivos raros y cambiar de distancia o escala de agregación? **Rival o límite:** Anomalía estadística puede deberse al codificador o a agregaciones artificiales.
- **Visualización de alto impacto:** Mapa de calor 31 temporadas + gráfico de puntos de episodios con lupa al pasar el cursor.
- **Datos adicionales:** CSV original; posible enriquecimiento de imágenes para casos atípicos.
- **Estado:** TESTABLE; NO afirmar resultados sin ejecutarlos.

### Q04 · ¿Los árboles dominaron siempre, o el promedio esconde una historia?

- **Familia generalizable:** PARADOJAS_MEZCLA (creencia popular avanzada).
- **1.er orden:** ¿Cómo cambia la presencia de árboles por temporada y tipo de episodio? **Métrica:** TREE OR TREES / n por temporada, anfitrión frente a invitados.
- **2.º orden:** Si el promedio es estable, ¿hay segmentos donde cambia fuertemente o se invierte una comparación? **Prueba:** Estratificar por invitados, temporada y motivo dominante, con n visibles; cuidado selección de subgrupos.
- **3.er orden:** ¿Cuáles resultados desaparecen tras ajustar por composición o cambiar denominador? **Rival o límite:** Simpson no se presupone; buscarlo sin seleccionarlo post hoc.
- **Visualización de alto impacto:** Small multiples por temporada con promedio global y bandas de tamaños.
- **Datos adicionales:** CSV fuente.
- **Estado:** TESTABLE; NO afirmar resultados sin ejecutarlos.

### Q05 · ¿Cuánto de Alaska persistió en una carrera pintada en Florida?

- **Familia generalizable:** BIOGRAFÍA_PAISAJE (memoria cultural e historia).
- **1.er orden:** ¿Qué peso tienen montañas, nieve y bosques a lo largo de las temporadas? **Métrica:** Prevalencias de familias de motivos; n por temporada y periodo.
- **2.º orden:** Si son frecuentes, ¿se trata de un sello único o de motivos comunes a la pintura televisiva del periodo? **Prueba:** Contrastar con corpus externo comparable y reportar diferencias de codificación.
- **3.er orden:** ¿Las referencias biográficas explican la elección de motivos o sólo ofrecen una historia que suena plausible? **Rival o límite:** Estilo e inspiración son constructos, no columnas del CSV; una correlación no prueba influencia personal.
- **Visualización de alto impacto:** Mapa biográfico con línea temporal y pictogramas cuantificados por periodo.
- **Datos adicionales:** Biografía primaria + corpus comparable externo si existe.
- **Estado:** EXTERNAL_DATA_NEEDED; NO afirmar resultados sin ejecutarlos.

### Q06 · ¿Descubrimos cuatro estilos o fabricamos cuatro salas?

- **Familia generalizable:** CLUSTERS_Y_MECANISMOS (detective/metodología).
- **1.er orden:** ¿Qué episodios quedan juntos bajo Jaccard, Euclídea y reglas curatorias? **Métrica:** ARI, silhouette en cada espacio, perfiles por sala y medoids.
- **2.º orden:** Si los grupos difieren, ¿qué etiquetas o pesos cambian más la asignación de casos frontera? **Prueba:** Ablation por familia y distancias; episodios que migran entre grupos.
- **3.er orden:** ¿Un historiador del arte —sin conocer la asignación— reconocería esos estilos, o solo motivos de composición? **Rival o límite:** Cuatro salas son restricción del museo; métricas y clústeres no miden calidad estética.
- **Visualización de alto impacto:** Matriz de transiciones entre clusters + tarjetas de episodio con vista previa condicionada a derechos.
- **Datos adicionales:** CSV + acceso legítimo a imágenes o enlaces.
- **Estado:** PARTLY_EXECUTED_REQUIRES_VALIDATION; NO afirmar resultados sin ejecutarlos.

### Q07 · ¿Una serie distinta aparece cuando Bob no está frente al lienzo?

- **Familia generalizable:** INVITADOS_Y_SELECCIÓN (social/representación).
- **1.er orden:** ¿En qué motivos difieren episodios GUEST=1 y GUEST=0? **Métrica:** Prevalencias con n=22 vs n=381 e incertidumbre descriptiva.
- **2.º orden:** Si difieren, ¿se debe a qué invitados aparecen en determinadas temporadas? **Prueba:** Estratificación temporal, revisar identidad y producción solo si existe fuente válida.
- **3.er orden:** ¿Qué conclusión queda si emparejamos temporadas y dejamos fuera episodios influyentes? **Rival o límite:** No generalizar a artistas, género, intención ni discriminación; muestra no aleatoria.
- **Visualización de alto impacto:** Dumbbell de proporciones con n y matriz de episodios invitados.
- **Datos adicionales:** Anotaciones GUEST, metadatos externos de episodios y quién realizó cada pintura.
- **Estado:** TESTABLE_DESCRIPTIVE; NO afirmar resultados sin ejecutarlos.

### Q08 · Dos cuadros con los mismos árboles, ¿pueden contar historias opuestas?

- **Familia generalizable:** VISUAL_VS_ETIQUETA (imágenes y medición).
- **1.er orden:** ¿Qué pares de episodios comparten etiquetas idénticas o muy similares? **Métrica:** Duplicados de patrones de 12 o 67 etiquetas, distancia Jaccard.
- **2.º orden:** Entre pares muy similares, ¿qué tan diferentes son sus colores o composiciones observables? **Prueba:** Unir por temporada/episodio con paletas y ejemplos de imágenes cuya licencia permita visualización.
- **3.er orden:** ¿Los clusters de etiquetas pierden estabilidad cuando incluimos paletas o embeddings de imágenes autorizadas? **Rival o límite:** No presentar similitud de etiqueta como semejanza estética completa.
- **Visualización de alto impacto:** Comparador de pares (lado a lado) con imagen opcional o marcador y paletas.
- **Datos adicionales:** jwilber paletas/colores; imágenes con permisos.
- **Estado:** EXTERNAL_JOIN_REQUIRED; NO afirmar resultados sin ejecutarlos.

### Q09 · ¿El mundo cambiaba mientras los paisajes permanecían iguales?

- **Familia generalizable:** CULTURA_HISTORIA (contexto histórico).
- **1.er orden:** ¿Hay cambios descriptivos importantes en motivos entre periodos 1983–1994? **Métrica:** Descomposición temporal por temporadas asociadas a fechas de emisión verificadas.
- **2.º orden:** Si una ruptura coincide con un evento cultural, ¿aparece también en periodos vecinos o series comparables? **Prueba:** Cortes alternativos y control por tendencias, no asumir causalidad.
- **3.er orden:** ¿Cuántas coincidencias similares aparecerían al probar eventos falsos o cortar la serie al azar? **Rival o límite:** Múltiples pruebas, sesgo retrospectivo y elección arbitraria de evento.
- **Visualización de alto impacto:** Timeline con incidentes biográficos/culturales anotados con certeza y test de placebo.
- **Datos adicionales:** Fechas reales y fuente histórica, comparación externa.
- **Estado:** HYPOTHESIS_EXTERNAL_TIMELINE; NO afirmar resultados sin ejecutarlos.

### Q10 · ¿Por qué recordamos los árboles, si el dato también cuenta otras historias?

- **Familia generalizable:** LEYENDA_Y_RECUERDO (memoria colectiva).
- **1.er orden:** ¿Qué proporción de episodios tienen y no tienen árboles, y qué otros motivos aparecen? **Métrica:** Prevalencia de familias, combinaciones frecuentes, contraejemplos.
- **2.º orden:** ¿Son los árboles especialmente dominantes en portadas, títulos, imágenes promocionales y frases repetidas? **Prueba:** Codificación externa de recursos promocionales de distintas épocas, evitando selección sesgada.
- **3.er orden:** ¿Coincide lo que la audiencia recuerda con lo que la serie mostró? ¿Qué método de encuesta sería válido? **Rival o límite:** Fama popular y memoria no están medidas en el dataset.
- **Visualización de alto impacto:** Contraste entre etiquetas observadas y, si se obtiene, muestra de material promocional con base.
- **Datos adicionales:** Fuentes promocionales y encuestas/estudios válidos.
- **Estado:** EXTERNAL_RECEPTION_DATA_NEEDED; NO afirmar resultados sin ejecutarlos.

### Q11 · ¿Un cuadro más cargado es necesariamente más complejo?

- **Familia generalizable:** COMPLEJIDAD_Y_ESTILO (medición y visualización).
- **1.er orden:** ¿Cuántas etiquetas de motivos aparecen por episodio y cómo evoluciona su distribución? **Métrica:** Número de etiquetas activas, familia agregada, densidad de motivos.
- **2.º orden:** ¿Episodios con el mismo conteo pueden ser visualmente muy diferentes? **Prueba:** Parejas emparejadas por número de etiquetas y examen de paletas/composición.
- **3.er orden:** ¿Qué dimensiones independientes de complejidad necesitaríamos para sostener una narrativa sobre evolución artística? **Rival o límite:** Más etiquetas no significa más destreza, esfuerzo, detalle ni mérito.
- **Visualización de alto impacto:** Scatter/densidad por episodio y panel de dos casos con mismo conteo, imágenes si se autoriza.
- **Datos adicionales:** Contenido visual/paletas con derechos e indicadores validados.
- **Estado:** TESTABLE_PROXY_EXTERNAL_FOR_STYLE; NO afirmar resultados sin ejecutarlos.

### Q12 · ¿Los ‘happy accidents’ eran errores o parte de un método?

- **Familia generalizable:** FALSABILIDAD (contraste de mito).
- **1.er orden:** ¿El CSV contiene alguna medida de error, accidente o improvisación? **Métrica:** Inventario de variables y fuentes posibles de transcripciones/episodios.
- **2.º orden:** Si no existe, ¿qué protocolo observable permitiría codificar cambios no planeados sin leer mentes? **Prueba:** Muestra anotada de videos con definición operacional de desviación y consentimiento/uso permitido.
- **3.er orden:** ¿Los resultados diferirían entre codificadores independientes y entre guion, edición y pintura terminada? **Rival o límite:** El slogan cultural no basta para atribuir intención psicológica.
- **Visualización de alto impacto:** Tabla de lo que miden las fuentes y árbol de hipótesis en vez de cifras inventadas.
- **Datos adicionales:** Videos/transcripciones derechos/permisos y protocolo cualitativo.
- **Estado:** BLOCKED_WITHOUT_NEW_SOURCE; NO afirmar resultados sin ejecutarlos.


## Familias transferibles a otros 85 datasets

1. Cambios de régimen o puntos de inflexión y explicaciones rivales.
2. Anomalías que aparecen/desaparecen al pasar de individuo a cohorte, año o región.
3. Simpson, denominadores, mezcla y subgrupos.
4. Cambios de diversidad, novedad, continuidad y repetición temporal.
5. El relato de una figura o institución frente al comportamiento medido.
6. Distancia entre proxy medible y concepto humano (estilo, calidad, éxito, justicia).
7. Contrastación de creencias con evidencia externa de que realmente son creencias difundidas.
8. Efectos de shocks exógenos con cortes placebo y comparadores, si son identificables.
9. Influencia de métricas, escalas, representaciones y algoritmos sobre clusters o rankings.
10. Silencios: qué datos faltan, quién no aparece y cómo cambia eso la historia.

## Cómo aprobar una pregunta protagonista

- Evita una pregunta cuyo desenlace final sea un conteo o yes/no.
- Exige población, unidad, denominador, mecanismo o rival, segundo y tercer orden.
- La primera gráfica despierta curiosidad; la última debe cambiar o matizar la interpretación.
- Requiere un gráfico que se pueda comprobar sin duplicar cifras manualmente.
- Registra fuentes y estados CALCULATED / EXTERNALLY_DOCUMENTED / TESTABLE_PENDING / BLOCKED.
- Prioriza preguntas con contexto humano y experimentos reales, no con espectáculo ficticio.

**Selección editorial preliminar (no resultado):** Q02 (evolución/novedad), Q03 (anomalías por escala), Q06 (los clusters como construcción), Q08 (proxies vs imágenes). Q01 (enfermedad) merece un DR especializado y solamente avanza con una cronología fiable y una conclusión explícitamente no causal, salvo diseño mejor identificado.
