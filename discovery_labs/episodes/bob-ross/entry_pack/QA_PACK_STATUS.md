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

**Pruebas de este cambio:** comprobaciones de estructura del contenido y coincidencia de 14 IDs antes del commit. Pendiente ejecutar el script Python en entorno canónico, tests del episodio y navegador real. Los PR #5, #10 y #11 ya están fusionados en `main`. Esta sección registraba un estado transitorio; no implica que la guía científica esté aprobada.

## Integración compartida
PR #11 (núcleo) y PR #5 (base Bob Ross) integrados en `main`. La skill, catálogo y plantilla viven solamente en `discovery_labs/shared/`. El wrapper `entry_pack/validate_pack.py` delega al validador compartido y añade invariantes de Bob Ross. La fusión de PR #10 **no autoriza** aprobar la Guía Científica, el guion o el video.


## QA posterior a la integración — alcance Bob Ross

- El banco editorial canónico sigue siendo `QUESTIONS_MASTER.md` + `questions_master.json` con **14 investigaciones**; `QUESTION_BANK.md` mantiene doce antecedentes solo como archivo histórico.
- `tests/test_entry_pack.py` se migró para verificar los 14 IDs, disparadores O2/O3 explícitamente condicionales, planes con baseline/modelo/estadística, 24 familias de modelos **en el catálogo compartido**, integridad de muestras y la única sección HTML de preguntas.
- Se recalculó el SHA-256 sobre el contenido original obtenido de GitHub: `42045c8b8aaa8296095d6b294927fb9d0f73a57259f59b560c375844c0fe01cf` (403×69; 66,315 bytes), y la muestra cruda de 13 filas coincide con observaciones reales. Esto corresponde a validación estructural vía JavaScript, **no** ejecución Python.
- Pendiente en un checkout real: `python discovery_labs/episodes/bob-ross/entry_pack/validate_pack.py`, `python -m unittest discover -s discovery_labs/episodes/bob-ross/tests -v`, `node discovery_labs/episodes/bob-ross/intake/qa_intake.cjs` y QA visual en navegador de V3.
- Estado: **Fase 0 lista para revisión; Fase 1 HTML no aprobada; Fases 2/3 bloqueadas**. No se han entrenado modelos, ejecutado análisis estadístico ni creado contenido audiovisual.
