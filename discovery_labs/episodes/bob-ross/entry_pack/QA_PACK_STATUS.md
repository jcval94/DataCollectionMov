# QA del Paquete de Entrada y Question Forge v2

## Integración y ejecución verificadas · 18 nov 2026

- Los PR [#11](https://github.com/jcval94/DataCollectionMov/pull/11), [#5](https://github.com/jcval94/DataCollectionMov/pull/5) y [#10](https://github.com/jcval94/DataCollectionMov/pull/10) quedaron **MERGED** en `main`.
- El workflow [AI Discovery Labs QA · run #44427475768](https://github.com/jcval94/DataCollectionMov/actions/runs/44427475768) concluyó **SUCCESS**, incluidos compilación de Python, unit tests compartidos, unit tests Bob Ross, `run.py --check`, contrato general y validador particular de 14 investigaciones.
- El workflow general del repositorio también concluyó **SUCCESS** sobre el mismo PR de cierre.
- **No se entrenaron modelos de investigación**, no se ejecutaron los Deep Research, no se aprobaron conclusiones clínicas, guion audiovisual ni video.
- Pendiente de forma deliberada: QA de navegador real de HTML V3, derechos de imágenes, segundo episodio real y aprobación humana de la guía. Estos no son requisitos para declarar completada la **integración de código**.


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

- La ejecución **local independiente** no se realizó; sí pasó el validador correspondiente en GitHub Actions.
- Render real en Chromium y revisión responsive, teclado/foco, contraste y gráficos de la guía V3 (la versión V2 anterior tuvo revisiones de navegador, pero **no** cuenta como QA de V3).
- Investigación histórica en profundidad, especialmente fechas de diagnóstico/grabación/emisión.
- Derechos de cada imagen original, licencias para miniaturas, políticas de hotlinking.
- Entrenamiento, contrastes estadísticos nuevos, ajuste con Optuna, análisis fuera de muestra o causalidad (fuera del alcance de CI/Paquete de Entrada).
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

**Pruebas de este cambio:** comprobaciones de estructura del contenido y coincidencia de 14 IDs antes del commit. Pendiente ejecutar el script Python en entorno canónico, tests del episodio y navegador real. La divergencia entre ramas se resolvió y PR #10 fue fusionado a `main` tras preservar contratos legacy y comprobar que el diff quedaba exclusivamente en Bob Ross. La ejecución automática de tests y QA visual se registra por separado.

## Integración compartida
PR #11 (núcleo), PR #5 (base Bob Ross) y PR #10 (Paquete de Entrada) integrados en `main`. La skill, catálogo y plantilla viven solamente en `discovery_labs/shared/`. El wrapper `entry_pack/validate_pack.py` delega al validador compartido y añade invariantes de Bob Ross. La fusión de PR #10 **no autoriza** aprobar la Guía Científica, el guion o el video.


## PR #12 — conciliación de QA posterior al merge

- Se preserva el registro de CI exitoso anterior y la información más reciente de `main`; ese resultado **no equivale** a que ya se haya ejecutado la suite del PR #12.
- `tests/test_entry_pack.py` comprueba el banco canónico de **14 investigaciones**, sus disparadores condicionales O2/O3 y la distinción entre modelo y ejercicio estadístico.
- Los recursos compartidos se resuelven en `discovery_labs/shared/model_catalog/MODEL_SET.md` y `discovery_labs/shared/skills/question-forge/SKILL.md`, evitando rutas locales eliminadas.
- `entry_pack/QUESTION_BANK.md` permanece como antecedente histórico; `questions_master.json` es el único banco científico vigente.
- La guía HTML científica continúa pendiente de aprobación humana. No se autoriza guion ni video.
