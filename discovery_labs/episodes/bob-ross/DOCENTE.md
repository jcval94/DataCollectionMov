# Guía de facilitación · Los árboles que faltaban

**Estado:** documento docente dentro de un repositorio público; NO es un solucionario privado, ni se publica en el portal del alumno. Falta ensayo humano de 45 minutos y revisión independiente.

## Objetivo pedagógico

Que cada alumno convierta una pregunta en una métrica y un denominador, use IA para preparar análisis, cuestione su primera interpretación y redacte una conclusión válida. El éxito **no** es aprender un algoritmo ni obtener una sorpresa obligatoria.

## Cronograma de 45 minutos

| Minutos | Acción docente | Señal de aprendizaje |
|---|---|---|
| 0–5 | Mostrar título y seis rutas. Votar una sin revelar métricas. | Elección argumentada |
| 5–10 | Preguntar «¿qué significa mejor, todos, rentable o diferente?». Recoger predicciones. | Métrica y unidad |
| 10–14 | Pedir a IA dos caminos; el grupo elige. | Decisión consciente |
| 14–28 | Usar el HTML; si el entorno está preparado, ejecutar los scripts y mostrar SVG. | Una tabla y una gráfica |
| 28–36 | Proponer un contraejemplo, otra distancia o un nuevo denominador. | Respuesta matizada |
| 36–42 | Debatir límites, sesgos y qué no vemos en estos datos. | No confundir asociación con causa |
| 42–45 | Pedir una conclusión con n/N, límite y pregunta nueva. | Tarjeta de descubrimiento |

Elige **una** ruta, no intentes terminar las seis en la misma clase.

## Datos de referencia (no inventados)

Fuente FiveThirtyEight original fijada por hash:

- **403 episodios**, 69 columnas; 67 etiquetas binarias.
- **381** episodios con GUEST=0 y **22** con GUEST=1.
- Entre los 381: **345** con TREE o TREES, **36** sin ambas etiquetas.
- Entre los 22 invitados: **16** con TREE o TREES.
- Entre el anfitrión: **150** con MOUNTAIN, MOUNTAINS o SNOWY_MOUNTAIN; **48** de esos 150 sin SNOW ni SNOWY_MOUNTAIN.
- Clasificación operacional **por reglas, no por aprendizaje**: agua/costa **72**, montañas **135**, bosques **169**, otros **5**. El orden de prioridad importa.
- La fuente anterior `examples/bob_ross_clustering/` ejecutó otro experimento de KMeans con distancias euclídeas en 12 familias y cuatro salas: tamaños **124, 118, 100, 39**. **No confundir con** la clasificación por reglas de este episodio o con k-medoids Jaccard.
- El nuevo `clustering.py` obtiene las salas de k-medoids para Jaccard/Euclídea. **Verificar sus cifras tras ejecutar el comando**; no presentarlas como patrones naturales ni como equivalentes al KMeans de otro proyecto.

Los números hacen referencia a la **codificación del archivo**. No atribuirlos a una revisión manual exhaustiva de 403 cuadros.

## Cómo conducir las seis rutas

### A — Negocio: el museo ficticio

Encargo: organizar obras en cuatro salas para que una persona visitante entienda sus motivos, sin saturación excesiva. Pregunta inicial: «¿Cómo definirías una sala?». Mostrar los tamaños de la regla fija y preguntar si el caso 'Otros' es razonable.

**Trampa honesta:** no tenemos entradas vendidas, costos, capacidad real, gustos ni ROI. Un problema monetario real requiere enriquecer la fuente. El objetivo actual es una decisión operacional hipotética. No inventar dinero.

### B — Social: anfitrión frente a invitados

Crear tabla de conteos con 381 y 22 denominadores. Mostrar por qué las barras de conteo absoluto no permiten comparar proporciones sin corrección; comparar 345/381 frente a 16/22.

**Trampa:** pequeña población de invitados; grupos no asignados al azar; no inferir discriminación, elección intencional, raza, género ni efectos causales.

### C — Descubrimiento: cuatro salas

Primero ver las doce familias, luego discutir si deberían pesar igual. El docente puede ejecutar `python clustering.py --write`, mostrar k-medoids Jaccard vs Euclídea y el ARI. Pedir representantes reales y explicar que una distancia para binarios es una elección metodológica.

**Trampa:** aumentar un score no demuestra validez artística. Elegir k=4 es el encargo del museo, no un resultado científico de «cuatro estilos».

### D1 — Creencia popular: todos los cuadros tienen árboles

Si los alumnos creen que sí, basta mostrar uno de los **36** contraejemplos codificados en el grupo anfitrión; luego revisar el resto. Reconocer que el archivo codificado no equivale a ver cada cuadro.

**Trampa:** `TREE` y `TREES` deben combinarse por OR. Presencia codificada ≠ número de árboles.

### D2 — Creencia popular: montaña implica nieve

Población condicional: 150 episodios con montaña. Entre ellos 48 no tienen nieve codificada. Interpretar 48/150, no 48/381.

**Trampa:** `SNOWY_MOUNTAIN` forma parte simultáneamente de montaña y nieve. Correlación parcialmente mecánica.

### E — Detective de datos: ID como feature

Definir «similitud visual» con las doce familias. Preguntar qué representa la temporada y por qué un número grande puede dominar la distancia. Referenciar el experimento existente en `examples/bob_ross_clustering/reference/README.md` que añadió un identificador secuencial artificial.

**Trampa:** los silhouette de distintos espacios no son una escala universal de «mejor». Aquí el ID no responde a la pregunta del museo.

## Prompt docente de contraste

> «Revisa el análisis de Bob Ross como estadístico adversarial. ¿Cuál es la unidad? ¿Cuál es el denominador? ¿Qué variables son metadatos y no motivos? ¿Qué mediciones faltan? Busca un contraejemplo y una interpretación alternativa. No afirmes causalidad ni popularidad real a partir de una tabla de etiquetas.»

## Antes de impartir

- [ ] Ejecutar `python run.py --check` con hash correcto.
- [ ] Ejecutar `python run.py --write` y `python clustering.py --write`.
- [ ] Ejecutar `python -m unittest discover -s .../tests -v`.
- [ ] Inspeccionar gráficas SVG en proyector/móvil y contraste/legibilidad.
- [ ] Probar keyboard-only y lector de pantalla en `episode.html`.
- [ ] Cronometrar una sesión con alumnos principiantes: instalación fuera de clase.
- [ ] Documentar revisores, errores, tiempos por acto y resultados; no publicar como clase aprobada antes.

## Rúbrica formativa (10 puntos)

- Pregunta y población claras: 2
- Métrica y denominador correctos: 2
- Evidencia visible y trazable: 2
- Prueba adversarial sólida: 2
- Conclusión responsable y nueva pregunta: 2

Una respuesta «no alcanza la evidencia» puede obtener puntuación máxima si demuestra por qué.
