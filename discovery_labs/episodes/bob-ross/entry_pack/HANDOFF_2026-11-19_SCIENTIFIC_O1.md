# Handoff científico · Bob Ross · continuación 19-11-2026

Este documento sucede a HANDOFF_2026-11-19.md. La fuente de estado ejecutado es `../research/README.md`, los manifiestos de resultados y el PR de la rama `research/bob-ross-o1-20261119`. No tratar el handoff anterior ni los informes recibidos como resultados posteriores a esta ejecución.

## Qué se completó

- Base: main `ce757809214fd6d38ffede9f4130d3c68feb2469`. Confirmados merges #12/#14/#15/#16. PR #2/#4/#6/#7 fuera de alcance.
- Auditoría con hash, blob upstream y 403×69. 3,221 positivos; PERSON existe en S03E10; CHIMNEY no. Dos títulos duplicados, tres filas vacías y excepciones jerárquicas documentadas. Diez blobs de research_received íntegros, sin reescrituras.
- Tres DR confrontados de manera focalizada: 54 registros con estado independiente. No se volvieron a ejecutar los prompts ni se declaró verificada toda la biografía. Graten contiene 3,324 en resumen/3,224 en cuerpo; causa histórica de diferencia con CSV no resuelta. Smithsonian directo 404, evidencia solo indexada. NPR/KPBS es testimonio; Ball State da año 1988, sin episodio de rodaje.
- 10 H integradas una vez en las 14 BR canónicas: H1/H7→BR-10, H2→BR-01, H3/H9→BR-07, H4→BR-08, H5→BR-05, H6→BR-09, H8→BR-14, H10→BR-13 como extensión con target externo. No segundo banco.
- Ranking: BR-14 91, BR-07 85, BR-09 83 ejecutables; BR-10 85 bloqueada por permisos. Paleta jwilber tiene join técnico 403/403; no se ingirió ni modeló. MIT de BobRossColors no resuelve imágenes upstream ni independencia de fuentes.
- O1 de BR-14 (403 episodios, 372 transiciones): cuatro pruebas de inhibición no sobreviven Holm. Nulo inconcluso, no equivalencia.
- O1 parcial BR-07: 66 pares con Fisher/BH; CABIN–WINTER 28 vs 11.96 esperados, lift 2.342, bootstrap temporadas 1.795–2.895; control estacional por permutación ≈.0001. No simbolismo ni causalidad; H3 sobre 26 minutos y tríos no ejecutados.
- O1 parcial BR-09: vacíos forman grupo propio en k=2…6. DR-05a activó solo su O2; O2 ejecutada: máximo del grid cambia k2→k3 al retirar vacíos; Euclídea cambia 179/381 asignaciones y quitar árbol 75/381 con matching. LOSO 31 reajustes ARI=1; representación 12 familias/64 etiquetas ARI .308. Estabilidad frente a temporada y sensibilidad frente a métrica no se contradicen.
- HTML V4 generado desde banco/resultados, 14 fichas en un índice, una O2 activada anidada en BR-09, ninguna O3 activa. No guion, storyboard ni video nuevos.

## Dónde leer y repetir

1. `../research/README.md`, `SOURCE_REVIEW.md`, `PROTOCOL.md`, `DR-05a.md`.
2. `../research/evidence/`: data_audit.json, episode_audit.csv, source_claim_matrix.csv, reconciliation.csv, ranking.json, palette_schema_review.json.
3. `../research/results/`: o1_results.json, 30,000 vectores nulos, 66 asociaciones, 381 asignaciones, run_manifest.json.
4. `../research/progressive_results/`: br09_o2.json, 31 reajustes, manifest.json.
5. `questions_master.json`: diseños originales conservados como PLAN_ONLY en design_status, con execution separado. `../research/execution_registry.json` registra estados de ejecución, no preguntas duplicadas.
6. `../research/QA.md`: 42 tests locales PASS, validadores y replicación O1 bit a bit; QA visual pendiente por acceso al navegador. CI del PR se verifica aparte.

```bash
cd discovery_labs/episodes/bob-ross
python research/audit.py
python research/reconcile.py
python research/experiments.py
python research/progressive.py
python research/render_guide.py
python -m unittest discover -s tests -v
python entry_pack/validate_pack.py
node research/qa_guide.cjs
```

El manifiesto O1 registra el banco original anterior a referencias de ejecución; commit `0f5b949bb51e31a075fe292dd74f455d8c1fed7f` preserva esa etapa. Reloj/plataforma del manifiesto pueden cambiar al repetir; los siete artefactos numéricos se replicaron idénticos en la misma versión Python.

## Qué sigue y qué permanece bloqueado

1. Revisión visual real de V4 en desktop, móvil y teclado; el navegador remoto no pudo acceder al servidor local. No darla por aprobada por pasar tests estáticos.
2. Revisar vacíos y excepciones del diccionario con activos autorizados, libro de códigos y doble anotación. No llenar tres valores para cuadrar 3,224.
3. Ampliar BR-09 con inicializaciones/algoritmos; O3 humana requiere permisos/evaluadores. Otras O2 permanecen condicionales. No transformar el p de CABIN–WINTER en mecanismo ni el nulo H8 en prueba de ausencia.
4. Resolver fuente/licencia de paletas para BR-10. Completar cronología/créditos solo para preguntas que los requieran. Salud/duelo no identificados desde CSV.
5. DR-04 especializado y DR-05b final diferidos; revisión bibliográfica de novedad no exhaustiva.
6. Aprobación humana explícita de commit científico antes de storytelling; otra aprobación antes de video. Crear PR no significa APPROVED ni autoriza audiovisual.

## Prompt de continuidad

Lee este handoff, research/README.md, SOURCE_REVIEW.md, PROTOCOL.md, DR-05a.md, execution_registry.json, los dos manifiestos y QA.md. Contrasta la rama/PR con main. Conserva originales y 14 IDs. Revisa resultados reales antes de ampliar; no repitas DR-01/02/03. Prioriza QA visual de V4, auditoría autorizada de vacíos/jerarquías y robustez algorítmica de BR-09. No abras otras O2/O3 sin trigger y evidencia, ni uses paletas/imágenes sin resolver permisos. Informa límites, nulos y novedad no demostrada. Actualiza PR/handoff y no inicies audiovisual sin aprobación explícita.
