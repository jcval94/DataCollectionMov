# QA del Paquete de Entrada y Question Forge v2

**Fecha:** 2026-11-18. **Contexto:** inspección estática contra la rama `feat/bob-ross-entry-pack-question-forge` y archivos recuperados desde GitHub. **No se entrenó ningún modelo ni se ejecutó Deep Research completo.**

## Comprobaciones verificadas en la rama

| Criterio | Resultado |
|---|---|
| Banco único `questions_master.json` | **PASS:** 14 preguntas, 14 IDs únicos |
| Preguntas O1 + O2 + O3 | **PASS:** 14/14 contienen las tres propuestas (O2/O3 condicionales, NO ejecutadas) |
| Modelos seleccionados | **PASS:** 14/14 señalan un `model_primary_id` de los 24 del `discovery_labs/shared/model_catalog/MODEL_SET.md` |
| Ejercicios estadísticos independientes | **PASS:** 14/14 incluyen propuesta formal de prueba/intervalo/remuestreo |
| MD vs JSON | **PASS:** los 14 IDs figuran en `QUESTIONS_MASTER.md` y JSON |
| Muestra | **PASS estructural:** 13 registros originales y 13 derivados, metadatos `403×69` |
| Skill reusable | **PASS:** skill compartida `discovery_labs/shared/skills/question-forge/SKILL.md` versión 2.1.0 |
| Guía científica HTML V3 en repo | **PASS estructural:** una sección `id="preguntas"`, 14 tarjetas, cero `id="investigaciones"`/«02B» |
| HTML duplicación de IDs DOM | **PASS:** ninguno detectado |
| JavaScript HTML | **PASS sintaxis**: código embebido se compiló sintácticamente; no se ejecutó una prueba visual de navegador |
| Tema enfermedad | **PASS editorial:** `BR-01` en primer lugar; cronología discutida, sin inferencia causal |
| Aprobación editorial | **PENDIENTE**: no aprobada por usuario |

## Qué NO está validado todavía

- Ejecución en el entorno local de `python entry_pack/validate_pack.py`.
- Render real en Chromium y revisión responsive, teclado/foco, contraste y gráficos de la guía V3 (la versión V2 anterior tuvo revisiones de navegador, pero **no** cuenta como QA de V3).
- Investigación histórica en profundidad, especialmente fechas de diagnóstico/grabación/emisión.
- Derechos de cada imagen original, licencias para miniaturas, políticas de hotlinking.
- Entrenamiento, contrastes estadísticos nuevos, ajuste con Optuna, análisis fuera de muestra o causalidad.
- Resultados de preguntas O2/O3, ya que dependen de O1 y pruebas adversariales.
- Ensayo pedagógico cronometrado de 45 minutos.

## Cómo verificar localmente

Desde la raíz del repo:

```bash
python discovery_labs/episodes/bob-ross/entry_pack/validate_pack.py
python discovery_labs/episodes/bob-ross/run.py --check
python -m unittest discover -s discovery_labs/episodes/bob-ross/tests -v
```

No se requiere entorno de entrenamiento; las comprobaciones de Paquete de Entrada son de estructura/integridad.

## Puertas

- **Entrada:** preparada para revisión.
- **Guía científica V3:** documento estructuralmente preparado; **PENDIENTE_DE_APROBACION_CIENTIFICA**.
- **Storytelling audiovisual:** BLOQUEADO.
- **Video:** BLOQUEADO.


## Auditoría metodológica adicional (18 noviembre de 2026)

Se detectó que el esquema original `questions_master.json` validaba la presencia de texto para O1/O2/O3, pero no exigía por separado desencadenantes, hipótesis rivales, baseline, validación ni el **por qué/dónde de la prueba estadística**. Se ampliaron las 14 fichas con esos contratos en JSON y Markdown y se endureció `validate_pack.py` para evitar falsos positivos. Las nuevas especificaciones son diseño editorial, **no resultados empíricos**.

**Advertencia de sincronización:** `research_guide.html` V3 es una instantánea estática de las tarjetas, NO una plantilla dinámica que lee `questions_master.json`. La correspondencia semántica completa y la automatización de su regeneración siguen pendientes de la Fase 1 autorizada. Esta reparación no modifica la guía HTML, ni inicia modelos ni investigaciones audiovisuales.

**Pruebas de este cambio:** comprobaciones de estructura del contenido y coincidencia de 14 IDs antes del commit. Pendiente ejecutar el script Python en entorno canónico, tests del episodio y navegador real. La rama de integración fue reconstruida sobre `main` después de fusionarse los PR #5 y #11; el PR #10 sigue en revisión. No fusionar el PR ni aprobar la guía sin QA Python/visual y aprobación humana.

## Integración compartida
PR #11 (núcleo) y PR #5 (base Bob Ross) integrados en `main`. La skill, catálogo y plantilla viven solamente en `discovery_labs/shared/`. El wrapper `entry_pack/validate_pack.py` delega al validador compartido y añade invariantes de Bob Ross. La fusión de PR #10 **no autoriza** aprobar la Guía Científica, el guion o el video.


## Verificación de integración sobre main (18 noviembre 2026)

- **Base:** `main` con PR #5 y PR #11 ya integrados; los archivos editados en la rama candidata permanecen exclusivamente bajo `discovery_labs/episodes/bob-ross/`.
- **Banco canónico:** 14 investigaciones O1→O2→O3 con condiciones y contrato modelo + estadística; 24 familias en el catálogo compartido.
- **Dato primario:** 403×69, 66,315 bytes, SHA-256 `42045c8b8aaa8296095d6b294927fb9d0f73a57259f59b560c375844c0fe01cf` recalculado con una verificación estructural de JavaScript sobre contenido recuperado de GitHub; muestra genuina de 13 filas.
- **Migración de test:** `tests/test_entry_pack.py` utiliza las 14 preguntas canónicas y no las 12 antiguas. `entry_pack/QUESTION_BANK.md` está señalado como histórico.
- **Pendientes explícitos:** ejecutar en un checkout de `main` + PR #10 el validador Python compartido, toda la suite del episodio, `intake/qa_intake.cjs`, la revisión de navegador/responsive y el Deep Research. No se han entrenado modelos ni ejecutado contrastes nuevos.
- **Gobernanza:** Fase 0 revisable; guía científica V3 sin aprobación; fases 2 y 3 bloqueadas.
