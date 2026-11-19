# Deep Research — plantilla reusable (adaptar al dominio)

**Regla:** mantener cinco **frentes de investigación**, pero distribuirlos en el tiempo según las evidencias y decisiones reales: **DR-A/B/C al principio, DR-D a profundidad después de identificar hallazgos, y DR-E como síntesis crítica de apertura de O2 y de cierre**. No son cinco llamadas simultáneas ni cinco análisis obligatoriamente exhaustivos. Los prompts son contratos, nunca evidencia ejecutada; no atribuir causalidad, características sensibles ni hechos no observados sin fuentes.

**Misión:** descubrir insights realmente nuevos y sorprendentes de cada dataset, sin fabricar novedad. Cada informe contesta **CÓMO** se investigó (procedencia, método, reproducibilidad), **POR QUÉ** la pregunta/hallazgo merece atención (rival, límite, contexto) y **PARA QUÉ** sirve (comprensión, decisión o siguiente experimento).

**Secuencia y criterio de activación:**
1. DR-A historia, DR-B datos y DR-C antecedentes/mitos **focalizados** producen un contexto contrastable.
2. Publicar HTML científico **inicial** con párrafo introductorio general y O1 propuestas; **NO publicar O2/O3 como hallazgos o preguntas activas**. El contrato puede contenerlas como hipótesis internas `CONDICIONAL`.
3. Responder O1 sobre el dataset real con incertidumbre; ejecutar **DR-E provisional** para revisar fuentes, resultados y activar las O2 respaldadas. Dejar bloqueadas las demás.
4. Tras ejecutar O2, activar O3 si una contradicción/hipótesis rival justifica nuevas pruebas. Profundizar DR-D **solo para insights seleccionados**; comprobar permisos mínimos de imágenes desde el inicio y no insertar imágenes sin licencia.
5. Cerrar DR-E con O2/O3 comprobados, visualizaciones validadas, conclusiones calibradas, bitácora por commit y aprobación humana del HTML. Ni síntesis ni HTML autorizan storytelling o video.

**Formato de avance:** `question_id`, `orden`, `parent_id`, `trigger`, `status`, `claim_id`, `evidence_artifact`, `version`, `next_action`. El HTML debe actualizarse a medida que se resuelven preguntas, no mostrar desde el principio la investigación completa.

## DR-A · Historia y contexto del dominio
Investigar cómo surgió el fenómeno, sus protagonistas/instituciones, eventos antes/durante/después, calendarios relevantes y tensiones humanas. Extraer una cronología con fechas/precisión y evidencias primarias y secundarias. Identificar eventos externos no representados por el dataset. Investigar 3 explicaciones rivales, no imponer una narrativa.

**Entregas:** línea temporal, registro claim→fuente, discrepancias y preguntas contextuales.

## DR-B · Arqueología de datos y enriquecimiento
Auditar origen, granularidad, cobertura, versionado, formatos, nulos, sesgos, licencias, claves, periodos y diferencias entre fecha de evento, captura/publicación y actualización. Buscar conjuntos complementarios y evaluar joins 1:1, 1:N, pérdida de filas, duplicados, permisos y drift.

**Entregas:** diccionario, perfil de calidad, sample real, manifiesto inmutable, plan Bronze/Silver/Gold, joins y bloqueos.

## DR-C · Mitos, estudios previos y mecanismos
Recopilar creencias/afirmaciones **realmente documentadas** con autor, fecha, fuente, evidencia y grado de difusión; no inventar mitos. Buscar antecedentes con estado DOCUMENTED/REPRODUCED/PENDING. Formular mecanismos alternativos: selección, mercado, regulación, producción, contexto histórico y errores de medición.

**Entregas:** registro de mitos, mapa de mecanismos, 2+ antecedentes relevantes y posibles contraejemplos.

## DR-D · Visualizaciones y derechos (profundizar tras O1 y priorización)
Diseñar figuras que prueben/contradigan preguntas: distribución, evolución, outliers multiescala, heterogeneidad, coocurrencia, comparación de modelos y figuras adversariales. Cada gráfico debe tener denominador, grano, fuente y método; QA móvil/teclado. Investigar derechos de imágenes y permisos de reutilización.

**Entregas:** diseño de figuras, prototipo de interacción, matriz de derechos, tabla de trazabilidad cálculo→figura.

## DR-E · Síntesis adversarial (checkpoint tras O1 y cierre tras DR-D)
Abrir un **checkpoint provisional solo después de DR-A/B/C y O1 medida**; cerrar la síntesis **después de DR-D, O2 y O3 cuando procedan**. Conciliar fechas y fuentes; distinguir VERIFIED/DISPUTED/PENDING/NOT_SUPPORTED; ejecutar la skill compartida Question Forge; mantener 8–15 investigaciones planificadas si lo justifica la fuente, pero publicar inicialmente O1 y solo activar O2→O3 según evidencia, un modelo y un ejercicio estadístico distinto por investigación, elegidos del catálogo compartido. Seleccionar 3–5 arcos prioritarios y demostrar factibilidad.

**Entregas:** QUESTIONS_MASTER.md y questions_master.json como ÚNICO banco, plan científico y visual, bloqueos, matriz de fuentes, criterios para research_guide.html.

## Gates
Nunca fabricar datasets, entrenamientos, inferencia causal ni fuentes. El Paquete de Entrada termina en estado ENTRY_READY_FOR_REVIEW; después se puede trabajar en Guía científica HTML. Storytelling audiovisual y video requieren aprobaciones humanas explícitas, por versión.
