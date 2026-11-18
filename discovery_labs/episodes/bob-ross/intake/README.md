# Paquete de entrada · AI Discovery Labs — Bob Ross

> **Objetivo:** antes de crear un HTML científico, investigar la historia, los datos y las posibilidades reales de descubrimiento. Todo lo que hay aquí es un **insumo de investigación**, no el informe aprobado, el storyboard ni el video.

## Lectura recomendada

1. [HISTORIA_BASE.md](HISTORIA_BASE.md) — hilo humano de la investigación, con hechos, incógnitas y riesgos de causalidad.
2. [DEEP_RESEARCH_MASTER.md](DEEP_RESEARCH_MASTER.md) — prompt coordinador: cinco investigaciones documentales que se complementan.
2. [prompts/01_BIOGRAFIA_EVENTOS.md](prompts/01_BIOGRAFIA_EVENTOS.md) — biografía y cronología médica sin inferencias indebidas.
3. [prompts/02_HISTORIA_CONTEXTO.md](prompts/02_HISTORIA_CONTEXTO.md) — contexto cultural, televisivo e histórico.
4. [prompts/03_CIENCIA_ANTECEDENTES.md](prompts/03_CIENCIA_ANTECEDENTES.md) — investigaciones, métodos y reproducciones existentes.
5. [prompts/04_FUENTES_VISUALES_DERECHOS.md](prompts/04_FUENTES_VISUALES_DERECHOS.md) — derechos de pinturas, joins e inspector hover.
6. [prompts/05_SINTESIS_HIPOTESIS.md](prompts/05_SINTESIS_HIPOTESIS.md) — síntesis, rivalidad de hipótesis, priorización de Q1/Q2/Q3.
7. [PLAN_DE_INVESTIGACION.md](PLAN_DE_INVESTIGACION.md) — lotes y pruebas de calidad.
8. [QUESTION_GRAPH.md](QUESTION_GRAPH.md) y [question_graph.json](question_graph.json) — 12 arcos, **24 preguntas de segundo orden y 12 de tercero**.
9. [skills/research-question-architect/SKILL.md](skills/research-question-architect/SKILL.md) — skill reutilizable y transferible a los otros 85+ casos.
10. [VISUAL_SPEC.md](VISUAL_SPEC.md) — 7 visualizaciones científicas y diseño de inspector contextual de pinturas condicionado por derechos.
11. [data_sample.csv](data_sample.csv) y [metadata.json](metadata.json) — **12 filas intencionales no representativas**, y metadatos de 403 episodios.
12. [EVIDENCE_SEEDS.md](EVIDENCE_SEEDS.md) + [EVIDENCE_LEDGER_TEMPLATE.csv](EVIDENCE_LEDGER_TEMPLATE.csv) — fuentes preliminares y ledger para verificar/contrastar.
13. [SCORECARD_TEMPLATE.csv](SCORECARD_TEMPLATE.csv) — rúbrica para elegir qué investigar. Los campos no están aprobados ni puntuados.
14. [PROMPT_AGENT_FASE0.md](PROMPT_AGENT_FASE0.md) — instrucción lista para usar en Codex/Claude Code/otra IA investigadora.

## Una pregunta puede ser atractiva y seguir siendo imposible

«¿La enfermedad cambió su pintura?» exige una fecha de diagnóstico, fechas de **grabación y realización** de obras, una muestra comparable después del evento, hipótesis rivales y un diseño que pueda identificar efectos. El CSV original no trae fechas de filmación ni datos médicos. No es válida una conclusión causal a partir de observar cambios por temporada.

Los números de episodios y motivos en `metadata.json` derivan del archivo original local y su estructura; la cronología biográfica está separada. Los títulos y pinturas no prueban que exista permiso para mostrarlas.

## Definición de preguntas mejoradas

Un conteo sencillo es una **prueba instrumental Q0**. No basta por sí solo para construir la investigación.

Cada uno de los 12 arcos tiene:
- Una Q1 humana y falsable.
- **Dos Q2** que nacen de observar Q1.
- **Una Q3** que busca mecanismos, robustez, agregación, representatividad o explicación alternativa.
- Fuentes externas necesarias y límites.
- Una visualización potente y una prueba adversarial.
- Un estado que diferencia lo ejecutado antes de las hipótesis.

Los 12 arcos son candidatos; **no** se han ejecutado ni convertido todavía en las seis rutas de `../episode.html`.

## Verificación del paquete (sin red)

Con Node.js instalado y desde la carpeta `intake/`:

```bash
node qa_intake.cjs
```

El verificador compara el SHA original, exige 12 muestras realmente presentes en el CSV, 12 arcos Q1, al menos 24 Q2 y 12 Q3 y confirma la presencia de los cinco prompts. **No reemplaza Deep Research ni prueba derechos de imágenes**. Si se incorpora al pipeline local, guardar sus salidas y commit como evidencia antes de afirmar que la fase está lista.

## Flujo de aprobación (estándar general)

**Fase 0 Intake → Fase 1 Guía HTML científica → Fase 2 Storytelling HTML → Fase 3 Video.**

Entre Fase 1 y 2 se exige aprobación humana explícita de la versión de HTML; entre Fase 2 y 3 se exige una segunda. No generar guion audiovisual o video mientras la guía científica no esté aprobada.

## Scope

Se añade contenido únicamente bajo `discovery_labs/episodes/bob-ross/intake/`; el episodio anterior y el dataset íntegro quedan intactos. La skill es portable: **no** está instalada globalmente por guardar este archivo. El agente debe leerla explícitamente o instalarla tras revisión.

**Estado del paquete:** DRAFT / RESEARCH_PENDING, no constitutivo de aprobación editorial.
