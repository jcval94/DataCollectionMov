# QA del Paquete de Entrada y Question Forge v2

**Fecha:** 2026-11-18. **Contexto:** inspección estática contra la rama `feat/bob-ross-entry-pack-question-forge` y archivos recuperados desde GitHub. **No se entrenó ningún modelo ni se ejecutó Deep Research completo.**

## Comprobaciones verificadas en la rama

| Criterio | Resultado |
|---|---|
| Banco único `questions_master.json` | **PASS:** 14 preguntas, 14 IDs únicos |
| Preguntas O1 + O2 + O3 | **PASS:** 14/14 contienen las tres propuestas (O2/O3 condicionales, NO ejecutadas) |
| Modelos seleccionados | **PASS:** 14/14 señalan un `model_primary_id` de los 24 del `MODEL_SET.md` |
| Ejercicios estadísticos independientes | **PASS:** 14/14 incluyen propuesta formal de prueba/intervalo/remuestreo |
| MD vs JSON | **PASS:** los 14 IDs figuran en `QUESTIONS_MASTER.md` y JSON |
| Muestra | **PASS estructural:** 13 registros originales y 13 derivados, metadatos `403×69` |
| Skill reusable | **PASS:** `skills/question-forge/SKILL.md` versión 2.0.0 |
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
