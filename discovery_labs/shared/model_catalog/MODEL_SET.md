# Model Set — catálogo científico compartido (24 familias)

**Fuente canónica:** `discovery_labs/shared/model_catalog/MODEL_SET.md`. Este catálogo pertenece a AI Discovery Labs, no a un episodio. Es un repertorio para **planear** métodos, no una autorización para entrenar. La selección debe responder una pregunta y cumplir el contrato de Question Forge.

Por cada pregunta principal: **al menos un modelo razonado más un ejercicio estadístico formal diferente**, con qué/por qué/dónde, datos disponibles, variable objetivo (si aplica), baseline, split, validación, complejidad, riesgo de leakage y una visualización evidencia. El uso de modelos complejos sin condiciones mínimas se rechaza.

El catálogo contiene variantes clásicas, supervisadas, no supervisadas, causales, temporales y simulación. **LSTM, RL, Optuna o riesgo colectivo no son automáticamente pertinentes**: exigir target, longitud de secuencia, señal, recompensa, datos de pérdidas o estructura experimental, según corresponda.

## Catálogo de familias

| ID | Modelo / familia | Qué investiga y cuándo conviene | Ejercicio estadístico obligatorio complementario | Ubicación en pipeline | Validación y límites |
|---|---|---|---|---|---|
| M01 | Regresión logística / GLM binomial | Prevalencia de un evento binario según tiempo, grupo o covariables | Tendencia binomial con IC 95%, test de coeficiente, efecto por unidad de periodo | Gold episódico → Research temporal | Evitar autocorrelación y pseudoindependencia; bootstrap por grupo o periodo pertinente |
| M02 | GAM binomial con spline penalizado | Cambios no lineales de prevalencias sin imponer un quiebre | Test comparativo suave vs lineal, IC y sensibilidad por nº de knots | Gold temporal → Research | Pocas periodos: regularizar y no sobreajustar |
| M03 | Detección de cambios (piecewise GLM / PELT con restricciones) | Identificar épocas con patrones diferentes | Test de cambio con permutación/bootstrap por bloques; penalizar selección de punto | Periodos ordenados → Research | No convertir orden de registro en fecha de intervención; controlar búsqueda múltiple |
| M04 | Modelo jerárquico beta-binomial | Tasas por periodos o segmentos con tamaños pequeños y shrinkage | Intervalos posterior/predictivo; comparación con tasas brutas | Gold observación-periodo → Research | Prior documentado; no afirmar «segmento anómalo» sin incertidumbre |
| M05 | Isolation Forest | Observaciones raras en variables numéricas o binarias multidimensionales | Prueba de rareza contra distribución nula y sensibilidad a contaminación | Gold a nivel de observación → Research anomalías | No valida importancia sustantiva; comparar con Hamming/Jaccard |
| M06 | LOF / distancia Jaccard y ranking de rareza | Vecinos atípicos dentro de categorías raras | Bootstrap/permutación de ranking por observación y season | Gold a nivel de observación → Research anomalías | Sensible a densidad; no borrar observaciones atípicas |
| M07 | K-medoids Jaccard | Agrupar perfiles binarios con representante real por sala | Silhouette dentro de la misma métrica, estabilidad bootstrap y ARI | Gold 12 familias → Research clusters | k elegido no demuestra estilos naturales |
| M08 | Clustering aglomerativo / HDBSCAN con distancias apropiadas | Estructuras alternativas, grupos desequilibrados o ruido | Test de estabilidad / coasignación por remuestreo | Gold 12 familias → Research clusters | HDBSCAN puede dejar muchos no asignados con n pequeño |
| M09 | Análisis de correspondencias múltiples (MCA) | Sintetizar coocurrencia de indicadores categóricos y ejes latentes | Permutación de inercia / sensibilidad a etiquetas correlacionadas | Silver etiquetas → Research & Visual | Embedding no demuestra dimensiones estéticas reales |
| M10 | Reglas de asociación / log-lineal binomial | Pares y tríos de motivos sobre/infrarepresentados | Fisher exacto, lift vs independencia, FDR Benjamini–Hochberg | Silver atributos → Research relaciones | Categorías derivadas solapadas pueden inducir dependencia; pre-especificar pares |
| M11 | Random Forest / Gradient Boosting supervisado | Predicción de una etiqueta válida con otros atributos predictivos | Baseline prevalencia, IC bootstrap de rendimiento, prueba de permutación | Gold + definición de target → Research predictivo | Excluir features derivados del target; validación según tiempo/entidad/grupo; cuidar clases minoritarias |
| M12 | Regresión regularizada L1/L2/Elastic Net | Predicción interpretable / selección de motivos asociados | Test por permutación de performance, estabilidad de coeficientes | Gold a nivel de observación → Research | Evitar leakage y selección post-hoc presentada como confirmatoria |
| M13 | Naive Bayes / modelo de clasificación de baselines | Demostrar importancia del baseline y supuestos de independencia | Test de bondad/calibración, confiabilidad y comparación con mayoría | Gold a nivel de observación → Research | Dependencia entre motivos invalida interpretaciones ingenuas |
| M14 | HMM / cadena de Markov | Evolución de estados latentes si hay secuencia temporal válida y suficientes observaciones | Matriz de transición, permutación de orden temporal, IC | Secuencia episódica/series → Research | Criterio temporal debe validarse; periodos ≠ fechas precisas |
| M15 | Modelos de series temporales clásicos (ARIMA/GLM estado-espacio) | Predecir series densas de categorías o frecuencias con origen temporal fiable | Diagnósticos de autocorrelación, Ljung–Box, intervalos y backtesting temporal | Gold temporal → Research | 31 periodos agregadas son poquísimas para claims predictivos |
| M16 | LSTM/transformers de secuencia | Alternativa AVANZADA solo con series largas adicionales, tarea definida y baseline mejorado | Comparación OOS con naive/ARIMA, IC y ablation | Datos externos ampliados → Experimental research | **No recomendado con pocas secuencias o muestras pequeñas**; coste/overfit |
| M17 | Monte Carlo / bootstrap por grupos | Propagar incertidumbre, simular procesos con parámetros declarados o asignaciones hipotéticas | IC por remuestreo, robustez de ranking y distribución de resultados | Gold + supuestos → Research | Separar simulación hipotética de datos observados |
| M18 | Optuna / búsqueda de hiperparámetros con CV anidada | Ajustar modelos SUPERVISADOS cuando hay target válido y n suficiente | Comparación OOS, test de diferencia y rango de métricas | Research tuning, nunca antes de split | Evitar fuga CV y optimización sobre test; tuning no es ciencia por sí solo |
| M19 | Regresión multinivel / modelos mixtos | Contrastar grupos/categorías mientras modelas efectos agrupados | IC para contrastes de grupo y sensibilidad a heterogeneidad | Gold observación/grupo → Research | Grupos pequeños limitan precisión; no inferir efectos causales por contraste observacional |
| M20 | Análisis causal (DID, serie interrumpida, synthetic control) | Efecto de intervención externa **SOLO si hay fecha, comparador, supuestos verificables** | Pre-trends, placebo, sensibilidad a confusores y calendario | Gold + contexto externo → Research causal | **No estimar efecto de enfermedad** por usar fecha tentativa; bloqueado |
| M21 | Simulación discreta / optimización restringida | Optimizar asignaciones hipotéticas bajo restricciones declaradas de capacidad o presupuesto | Sensibilidad de parámetros y distribución Monte Carlo de resultados | Gold + parámetros hipotéticos → Applied simulation | No estimar resultados económicos sin variables de ingreso, costes y demanda |
| M22 | Riesgo colectivo (frecuencia × severidad, Poisson-Gamma) | Para datos futuros con eventos y pérdidas/impacto; escenarios de riesgo | Bondad de ajuste, dispersion, IC para VaR/TVaR | Future data con eventos y severidades → Research | **No aplicable al CSV actual sin eventos/pérdidas** |
| M23 | Aprendizaje por refuerzo / bandits | Para futuras decisiones repetidas con acciones, reward e interacción/simulador | Evaluación off-policy, intervalos, baseline aleatorio | Future simulador/entorno → Research | **No aplicable a observacións estáticos sin reward** |
| M24 | Bondad de ajuste / modelos de generación binaria | ¿Se ajusta una distribución paramétrica a los datos observados? | Chi-cuadrada con celdas suficientes, G-test, bootstrap paramétrico | Silver validado → Research | Tablas dispersas: preferir exacto/permutación y modelar dependencia |

## Mapeo por tipo de problema (genérico)

| Necesidad | Familias candidatas | Prueba o ejercicio separado | Riesgo principal |
|---|---|---|---|
| Evolución en el tiempo | M01–M04, M15 | Tendencia, intervalos, permutación por periodo | Orden temporal incorrecto, múltiples quiebres |
| Rarezas y casos extremos | M05–M06, M17 | Bootstrap de ranking, null model, sensibilidad a umbrales | Interpretar rareza como error o mérito |
| Grupos y estructura | M07–M09 | Estabilidad de asignaciones, ARI, validación externa | Imponer etiquetas naturales a grupos arbitrarios |
| Dependencia entre atributos | M10, M24 | Fisher, FDR, bondad de ajuste | Coocurrencia inducida por definición |
| Predicción supervisada | M11–M13, M18 | Baseline, CV/OOS, permutación y calibración | Leakage, selección de target |
| Series y estados | M14–M16 | Diagnóstico temporal, backtesting, ablation | Series insuficientes o mal ordenadas |
| Heterogeneidad y grupos | M19 | Intervalos por grupo y sensibilidad | Confusión y tamaños pequeños |
| Causalidad hipotética | M20 | Placebos, pretrends, sensibilidad a confusores | No identificabilidad |
| Decisiones y riesgo | M21–M23 | Sensibilidad de supuestos, simulación, evaluación off-policy | Faltan reward, costos, severidad o entorno |

## Ficha obligatoria del plan de modelo

En `questions_master.json`, para cada investigación almacenar: `model_primary_id`, `model_why`, `model_where`, `model_data`, `model_baseline`, `statistical_exercise`, `test_or_interval`, `validation`, `visual`, `feasibility`, `blocked_reason` (o equivalentes semánticos con esquema versionado). El ejercicio estadístico debe tratar una duda adicional o cuantificar incertidumbre, no repetir el mismo nombre del modelo.

Una propuesta bloqueada puede permanecer en el paquete como hipótesis externa, pero debe haber una opción viable con el dato actual cuando la pregunta se presente como realizable. Ninguna técnica se declara ejecutada por figurar en este catálogo.

## Estados

`PLAN_ONLY`, `DATA_FEASIBLE`, `BLOCKED_MISSING_TARGET`, `BLOCKED_TIMEBASE`, `BLOCKED_REWARD`, `EXECUTED`, `REVIEWED`, `APPROVED` (los tres últimos requieren evidencia real y autorización apropiada).

**Gobernanza:** Paquete de entrada → Guía científica HTML y aprobación → Storytelling audiovisual HTML y aprobación → video. No usar el catálogo para disparar entrenamientos en fase de planeación.
