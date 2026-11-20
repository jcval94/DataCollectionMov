# QA de la investigación · 19-11-2026

## Comprobaciones locales ejecutadas

| Comprobación | Resultado |
|---|---|
| Suite Bob Ross, incluye nuevas invariantes científicas | 42 tests PASS |
| Suite del validador compartido | 6 tests PASS |
| `run.py --check` | PASS; snapshot y conteos históricos |
| `entry_pack/validate_pack.py` | PASS; 14 modelos y 14 contrastes de diseño; no ejecuta los modelos |
| `shared/validators/validate_entry_pack.py` | PASS; contrato estático del banco y guía |
| `qa_static.cjs` del episodio heredado | PASS; sigue existiendo la UI anterior |
| `research/qa_guide.cjs` | PASS_STATIC_ONLY; 14 fichas, IDs, anchors, rutas locales, sintaxis JS y 381 episodios del inspector |
| `compileall` de shared y Bob Ross | PASS |
| `git diff --check` | PASS |
| Archivo recibido | Diez blobs coinciden con su MANIFEST; no se editó research_received |
| Segunda ejecución completa O1 | Siete artefactos numéricos/CSV idénticos byte a byte; [replication_check.json](replication_check.json) |
| Fisher independiente | 66 tablas frente a scipy.stats.fisher_exact; error absoluto máximo 2.22e−16. Scipy no es dependencia del pipeline |

Las pruebas nuevas comprueban: expectativa exacta de adyacencias por enumeración, corrección múltiple conocida, Fisher exacto de referencia, constantes sin falsa inhibición, no puentear huecos, matching invariante a nombres de cluster, conservación de informes, hashes de resultados y publicación progresiva solo con padre medido.

El manifiesto de O1 preserva hashes del diseño original al ejecutar; el banco recibió referencias de ejecución después. Los resultados numéricos no dependen de esa edición editorial. Manifiestos de O2 y guía fijan la revisión que consumieron. Los relojes/plataformas del manifiesto cambian entre ejecuciones y no se comparan como salida numérica.

El primer `diff --check` señaló finales CRLF de los CSV de investigación. Se fijaron atributos locales `-text` y `whitespace=cr-at-eol` para conservar sus bytes RFC 4180 y hashes; las comprobaciones contra main y el diff final pasan. No se alteraron los datos para resolver una advertencia de formato. Los dos SVG pasan parseo XML y tienen title/desc; esto tampoco acredita render visual.

## Pendiente de inspección visual

El navegador remoto no pudo abrir el servidor local (`ERR_CONNECTION_REFUSED`); no se certifican render, responsive móvil, navegación de teclado, interacción real del selector, contraste ni accesibilidad integral. El intento de inspeccionar la pestaña de error fue rechazado por la política de URL del navegador. No se continuó por vías alternativas de navegador.

Se comprobaron estructura y sintaxis; eso no reemplaza una prueba visual. La guía incorpora select nativo etiquetado, controles HTML details/summary, focus visible, alt de SVG, tabla textual y fallback noscript. Su comportamiento requiere verificación en navegador accesible antes de aprobación científica/editorial.

## Integración de PR #17

Se integró main `b12e577f36addce2e686d7768eeee7311aa0ac87` durante la revisión del PR #18. Se conservan sus templates, protocolo y tres tests. Total local final: 42 tests Bob Ross + 6 compartidos = 48 PASS. Tres paquetes HF validan contra JSON Schema draft 2020-12 (jsonschema como verificación de desarrollo); sus decisiones son PENDING y QA visual false. Tests stdlib comprueban resumen primero, IDs únicos, evidencia/rutas y ausencia de promoción O2 sin HF-02. No se simulan HF-03/HF-04 ni aprobación retrospectiva.

## CI de GitHub

El CI anterior de main se verificó en el SHA de merge #16, run 44579116224, success. El resultado del PR de esta rama se documenta en el PR al publicarlo; no se hereda de aquel run. Los workflows existentes cubren compileall, las suites unitarias, datos congelados y contratos. No ejecutan las permutaciones largas ni una prueba visual: esas se verificaron localmente según los límites anteriores.
