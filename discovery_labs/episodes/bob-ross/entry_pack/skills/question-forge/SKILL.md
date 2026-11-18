---
name: question-forge
description: Diseña preguntas de investigación memorables, falsables, contextuales y de varios órdenes a partir de datasets reales, hipótesis externas y evidencia verificada. Para AI Discovery Labs y cualquier dataset.
version: 1.0.0
---
# Question Forge — habilidad reusable de preguntas científicas y narrativas

## Activación
Usar ANTES de escribir el reporte científico HTML de cualquier episodio; nunca fabricar una historia cerrada antes de analizar los datos. Acepta el paquete de entrada (dataset, perfilado, fuentes externas, antecedentes, licencias, metadata y preguntas heredadas). Produce un **grafo investigable de preguntas**, no una lista decorativa.

## Regla fundamental
**Una consulta simple es un paso del análisis; no necesariamente es una pregunta principal.**
Ejemplo: `COUNT(*) WHERE TREE=0` es evidencia para «¿Hasta qué punto la imagen popular de Bob Ross representa su trabajo, y cambió esa representación con el tiempo?». No se fuerza cada pregunta a ser causal ni el hallazgo a sorprender.

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
Entregar: `question_graph.json`, priorización; mapa de familias y arcos O1→O2→O3; tabla fuente-afirmación; 3–5 rutas de alta calidad; plan de visualizaciones y pruebas adversariales. Construir rutas alternativas para «apoya», «refuta» y «no alcanza la evidencia». Ninguna pregunta pasa a `EXECUTED` sin cálculo reproduccible ni a `APPROVED` sin revisión humana.

## Control de las tres etapas
Esta skill sólo prepara el **Paquete de Entrada y la Guía Científica (Fase 1)**. No genera guion audiovisual, voz, storyboard de video, Remotion ni MP4 hasta que el usuario apruebe explícitamente la versión de la guía. El contenido de historia que produce es científico/editorial, no un guion definitivo de video.
