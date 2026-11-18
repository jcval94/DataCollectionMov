# Banco único de investigaciones — Bob Ross · Q-FORGE v2

> **FUENTE CANÓNICA EDITORIAL.** Las seis preguntas antiguas de `../questions.json` son puertas de entrada/interfaz, **no constituyen otro bloque narrativo**. Las consultas anteriores pasan a ser pasos O1, pruebas o microejercicios dentro de las investigaciones que siguen. Aquí está toda la selección, en **un solo bloque**, con problemas de O1, O2 y O3, al menos un **modelo** y un **ejercicio estadístico separado** por investigación.

## Regla de honestidad
Los modelos y ejercicios estadísticos siguientes son **planes, no ejecuciones**. Se indican qué, por qué y dónde; no se han entrenado modelos ni se atribuyen resultados. En preguntas con datos externos faltantes, la factibilidad es `BLOCKED` y su investigación permanece abierta. Datos de salud no están en el CSV; su fecha y su interpretación histórica deben reconciliarse antes de correlacionarla con episodios.

## Un solo bloque: 14 investigaciones con rutas O1→O2→O3

### BR-01 · ¿Cambió la pintura cuando cambió la vida de Bob Ross?

*La calma de la pantalla oculta una cronología mucho más compleja.*

**Pregunta principal:** ¿Existen rupturas verificables en motivos y complejidad hacia el final del programa, y hasta dónde podemos contrastarlas con acontecimientos personales?

**Orden 1 — ¿Qué vemos?** Examinar tendencias por temporada de familias de motivos, diversidad y escenas raras, sin fechas clínicas superpuestas por defecto.

**Orden 2 — ¿Qué nos obliga a preguntar el primer hallazgo?** Si aparece una ruptura tardía, ¿se reproduce al separar invitados, reducir dimensionalidad y usar ventanas alternativas?

**Orden 3 — ¿Qué explicación rival, sesgo o mecanismo podría cambiar la conclusión?** ¿Qué pasa al introducir cronologías verificadas de grabación y biografía y comparar causas rivales como cambios de producción, paletas y selección? ¿Qué parte NO puede atribuirse a la enfermedad?

**Modelo propuesto (M03):** Modelo binomial segmentado con detección restringida de cambio. **Por qué:** Busca cambios descriptivos en tasas temporales sin postular que una enfermedad los causó. **Dónde:** Research → tendencias por temporada, solo después de validar el orden temporal.

**Ejercicio estadístico (distinto del modelo):** Prueba de quiebre por bootstrap/permutación de bloques con corrección de búsqueda; intervalos por temporada.

**Datos necesarios:** CSV entero; FECHAS externas grabación/emisión y cronología médica como contexto separable.

**Visualización que cuenta la evidencia:** Heatmap de temporadas con banda de eventos biográficos etiquetados por fuente y precisión; dos paneles antes/después, sin flecha causal.

**Estado:** `BLOCKED_CONTEXT_TIMELINE`. **Advertencia:** Fuentes cronológicas no coinciden: Outside menciona primavera de 1994; otros relatos sitúan diagnóstico poco después de la muerte de Jane en 1992. Investigar discordancia antes de usar un marcador temporal.

### BR-02 · ¿Pintaba recuerdos de Alaska o una fórmula televisiva?

*Las montañas que recordamos podrían representar técnica, biografía o ambas.*

**Pregunta principal:** ¿Cómo cambian nieve, montañas y bosques entre temporadas, y qué evidencia externa sostiene la asociación con Alaska?

**Orden 1 — ¿Qué vemos?** Comparar tasas de escenas con montañas/nieve/bosques y sus coocurrencias a lo largo del programa.

**Orden 2 — ¿Qué nos obliga a preguntar el primer hallazgo?** Si se concentra un motivo en un periodo, ¿persiste dentro de episodios del anfitrión y con otras definiciones de montaña/nieve?

**Orden 3 — ¿Qué explicación rival, sesgo o mecanismo podría cambiar la conclusión?** ¿Podemos distinguir recuerdos biográficos de preferencias del formato didáctico con entrevistas y archivos de producción?

**Modelo propuesto (M02):** GAM binomial penalizado. **Por qué:** Permite estudiar trayectorias no lineales sin fingir rupturas puntuales. **Dónde:** Gold episodio-temporada → Research evolutivo.

**Ejercicio estadístico (distinto del modelo):** Tendencia binomial e intervalos por temporada, comparación contra un GLM lineal por remuestreo.

**Datos necesarios:** CSV; entrevistas verificables sobre Alaska y aprendizaje de pintura.

**Visualización que cuenta la evidencia:** Small multiples de montañas, nieve, árboles, n/N y citas en una línea temporal histórica separada.

**Estado:** `PLANNED_DATA_FEASIBLE`. **Advertencia:** SNOWY_MOUNTAIN entra en montaña y nieve por construcción.

### BR-03 · ¿El estilo evolucionó, o solo cambió qué dibujaba en televisión?

*Dos temporadas pueden parecer distintas sin haber cambiado el estilo pictórico.*

**Pregunta principal:** ¿Se alteró con el tiempo la mezcla de motivos y cuánta diversidad hay por temporada?

**Orden 1 — ¿Qué vemos?** Medir tasas multivariadas y diversidad de motivos por temporada con n explícito.

**Orden 2 — ¿Qué nos obliga a preguntar el primer hallazgo?** Si dos eras difieren, ¿qué etiquetas explican la diferencia y cuánta heterogeneidad hay dentro de cada periodo?

**Orden 3 — ¿Qué explicación rival, sesgo o mecanismo podría cambiar la conclusión?** ¿El contraste permanece al usar paletas, color o técnicas externas, o solo refleja nuestra codificación?

**Modelo propuesto (M04):** Beta-binomial jerárquico con shrinkage. **Por qué:** Estabiliza estimaciones de temporadas pequeñas y evita confundir ruido con cambios de estilo. **Dónde:** Gold agregado por temporada → Research periodos.

**Ejercicio estadístico (distinto del modelo):** Contrastes de tasas con intervalos/predicción posterior y sensibilidad a definición de eras.

**Datos necesarios:** CSV S01–S31, paleta e imágenes con derechos solo si autorizadas.

**Visualización que cuenta la evidencia:** River chart de motivos por era + heatmap de 31×12 con pequeñas multiples e incertidumbre.

**Estado:** `PLANNED_DATA_FEASIBLE`. **Advertencia:** Cambiar motivos no prueba cambiar técnica o estilo.

### BR-04 · ¿Y si la pintura más extraña fuera la pista de una temporada extraordinaria?

*Un episodio raro puede ser un error; una temporada rara puede ser una historia.*

**Pregunta principal:** ¿Qué episodios y temporadas se apartan del repertorio habitual, según una definición explícita de rareza?

**Orden 1 — ¿Qué vemos?** Obtener score de rareza por episodio usando doce motivos y comparar con vecinos similares.

**Orden 2 — ¿Qué nos obliga a preguntar el primer hallazgo?** ¿Las anomalías se acumulan en temporadas o tramos completos, tras normalizar por tamaño de temporada?

**Orden 3 — ¿Qué explicación rival, sesgo o mecanismo podría cambiar la conclusión?** ¿El resultado sobrevive a cambiar métrica/contaminación, bootstrap por temporada y revisar etiquetas de casos extremos?

**Modelo propuesto (M05):** Isolation Forest con comparador por distancia Jaccard. **Por qué:** Prioriza perfiles inusuales sin inventar una variable objetivo. **Dónde:** Gold por episodio → Research anomalies; luego agregación por temporada/era.

**Ejercicio estadístico (distinto del modelo):** Test por permutación de concentración estacional e intervalos bootstrap de rankings.

**Datos necesarios:** 403 episodios, GUEST, doce familias; fotografías verificadas opcionales.

**Visualización que cuenta la evidencia:** Panel coordinado: matriz de rareza por episodio, ranking de temporadas y tarjeta de contraejemplos.

**Estado:** `PLANNED_DATA_FEASIBLE`. **Advertencia:** La rareza estadística no significa valor estético ni error.

### BR-05 · ¿Por qué recordamos a Bob Ross por los árboles si su catálogo es más amplio?

*La imagen cultural puede ser más uniforme que los episodios reales.*

**Pregunta principal:** ¿Cuánto describe el arquetipo de los «árboles felices» el repertorio y cómo evoluciona lo que no encaja en él?

**Orden 1 — ¿Qué vemos?** Contrastar TREE/TREES y sus ausencias con denominadores explícitos para anfitrión e invitados.

**Orden 2 — ¿Qué nos obliga a preguntar el primer hallazgo?** ¿Los episodios sin árboles son un repertorio visual reconocible, y se agrupan por época o tema?

**Orden 3 — ¿Qué explicación rival, sesgo o mecanismo podría cambiar la conclusión?** ¿La excepcionalidad sobrevive otra taxonomía y evidencia visual autorizada, o revela una limitación de las etiquetas?

**Modelo propuesto (M01):** GLM logístico de presencia de árbol vs temporada/motivos no redundantes. **Por qué:** Permite explorar tendencia y covariables sin reducir la investigación a un conteo. **Dónde:** Gold episódico → Research mito e iconografía.

**Ejercicio estadístico (distinto del modelo):** IC binomial exacto para proporción sin árboles y contraste de tendencia por temporada.

**Datos necesarios:** TREE,TREES, GUEST,temporada, otras etiquetas; fuentes culturales que acrediten la asociación popular.

**Visualización que cuenta la evidencia:** Mosaico completo de 403 episodios y zoom en 36 contraejemplos del anfitrión con hover/focus.

**Estado:** `COUNT_VERIFIED_MODEL_NOT_RUN`. **Advertencia:** 36/381 sin árboles entre anfitrión, ya observado; modelo pendiente.

### BR-06 · ¿Eran accidentes felices o decisiones cuidadosamente preparadas?

*La espontaneidad televisiva puede coexistir con tres versiones de una obra.*

**Pregunta principal:** ¿Qué sabemos de la preparación real de los cuadros y qué parte de la aparente espontaneidad puede estudiarse con datos?

**Orden 1 — ¿Qué vemos?** Documentar testimonios sobre versiones de referencia, grabación y libros; describir repetición de motivos del CSV.

**Orden 2 — ¿Qué nos obliga a preguntar el primer hallazgo?** ¿Los cambios de combinaciones por temporada se explican por formato didáctico o por supuesta improvisación?

**Orden 3 — ¿Qué explicación rival, sesgo o mecanismo podría cambiar la conclusión?** ¿Qué corpus de obras y registros de producción permitiría comprobar las dos hipótesis rivales sin extrapolar del CSV?

**Modelo propuesto (M17):** Modelo de simulación Monte Carlo de escenarios de diseño/selección. **Por qué:** Muestra qué conclusiones dependerían de supuestos sobre versiones no observadas, sin afirmar haberlas medido. **Dónde:** Research de sensibilidad y datos faltantes; solo propuesto, depende de evidencia documental.

**Ejercicio estadístico (distinto del modelo):** Análisis de sensibilidad y límites de identificación para versiones no observadas; sin p-values ficticios.

**Datos necesarios:** Archivo original; entrevistas de producción y posible correspondencia entre tres versiones externas.

**Visualización que cuenta la evidencia:** Diagrama de versiones y matriz de evidencia disponible/ausente con simulaciones hipotéticas etiquetadas.

**Estado:** `BLOCKED_EXTERNAL_VERSIONS`. **Advertencia:** La preparación de tres versiones está documentada por NPR; el CSV no permite probar espontaneidad.

### BR-07 · ¿Qué combinaciones de paisajes sorprenden más de lo que sugieren las frecuencias?

*Dos elementos pueden aparecer juntos a menudo simplemente porque son comunes.*

**Pregunta principal:** ¿Cuáles son los pares/tríos de motivos que realmente exceden su coocurrencia esperada?

**Orden 1 — ¿Qué vemos?** Estimar tasas marginales y coocurrencias sobre los 381 episodios del anfitrión.

**Orden 2 — ¿Qué nos obliga a preguntar el primer hallazgo?** ¿Las asociaciones se concentran en temporadas o se mantienen entre épocas?

**Orden 3 — ¿Qué explicación rival, sesgo o mecanismo podría cambiar la conclusión?** ¿Se sostienen al controlar pruebas múltiples, etiquetas construidas por OR y frecuencias base?

**Modelo propuesto (M10):** Modelo log-lineal / reglas de asociación con baseline de independencia. **Por qué:** Separa popularidad marginal de asociación verdadera entre características. **Dónde:** Silver indicadores → Research asociaciones multivariadas.

**Ejercicio estadístico (distinto del modelo):** Fisher exacto por par y FDR, con lift e IC para asociaciones elegidas.

**Datos necesarios:** Matriz binaria de 12 familias, dependencia explícita SNOWY_MOUNTAIN.

**Visualización que cuenta la evidencia:** Heatmap de lift vs esperado con tooltips de episodios y anotación de asociaciones mecánicas.

**Estado:** `PLANNED_DATA_FEASIBLE`. **Advertencia:** No atribuir intención artística a coocurrencia.

### BR-08 · ¿Qué sucede con el paisaje cuando Bob cede el pincel?

*No todos los 403 episodios fueron pintados por la misma persona.*

**Pregunta principal:** ¿Cómo cambia el repertorio etiquetado entre los 381 episodios del anfitrión y los 22 invitados?

**Orden 1 — ¿Qué vemos?** Comparar prevalencias y patrones con n visibles, sin interpretar causalidad.

**Orden 2 — ¿Qué nos obliga a preguntar el primer hallazgo?** ¿Desaparecen diferencias al comparar dentro de temporadas con invitados?

**Orden 3 — ¿Qué explicación rival, sesgo o mecanismo podría cambiar la conclusión?** ¿Qué hipótesis alternativas —tema programado, invitado elegido, época, estilo— pueden distinguirse con metadatos adicionales?

**Modelo propuesto (M19):** Modelo multinivel regularizado por temporada. **Por qué:** Permite explorar diferencias controlando composición temporal sin sobreinterpretar n=22. **Dónde:** Gold episodio+GUEST → Research contraste grupos.

**Ejercicio estadístico (distinto del modelo):** Fisher exacto e intervalos para diferencia de proporciones (n pequeño).

**Datos necesarios:** GUEST,temporada,motivos, identidad invitado si se obtiene externa.

**Visualización que cuenta la evidencia:** Dumbbell de tasas y n por grupo + pequeño panel de temporadas con invitados.

**Estado:** `DESCRIPTIVE_VERIFIED_MODEL_NOT_RUN`. **Advertencia:** 345/381 anfitrión vs 16/22 invitados con árboles; solo descripción.

### BR-09 · ¿Descubre el algoritmo cuatro estilos, o solo cuatro salas arbitrarias?

*Un modelo puede producir grupos precisos aunque no correspondan a algo perceptible.*

**Pregunta principal:** ¿Qué perfiles de motivos aparecen al agrupar los episodios y qué significa realmente un grupo?

**Orden 1 — ¿Qué vemos?** Construir k-medoids Jaccard sobre doce familias y describir perfiles y medoids.

**Orden 2 — ¿Qué nos obliga a preguntar el primer hallazgo?** ¿Cuántos episodios cambian de grupo al modificar distancia, k o la etiqueta árbol?

**Orden 3 — ¿Qué explicación rival, sesgo o mecanismo podría cambiar la conclusión?** ¿Evaluadores humanos reconocerían los mismos estilos viendo obras con permisos, o solo etiquetamos por nuestra ontología?

**Modelo propuesto (M07):** K-medoids Jaccard frente a clustering aglomerativo y Euclídea. **Por qué:** Los medoids son episodios reales y las distancias se ajustan a indicadores binarios. **Dónde:** Gold motivos → Research clustering; UI hover/focus con representante.

**Ejercicio estadístico (distinto del modelo):** ARI entre particiones e intervalos bootstrap de estabilidad por grupo.

**Datos necesarios:** 12 familias de 381 episodios; obras reales solo derechos y mapping verificados.

**Visualización que cuenta la evidencia:** Alluvial de cambios de sala + medoids/episodios interactivos con preview sujeto a licencia.

**Estado:** `EXISTING_CLUSTERING_PARTIAL_MODEL_EXT_NOT_RUN`. **Advertencia:** k=4 es restricción didáctica; ARI no es calidad artística.

### BR-10 · ¿Cambió de paleta aunque sus paisajes parecieran los mismos?

*Una escena puede conservar árboles mientras sus colores y atmósfera evolucionan.*

**Pregunta principal:** ¿Se transformó el uso de colores por temporadas, incluso en motivos equivalentes?

**Orden 1 — ¿Qué vemos?** Conseguir paletas por episodio y evaluar cobertura del join 1:1.

**Orden 2 — ¿Qué nos obliga a preguntar el primer hallazgo?** Si hay una tendencia cromática, ¿persiste dentro de escenas con los mismos motivos?

**Orden 3 — ¿Qué explicación rival, sesgo o mecanismo podría cambiar la conclusión?** ¿Es una señal de práctica artística o un sesgo de materiales, catalogación o disponibilidad de imágenes?

**Modelo propuesto (M09):** Análisis de correspondencias múltiples para paletas categóricas. **Por qué:** Explora asociaciones latentes entre colores etiquetados y motivos sin confundirlas con estilo. **Dónde:** Enriched Gold (join validado) → Research paletas.

**Ejercicio estadístico (distinto del modelo):** Permutación para cambio de composición por era y corrección de multiplicidad.

**Datos necesarios:** Datos de paletas externos con licencia y claves temporada/episodio; CSV original no contiene colores.

**Visualización que cuenta la evidencia:** Río cromático temporal y tarjetas comparables de un mismo motivo.

**Estado:** `BLOCKED_EXTERNAL_PALETTES`. **Advertencia:** Sin join validado no es respondible con el CSV primario.

### BR-11 · ¿Y si los 403 episodios fueran solo la cara visible de su obra?

*El programa televisado no agota necesariamente las pinturas preparadas para él.*

**Pregunta principal:** ¿Qué se pierde al estudiar solo episodios emitidos cuando existían versiones de referencia, libros y obras preparadas no emitidas?

**Orden 1 — ¿Qué vemos?** Mapear el universo documentado y la cobertura real de cada fuente, sin sumar obras heterogéneas como filas equivalentes.

**Orden 2 — ¿Qué nos obliga a preguntar el primer hallazgo?** ¿Podría la selección de emisiones explicar el repertorio que percibimos?

**Orden 3 — ¿Qué explicación rival, sesgo o mecanismo podría cambiar la conclusión?** ¿Qué conclusiones cambiarían bajo escenarios plausibles de sesgo de selección, una vez observadas muestras adicionales autorizadas?

**Modelo propuesto (M17):** Simulación de sesgo de cobertura y escenarios límite. **Por qué:** Expone la incertidumbre sobre piezas ausentes sin inventar observaciones individuales. **Dónde:** Data quality / corpus audit → Research selección.

**Ejercicio estadístico (distinto del modelo):** Análisis de sensibilidad de prevalencias con límites superior/inferior bajo escenarios declarados.

**Datos necesarios:** 403 episodios, fuentes NPR sobre tres versiones, AP sobre siete obras temporada 32.

**Visualización que cuenta la evidencia:** Diagrama de conjuntos y capas de versiones con cobertura y huecos explícitos.

**Estado:** `BLOCKED_EXTERNAL_COVERAGE`. **Advertencia:** No tratar «3×403» como número probado de cuadros distintos ni siete obras como episodios.

### BR-12 · ¿Podemos diseñar un museo sin confundir organización con rentabilidad?

*La mejor sala depende de qué entiende el visitante, no solo de los cuatro clusters.*

**Pregunta principal:** ¿Qué distribución de episodios en cuatro salas hace más clara y equilibrada una experiencia hipotética?

**Orden 1 — ¿Qué vemos?** Comparar agrupamiento por reglas y por k-medoids según tamaño y diversidad de motivos.

**Orden 2 — ¿Qué nos obliga a preguntar el primer hallazgo?** ¿Qué salas se desequilibran al variar restricciones, k, prioridades o demanda hipotética?

**Orden 3 — ¿Qué explicación rival, sesgo o mecanismo podría cambiar la conclusión?** ¿Qué datos reales de visitantes, capacidad y costos harían falta para convertir la curaduría en decisión de negocio?

**Modelo propuesto (M21):** Optimización discreta/simulación de asignación con restricciones declaradas. **Por qué:** Distingue un problema de diseño operativo de una predicción de ingresos ausente del dataset. **Dónde:** Gold motivos → Simulation hypothetical.

**Ejercicio estadístico (distinto del modelo):** Monte Carlo de sensibilidad de tamaños y prueba de permutación de diferencia frente a asignación aleatoria.

**Datos necesarios:** 381 episodios anfitrión y escenarios explícitamente hipotéticos; costos no observados.

**Visualización que cuenta la evidencia:** Planos comparativos de salas y distribución con intervalos de simulación.

**Estado:** `PLAN_ONLY_BUSINESS_DATA_MISSING`. **Advertencia:** NO ROI, no ingresos sin datos.

### BR-13 · ¿Cuándo un modelo «mejor» empieza a responder la pregunta equivocada?

*Un score impresionante puede ser la firma de una fuga de información.*

**Pregunta principal:** ¿Cómo cambian calidad aparente y utilidad real al predecir motivos usando metadatos que no pertenecen al cuadro?

**Orden 1 — ¿Qué vemos?** Definir un target de motivo independiente y baseline por prevalencia; entrenar solo en fase posterior si se autoriza.

**Orden 2 — ¿Qué nos obliga a preguntar el primer hallazgo?** ¿Mejora el score si agregamos ID/temporada o proxies del target? ¿Es mejora espuria?

**Orden 3 — ¿Qué explicación rival, sesgo o mecanismo podría cambiar la conclusión?** ¿Persiste OOS con holdout temporal, bloqueo por temporada y evaluación con features permitidas? ¿Cómo cambia la interpretación del alumno?

**Modelo propuesto (M11):** Random Forest controlado y baseline logístico; tuning Optuna opcional M18 solo si aporta. **Por qué:** Permite ilustrar leakage y comparación honesta de modelos supervisados. **Dónde:** Research predictivo → plan de validación por temporadas.

**Ejercicio estadístico (distinto del modelo):** Test de permutación de performance OOS e intervalos por bootstrap de grupo.

**Datos necesarios:** 67 etiquetas originales, target definido SIN derivadas equivalentes, fechas si disponibles.

**Visualización que cuenta la evidencia:** Comparación de scores en validación ingenua vs temporal y muestra de fugas.

**Estado:** `PLAN_ONLY_PREVIOUS_REFERENCE_TO_VERIFY`. **Advertencia:** No entrenar, optimizar ni calcular métricas nuevas en el Paquete de Entrada.

### BR-14 · ¿Eran los paisajes una secuencia con memoria o una mezcla de motivos?

*La televisión tiene orden; la pintura no necesariamente tiene transiciones previsibles.*

**Pregunta principal:** ¿El motivo de un episodio ofrece información sobre el siguiente, más allá de la frecuencia base?

**Orden 1 — ¿Qué vemos?** Definir orden SxxExx con advertencia sobre diferencia entre grabación/emisión y medir transiciones de motivos.

**Orden 2 — ¿Qué nos obliga a preguntar el primer hallazgo?** Si hay dependencia secuencial, ¿se concentra en determinadas temporadas o desaparece al permutar el orden?

**Orden 3 — ¿Qué explicación rival, sesgo o mecanismo podría cambiar la conclusión?** ¿Es un fenómeno de programación televisiva, producción por lotes o una señal visual estable? ¿Qué fechas externas necesitamos?

**Modelo propuesto (M14):** Cadena de Markov de estados de motivos agregados, HMM opcional si datos lo permiten. **Por qué:** Investiga dependencia temporal sin requerir LSTM con 31 temporadas. **Dónde:** Research secuencias a partir de orden verificable.

**Ejercicio estadístico (distinto del modelo):** Permutación del orden dentro de temporada + intervalo para diferencias de transición vs prevalencia base.

**Datos necesarios:** IDs de episodios y familias, calendario de emisión para validar orden.

**Visualización que cuenta la evidencia:** Matriz de transición y recorrido episodio→episodio con contraste permutado.

**Estado:** `PLAN_ONLY_TEMPORAL_ORDER_TO_VALIDATE`. **Advertencia:** Evitar asumir que orden de emisión equivale a orden de creación.

## Mapeo de las rutas antiguas: NO mostrar dos bloques

| Ruta antigua | Integración correcta en esta lista |
|---|---|
| A · Museo | `BR-12` como un escenario operativo, sin monetización inventada |
| B · Social/invitados | `BR-08` como contraste descriptivo con incertidumbre y selección |
| C · Clustering | `BR-09` y `BR-13` (evaluación adversarial de métricas) |
| D1 · Árboles | `BR-05` como primer resultado, no historia completa |
| D2 · Montañas/nieve | `BR-02` como pieza del legado y codificación, no simple conteo |
| E · ID engañoso | `BR-13` como contraste leakage, validación y modelos |

Las nuevas preguntas sobre enfermedad (`BR-01`), historia (`BR-03`), atípicos multiescala (`BR-04`), espontaneidad (`BR-06`), combinaciones (`BR-07`), paleta (`BR-10`), obras excluidas (`BR-11`) y secuencias (`BR-14`) tienen la **misma jerarquía editorial** que las heredadas; nunca crear sección «2B».

## Prioridad científica por lotes, no de modelos entrenados

**Lote de diseño inicial:** BR-01 (biografía/salud), BR-03 (evolución), BR-04 (atípicos), BR-05 (mito) y BR-09 (clusters). La siguiente IA debe investigar fuentes y escoger rutas por factibilidad real. 

**Lote de ampliación:** BR-07 (coocurrencias), BR-08 (invitados), BR-13 (leakage), BR-14 (secuencia).

**Dependencias externas importantes:** BR-06, BR-10 y BR-11, además de la fecha clínica/producción de BR-01.

**Modelo LSTM, RL, Optuna, riesgo colectivo:** consultar `MODEL_SET.md` para condiciones de elegibilidad. No forzarlos en Bob Ross sin datos/target/reward suficientes; figurar como opciones futuras en otros episodios.

## Requisitos para el primer HTML
El apartado **02 / Las preguntas de esta investigación** será UNA SOLA sección integrada que incluya las 14 opciones, filtros o tarjetas por tema y detalles expandidos de O1/O2/O3 + modelo + estadística + visualización + faltantes. El prólogo debe narrar primero quién fue Bob Ross. El tema de enfermedad no puede quedar escondido en un detalle O3: `BR-01` es una investigación protagonista con advertencia de causalidad. La guía científica puede resumir técnicas, pero el banco estructurado es siempre `questions_master.json`.

**Gate:** Paquete de Entrada listo para revisión de preguntas; no guion/video hasta la aprobación explícita de `research_guide.html`.
