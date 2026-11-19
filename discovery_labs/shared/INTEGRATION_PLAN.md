# Integración de AI Discovery Labs: estado real y siguientes puertas

**Corte:** 18 noviembre 2026. **Repositorio:** `jcval94/DataCollectionMov`.

## Integración técnica: realizada

| PR | Contenido | Estado | Commit en `main` |
|---|---|---|---|
| [#11](https://github.com/jcval94/DataCollectionMov/pull/11) | Núcleo compartido: Question Forge V2.1, 24 modelos, plantillas, validadores | **MERGED** | `fd74589da73426e6262f15c508910cdf0750f251` |
| [#5](https://github.com/jcval94/DataCollectionMov/pull/5) | Base del episodio Bob Ross, datos originales, scripts y material histórico | **MERGED** | `9b32cdd35de1a4167c9cb1eab66e318b9fcf8398` |
| [#10](https://github.com/jcval94/DataCollectionMov/pull/10) | Paquete de Entrada canónico de 14 investigaciones + guía HTML científica V3 | **MERGED** | `63984a06ea4321647acc00d31e348f65e77e5d0e` |

**Estrategia de reconciliación:** se integró primero el motor compartido y la base Bob Ross. Los cambios del PR #10 se combinaron sobre el árbol actualizado de `main` conservando campos legacy requeridos por tests, con un merge commit de dos padres en su rama; luego se revisó que el diff de PR #10 afectara solo Bob Ross. El PR quedó fusionable sin sobrescribir cambios ajenos al episodio.

## Arquitectura canónica en main

```text
discovery_labs/
  shared/
    skills/question-forge/SKILL.md
    model_catalog/MODEL_SET.md
    templates/{ENTRY_PACK_TEMPLATE,DEEP_RESEARCH_TEMPLATE,START_HERE_TEMPLATE}.md
    validators/{validate_entry_pack.py,tests/}
  episodes/
    bob-ross/
      README.md
      entry_pack/
        START_HERE_NEW_CHAT.md
        QUESTIONS_MASTER.md
        questions_master.json
        DEEP_RESEARCH_PROMPTS.md
        CONTEXT_CLAIMS.md
        MODEL_FIT_BOB_ROSS.md
        metadata.json
        sample_raw.csv
        sample_features.csv
        RESEARCH_PLAN.md
        VISUAL_DESIGN.md
        validate_pack.py
      research_guide.html
```

**Única fuente viva:** Question Forge en `shared/skills/` y los 24 modelos en `shared/model_catalog/`. Las tres copias locales inicialmente añadidas por PR #10 se eliminaron antes de fusionar. Los archivos `intake/`, `entry_pack/question_graph.json`, `questions.json` y las skills `research-question-architect` de PR #5 son **históricos o de compatibilidad**, no segundo estándar editorial; no deben utilizarse para nuevos episodios. No eliminar contenido previo hasta auditar cada consumidor.

## Quality gates técnicos

- [x] 14 investigaciones canónicas de Bob Ross, 14 IDs únicos.
- [x] 14/14 con O1, O2, O3; modelo válido y ejercicio estadístico distinto en fase de diseño.
- [x] Catálogo compartido de 24 familias no dependiente de Bob Ross.
- [x] Muestra de 13 filas originales y 13 derivadas; metadatos de 403×69.
- [x] HTML con una sección de preguntas y 14 tarjetas; enfermedad y límites causales explícitos.
- [x] Compatibilidad con pruebas legacy de Fase 0 preservada al integrar metadatos y grafo histórico.
- [x] PRs #5, #10 y #11 fusionados.
- [x] Validación **ejecutada por GitHub Actions**, no solo estática. [AI Discovery Labs QA, run #44427475768](https://github.com/jcval94/DataCollectionMov/actions/runs/44427475768) (**SUCCESS**): sintaxis, tests compartidos sintéticos, tests legado Bob Ross, dataset, validador común y 14 preguntas. El workflow general `Validar código y catálogo` también concluyó **SUCCESS** en el mismo PR.
- [ ] Validar un **segundo episodio real** con el motor compartido. Los tests con episodio sintético validan el contrato, pero no demuestran una segunda migración real.
- [ ] QA de navegador de `research_guide.html` V3, permisos de imágenes, Deep Research completo y ensayo docente.

## Puertas científicas — permanecen bloqueadas

**Fase 0:** paquete integrado como diseño investigable.

**Fase 1:** guía científica HTML V3, todavía **PENDIENTE DE APROBACIÓN** de la persona usuaria; no implica investigación histórica concluida.

**Fase 2:** storytelling audiovisual HTML, **BLOQUEADO** hasta aprobación explícita de Fase 1.

**Fase 3:** video, **BLOQUEADO** hasta aprobación explícita de Fase 2.

La fusión de GitHub no autoriza entrenamiento, inferencias clínicas/causales ni producción audiovisual.

## Comandos para cualquier persona o agente

```bash
python -m unittest discover -s discovery_labs/shared/validators/tests -v
python -m unittest discover -s discovery_labs/episodes/bob-ross/tests -v
python discovery_labs/episodes/bob-ross/run.py --check
python discovery_labs/shared/validators/validate_entry_pack.py \
  --entry-pack discovery_labs/episodes/bob-ross/entry_pack \
  --guide discovery_labs/episodes/bob-ross/research_guide.html
python discovery_labs/episodes/bob-ross/entry_pack/validate_pack.py
```
