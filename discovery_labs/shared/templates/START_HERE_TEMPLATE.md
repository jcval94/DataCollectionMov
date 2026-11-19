# START HERE — [nombre del episodio] · AI Discovery Labs

## Objetivo y estado actual
Caso: [slug] · Dataset [fuente] · Unidad [grano] · Pregunta humana principal [pregunta].
Fase: Entrada / Guía científica / Storytelling HTML / Video.
Última aprobación explícita: [fase, versión, quién, fecha] o PENDIENTE.

## Repositorio y ramas
Repo: [owner/repo] · PRs: [URLs, bases, estado]
Carpeta autorizada: discovery_labs/episodes/[slug]/
No editar fuera de esta ruta sin aprobación.

## Motor compartido (no duplicar)
- discovery_labs/shared/skills/question-forge/SKILL.md
- discovery_labs/shared/model_catalog/MODEL_SET.md
- discovery_labs/shared/templates/ENTRY_PACK_TEMPLATE.md
- discovery_labs/shared/validators/validate_entry_pack.py

## Paquete específico (leer en orden)
1. entry_pack/README.md
2. entry_pack/metadata.json y sample_raw.csv
3. entry_pack/CONTEXT_CLAIMS.md y DEEP_RESEARCH_PROMPTS.md
4. entry_pack/QUESTIONS_MASTER.md y questions_master.json
5. entry_pack/RESEARCH_PLAN.md y VISUAL_DESIGN.md
6. research_guide.html (si ya existe)

## Evidencia y límites actuales
[Contar observaciones, variables, unidad, periodos, hash, derechos, resultados realmente ejecutados, afirmaciones disputadas, factores externos faltantes, modelos solo planeados.]

## Próxima acción concreta
[Una acción permitida en la fase actual, criterios de aceptación, comandos de QA.]

## Prohibiciones
No fusionar PRs, entrenar, generar guion audiovisual o video sin autorización correspondiente. Ninguna propuesta de modelo cuenta como ejecución. Una guía publicada no equivale a aprobada.

## Prompt literal de continuidad
> Inspecciona estado real de repo/PR y lee START_HERE, skill compartida y el paquete específico de [slug]. Realiza únicamente [tarea]. Mantén preguntas en UN banco, O1/O2/O3, modelo+estadística por investigación; respeta derechos y las puertas de aprobación.
