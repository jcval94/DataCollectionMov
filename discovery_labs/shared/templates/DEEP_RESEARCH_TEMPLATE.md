# Deep Research — plantilla reusable (adaptar al dominio)

**Regla:** cinco frentes, cuatro independientes y una síntesis final. Los prompts son contratos de investigación, no evidencia ejecutada. No atribuir causalidad, características sensibles o hechos no observados sin fuentes verificadas.

## DR-A · Historia y contexto del dominio
Investigar cómo surgió el fenómeno, sus protagonistas/instituciones, eventos antes/durante/después, calendarios relevantes y tensiones humanas. Extraer una cronología con fechas/precisión y evidencias primarias y secundarias. Identificar eventos externos no representados por el dataset. Investigar 3 explicaciones rivales, no imponer una narrativa.

**Entregas:** línea temporal, registro claim→fuente, discrepancias y preguntas contextuales.

## DR-B · Arqueología de datos y enriquecimiento
Auditar origen, granularidad, cobertura, versionado, formatos, nulos, sesgos, licencias, claves, periodos y diferencias entre fecha de evento, captura/publicación y actualización. Buscar conjuntos complementarios y evaluar joins 1:1, 1:N, pérdida de filas, duplicados, permisos y drift.

**Entregas:** diccionario, perfil de calidad, sample real, manifiesto inmutable, plan Bronze/Silver/Gold, joins y bloqueos.

## DR-C · Mitos, estudios previos y mecanismos
Recopilar creencias/afirmaciones **realmente documentadas** con autor, fecha, fuente, evidencia y grado de difusión; no inventar mitos. Buscar antecedentes con estado DOCUMENTED/REPRODUCED/PENDING. Formular mecanismos alternativos: selección, mercado, regulación, producción, contexto histórico y errores de medición.

**Entregas:** registro de mitos, mapa de mecanismos, 2+ antecedentes relevantes y posibles contraejemplos.

## DR-D · Visualizaciones y derechos
Diseñar figuras que prueben/contradigan preguntas: distribución, evolución, outliers multiescala, heterogeneidad, coocurrencia, comparación de modelos y figuras adversariales. Cada gráfico debe tener denominador, grano, fuente y método; QA móvil/teclado. Investigar derechos de imágenes y permisos de reutilización.

**Entregas:** diseño de figuras, prototipo de interacción, matriz de derechos, tabla de trazabilidad cálculo→figura.

## DR-E · Síntesis adversarial
Ejecutar DESPUÉS de DR-A...D. Conciliar fechas y fuentes; distinguir VERIFIED/DISPUTED/PENDING/NOT_SUPPORTED; ejecutar la skill compartida Question Forge; generar 8–15 investigaciones si lo justifica la fuente, con O1→O2→O3 condicionales, un modelo y un ejercicio estadístico distinto por investigación, elegidos del catálogo compartido. Seleccionar 3–5 arcos prioritarios y demostrar factibilidad.

**Entregas:** QUESTIONS_MASTER.md y questions_master.json como ÚNICO banco, plan científico y visual, bloqueos, matriz de fuentes, criterios para research_guide.html.

## Gates
Nunca fabricar datasets, entrenamientos, inferencia causal ni fuentes. El Paquete de Entrada termina en estado ENTRY_READY_FOR_REVIEW; después se puede trabajar en Guía científica HTML. Storytelling audiovisual y video requieren aprobaciones humanas explícitas, por versión.
