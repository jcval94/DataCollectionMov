# Auditoría transversal de DataCollectionMov — 5 de noviembre de 2026

Base revisada: `8a222d541a599d7cffde368191d99fac919ff9e4`. Se revisaron estructura, paquete Python, recolectores, nueve workflows de recolección, almacenamiento, scripts de descubrimiento, catálogo, plan docente y SubRepo. El árbol contiene **10,587 archivos y 3,349,012,655 bytes (~3.35 GB)**. La revisión del histórico fue de inventario y manifiestos seleccionados, no lectura ni validación de cada registro de esos 3.35 GB.

La auditoría encontró fallos concretos y deja correcciones, pruebas y CI. No equivale a declarar que todas las fuentes están disponibles o que cada workflow produce datos completos. Se conservaron históricos y material educativo; se retiró únicamente una caché temporal de autenticación.

## Hallazgos y correcciones

| Prioridad | Hallazgo comprobado | Cambio / estado |
| --- | --- | --- |
| Alta | `data/tmp/metrobus_auth_cache.json` estaba versionado y contenía URLs AWS firmadas con token, firma y credencial temporal. | Retirado del árbol y añadido `/data/tmp/` al nuevo `.gitignore`. Las URLs observadas caducaron el 5 nov a las 09:40:29 UTC, antes de esta revisión. Las versiones históricas siguen en Git; retirar un archivo no elimina su historia. No se publican aquí valores ni URLs firmadas. |
| Alta | Un `MAPS` vacío impedía recurrir a `GOOGLE_MAPS_API_KEY` por usar `getenv` anidado; TomTom tenía el mismo patrón con su alternativa. | Elegir primer valor no vacío, conservando precedencia existente: MAPS → GOOGLE_MAPS_API_KEY; TOMTOM → TOMTOM_KEY. Aplicado también al generador de rutas de incidentes. |
| Alta | Rutas sin duración podían obtener score cero y nivel Bajo; errores con duración podían contaminar la escala. | Desconocidos permanecen NaN/sin nivel; normalización excluye rutas no válidas. Las observaciones válidas conservan la fórmula y pesos existentes. Los CSV ya publicados no se reescribieron: el cambio aplica a nuevas ejecuciones. |
| Alta | `append_artifact_manifest` reemplazaba los artefactos anteriores al guardar otro en el mismo snapshot. | Conservar lista y actualizar por nombre, verificando identidad de manifiesto. |
| Media | Un ID de snapshot repetido sobrescribía el CSV histórico y el actual. | Crear histórico con exclusión y rechazar colisiones; reemplazo del actual mediante archivo temporal. No se implementa una transacción atómica de toda la corrida: aún puede haber publicación parcial entre tablas. |
| Media | Manifiestos nuevos de tablas no registraban hash; metadatos entrantes de otro snapshot podían conservarse sin actualizar. | SHA-256 del CSV completo y metadatos de captura renovados. Sin backfill de miles de manifiestos anteriores. |
| Media | Lectura de `current` infería llaves numéricas y podía perder ceros iniciales. | Leer como texto campos terminados en `_id` y claves postales/geográficas explícitas. No se afirma que pueda recuperar ceros ya perdidos. |
| Media | `daily_weekdays`, `hourly_weekdays` y `every_2_hours_weekdays` del ejecutor de notebook devolvían verdadero también en domingo. | Respetar lunes–viernes. `daily` sigue incluyendo fines de semana. Los horarios dentro de un día siguen a cargo de los workflows. |
| Media | Inputs de mes se interpolaban directamente dentro del shell del workflow ECOBICI histórico; tampoco se validaban antes de consultar la fuente. | Pasar por variables de entorno y array Bash con comillas; validar formato/mes y orden antes de red. |
| Media | La excepción final de DENUE podía mostrar una URL con el token en la ruta. | Mensaje con tipo de error e intentos, sin URL/cuerpo ni cadena de excepción. Se prueba con un token ficticio. |
| Media | No había suite de regresión ni workflow de validación independiente de recolectores. | Añadidos `tests/test_audit_regressions.py`, extra `.[audit]` y workflow de lectura sin secretos, con checkout disperso para no descargar históricos. |
| Baja | `datetime.utcnow()` en almacenamiento genera deprecaciones. | UTC explícito en almacenamiento, preservando formato Z. Otros módulos antiguos aún tienen llamadas a revisar gradualmente. |

## Pruebas ejecutadas

**13 pruebas pasan** con las correcciones. La misma suite, aplicada a los archivos originales del commit base, obtiene **12 fallos y 1 acierto**. Son regresiones reproducidas, no trece fallos distintos: hay parametrización de periodicidades y meses inválidos.

| Caso de prueba | Resultado |
| --- | --- |
| Hash, reemplazo de metadatos y rechazo de colisión sin alterar current | PASS |
| Dos artefactos en un snapshot; actualizar uno sin borrar el otro | PASS |
| Tres periodicidades de días laborables; domingo y lunes | PASS × 3 |
| MAPS vacío usa la alternativa sin hacer petición real | PASS |
| Ruta no existente/faltante no recibe criticidad baja y no altera escala válida | PASS |
| Cuatro combinaciones inválidas de meses rechazadas antes de red | PASS × 4 |
| Error DENUE no expone URL/token ficticio | PASS |
| Ocho contratos del piloto retail se mantienen | PASS |

Otras comprobaciones:

- `compileall` en src, scripts y scripts de SubRepo: PASS.
- JSON de catálogos y resultados de fuentes: 5 archivos parseados, PASS.
- YAML de workflows: 10 archivos parseados incluyendo el nuevo validador, PASS. Esto no sustituye una ejecución en Actions ni `actionlint`.
- Plan de exploración: 72 fuentes, 216 preguntas y referencias válidas, PASS.
- Retail `--self-check`: ocho comprobaciones, PASS; no se volvió a descargar el archivo completo ni a recalcular todos sus importes.
- Demo DOF/Git: ejecutada en repositorio temporal, dos commits, un cambio y árbol limpio, PASS.
- `pip check`: sin requisitos rotos en el entorno instalado; no sustituye una auditoría de vulnerabilidades o un lockfile.
- Escaneo acotado de patrones de claves Google/GitHub: 78 archivos de texto materializados de hasta 2 MB, sin candidatos. No fue escaneo exhaustivo de historia, binarios o todos los archivos de datos. El hallazgo de URLs firmadas se verificó por separado.
- `git diff --check`: PASS.

### Consultas públicas nuevas

[Evidencia, registros e imagen en el README de fuentes](source_checks/README.md) · [Resultados JSON](source_checks/results.json).

| Fuente | Petición de esta auditoría |
| --- | --- |
| ECOBICI GBFS | DATA_SAMPLE |
| USGS sismos | DATA_SAMPLE |
| Met arte | DATA_SAMPLE |

Las tres operaciones públicas se ejecutaron sin credenciales personales ni APIs de pago. No se sobrescribió el informe acumulado de 72 fuentes. Los tests anteriores de las otras fuentes conservan sus fechas; no se afirma que se hayan reprocesado aquí.

## Automatizaciones y datos observados

[Inventario de evidencia y últimos manifiestos por fuente](evidence.json).

Se inspeccionaron 35 ejecuciones recientes de Actions: todas tenían `success`. La campaña TomTom puede terminar con éxito fuera de ventana sin consultar ni producir datos; por eso un estado verde no acredita ingesta. No se modificaron horarios ni se activó la campaña, y no se ejecutaron consultas de Google, DENUE o Metrobús con secretos.

| Fuente | Último manifiesto de tablas observado (UTC) | Evidencia de filas |
| --- | --- | --- |
| Metrobús | 2026-11-05 06:40:32 | 829 posiciones; 829 enriquecidas; alertas y trip updates con cero filas. Cero alertas no demuestra por sí mismo error. |
| TomTom | 2026-11-05 07:00:08 | 12 puntos de flujo y 458 incidentes. |
| ECOBICI | 2026-11-05 07:11:27 | 677 filas de estado y 677 enriquecidas. |
| Google Routes | 2026-11-04 20:30:56 | 18 elementos de matriz/score, 8 pares y 4 modos; cantidad no garantiza todas las rutas exitosas. |
| DENUE | 2026-10-08 16:27:53 | 10,591 registros sector 61; 881 de educación superior estimada. Cadencia mensual configurada, siguiente día 8. |

Los tiempos son los del manifiesto, no una prueba de frescura del proveedor. La revisión de 35 ejecuciones no cubre toda la historia ni explica todos los retrasos entre cron y comienzo real. Las alertas de frescura y la distinción OK/parcial/omitido son trabajo prioritario posterior.

Hay **46 tablas configuradas; 24 sin CSV current** en el árbol auditado. Todas esas 24 estaban habilitadas en configuración: 11 GTFS estáticas y 13 de históricos/resúmenes ECOBICI. No se inventaron archivos ni se lanzó una descarga masiva para llenar el hueco. Algunas tablas GTFS son opcionales en un feed; la ausencia de routes/stops y del histórico normalizado sí merece investigar las ejecuciones específicas. El realtime de Metrobús descarga estático como fallback pero no lo persiste como tablas estáticas en esa misma función.

## Catálogo, enseñanza y pilotos

Se preservaron las 72 fuentes, sus muestras y errores, las 216 preguntas, las cuatro skills documentadas y el plan docente de 22 clases. El estado de un piloto no se confunde con una clase lista ni con una evaluación de un modelo de IA. La auditoría no modifica rúbricas, calendarios o plataforma del curso.

El piloto retail y el validador de exploración usan comprobaciones con `assert`; ejecutar con `python -O` podría omitir algunas. Utilizar comandos normales de los README; migrar invariantes críticas a excepciones explícitas es una mejora posterior. Las dependencias de PDF/imagen/gráfica se agrupan ahora en el extra opcional de auditoría; los recolectores mantienen sus dependencias originales.

## Pendientes priorizados

1. **P1 — cobertura:** investigar los workflows GTFS estático/ECOBICI histórico y recuperar un corte acotado y validado. No interpretar configuración habilitada como datos disponibles.
2. **P1 — almacenamiento:** plan de archivo incremental y formatos compactos con manifiestos/punteros, preservando originales. Git ya contiene ~3.35 GB en el árbol; no se borraron históricos ni se reescribió historia durante esta auditoría.
3. **P1 — observabilidad:** reportar recolección completa, parcial, omitida y fallida; vigilar frescura por tabla. Google captura errores parciales y TomTom conserva códigos de error de puntos: fila no equivale a dato válido.
4. **P1 — publicación concurrente:** varios workflows escriben docs/tablas.md y hacen pull/rebase/push sin reintento. Evitar un único grupo global que pueda descartar corridas pendientes; diseñar publicación con reintentos y comprobar conflictos antes de generalizarla.
5. **P2 — autenticación:** el fallback local Metrobús aún no verifica expiración antes de usar caché; nunca versionarla. Revisar historia según política de exposición; las URLs concretas observadas ya caducaron.
6. **P2 — procedencia:** hash para artefactos, contratos de esquema/llaves por tabla y validación histórica por lotes. Los cambios actuales añaden hashes de CSV hacia adelante, no certifican el archivo anterior completo.
7. **P2 — rutas de incidentes/SubRepo:** revisar aparte datos semilla `fallback_seed`, estimaciones `fallback_*`, ruta local Windows por defecto y Apps Script; no se ejecutó el generador que puede hacer llamadas pagadas. La presencia de GeoJSON/HTML no valida ubicación real, capacidad o despacho de unidades.
8. **P2 — compatibilidad:** lockfile/matriz de Python y escaneo de dependencias. Pruebas locales en Python 3.12; nuevo CI declara 3.11, aún por confirmar en Actions.
9. **P2 — fecha local:** `parse_run_date`/ejecutor legado aún usan `date.today()` del host y no la zona de configuración. Revisar etiquetas de día en capturas UTC cercanas a medianoche local sin alterar retrospectivamente los originales.
10. **P3 — documentación:** `run --notebook Get_Datos_API.ipynb` es un camino legado citado por docs.py aunque ese archivo no existe en la raíz auditada. Priorizar el comando `source` usado por los workflows. La cobertura curricular/documental no equivale a ensayo pedagógico.

## Reproducir sin secretos

```bash
python -m pip install -e '.[audit]'
python -m pytest -q tests
python -m compileall -q src scripts SubRepo/scripts
python scripts/render_exploration_plan.py --check
python scripts/run_discovery.py --self-check
python examples/dof_git/demo_git.py --report /tmp/dof-audit.md
# Reintento público opcional; resultados separados del informe acumulado:
python scripts/probe_catalog_sources.py --only ecobici-gbfs met-arte usgs-sismos --output /tmp/source-audit
```

Las pruebas de almacenamiento escriben sólo en directorios temporales. La CI nueva valida código y catálogo, no ejecuta recolectores, publica datos ni usa secretos. Cambiar de versión del entorno o de las fuentes puede producir resultados distintos: conservar URL, corte, hash y versión del código al comparar.
