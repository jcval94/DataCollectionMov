# Kit del alumno · Los árboles que faltaban

**AI Discovery Labs · 45 minutos · Sin saber programar de antemano**

## Tu misión

Un equipo curatorial quiere investigar las pinturas de *The Joy of Painting*. No tienes que adivinar lo que piensa una IA: necesitas **elegir una pregunta, decidir qué contar, interpretar datos y defender una conclusión**.

Abre `episode.html` directamente en el navegador. No se guardan ni envían tus respuestas. Al principio elige una de seis preguntas (A, B, C, D1, D2 o E). La clase trabaja **una**.

| Código | Perspectiva | Lo que vas a investigar |
|---|---|---|
| A | Negocio, escenario ficticio | Cómo distribuir 381 episodios en cuatro salas (no tenemos precios ni costos) |
| B | Social / representación | Diferencias descriptivas entre anfitrión e invitados |
| C | Descubrimiento | Agrupar por motivos y cuestionar el método |
| D1 | Creencia popular | ¿Hay árboles en todos? |
| D2 | Creencia popular | ¿Hay nieve en todas las montañas? |
| E | Detective | ¿Cómo engaña un modelo si usamos identificadores como features? |

### Antes de empezar (0–10 min)

1. Vota sin ver los resultados.
2. Escribe: **«Creo que ___ porque ___»**.
3. Define tu unidad y tu denominador. ¿Se habla de episodios, pinturas físicas, espectadores o dinero?
4. Pregunta a la IA qué datos necesitarías, **sin pedirle todavía una conclusión**.

### Tu copiloto IA (10–14 min)

Copia este mensaje a tu IA preferida, cambiando lo que aparece entre corchetes:

> Estoy investigando [pregunta elegida] usando exclusivamente el CSV local de Bob Ross, con un episodio por fila y etiquetas binarias. Soy principiante. Propón dos caminos: uno descriptivo y otro exploratorio, con las columnas, el denominador y una comprobación para detectar una conclusión errónea. No supongas resultados que no hayas calculado. Nunca uses temporada, título ni ID como características estéticas. Si faltan datos para monetizar, dilo.

Elige el camino que mejor responda **tu** pregunta. Explica por qué descartaste el otro.

### Investiga (14–28 min)

Si utilizas la terminal, desde la raíz del repositorio:

```bash
python discovery_labs/episodes/bob-ross/run.py --check
python discovery_labs/episodes/bob-ross/run.py --write
python discovery_labs/episodes/bob-ross/clustering.py --write
```

El primer comando verifica la fuente. Los otros generan tablas, figuras y el análisis de cuatro salas en la carpeta `output/`.

Si no tienes Python preparado, la página `episode.html` calcula visualizaciones descriptivas en el navegador a partir de datos reales embebidos y no necesita internet.

Observa qué está midiendo el gráfico: n, rango, definición de árbol/montaña y si se excluyeron invitados.

### Pon a prueba (28–36 min)

Pide a la IA:

> Actúa como una revisora estadística escéptica. Intenta refutar nuestra conclusión [describir], usando la fuente, los denominadores, las etiquetas y al menos una definición alternativa. Separa hechos de suposiciones. No presentes una cifra de cluster como «calidad artística».

Preguntas para discutir:

- ¿Cambiaría algo al incluir invitados?
- ¿Contamos TREE o TREE/TREES? ¿Qué significa SNOWY_MOUNTAIN?
- ¿Qué pasa si construimos un grupo con cuatro salas porque el museo lo pidió?
- ¿Qué no puede responder este dataset?

### Firma (36–45 min)

Completa una frase con **cuatro piezas**:

1. **Respuesta:** según el archivo...
2. **Evidencia:** n/N y gráfica o tabla...
3. **Límite:** no podemos afirmar...
4. **Siguiente investigación:** habría que comprobar...

Ejemplo de forma, **no de contenido**:

> «Entre [N] episodios de [población], [n] presentan [motivo]. La gráfica [X] lo muestra. Esto no prueba [conclusión prohibida] porque [limitación]. Para saber [nuevo objetivo] necesitaríamos [datos nuevos].»

## Entregable

Tu equipo entrega una **tarjeta de descubrimiento** con: pregunta, hipótesis original, métrica y denominador, visualización, prueba adversarial, conclusión de 3–5 líneas y una siguiente pregunta. Opcionalmente añade el prompt que funcionó mejor y qué le corregiste a la IA.

No se califica si acertaste al inicio. Se evalúa si pudiste justificar lo que afirmas.
