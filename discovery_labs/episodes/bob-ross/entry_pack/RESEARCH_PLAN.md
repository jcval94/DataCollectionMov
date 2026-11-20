# Plan de investigación — Bob Ross como una historia, no como una tabla

## Misión de descubrimiento y tres preguntas guía

**Objetivo:** descubrir insights increíbles por su originalidad y solidez científica sobre cada dataset; aquí, detectar estructuras, excepciones, transiciones o límites insospechados de los episodios de Bob Ross, sin construir una sorpresa ficticia ni confundir correlación y causa.

En cada experimento, pregunta, gráfico e insight documentar:

- **CÓMO:** CSV y versiones, filtros y denominadores, transformación, modelo, prueba estadística independiente, evaluación, controles y código reproducible.
- **POR QUÉ:** qué tensión científica o biográfica importa, por qué elegimos ese método y qué explicaciones rivales podrían producir el patrón.
- **PARA QUÉ:** qué cambia en nuestra interpretación y qué aprendizaje, decisión o siguiente investigación permite. No vender utilidad causal o económica que no pueda medirse.

Una ausencia de patrón, un hallazgo nulo o un sesgo de etiquetado pueden ser insights superiores a una visualización espectacular sin respaldo.

## Tesis editorial de trabajo (aún NO demostrada)
Bob Ross construyó durante más de una década un lenguaje visual y pedagógico reconocible. El dataset permite medir una parte: **motivos etiquetados por episodio**. La investigación debe explorar cómo se construyó, si evolucionó, dónde están sus excepciones y qué **no podemos** inferir sin otras fuentes.

El sujeto es **la historia documentada de Bob Ross y de su obra televisiva**. La unidad estadística del archivo es un episodio; no una pintura física, ni una audiencia, ni una fecha de ejecución del cuadro, ni un marcador de salud.

## Hipótesis históricas para investigar, sin resultados anticipados
1. **Evolución creativa:** entre S01 y S31 cambian combinaciones y diversidad de motivos; puede ser gradual o mostrar quiebres.
2. **Situación personal:** el diagnóstico de linfoma es un evento externo, cercano al cierre de la serie según fuentes biográficas. **No hay inferencia causal automática** y deben verificarse la fecha, el orden de grabación y explicaciones alternativas.
3. **Herencia de Alaska:** la relación con montañas/nieve es narrativa plausible; el CSV no trae el lugar real en que se inspira cada cuadro.
4. **Más allá del arquetipo:** hay 36 episodios del anfitrión sin TREE/TREES; estudiar quiénes son y por qué el arquetipo persiste.
5. **Obra no emitida:** existen siete pinturas preparadas para la temporada 32 (AP); no están necesariamente representadas en este CSV: una frontera de cobertura.
6. **Espontaneidad versus producción:** entrevistas cuentan que podía preparar tres versiones de un cuadro; el CSV no registra ensayos/guiones.

## Contrato de modelos y pruebas estadísticas (planeación antes de ejecutar)

**Cada una de las 14 preguntas canónicas** de `QUESTIONS_MASTER.md` debe incluir **al menos un modelo** y **un ejercicio estadístico diferente**, con qué, por qué, dónde, fuente, baseline, validación, riesgos y figura. La selección debe proceder de `discovery_labs/shared/model_catalog/MODEL_SET.md` (24 familias). No se entrena ninguno en este Paquete de Entrada. El HTML de Fase 1 muestra un bloque único de preguntas; las seis anteriores son subejercicios, no una sección «2B».

## Etapas de investigación y HTML incremental (Fase 0 → Fase 1)

Las **14 investigaciones** se conservan como un único banco canónico; los diseños O2/O3 continúan en JSON/Markdown con `CONDICIONAL`, **no son preguntas activas ni resultados en el HTML inicial**. Concentrar ejecución profunda en 3–5 arcos seleccionados, sin forzar las 14.

| Etapa | Trabajo y dependencia | Entrega/puerta |
|---|---|---|
| 0. Verificar origen | Hash y 403×69, nulos, invitados, etiquetas, unit of analysis | `DATACHECKED` |
| 1. Contexto temprano | **DR-01** biografía y salud con controversias; **DR-02** cronología/grabación/datos; **DR-03** antecedentes/mitos priorizados | Registro de hechos e incertidumbres; `CONTEXT_REVIEWED` |
| 2. HTML científico **v0** | Abrir `research_guide.html` con **un párrafo general contextual al principio**, propósito CÓMO/POR QUÉ/PARA QUÉ, estructura e índice único de **O1**; sin O2/O3 públicas ni hallazgos nuevos imaginados | `O1_PLAN_VISIBLE`; artefacto no aprobado |
| 3. Medir O1 | EDA y métodos reproducibles sobre todo el dataset, denominadores, incertidumbre, hipótesis nulas, baselines y control de invitados | Evidencias, CSV/JSON/versiones, `O1_ANSWERED` por pregunta |
| 4. Síntesis crítica intermedia | **DR-05a** contrasta DR-01/02/03 con **resultados O1 realmente medidos** y autoriza o bloquea ramas O2. No exige DR-04 aún | `O2_ACTIVATION_REVIEWED` y lista de gatillos observados |
| 5. Investigación adaptativa | Publicar O2 válidas **solo después del paso 4**, ejecutarlas; a partir de su resultado, agregar O3 únicamente si existe hipótesis rival investigable; mostrar resultados nulos también | `O2_ANSWERED` / `O3_TRIGGERED` / `BLOCKED` por pregunta |
| 6. Evidencia visual | **DR-04** se profundiza según insights efectivamente seleccionados, figuras adversariales, derechos, explorer y QA; **triage mínimo de licencias desde la etapa 1** | `VISUAL_REVIEWED` |
| 7. Cierre adversarial | **DR-05b** reconcilia nuevas fuentes, O1/O2/O3, robustez, contradicciones y límites; actualiza guía y cambios versionados | `RESEARCH_REPRODUCIBLE` / `FINAL_SYNTHESIS_REVIEWED` |
| 8. QA y versión | Revisión HTML móvil/teclado, sources→métricas→figuras, reproducibilidad, criterio docente; solicitar aprobación del commit específico | `HUMAN_APPROVAL_PENDING` |

### Human Feedback — hitos de decisión con informes HTML

El protocolo vigente está en [HUMAN_FEEDBACK_CHECKPOINTS.md](HUMAN_FEEDBACK_CHECKPOINTS.md), basado en las plantillas y schema compartidos de `discovery_labs/shared/templates/HUMAN_FEEDBACK_*`.

| Hito del plan anterior | Feedback humano y artefacto | Límite |
|---|---|---|
| Tras etapas **0–1** de calidad, fuentes y priorización (antes de 2–3) | **HF-00** Brújula: calidad del dataset, matriz de fuentes, preguntas top y decisión de 3–5 O1 | Diagramas de cobertura, **no resultados ficticios** |
| Tras etapa **3**, 1–2 O1 realmente ejecutadas | **HF-01** Descubrimientos: efectos nulos o sorpresa con baselines, permutación o sensibilidad | Mostrar evidencia y contradicción |
| Tras etapa **4** (DR-05a) y antes de promover etapa 5 | **HF-02** Decisión O2: rutas activables con trigger, coste y rival | **Gate humano para prioridades O2** |
| Tras etapa **5**, DR-04 etapa 6, antes de DR-05b | **HF-03** Robustez: sensibilidad de O2/O3 y visualizaciones basadas en hallazgos | No presentar hipótesis bloqueadas como completadas |
| Tras etapas **7–8** antes de storytelling | **HF-04** Aprobación científica: guías y figures QA, decisiones y resultados finales | **`RESEARCH_APPROVED:<commit>` obligatorio** |

Cada hito publica un `human_feedback/HF-XX/vNN/report.html` que inicia con **resumen ejecutivo** (qué aprendimos, cambio sobre checkpoint anterior, sorpresa sustentada, recomendación y bloqueo), seguido por 2–4 **buenas gráficas** si hay datos; comparaciones, incertidumbre, baseline, figura adversarial, fuentes, n, denominadores, código y derechos. Preguntar al usuario **máximo tres cosas** que afecten decisiones, mostrando opción recomendada y el coste de posponer. Guardar `feedback.md` y `checkpoint.json` y no inferir aprobación.

**Condición de publicación:** una O2 exige `DR_01_02_03_DONE + O1_ANSWERED + DR_05a_REVIEWED`, o una excepción justificada y explícita cuando el contexto de la pregunta no requiera uno de los frentes. Una O3 exige `O2_ANSWERED + RIVAL_CHECK_DEFINED`. Guardar ID padre, condición realmente observada, evidencia vinculada, estado y versión. **Los diseños O2/O3 no se borran** del paquete; simplemente permanecen internos y no se anticipan al lector.

**Versión científica viva:** cada avance del HTML incluye `guide_version`, `question_id`, `order`, `parent_id`, `trigger_evidence`, `claim_refs`, `analysis_artifact`, `status`, `updated_at` y `change_reason`. Corregir resultados con historial y sin simular continuidad. El archivo HTML V3 existente es una **instantánea preliminar estática**: su siguiente revisión deberá ajustar la exposición progresiva de O2/O3 y la estructura. **No se modifica ni aprueba el HTML en esta fase de documentación.**

## Métodos por tema
- **Trayectorias:** tasa de cada motivo por temporada, intervalos o bandas, small multiples, cambios observados con contraste contra modelo suave, sensibilidad a invitados y complejidad de etiquetas.
- **Cortes temporales:** usar temporada como ordinal; fechas de grabación/emisión solo si se consiguen y califican. No superponer «diagnóstico» sobre el episodio que lo sucede por índice.
- **Atípicos multiescala:** rareza por combinación frente a frecuencia base, tamaños de grupo, especificación de métrica y bootstrap por temporada; escalar episodio → temporada → era. Contrastar efectos espurios por denominadores pequeños.
- **Combinaciones:** lift y coocurrencias frente a esperados, corregir pruebas múltiples, separar dependencias constructivas como SNOWY_MOUNTAIN.
- **Clustering:** comparar con el KMeans ya existente y el k-medoids Jaccard; ARI, tamaño, medoids, estabilidad y asignaciones. Nunca «cuatro estilos verdaderos» sin evaluación externa.
- **Cultura e historia:** triangulación narrativa de por lo menos dos fuentes independientes, diferencias entre biografía y dataset, registrar versiones y contradicciones.
- **Causalidad salud-estilo:** describir hechos verificables y posibles cambios, sin atribución causal si no existen mediciones temporales y controles sólidos.

## Guía de prioridad
**Lote A:** evolución + outliers jerárquicos + mito de árboles (entradas narrativas accesibles). **Lote B:** clustering + paleta/imagen (necesita enriquecimiento, derechos y revisiones). **Lote C:** asociación biográfica y lagunas de cobertura (requiere varias fuentes externas).

Una buena pregunta queda **bloqueada honestamente** si no alcanza evidencia; eso es una lección, no un fracaso.

## Cómo debe verse el documento HTML de Fase 1

**Párrafo inicial orientativo (contexto, no resultado):**

> Entre 1983 y 1994, *The Joy of Painting* convirtió la pintura de paisajes en una experiencia televisiva accesible. El archivo de FiveThirtyEight reúne etiquetas de motivos para 403 episodios, pero no fotografías, fechas precisas de grabación ni información clínica. Este laboratorio investiga qué patrones y excepciones podemos encontrar en esas etiquetas, si cambian entre temporadas y qué historias sobre Bob Ross requieren fuentes externas. Partimos de preguntas abiertas, distinguimos lo que podemos medir de lo que no y permitimos que cada resultado determine la siguiente investigación.

**Estructura fija y ampliable del HTML**, sin convertir el documento en dos bancos de preguntas:

1. **Contexto general**: párrafo de apertura, quién era Bob Ross, cronología documentada y precauciones.
2. **Misión CÓMO / POR QUÉ / PARA QUÉ**: qué insight innovador perseguimos, por qué podría importar y cómo lo refutaríamos.
3. **El dataset y su frontera**: 403 episodios, unidad, fuentes, derechos, huéspedes, eventos externos sin fecha fiable.
4. **Índice único de investigaciones y O1**: 14 candidatas iniciales, priorización, hipótesis, modelos y tests planificados; O2/O3 permanecen internos hasta tener gatillos medidos.
5. **Resultados acumulativos O1**: métodos, visualizaciones, incertidumbre, explicaciones rivales y estado de cada pregunta.
6. **Nuevas O2 y O3 activadas**: se agrega esta parte dentro del **mismo bloque editorial** **después** de responder O1, cotejar Deep Research y obtener resultados O2; toda rama referencia su padre y evidencia.
7. **Insights, contraargumentos y utilidad**: cada hallazgo responde Cómo/Por qué/Para qué con límites, nulos y alternativas, sin exagerar causalidad.
8. **Reproducibilidad, bitácora y aprobación**: hashes, scripts, fuentes, versiones, dudas pendientes y aprobación humana explícita.

El HTML **debe cambiar a medida que progrese la investigación**; no presentar desde v0 una conclusión final ni mostrar rutas condicionales como preguntas ya nacidas. Diferenciar `PLANNED`, `BLOCKED`, `VERIFIED`, `REFUTED`, `INCONCLUSIVE` y `APPROVED`.

## Definición de éxito visual
Una figura debe cambiar cómo entendemos algo: mostrar antes/después o grupo/composición; comparar absoluto/porcentaje; mostrar incertidumbre; permitir inspección individual y regreso al agregado. Toda interacción debe ser accesible vía teclado y focus, funcionar con fallback offline y nunca ofrecer una pintura como imagen integrada sin derechos verificados.

## Puertas de aprobación
- [ ] Investigación de contexto citada, fechas y afirmaciones conciliadas.
- [ ] Al menos tres arcos O1→O2→O3 revisados y ejecutados donde haya dato disponible (o marcados bloqueados).
- [ ] QA de datos y figures calculadas desde snapshots versionados.
- [ ] Explicaciones rivales, robustez, incertidumbre y categorías claras.
- [ ] Licencias de imágenes/hotlink verificados; fallback gráfico sin retratos ni pinturas.
- [ ] HTML narrativo/técnico con pruebas mobile, scroll, hover/focus/teclado y lectura accesible.
- [ ] Documento firmado por el usuario: `RESEARCH_APPROVED:<commit>`.

Solo al pasar **todas** las puertas necesarias y contar con aprobación humana puede arrancar el storytelling audiovisual.
