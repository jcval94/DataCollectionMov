# Paquete de entrada · AI Discovery Labs / Bob Ross

> **Antes de producir la guía científica:** comprender el mundo, las fuentes, las posibles historias y qué no puede medirse. Este paquete es el estándar portable de AI Discovery Labs. No autoriza video ni guion audiovisual.

**Estado:** `PHASE_0_DRAFT`. La investigación externa tiene prompts y un registro inicial de enlaces; los cuatro Deep Research especializados **NO** están ejecutados ni aprobados por este paquete.

## Abrir en orden

| Archivo | Pregunta que resuelve |
|---|---|
| [metadata.json](metadata.json) | ¿Qué es el dataset, qué volumen tiene y qué falta? |
| [data_sample.csv](data_sample.csv) | ¿Cómo se ven sus registros reales? Pequeña muestra **intencional**, no aleatoria |
| [sources.json](sources.json) | ¿Qué fuentes y permisos investigar y cómo verificar las afirmaciones? |
| [DEEP_RESEARCH_PROMPTS.md](DEEP_RESEARCH_PROMPTS.md) | ¿Qué investigaciones contextuales lanzar y cómo sintetizarlas? DR-1 a DR-5 |
| [QUESTION_BANK.md](QUESTION_BANK.md) | ¿Cuáles son las 12 investigaciones profundas propuestas con 1.º → 2.º → 3.er orden? |
| [question_graph.json](question_graph.json) | Contrato estructurado para que un agente recorra preguntas y pruebas |
| [skills/research-question-architect/SKILL.md](skills/research-question-architect/SKILL.md) | Skill reusable para diseñar preguntas no triviales en futuros datasets |
| [VISUAL_EVIDENCE.md](VISUAL_EVIDENCE.md) | Cómo hacer gráficos visualmente poderosos sin perder ética ni exactitud |
| [PLANNING.md](PLANNING.md) | Plan por bloques y puertas de aprobación |
| [PHASE1_GUIDE_PROMPT.md](PHASE1_GUIDE_PROMPT.md) | Prompt para construir la primera guía HTML científica cuando el paquete se revise |

## Qué cambia frente al episodio inicial

La pregunta «¿cuántos cuadros tienen árboles?» sigue siendo una **medición útil**, no el desenlace. Nuevas posibles protagonistas: evolución y novedad a lo largo de 31 temporadas; anomalías que desaparecen con agregación; cambios temporales en relación con historia y biografía; distancia entre motivos y estilo real; clusters que cambian al cambiar método; creencias que requieren fuentes externas.

### Investigación de tercer orden
Ejemplo conceptual, aún por ejecutar:
- **1.º:** parece que un motivo se vuelve más frecuente en las últimas temporadas.
- **2.º:** ¿se debe a un cambio abrupto o a una tendencia antigua? ¿Se mantiene sin invitados?
- **3.º:** ¿un marcador biográfico explica realmente el patrón o es una coincidencia al elegir un punto de corte retrospectivamente? ¿Persistiría en ventanas alternativas?
Si el orden 1 **no** muestra cambio, el orden 2 debe indagar por qué parecía que lo había y el orden 3 contrastar sesgos/agrupación.

## Contexto biográfico sin ficción

La historia de Bob Ross merece investigación independiente: formación y Alaska, wet-on-wet y televisión educativa, temporadas, invitados, empresa, salud y legado. El CSV NO contiene fecha exacta por registro, diagnóstico, imágenes ni valoración estética.

En particular, la pregunta «¿su enfermedad cambió su estilo?» **no tiene respuesta causal directa con estos datos**. Es legítimo diseñar una investigación histórica y una comparación descriptiva con eventos bien fechados y controles, siempre que no se lea salud a partir de una imagen.

## Métodos para añadir otro dataset

1. Copiar la skill fuera de este episodio solo en un cambio autorizado.
2. Sustituir metadata y muestra reales, nunca sintéticas.
3. Lanzar DR por contexto humano, literatura/datos externos, preguntas y activos/derechos.
4. Redactar al menos un árbol de 1er/2.º/3er orden por investigación protagonista.
5. Completar la Fase 1 HTML, obtener aprobación, después Fase 2 audiovisual, obtener segunda aprobación y por último video.

## Derechos

Datos de etiquetas FiveThirtyEight CC BY 4.0, la obra pictórica y las imágenes/video/audio tienen titulares distintos. Puede usarse un enlace externo a una galería y una ficha sin imagen; previsualizar cuadros en tooltip depende de una licencia o autorización específica. El método debe ofrecer teclado/tap, no solo hover.

## Fases autorizadas ahora

- **Fase 0:** editar paquete, investigar, validar.
- **Fase 1:** construir la guía científica HTML solo cuando los datos y fuentes estén preparados.
- **Fase 2:** **BLOQUEADA** hasta la aprobación explícita de una versión concreta de la guía.
- **Fase 3:** **BLOQUEADA** hasta la aprobación explícita de una versión concreta del storytelling audiovisual.

Mantener modificaciones en `discovery_labs/episodes/bob-ross/`. Material de este paquete no debe confundirse con resultados ya computados, ni sustituye los tests de `run.py`.
