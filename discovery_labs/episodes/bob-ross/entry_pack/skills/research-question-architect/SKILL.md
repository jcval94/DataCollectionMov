---
name: research-question-architect
description: Diseña preguntas de investigación memorables, multinivel y falsables a partir de un dataset y contexto externo verificado. Requiere preguntas de segundo y tercer orden; evita contar filas como hallazgo principal.
version: "1.0"
scope: "Reusable across AI Discovery Labs: copy this skill or publish it as a shared skill after approval."
---

# Research Question Architect — Skill de preguntas de alto impacto

## Cuándo activarla
Al comenzar cualquier investigación con una fuente de datos; antes de diseñar gráficos, narrativas de video o scripts definitivos. Puede emplearse en una segunda auditoría cuando el inventario está lleno de preguntas que se resuelven con un simple `GROUP BY`.

## Inputs obligatorios
1. Dataset: muestra real, diccionario, grano, cobertura, calidad, restricciones y fuente primaria.
2. Contexto: biografía/historia del protagonista, fechas, controversias, instituciones, sucesos externos y antecedentes con URL y grado de fiabilidad.
3. Objetivo educativo y público: pregunta que importe al mundo real, no técnica que queremos practicar.
4. Posibles cruces entre fuentes y permisos de uso.
5. Lo que ya sabemos del análisis exploratorio, separado de lo que aún no se ha ejecutado.

## Algoritmo obligatorio (no redactar preguntas directamente)

### A. Entender el universo
Leer el dataset e identificar: qué representa una fila, qué NO representa, periodos reales frente a etiquetas secuenciales, sesgos y variables ausentes. Generar un mapa de actores, incentivos, contradicciones, cambios y límites de medición.

### B. Localizar tensiones narrativas auténticas
Investigar al menos seis ejes cuando correspondan:
- **Cambio y ruptura:** periodos, decisiones, shocks, enfermedad o cambios institucionales; contrastar múltiples puntos de corte y no inferir causas sin diseño.
- **Escala y outliers:** episodios → temporadas → periodos → subgrupos; cuestionar si la anomalía sobrevive al cambiar agregación, normalización o muestra.
- **Paradojas y segmentación:** la conclusión global puede invertirse por mezcla de grupos, composición o denominadores.
- **Ausencias y silencios:** qué eventos, voces, lugares o categorías no aparecen; ausencia de etiqueta ≠ ausencia en la realidad.
- **Mecanismos y explicación:** qué variables conducen a un patrón; buscar contraejemplos y confusores.
- **Evolución, novedad y repetición:** complejidad/diversidad y variación con el tiempo, evitando equiparar una métrica a excelencia.
- **Contexto externo:** biografía, noticias, políticas, normas, cambios culturales o tecnología, con fecha y procedencia.
- **Comparación con alternativa:** casos o unidades comparables para separar tendencia general de fenómeno propio.
- **Legado o consecuencias:** impacto, recepción, imitación o difusión, SOLO si hay observaciones externas válidas.
- **Robustez:** ¿qué ocurre al modificar periodo, unidad, etiqueta o modelo?

### C. Árbol de pregunta obligatorio
Cada investigación importante debe contener:
- **Orden 1 (observación):** ¿qué patrón medible existe y en qué población?
- **Orden 2 (explicación):** el resultado del orden 1 determina cuál de varias nuevas preguntas se activa. ¿Para quién, desde cuándo, por qué podría pasar, es artefacto del dato?
- **Orden 3 (síntesis / adversario):** parte de la respuesta de segundo orden, contrasta una explicación rival o una fuente externa. Debe poder cambiar la conclusión o precisar qué NO puede inferirse.
- Registrar **trigger explícito**, ramificaciones si el primer resultado es contrario, refutación, nueva fuente y salida visual para cada nodo.
No escribir una cadena fija disfrazada de preguntas de segundo orden: debe existir dependencia de los resultados.

### D. Seis perspectivas, pero no seis trivialidades
Mantener A negocio, B social, C descubrimiento, D1/D2 creencias, E detective. Una creencia debe ser **afirmación verificable y culturalmente reconocible con evidencia de su difusión**; si no, llamarla «hipótesis provocadora», no «mito popular».
Rediseñar D1 y D2 como tensiones investigables, NO como sí/no que se agotan en una consulta.

### E. Puntuación individual (0–5 por dimensión)
- Intriga legítima, importancia humana, originalidad, medibilidad/identificabilidad, profundidad segundo/tercer orden, posibilidad visual, rigor/falsabilidad, reproducibilidad, valor docente y protección ética (10 dimensiones, máximo 50).
Umbrales:
- **>=40:** candidata a portada, si la evidencia es suficiente.
- **30–39:** oportunidad de mejorar y validar fuentes.
- **<30:** descartarla como pregunta protagonista; puede sobrevivir como subpregunta EDA.
- Cualquier afirmación causal sin identificación, denuncia sin evidencia, lesión de derechos o ausencia de datos críticos BLOQUEA por encima del puntaje.

## Contrato de salida por pregunta
```json
{
  "id": "estable",
  "headline": "curiosa pero no engañosa",
  "human_stakes": "por qué le importa al público",
  "order_1": {"question": "...", "metric": "...", "denominator": "...", "fig": "..."},
  "order_2": [
    {"trigger": "si O1=...", "question": "...", "additional_data": ["..."], "test": "..."},
    {"trigger": "si O1 no=...", "question": "...", "additional_data": ["..."], "test": "..."}
  ],
  "order_3": {"depends_on": "O2", "question": "...", "rival_explanation": "...", "falsifier": "..."},
  "evidence_status": "CALCULATED | EXTERNALLY_DOCUMENTED | TESTABLE_PENDING | BLOCKED",
  "sources": [],
  "methods": [],
  "visual_concept": "...",
  "anti_claims": [],
  "score": {"total": 0, "rationale": "..."}
}
```

## QA antes de enviar al analista
1. La pregunta **no** se contesta completamente con COUNT, MIN, MAX o un gráfico de frecuencia.
2. Si depende de contexto externo, cada dato contextual tiene fuente/fecha y verificación pendiente explícita.
3. Existe un denominador definido y una métrica que responde al verbo de la pregunta.
4. El segundo orden aparece tras observaciones, no solo ante el título.
5. El tercero desafía una hipótesis del segundo y añade valor real.
6. Hay al menos una visualización capaz de cambiar una intuición.
7. Ninguna afirmación dice que una biografía demuestra una causa en la serie.
8. El alumno puede decidir e interpretar el resultado sin programar.
9. Se ofrecen resultados negativos/nulos o contradicciones como desenlaces posibles.
10. Reportar 6–12 preguntas exploratorias, seleccionar 2–4 fuertes para la guía principal, mantener las seis perspectivas como rutas votables.

## Regla editorial y de pipeline
**Paquete de entrada (fuentes + preguntas multinivel) → guía científica HTML completa → APROBACIÓN EXPLÍCITA → storytelling audiovisual HTML → APROBACIÓN EXPLÍCITA → video.**
No escribas intro de video, teaser ni storyboard hasta aprobar la guía científica. Una ruta de investigación de 45 minutos puede ser una selección del árbol, no todo el árbol completo.

## Generalización
El skill no debe contener datos hardcodeados de Bob Ross. Cada nuevo episodio aporta un archivo de contexto + dataset + análisis exploratorio y genera un árbol de preguntas nuevo. En el episodio Bob Ross, leer `entry_pack/QUESTION_BANK.md` para ejemplos, pero no trasplantarlos ciegamente a los demás temas.
