---
name: question-forge
description: Diseña un único banco de preguntas de investigación memorables, con contexto externo, niveles O1/O2/O3 y, para CADA pregunta, al menos un modelo y una prueba estadística planificados. Funciona con cualquier dataset y exige paquete de entrada y aprobación de la guía científica.
version: 2.1.0
---
# Question Forge — habilidad reusable de preguntas científicas y narrativas

## Misión: descubrir insights extraordinarios, nuevos y verificables

**Objetivo central de AI Discovery Labs:** descubrir en **cada dataset** insights sorprendentes, útiles e innovadores que una lectura superficial no revelaría. Innovar significa formular una hipótesis no obvia, contrastarla y explicar sus implicaciones; **no** exagerar, prometer un hallazgo espectacular o inventar patrones cuando los datos no lo sostienen. También son descubrimientos valiosos refutar una intuición popular, reconocer un sesgo, demostrar ausencia de evidencia o encontrar una variable/fuente que cambie la interpretación.

**Contrato CÓMO · POR QUÉ · PARA QUÉ, obligatorio en el episodio, cada investigación y cada hallazgo publicado:**

- **CÓMO:** de dónde salen los datos, qué transformación/segmentación se hace, qué modelo y **ejercicio estadístico independiente** se usan, supuestos, denominador, baseline, validación, incertidumbre y cómo reproducirlo.
- **POR QUÉ:** qué tensión, mecanismo, excepción o hipótesis rival hace importante la pregunta; por qué el método es apropiado y por qué el patrón observado merece atención. Diferenciar explicación sustentada de simple correlación.
- **PARA QUÉ:** qué cambia en nuestra comprensión, qué decisión o siguiente experimento permite, qué límite revela y para quién resulta útil. Si no hay aplicación directa, explicitar su valor científico o pedagógico, sin inventar impacto práctico.

No confundir **por qué elegimos el método** con **por qué ocurrió el fenómeno**: lo segundo puede permanecer desconocido. Una pregunta solo se promociona a hallazgo cuando tiene evidencia reproducible y una interpretación calibrada.


## CONTRATO CANÓNICO — obligatorio en TODO episodio

1. **Un único bloque editorial:** no presentar «seis preguntas básicas» más «preguntas nuevas» aparte; no usar «2B». Leer preguntas heredadas como insumos, no como contenido inmovible. **Fusionar, descartar o elevar** las consultas simples a evidencia o ejercicios de las preguntas profundas. Entregar **un solo banco canónico** `QUESTIONS_MASTER.md` + `questions_master.json`. El HTML muestra UNA sola sección de preguntas con tarjetas de todos los casos y facetas de exploración. No debe mostrar dos listas paralelas.
2. **Cada pregunta principal (sin excepción) tiene dos diseños distintos, AÚN SIN EJECUTAR:** un modelo `model_primary_id/model_name` de `discovery_labs/shared/model_catalog/MODEL_SET.md` y un ejercicio estadístico formal (hipótesis y contraste, IC, bootstrap, permutación, Fisher, bondad de ajuste, CV/OOS, etc.) con `qué/por qué/dónde/variables/baseline/validación`. El ejercicio estadístico NO es sinónimo de simplemente elegir el modelo.
3. **Sin entrenar nada durante el paquete:** no ejecutar modelos, tuning con Optuna, simulaciones, scraping o pruebas estadísticas nuevas cuando la solicitud sea solo de planeación. Registrar `PLAN_ONLY` o `BLOCKED`; los conteos previamente verificados son evidencia de contexto, no nuevos experimentos.
4. **Relevancia antes de sofisticación:** no imponer LSTM, Transformers, RL, riesgo colectivo o Optuna en un dataset que no tenga secuencia suficiente, reward, pérdida, target o validación. Mencionar alternativas factibles con criterios; no ofrecer 24 modelos por pregunta.
5. **Pregunta histórica/bio y causa:** un hecho fuera del dataset es un insumo legítimo para hipótesis potentes. Antes de afirmar una relación, investigar cronología, periodos de medición, tiempo de emisión vs creación, explicaciones rivales y evidencia de imposibilidad. Si contexto clave es sensible (p. ej. enfermedad de un sujeto histórico), usar fuentes verificadas y no especular sobre estados mentales, estado clínico por un gráfico ni mecanismo causal sin identificación válida.
6. **O2 y O3 se activan y publican por evidencia:** cada O2 requiere condición `trigger_from_O1` **y resultados O1 comprobados más Deep Research contextual pertinente**; cada O3 requiere `trigger_from_O2` ejecutado y una prueba rival independiente. En el paquete canónico se **diseñan** O2/O3 como candidatos **CONDICIONALES**, pero el **HTML inicial muestra únicamente O1**; O2 y O3 se incorporan progresivamente como nuevas preguntas visibles, nunca se anuncian como hallazgos anticipados.
7. **Visualización científica obligatoria:** proponer por pregunta una figura que cambia la comprensión, una adversarial y un inspector detallado (hover, focus, tap; ID, método, fuente y derechos); imágenes ajenas solo con autorización. Vincular cada escena a cálculo y denominador.
8. **Paquete de entrada antes de guía:** `START_HERE_NEW_CHAT.md`, `DEEP_RESEARCH_PROMPTS.md`, `metadata.json`, `sample_raw.csv`, `sample_features.csv`, `RESEARCH_PLAN.md`, `MODEL_SET.md`, `QUESTIONS_MASTER.md`, `questions_master.json`, `VISUAL_DESIGN.md`, y `sources/claims` (cuando se ejecuta Deep Research). El paquete incluye un checklist de faltantes y decisiones, y un prompt portable para una conversación nueva.
9. **Fases bloqueadas:** Entrada → guía científica HTML → aprobación humana explícita de una versión → storytelling audiovisual → aprobación → video. La skill nunca crea guion/video de oficio.

### Ficha de una pregunta (campos mínimos nuevos)
```yaml
id: BR-01
title: ¿Cambió la pintura cuando cambió la vida de un caso histórico?
research_question: ...
order_1: {question: ..., metric: ..., denominator: ..., status: PLAN_ONLY}
order_2: {question: ..., trigger_from_O1: "si ...", status: CONDITIONAL}
order_3: {question: ..., trigger_from_O2: "si ...", rival_hypothesis: ..., status: CONDITIONAL}
external_context: [{claim: ..., source_url: ..., status: VERIFIED|DISPUTED|PENDING}]
model:
  primary_id: M03
  what: modelo binomial segmentado
  why: detectar rupturas descriptivas sin inferir causalidad
  where: Research / temporada
  data: ...
  baseline: ...
  validation: ...
statistical_exercise:
  what: prueba de quiebre con bootstrap de bloques
  why: evaluar si el patrón supera el ruido
  where: Research / contrastes
  design: ...
visual: {main: ..., adversarial: ..., hover_card: ...}
gates: {licenses: ..., adequate_n: ..., chronology: ..., image_rights: ...}
status: PLANNED
```

### QA automático de salida
- Cada ID es único. `questions_master.json` y `QUESTIONS_MASTER.md` expresan el mismo conjunto de preguntas.
- Cero preguntas principales sin modelo **y** ejercicio estadístico. Ambas propuestas tienen nombre, razón, ubicación y datos.
- Ninguna afirmación causal sin estrategia de identificación y evidencia.
- Cero preguntas «orden 2/3» sin desencadenante condicional explícito o resultado medido.
- Todas las preguntas históricas indican nivel de evidencia del dato externo.
- Comparar el banco heredado y documentar dónde quedó integrado (tabla de trazabilidad), sin mantenerlo como segunda sección visible.
- El primer HTML sólo tiene **una sección principal de preguntas** con todas las rutas y un filtro/índice opcional; la biografía no se esconde como apéndice.
- La skill **no** ejecuta entrenamiento ni crea guion/video.

## HTML científico vivo: estructura y revelación de preguntas por evidencia

El HTML de Fase 1 es una **bitácora científica versionada**, no una diapositiva que presupone su final. Su primera versión se puede construir como esqueleto editorial sin resultados nuevos; cada iteración conserva el contexto y **agrega o corrige** apartados conforme progresa la investigación. No reescribir silenciosamente conclusiones anteriores.

**Orden obligatorio del HTML inicial:**

1. **Párrafo de contexto general al inicio del contenido principal:** quién/qué representa el fenómeno, origen y periodo del dataset, problema humano o científico y por qué vale la pena investigarlo; no adelantar resultados ni atribuir causalidad.
2. **Objetivo explícito:** qué insight no obvio buscamos y **CÓMO, POR QUÉ y PARA QUÉ** lo investigaremos.
3. **Datos, cobertura y límites:** unidad de observación, denominadores, procedencia, licencias, sesgos, periodos y fuentes externas pendientes.
4. **Único índice/bloque de preguntas:** preguntas de **primer orden O1** visibles, con hipótesis, diseño del modelo y del ejercicio estadístico, estado y prerequisitos; sin un segundo bloque de «preguntas avanzadas».
5. **Evidencia y resultados:** espacios con estados honestos `PENDIENTE`, `EN_ESTUDIO`, `VERIFICADO`, `REFUTADO` o `INCONCLUSO`; figuras sólo tras cálculo y QA.
6. **Interpretación adversarial, utilidad, reproducibilidad y próximos pasos:** fuentes, alternativas, incertidumbre, decisiones, preguntas aún bloqueadas, changelog de versión y gate humano.

**Activación progresiva (distinguir documentación interna de publicación):**

- **Diseño/HTML v0:** el JSON y Markdown pueden prever O2/O3 con `trigger`, pero el HTML **no muestra esas preguntas como tareas activas ni las responde**. El lector ve O1, sus hipótesis y lo que aún falta. No bastan títulos de O2 escritos de antemano.
- **DR temprano + O1:** verificar contexto/datos/antecedentes (DR-A/B/C, con foco según el caso), **responder O1 con cálculos reproducibles** y ejecutar una síntesis crítica provisional (DR-E). Solo entonces activar en HTML **las O2 justificadas por esos resultados y fuentes**; registrar `parent_id`, evidencia que activa, fecha/versión y estado. Si O1 es nula, las O2 se reformulan hacia explicación del nulo, sesgo o límite.
- **O2 → O3:** ejecutar O2; solo después agregar O3 que contraste su explicación y registre una hipótesis rival o fuente independiente. Una rama sin soporte permanece interna o `BLOQUEADA`.
- **Visualización especializada (DR-D):** investigación visual y de derechos **después** de identificar qué insight merece mostrarse; hacer **triage temprano de licencias** antes de insertar cualquier imagen. Cerrar síntesis final DR-E después de O2/O3 y DR-D, con QA.
- **Actualización de cada hito:** mantener ID estable, versión/commit, `observed_at`, estado, artefacto de cálculo, fuente, método, incertidumbre, correcciones y siguiente decisión. Distinguir evidencia observada de hipótesis planificada; enlazar datos→pregunta→resultado→figura.

**Ritmo de las cinco investigaciones:** conservar los cinco *frentes* (DR-A historia; B datos; C antecedentes; D visual/derechos; E síntesis adversarial), pero **NO exigir cinco Deep Research exhaustivos y paralelos**. A/B/C son preparación contextual; D se amplía cuando hay resultados; E es un **gate de síntesis**, inicialmente provisional tras DR temprano + O1 y definitivo tras la iteración científica. El esfuerzo profundo se asigna según incertidumbre y valor, no por cuotas.

El HTML inicial, su actualización o una ejecución técnica **no sustituyen** la aprobación explícita de Fase 1 antes de pasar al audiovisual.

## Activación
Usar ANTES de escribir el reporte científico HTML de cualquier episodio; nunca fabricar una historia cerrada antes de analizar los datos. Acepta el paquete de entrada (dataset, perfilado, fuentes externas, antecedentes, licencias, metadata y preguntas heredadas). Produce un **grafo investigable de preguntas**, no una lista decorativa.

## Regla fundamental
**Una consulta simple es un paso del análisis; no necesariamente es una pregunta principal.**
Ejemplo: `COUNT(*) WHERE TREE=0` es evidencia para «¿Hasta qué punto la imagen popular de un caso histórico representa su trabajo, y cambió esa representación con el tiempo?». No se fuerza cada pregunta a ser causal ni el hallazgo a sorprender.

## Entradas obligatorias
- `dataset_id`, versión, hash, grano, cobertura real, campos, licencias.
- 10–20 filas reales variadas (no solo primeras 10); perfilado preliminar y límites de acceso.
- Línea de tiempo y contexto histórico/sectorial, con fuentes externas calificadas.
- Al menos dos antecedentes analíticos y afirmaciones populares **atribuibles** (si existen).
- Preguntas heredadas, ruta de prueba ejecutable, permisos para material visual.
- Resultados previos separados de hipótesis no verificadas.

## Método Q-FORGE (10 etapas)
1. **Leer la historia detrás de los datos:** quién produjo los registros, cuándo y por qué; qué ocurrió alrededor; qué eventos no aparecen en el CSV.
2. **Mapa del dominio:** actores, incentivos, evolución histórica, decisiones, instituciones, tensiones, variables omitidas.
3. **Mapa de variables:** distinguir observables, proxies, etiquetas, denominadores, selección, censura, fuentes adicionales y posibles joins.
4. **Ocho familias de investigación:** evolución y rupturas; outliers multiescala; mecanismos y explicaciones rivales; combinaciones y redes; brecha mito-realidad; heterogeneidad y paradojas; ausencias y sesgos de medición; transferencia/contrafactual y frontera de la evidencia. Añadir economía/social/exploración cuando el dato lo permita.
5. **Generar una pregunta raíz** por familia, que tenga tensión humana y sea medible o pueda declarar con precisión qué falta para medirla.
6. **Traducir la pregunta en estimando:** población, unidad, periodo, n/N, variable, test mínimo, baseline, alternativas.
7. **Crear pregunta de segundo orden:** debe estar gatillada por un hallazgo real, por ejemplo una tendencia agregada que oculta un cambio por temporada; sin datos ejecutados escribir «condicional».
8. **Crear al menos una pregunta de tercer orden:** investigar explicaciones rivales, mecanismos, estabilidad o consecuencias del resultado de segundo orden. Crear vínculos `parent_id` + `trigger` y un grafo acíclico.
9. **Diseñar la visualización como argumento:** qué se ve primero, comparación, anotación, incertidumbre, desagregación, hover/teclado, figura adversarial y fuente; no prometer una imagen que no tiene permisos.
10. **Evaluar y seleccionar:** puntuar, eliminar redundancias, rechazar preguntas imposibles, priorizar investigación sobre espectacularidad.

## Reglas de nivel y de evidencia
- **Orden 1 (O1)**: describe o compara una propiedad, distribución o cambio directamente observado.
- **Orden 2 (O2)**: nace de una anomalía, resultado inesperado, tensión, heterogeneidad o excepción identificada en O1; siempre registrar el `trigger`.
- **Orden 3 (O3)**: intenta explicar o cuestionar la inferencia de O2 con una prueba independiente, fuente nueva, hipótesis rival o validación temporal; NO es una frase con tres «por qué».
- Estado de cada pregunta: `IDEA`, `CONTEXT_VERIFIED`, `DATA_FEASIBLE`, `EXECUTED`, `REFUTED`, `BLOCKED_EXTERNAL_DATA`, `APPROVED`. El estado es explícito, no heredado.
- No promocionar relaciones observacionales a «X causó Y». La biografía, enfermedad, cambio regulatorio o shock externo son **hipótesis contextuales** hasta que exista una cronología y una estrategia de inferencia válida.
- Un mito/creencia popular necesita una fuente original o una muestra verificable de que alguien lo sostiene. Sin evidencia, llamarlo «pregunta provocadora», no «creencia popular extendida».
- Las preguntas de dinero no pueden afirmar rentabilidad sin costes y precios; las sociales no infieren discriminación sin diseño y variables; las de IA no usan identificadores arbitrarios ni información futura como features.

## Ocho patrones de preguntas transferibles
1. **Evolución y quiebres:** ¿Cuándo cambió de verdad el patrón, y cómo distinguimos maduración de un evento externo?
2. **Outliers multiescala:** ¿Qué casos, grupos y periodos rompen el patrón? ¿Es rareza, error o señal significativa? (fila → grupo → temporada → era).
3. **Explicaciones alternativas:** ¿Qué podría producir el mismo resultado observado, y qué nueva evidencia distinguiría las causas?
4. **Combinaciones inesperadas:** ¿Qué elementos coocurren más o menos de lo esperado tras controlar la frecuencia base?
5. **Mito vs realidad:** ¿La imagen popular sobrevive a medir con variables, definiciones y denominadores distintos?
6. **Heterogeneidad y paradojas:** ¿La tendencia global persiste por segmentos, cohortes, invitado/anfitrión y métodos?
7. **Lo invisible:** ¿Qué queda excluido del dataset y cómo cambia la interpretación si lo añadimos o tratamos de recuperarlo?
8. **Mecanismo y frontera:** ¿Qué intervención, evento o validación externa necesitaríamos para pasar de describir a explicar?

## Rubrica de 100 puntos (evaluar 0–5 cada dimensión, convertir a peso)
- Curiosidad y tensión humana 15.
- Anclaje en biografía, historia o dominio 10.
- Rigor y falsabilidad / especificación del estimando 20.
- Potencial real de insight y sorpresa honesta 15.
- Capacidad de generar O2 y O3 basadas en datos 15.
- Poder visual y recorrido narrativo 10.
- Viabilidad y coste para 45 minutos (preproceso fuera de clase) 10.
- Seguridad epistémica, ética y derechos 5.

**Puertas bloqueantes** (aunque la puntuación sea alta): sin fuente para dato externo central; falsa afirmación causal; imágenes sin permiso; variable requerida inexistente y sin plan; pregunta irresoluble camuflada de resultado. Seleccionar 3–5 arcos potentes, no inflar el número de «preguntas aprobadas».

## Contrato JSON por pregunta
```json
{
  "id": "D85-Q07-O2",
  "parent_id": "D85-Q07-O1",
  "order": 2,
  "family": "outliers_multiescala",
  "title": "¿La rareza es de un episodio o de toda una temporada?",
  "hook": "El episodio que rompe el paisaje típico",
  "research_question": "...",
  "narrative_purpose": "resistir la primera impresión",
  "historical_context": [{"claim":"...","source_url":"...","confidence":"VERIFIED|DISPUTED|PENDING"}],
  "trigger": {"result_id": "...", "actual_value": null, "condition": "si resulta atípico..."},
  "hypotheses": ["...", "..."],
  "estimand": {"grain":"episode|season|era","population":"...","measure":"...","denominator":"...","time_basis":"broadcast|recording|unknown"},
  "required_data": [{"source":"fivethirtyeight","columns":["..."],"status":"AVAILABLE|MISSING|TO_VERIFY"}],
  "method": {"baseline":"...", "main":"...", "adversarial":"...", "uncertainty":"..."},
  "visual": {"form":"heatmap|small_multiples|...","reveal":"...","tooltip":"...", "image_rights_status":"..."},
  "outcome_paths": {"supports":"...","refutes":"...","inconclusive":"..."},
  "limitations": ["..."],
  "score": null,
  "status": "IDEA"
}
```

## Definición de terminado
Entregar: el único banco canónico `QUESTIONS_MASTER.md` + `questions_master.json`, `MODEL_SET.md`, `START_HERE_NEW_CHAT.md`, `question_graph.json` de dependencias (no un segundo banco visible), priorización; mapa de familias y arcos O1→O2→O3; tabla fuente-afirmación; 3–5 rutas de alta calidad; plan de visualizaciones y pruebas adversariales. Construir rutas alternativas para «apoya», «refuta» y «no alcanza la evidencia». Ninguna pregunta pasa a `EXECUTED` sin cálculo reproduccible ni a `APPROVED` sin revisión humana.

## Control de las tres etapas
Esta skill sólo prepara el **Paquete de Entrada y la Guía Científica (Fase 1)**. No genera guion audiovisual, voz, storyboard de video, Remotion ni MP4 hasta que el usuario apruebe explícitamente la versión de la guía. El contenido de historia que produce es científico/editorial, no un guion definitivo de video.


## Formatos y compatibilidad

Un arco puede almacenarse como un objeto O1/O2/O3 o como tres nodos enlazados, pero **una investigación tiene exactamente un registro editorial canónico**. El formato serializado debe permitir leer: identificador, raíz, O1/O2/O3, triggers condicionales, modelo, ejercicio estadístico, estimando, fuentes, estado y limitaciones. Adaptar el esquema del episodio sin imponer nombres, IDs ni cantidades a todos los datasets.

### Ubicaciones oficiales

- Skill: `discovery_labs/shared/skills/question-forge/SKILL.md`.
- Catálogo: `discovery_labs/shared/model_catalog/MODEL_SET.md`.
- Plantilla: `discovery_labs/shared/templates/ENTRY_PACK_TEMPLATE.md`.
- Validador: `discovery_labs/shared/validators/validate_entry_pack.py`.
- Cada episodio contiene **solo el paquete específico**: biografía/dominio, prompts concretos, preguntas, muestra, metadatos, datos y visuales; no copia mantenida de la skill.

### Migración de episodios ya iniciados

Cuando se reemplace una copia local, mantener una nota de compatibilidad que apunte a la ubicación compartida y probar enlaces y validadores. Si la infraestructura compartida está en un PR sin fusionar, dejar explícita la dependencia; no afirmar que los enlaces están resueltos en la rama del episodio hasta integrar la dependencia.

## QA

- Preguntas únicas y mismo conjunto de IDs en Markdown y JSON.
- Todas las preguntas con un modelo pertinente y ejercicio estadístico distinto; declarar qué, por qué, dónde, baseline y validación.
- O2/O3 condicionales con trigger e hipótesis rival; no presentarlos como hallazgos.
- Afirmaciones externas con fuentes, conflictos y límites; gráficos con unidades y denominadores.
- Guía HTML científica no equivale a aprobación humana; storytelling y video permanecen bloqueados.
