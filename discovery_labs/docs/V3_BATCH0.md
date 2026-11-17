# AI Discovery Labs V3 · Lote 0

Corte local: 16 de noviembre de 2026. Estado: implementación técnica candidata, sin aprobación de aula ni publicación. La auditoría y ampliación se apoyan en el PR #2, commit `0c5a0c555dc5f3a006d2bd7d16b904b463e95757`; el curso se inspeccionó en PR #101, `d702482bef99b12f19d0a3116a5aed6d7fc5f5ad`. Ambos estaban abiertos en borrador y con CI aprobada. [Línea base comprobada](../evidence/v3/baseline.json).

## Resultado funcional y alcance

Se conserva toda la evidencia V2. Un pipeline adicional lee sus mismos snapshots, construye Silver y Gold, ejecuta investigaciones permitidas y exporta figuras, storyboards y kits. El banco sigue teniendo 86 fuentes, 13 categorías y 516 preguntas; los 270 textos heredados no se reescriben. Los nuevos contratos se aplican por ID canónico mediante la interfaz de agentes, sin convertir retrospectivamente un diseño V2 en una ejecución V3.

| Fuente | Snapshot medido | Contratos | Preguntas ejecutadas | Figuras distintas | Formatos exportados | Rutas sin datos suficientes |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| UCI Retail | 7,293 líneas, 7 columnas | 6 | 3 | 3 | 12 | C, D1, D2 |
| NBA Elo | 2,622 equipo-partidos, 23 columnas | 6 | 3 | 4 | 16 | A, B, C |
| Bob Ross | 403 episodios, 69 columnas | 6 | 6 | 7 | 28 | Ninguna dentro del alcance de etiquetas |
| Total Lote 0 | Tres snapshots originales de V2 | 18 | 12 | 14 | 56 | Seis contratos bloqueados |

Una figura tiene dos tamaños, cada uno en PNG y SVG: 28 renderizados PNG y 28 SVG. No son 56 preguntas ni 56 hallazgos independientes. Hay 12 storyboards de siete actos, 12 guiones de screencast de 55 minutos y tres kits candidatos de alumno. Un ZIP contiene snapshot minimizado, diccionario, licencia/manifiesto, tablas, galería sin conexión y código Python ejecutable. El guion y las referencias de facilitación se generan fuera de ese ZIP.

Sólo Bob Ross dispone de las seis perspectivas ejecutables. Retail y NBA ofrecen tres rutas en sus kits candidatos: las otras se explican, pero no se pueden votar. Por ello no se declara finalizado el lote conforme a una clase con seis opciones por fuente. Ninguna práctica tiene `CLASS_READY` ni `PUBLISHED`.

## Cambios que aportan nueva evidencia

- **Retail:** Silver conserva todas las filas, motivos acumulables de exclusión e importes Decimal exactos. Gold reconcilia bruto, créditos y neto con V2. Contrasta duplicados y ausencia de ID por línea/factura. Un mes no permite estacionalidad anual; no hay costos para margen ni IDs para recurrencia.
- **NBA:** verifica rival, marcador, fecha, localía, fase, Elo y probabilidades recíprocas. Reconstruye 15 series completas y elige favorito con Elo anterior al primer partido. Compara Brier con p=0.5 mediante diferencias emparejadas y sensibilidad por fechas. Distingue 1,311 partidos únicos de 1,309 con localía: dos son neutrales. No transforma victorias locales en un efecto causal.
- **Bob Ross:** añade selección de doce episodios por cobertura de etiquetas, baseline cronológico y cien selecciones aleatorias. Compara invitados con anfitrión en un dotplot real. El clustering se contrasta con treinta permutaciones de marginales. El control de contaminación mantiene muestra, Euclídea y k=4, cambiando sólo la escala de temporada. Ausencia de `TREE/TREES` no se confunde con ausencia visual de cualquier árbol: `PALM_TREES` se explicita fuera de esa definición.

Los resultados y limitaciones se calculan en `research/results.json`; ninguna conclusión se fija para conseguir un relato. La silueta de la representación observada y una baja estabilidad entre distancias pueden coexistir: ninguna demuestra cuatro estilos naturales.

## Ejecutar antes de clase

Desde la raíz, con Python 3.12 y las dependencias fijadas:

```sh
python -m pip install -r discovery_labs/requirements-ci.txt
python discovery_labs/scripts/run_research.py
python -m unittest discover -s discovery_labs/tests -v
python -m playwright install chromium
python discovery_labs/tests/research_browser.py
```

`run_research.py` no descarga datos ni consulta modelos. La ingesta de originales sigue usando `prepare_snapshots.py --download --cache /ruta/cache`, antes de clase, verificando los hashes originales. En Retail, Bronze del paquete es el snapshot V2 previamente minimizado; no se vuelve a publicar un original con identificadores de clientes.

Salida por fuente en `discovery_labs/output/v3/<source_id>/`:

| Carpeta/archivo | Contenido y verificación |
| --- | --- |
| `bronze/receipt.json` | Procedencia, licencia, hash, bytes y selección del snapshot intacto |
| `silver/records.csv` | Tipos corregidos, fila original y motivos de exclusión, sin perder registros |
| `quality/` | Perfil medido, reglas, nulos/cardinalidades/extremos, memoria y transformaciones |
| `gold/*.csv` | Tablas de pregunta y sensibilidad; grano y denominador definidos en contratos |
| `research/` | Contratos específicos y resultados cuantitativos por ID |
| `visualization/` | PNG/SVG de móvil/proyección, alt, metadatos y hashes de tabla/código/datos |
| `education/` | Registro del alumno, galería y storyboards con bifurcaciones |
| `teacher/` | Facilitación, referencias y formato de ensayo; sólo preparación local |
| `student-offline.zip` | Distribución candidata de alumno mediante lista explícita de archivos |
| `gates.json` | Puertas por pregunta; ensayo y publicación cerrados |
| `receipt.json` | Huella de entradas/código/contratos/entorno y hashes de todos los artefactos |

Las salidas regenerables están ignoradas por Git. La CI conserva capturas y ZIP de alumno como artefactos; **no sube `teacher/`**. No publicar el árbol `output/` completo ni usar un parámetro de URL como protección docente. Los resultados de investigación sobre datos públicos no son una clave de evaluación del curso; no se incorpora ninguna respuesta de retos, tolerancia o rúbrica de calificación al curso.

## Reproducción, cache y recuperación

La cache verifica contenido, snapshot, manifiesto, diccionario, contrato, código, Python y dependencias. Una alteración invalida la cache; `--force` regenera en staging. Un fallo deja un error JSON y conserva la última salida íntegra; la nueva ejecución sólo se promueve cuando tiene su recibo. Para verificar un resultado existente:

```sh
python discovery_labs/scripts/agent_tools.py verify --case nba-elo
python discovery_labs/scripts/agent_tools.py results --case nba-elo --question D10-D1
```

La interfaz JSON admite `catalog`, `schema`, `quality`, `run`, `results`, `storyboard` y `verify`. `catalog` devuelve las 86 fuentes y 516 preguntas con estados V3 superpuestos. `run` exige fuente y pregunta permitidas; rechaza rutas bloqueadas o ajenas. Usa proceso hijo con 60 s de pared, 50 s de CPU, 4 GiB de espacio de direcciones, archivos de hasta 32 MiB y red deshabilitada. El entorno del hijo no hereda tokens API. No admite comandos, consultas SQL o Python arbitrarios. Estos controles acotan este ejecutor de código confiable, no constituyen una sandbox para código hostil. Un MCP nuevo no aporta valor todavía: puede envolver estas herramientas cuando haya un cliente y autenticación concretos, sin abrir un servicio permanente.

## Visualización y QA

Cada figura está vinculada a pregunta y CSV con hash. Las etiquetas incluyen periodo, unidades, denominador, atribución y prefijos de hashes; los metadatos conservan SHA256 completos y fuente. Las variantes móviles reducen categorías visibles cuando corresponde y lo declaran. Sus asignaciones y cálculos permanecen iguales.

La revisión encontró un recorte de la leyenda de color en el heatmap móvil y una nota exterior que repetía el número de categorías de la variante equivocada. Ambos se corrigieron. Los tests de límites de texto consideran sólo marcas realmente dibujadas por Matplotlib. La repetición detectó además una configuración tipográfica global dependiente del orden de ejecución; se fijó antes de crear cada figura.

Chromium comprueba las 12 rutas en 1440×1000 y 390×844: 24 combinaciones, 28 capturas de figuras, decodificación, alternativas de texto, revelación tras apuesta, ausencia de rutas bloqueadas, cero errores JS, cero red y ningún desbordamiento horizontal. Las capturas y figuras fueron inspeccionadas; la revisión exacta se liga a hashes en `evidence/v3/visual-review.json`. Esa revisión del asistente **no** es ensayo humano ni revisión docente independiente. SVG tiene la misma figura y metadatos; la revisión de navegador usa los PNG del paquete.

## Criterios de calidad y aprobación

[Rúbrica de 100 puntos](../contracts/rubric100.json): datos 20, rigor 20, preprocesamiento 15, visualización 15, storytelling 15, aula 10 y mantenimiento 5. Cada dimensión contiene criterios observables. No se asigna una puntuación global sin revisión independiente. Licencias incompatibles, privacidad, cálculos incorrectos, fuga, inferencia no sustentada y gráficos contradictorios son vetos aunque el promedio fuera alto.

Las puertas se aplican a pregunta/snapshot, no a toda una fuente por transitividad. `DATA_READY` exige validación; `RESEARCH_READY` exige ejecución; `VISUAL_READY` exige revisión del render exacto; `STORY_READY` requiere siete actos con evidencia; `CLASS_READY` necesita ensayo humano y revisión independiente. `PUBLISHED` requiere distribución autorizada e integración. Las dos últimas permanecen cerradas en esta entrega.

## Progreso con denominadores explícitos

| Dimensión | Lote 0 | Biblioteca completa |
| --- | --- | --- |
| Inventario preservado | Tres fuentes del lote identificadas | 86/86 = 100% |
| Procesamiento V3 validado | 3/3 = 100% | 3/86 = 3.5% |
| Contratos específicos V3 | 18/18 = 100% | 18/516 = 3.5%; los 516 diseños V2 permanecen |
| Investigación ejecutada | 12/18 = 66.7% | 12/516 = 2.3% |
| Preguntas con figuras V3 revisadas | 12/18 = 66.7% | 12/516 = 2.3% |
| Narrativas ligadas a ejecución | 12/18 = 66.7% | 12/516 = 2.3% |
| Fuentes con las seis rutas técnicamente preparadas | 1/3 = 33.3% | 1/86 = 1.2% |
| Aprobación pedagógica | 0/3 = 0% | 0/86 = 0% |

No se resume en un porcentaje global. Las seis rutas bloqueadas no se suman como ejecutadas ni como clases listas. Los tiempos de CPU constan en cada runtime y no prueban los 45 minutos de aula.

## Lote 1: preflight realizado, ejecución sin iniciar

[Siete fichas de acceso, derechos y QA](../evidence/v3/batch1-preflight.json). Se verificaron documentos primarios del productor; no se descargaron ni validaron siete datasets completos. StatsBomb conserva su ID, pero su PDF restringe redistribución y explotación comercial: [lectura, localizadores y hash](../evidence/v3/statsbomb-rights.json). Se selecciona como sustituto operativo a evaluar el dataset de eventos de fútbol de Pappalardo/Massucco, cuyo descriptor declara CC BY 4.0; su ítem, versión y bytes aún deben verificarse. No se añade una entrada número 87 al inventario.

ECOBICI requiere términos del CSV concreto y versión de estaciones; OpenFlights es histórico y exige revisar condiciones para cada distribución; NASA necesita consulta/tabla/referencias y tratamiento de límites; NYC exige denominadores de inspección; Open Food Facts distingue licencias de datos/imágenes y unidades; Airbnb necesita minimización y política de distribución. Ninguno recibe `DATA_READY` por haber leído una página.

## Ensayo humano preparado y próximo trabajo

Cada `teacher/ENSAYO.json` solicita pregunta votada, tiempos observados por segmento, incidentes, identificador anónimo del observador, revisión docente y correcciones. Realizar primero un ensayo con las seis rutas de Bob Ross disponibles y una sola votada. El principiante debe explicar una unidad, cambiar o defender su predicción, corregir a la IA y cerrar con argumento y límite. No registrar nombres ni respuestas del alumno en un repositorio público.

Supuestos: actividad formativa opcional, entorno preinstalado, snapshots históricos, sin evaluación automática ni descarga en vivo. Riesgos abiertos: seis preguntas requieren datos adicionales; derechos específicos del Lote 1; revisión docente y tiempos reales de aula; visuales conservan legibilidad técnica pero aún necesitan prueba con alumnos y proyector real. Próxima slice técnica: snapshot pequeño y versionado de NASA u OpenFlights tras cerrar derechos de distribución, usando estos mismos contratos sin imponerles el análisis de los pilotos tabulares.
