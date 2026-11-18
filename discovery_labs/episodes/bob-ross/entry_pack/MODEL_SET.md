# Model Set v1 — menú razonado de modelos + ejercicios estadísticos

**Propósito:** ofrecer a Question Forge un repertorio **transferible** que permita seleccionar, para CADA pregunta principal, **al menos un modelo concreto y un ejercicio estadístico distinto**, indicar qué responde cada uno, cuándo usarlo, dónde situarlo en el pipeline, cómo validarlo y por qué descartarlo. **Este archivo no ejecuta ni entrena modelos.**

## Selección antes de sofisticación

Los modelos no se agregan para «demostrar IA», sino para ayudar a investigar una hipótesis. Se propone un baseline interpretable, un modelo adecuado y un ejercicio estadístico independiente. El autor debe especificar: datos necesarios, n efectivo, target, features admisibles, métrica, split, riesgos, coste, figura, lugar de ejecución y alternativa en caso de no viabilidad.

**Restricciones Bob Ross:** 403 episodios (381 del anfitrión, 22 invitados), 31 temporadas, 67 indicadores binarios originales, 12 familias derivadas. No hay outcome clínico, preferencias de audiencia ni fecha exacta de grabación; la unidad no son pinturas físicas. 31 temporadas **no** constituyen una serie larga para deep learning. La enfermedad es contexto histórico: una coincidencia temporal no prueba efecto. El número de episodio, temporada y títulos no son rasgos pictóricos para clustering.

## Catálogo de familias

| ID | Modelo / familia | Qué investiga y cuándo conviene | Ejercicio estadístico obligatorio complementario | Ubicación en pipeline | Validación y límites |
|---|---|---|---|---|---|
| M01 | Regresión logística / GLM binomial | Prevalencia de TREE/TREES u otro motivo según temporada y covariables | Tendencia binomial con IC 95%, test de coeficiente, efecto por unidad de temporada | Gold episódico → Research temporal | Evitar autocorrelación y pseudoindependencia; bootstrap por temporada |
| M02 | GAM binomial con spline penalizado | Cambios no lineales de prevalencias sin imponer un quiebre | Test comparativo suave vs lineal, IC y sensibilidad por nº de knots | Gold temporal → Research | Pocas temporadas: regularizar y no sobreajustar |
| M03 | Detección de cambios (piecewise GLM / PELT con restricciones) | Identificar épocas con patrones diferentes | Test de cambio con permutación/bootstrap por bloques; penalizar selección de punto | Temporadas ordenadas → Research | No confundir estación con fecha de diagnóstico; controlar búsqueda múltiple |
| M04 | Modelo jerárquico beta-binomial | Tasas por temporada con tamaños pequeños y shrinkage | Intervalos posterior/predictivo; comparación con tasas brutas | Gold episodio-temporada → Research | Prior documentado; no afirmar «temporada anómala» sin incertidumbre |
| M05 | Isolation Forest | Episodios raros en motivos binarios multidimensionales | Prueba de rareza contra distribución nula y sensibilidad a contaminación | Gold episodios → Research anomalías | No valida importancia artística; comparar con Hamming/Jaccard |
| M06 | LOF / distancia Jaccard y ranking de rareza | Vecinos atípicos dentro de categorías raras | Bootstrap/permutación de ranking por episodio y season | Gold episodios → Research anomalías | Sensible a densidad; no borrar observaciones atípicas |
| M07 | K-medoids Jaccard | Agrupar perfiles binarios con representante real por sala | Silhouette dentro de la misma métrica, estabilidad bootstrap y ARI | Gold 12 familias → Research clusters | k elegido no demuestra estilos naturales |
| M08 | Clustering aglomerativo / HDBSCAN con distancias apropiadas | Estructuras alternativas, grupos desequilibrados o ruido | Test de estabilidad / coasignación por remuestreo | Gold 12 familias → Research clusters | HDBSCAN puede dejar muchos no asignados con n pequeño |
| M09 | Análisis de correspondencias múltiples (MCA) | Sintetizar coocurrencia de indicadores categóricos y ejes latentes | Permutación de inercia / sensibilidad a etiquetas correlacionadas | Silver etiquetas → Research & Visual | Embedding no demuestra dimensiones estéticas reales |
| M10 | Reglas de asociación / log-lineal binomial | Pares y tríos de motivos sobre/infrarepresentados | Fisher exacto, lift vs independencia, FDR Benjamini–Hochberg | Silver motivos → Research relaciones | SNOWY_MOUNTAIN induce dependencia; pre-especificar pares |
| M11 | Random Forest / Gradient Boosting supervisado | Predicción de motivo o invitado con otras etiquetas, si target tiene sentido | Baseline prevalencia, IC bootstrap de rendimiento, prueba de permutación | Gold + definición target → Research predictivo | Excluir features derivados del target; validación por temporada; n invitado=22 |
| M12 | Regresión regularizada L1/L2/Elastic Net | Predicción interpretable / selección de motivos asociados | Test por permutación de performance, estabilidad de coeficientes | Gold episodios → Research | Evitar leakage y selección post-hoc presentada como confirmatoria |
| M13 | Naive Bayes / modelo de clasificación de baselines | Demostrar importancia del baseline y supuestos de independencia | Test de bondad/calibración, confiabilidad y comparación con mayoría | Gold episodios → Research | Dependencia entre motivos invalida interpretaciones ingenuas |
| M14 | HMM / cadena de Markov | Evolución de estados latentes si hay secuencia temporal válida y suficientes observaciones | Matriz de transición, permutación de orden temporal, IC | Secuencia episódica/series → Research | Criterio temporal debe validarse; temporadas ≠ fechas precisas |
| M15 | Modelos de series temporales clásicos (ARIMA/GLM estado-espacio) | Predecir series densas de categorías o frecuencias con origen temporal fiable | Diagnósticos de autocorrelación, Ljung–Box, intervalos y backtesting temporal | Gold temporal → Research | 31 temporadas agregadas son poquísimas para claims predictivos |
| M16 | LSTM/transformers de secuencia | Alternativa AVANZADA solo con series largas adicionales, tarea definida y baseline mejorado | Comparación OOS con naive/ARIMA, IC y ablation | Datos externos ampliados → Experimental research | **NO recomendado para Bob Ross 403×67**; coste/overfit |
| M17 | Monte Carlo / bootstrap por grupos | Propagar incertidumbre, simular orden de eventos o asignaciones del museo ficticio | IC por remuestreo, robustez de ranking y distribución de resultados | Gold + supuestos → Research | Separar simulación hipotética de datos observados |
| M18 | Optuna / búsqueda de hiperparámetros con CV anidada | Ajustar modelos SUPERVISADOS cuando hay target válido y n suficiente | Comparación OOS, test de diferencia y rango de métricas | Research tuning, nunca antes de split | Evitar fuga CV y optimización sobre test; tuning no es ciencia por sí solo |
| M19 | Regresión multinivel / modelos mixtos | Contrastar temporadas e invitados mientras modelas agrupación | IC para efecto de GUEST y sensibilidad por temporada | Gold episodio/grupo → Research | 22 invitados limitan precisión; no inferir «impacto social» causal |
| M20 | Análisis causal (DID, serie interrumpida, synthetic control) | Efecto de intervención externa **SOLO si hay fecha, comparador, supuestos verificables** | Pre-trends, placebo, sensibilidad a confusores y calendario | Gold + contexto externo → Research causal | **No estimar efecto de enfermedad** por usar fecha tentativa; bloqueado |
| M21 | Simulación discreta / optimización restringida | Repartir un museo hipotético en salas con restricciones de capacidad declaradas | Sensibilidad de parámetros y distribución Monte Carlo de resultados | Gold + parámetros hipotéticos → Applied simulation | No calcular ingresos sin precio, visitas ni costos |
| M22 | Riesgo colectivo (frecuencia × severidad, Poisson-Gamma) | Para datos futuros con eventos y pérdidas/impacto; escenarios de riesgo | Bondad de ajuste, dispersion, IC para VaR/TVaR | Future data con eventos y severidades → Research | **No aplicable al CSV actual sin eventos/pérdidas** |
| M23 | Aprendizaje por refuerzo / bandits | Para futuras decisiones repetidas con acciones, reward e interacción/simulador | Evaluación off-policy, intervalos, baseline aleatorio | Future simulador/entorno → Research | **No aplicable a episodios estáticos sin reward** |
| M24 | Bondad de ajuste / modelos de generación binaria | ¿Se ajusta una distribución simple al patrón de motivos? | Chi-cuadrada con celdas suficientes, G-test, bootstrap paramétrico | Silver binario → Research | Tablas dispersas: preferir exacto/permutación y modelar dependencia |

## Mapear métodos a las preguntas (sin entrenar)

- **Historia/evolución:** M01 + IC/test de tendencia, M02/M03 si se justifica; temporal ordinal.
- **Hipótesis de salud:** M03 solo para cambios descriptivos con fechas verificadas; M20 **bloqueado**, no atribución clínica.
- **Outliers:** M05 + bootstrap/ranking robusto; comparar rareza episodio/temporada/era.
- **Mitos:** M01 o M12 y test binomial/intervalos, más grupos y variantes de definición.
- **Coocurrencia:** M10 + Fisher/FDR y contraste contra base-rate; diagramas de lift.
- **Clustering:** M07/M08 + estabilidad por bootstrap/ARI, más panel de representantes.
- **Invitados:** M19 + test exacto de Fisher e IC con n=22; no causal.
- **Paleta externa:** M09/M12 + pruebas de distribución/color solo tras join y permiso.
- **Cobertura:** M17 (escenarios de sensibilidad) + análisis de selección/missingness, sin inventar datos de pinturas ocultas.
- **Museo ficticio:** M21 + simulaciones de balance/redistribución, indicando hipótesis.

## Contrato por pregunta

Cada pregunta del banco debe tener exactamente estos campos de **plan**, aunque ninguna técnica esté ejecutada:
`model_primary_id`, `model_why`, `model_where`, `model_data`, `model_baseline`, `statistical_exercise`, `test_or_interval`, `visual`, `validation`, `feasibility`, `blocked_reason`.

Como mínimo **1 modelo propuesto + 1 ejercicio estadístico** por pregunta. Si el dataset no permite aplicar el modelo relevante, se etiqueta `BLOCKED_EXTERNAL_DATA` y se propone un modelo viable alternativa sin fingir resultados. No obligar LSTM/RL/CV+Optuna o riesgo colectivo para cumplir una cuota.

## Pasos posteriores y puertas de evaluación

Esta fase es **PLANEACIÓN**, no entrenamiento. Más adelante: reproducir baseline → verificar supuestos y pruebas → entrenar modelo si aporta valor → evaluar OOS/robustez → narrativa científica → aprobación humana. Los resultados de modelos no autorizan inferencias causales por sí solos.

**Prohibido** ejecutar entrenamientos, tuneo, inferencias, caches nuevos o scraping de imágenes a partir de esta lista sin encargo explícito. Solo se crean diseños evaluables para el Paquete de Entrada y la Guía Científica Fase 1.
