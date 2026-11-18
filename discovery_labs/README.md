# AI Discovery Labs · V3

La ampliación V3 es aditiva: [operación y resultados del Lote 0](docs/V3_BATCH0.md). Conserva sin modificación los snapshots, catálogos, evidencias y pilotos V2 descritos más abajo. El catálogo unificado para agentes aplica los contratos V3 sobre las 516 preguntas sin borrar sus diseños originales. V3 ejecuta 12 preguntas; seis de los 18 contratos del lote quedan bloqueados por datos ausentes. Los kits candidatos y la CI son verificables; ninguna clase está aprobada.

```sh
python discovery_labs/scripts/run_research.py
python discovery_labs/scripts/agent_tools.py catalog
python discovery_labs/tests/research_browser.py
```

## Base V2 preservada

Una biblioteca para transformar una pregunta en una investigación responsable con IA. Público: principiantes, práctica opcional de aproximadamente 45 minutos, con preparación fuera de clase. Corte editorial: 16 de noviembre de 2026.

## Estado comprobado

- **86 entradas únicas** conciliadas: 78 fuentes originales = 37 seleccionadas + 41 omitidas; más ocho propuestas posteriores.
- **516 preguntas diseñadas:** 270 heredadas con texto original y contrato de auditoría; 246 nuevas para las fuentes omitidas. Hay nueve preguntas con ejecución técnica y 507 sin ejecutar. Diseño no equivale a viabilidad comprobada.
- **86 fuentes con prueba de acceso fechada:** se conservan estados previos, metadatos y límites. Una portada, API de metadatos o muestra no valida el dataset completo.
- **Tres pilotos ejecutables offline**, con datos reales, derechos revisados para sus snapshots, hashes, tablas, gráficos, sensibilidad y dos o más rutas habilitadas.
- **19 antecedentes documentados externamente**, cinco registros de reproducción (tres pilotos V2 y dos análisis preexistentes) y 239 candidatos pendientes de lectura. Se registraron 86 búsquedas públicas; no son 86 revisiones bibliográficas exhaustivas ni 258 antecedentes validados.
- **Cero prácticas aprobadas para clase:** falta ensayo humano real de 45 minutos y revisión docente independiente. No se sustituye por tiempo de CPU.

## Abrir y ejecutar

Desde la raíz del repositorio, con Python 3.12 y dependencias preparadas antes de clase:

```bash
python -m pip install -r discovery_labs/requirements.txt
python discovery_labs/scripts/run_pilots.py
python discovery_labs/scripts/build_catalog.py
python discovery_labs/scripts/finalize_evidence.py
python discovery_labs/scripts/build_delivery.py
python -m unittest discover -s discovery_labs/tests -v
node discovery_labs/tests/dashboard_logic.cjs
```

Abrir `discovery_labs/dashboard/index.html` en un navegador. Es un archivo autocontenido: datos y gráficos embebidos, sin servicios externos, cuentas o seguimiento. Ofrece categoría, técnica, dificultad y viabilidad; muestra ranking, top por categoría, preguntas, antecedentes y bloqueadores. El HTML generado se regenera, no se versiona.

La lógica del dashboard pasó 14 checks. La prueba en Chromium real pasó en CI con Playwright 1.56.0 y Ubuntu 24.04: escritorio 1440×1000, móvil 390×844, filtros, exportación, imágenes y cero llamadas remotas o errores JavaScript. Se inspeccionaron las capturas. El navegador local quedó bloqueado por el entorno, por lo que esa limitación se resolvió mediante CI, sin relajar pruebas. [Lógica](evidence/dashboard_qa.json) · [Evidencia de navegador](evidence/dashboard_browser_ci.json).

## Navegar el sistema

| Recurso | Propósito |
| --- | --- |
| [Conciliación](catalog/reconciliation.json) | IDs canónicos, grupos 37/41/8 y hashes de entradas originales |
| [Fuentes](catalog/sources.json) · [CSV](catalog/sources.csv) | Metadatos declarados y verificados separados; desconocidos con cómo obtener evidencia |
| [Preguntas](catalog/questions.json) · [CSV](catalog/questions.csv) | Hipótesis, métrica, denominador, dos caminos, refutación y límites por pregunta |
| [Antecedentes](catalog/antecedents.json) · [CSV](catalog/antecedents.csv) | Distingue documentación, ejecución y candidato sin revisar |
| [Ranking](catalog/ranking.json) · [CSV](catalog/ranking.csv) | 86 fuentes, nueve criterios, pesos, top 10 y top 3 de cada categoría |
| [Auditoría de estado](catalog/audit_summary.json) | Conteos y requisitos todavía incumplidos |
| [Retail](pilots/uci-retail/README.md) | Neto firmado y cambio de denominador |
| [NBA](pilots/nba-elo/README.md) | Partidos únicos, calibración y fuga temporal |
| [Bob Ross](pilots/bob-ross-elementos/README.md) | Contraejemplos y agrupamientos inestables |
| [Alumno](templates/ALUMNO.md) · [Docente](templates/DOCENTE.md) | Secuencia de 45 minutos, elección, crítica a la IA y firma |
| [Búsquedas](evidence/search_log.json) | Consulta, fecha, URL y localizador; sin copiar artículos |

## Reproducibilidad y derechos

Cada piloto valida SHA256, esquema y dominio antes del análisis. Los tests bloquean red, repiten cálculos y gráficos, rechazan snapshots adulterados y prueban corrupción del dominio. Las pruebas no abren APIs ni ejecutan modelos. Las descargas originales pesadas se mantienen fuera de Git.

Para reconstruir snapshots, preparar los originales fuera de clase con `scripts/prepare_snapshots.py --download --cache /ruta/cache`, o proporcionar en esa carpeta los originales cuyos hashes constan en los manifiestos. El script rechaza versiones diferentes antes de reemplazar el snapshot. La alternativa offline de ejecución son los mismos datos reales incluidos; el dashboard ofrece además referencia precalculada para contingencias.

Todos los datos del piloto tienen atribución y licencia CC BY 4.0 en su manifiesto. Eso no extiende permisos a pinturas, vídeos o audio. Se eliminaron identificadores de clientes de retail, conservando un indicador de ausencia para estudiar el sesgo de exclusión. Los datos de estudiantes y sus respuestas no se recogen ni se guardan en este repositorio.

La igualdad exacta con las referencias originales de retail completo y Bob Ross quedó registrada en [reproducciones previas](evidence/prior_reproductions.json). El piloto retail V2 usa una selección por facturas y no se presenta como la reproducción de los importes del dataset completo.

## Lo que sigue abierto

Para las 83 fuentes sin snapshot de piloto siguen pendientes, según corresponda, licencia específica, universo físico, periodos observados, nulos/duplicados, revisiones y representatividad. La documentación declarada no cubre esas puertas. Cada ficha describe cómo comprobarlo; no se rellenan tamaños ni fechas a partir de intuición.

Los candidatos bibliográficos requieren leer el antecedente, cotejar su dataset y extraer método, resultado y limitaciones. No se promete que existan tres análisis independientes para todas las fuentes. Una guía o un mirror no cuentan como investigación exitosa por sí solos.

Las creencias D1/D2 son afirmaciones candidatas; su popularidad no se ha demostrado. Las hipótesis y métodos de las 507 preguntas no ejecutadas deben ajustarse al esquema real antes de ofrecerse en clase. No se fuerza una ruta con ingresos, costos, exposición o causalidad ausentes.

## Cambios pequeños de integración

1. Catálogo: conciliación, banco, evidencia de acceso y bibliografía con estados; sin activar nuevos recolectores.
2. Ejecución: snapshots minimizados, pilotos, tests, dashboard y CI offline. Mantener abierta la aprobación de aula.
3. Curso: documento de integración en `mvp-ds-course`, vinculado a esta versión; sin modificar niveles, pagos o calendario.
4. Tras el ensayo: producir release separado para alumno/docente; consumir únicamente un commit/release fijado y aprobado. No publicar guiones docentes en `dist/`.

## Vertical slice

Usuario: principiante que decide con IA. Entrada: pregunta votada y snapshot real verificado. Flujo: predicción → contrato medible → dos caminos → ejecución → adversario → firma. Salida: tabla/gráfico, magnitud, límite y decisión. Prueba manual: realizar la sesión completa con registro de tiempos e incidentes. Definition of Done: todas las puertas técnicas y pedagógicas, incluida esa sesión, con evidencia. Fuera de alcance: calificar alumnos, inferir causalidad o publicar automáticamente una clase. Próxima slice recomendada: ensayo humano del piloto retail y revisión visual en navegador.
