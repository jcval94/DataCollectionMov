# Cuatro salas para Bob Ross

## El encargo

El **Museo Imaginario** —un cliente ficticio para este ejercicio— prepara una exposición sobre Bob Ross. Tiene cuatro salas y un archivo real con elementos identificados en episodios de *The Joy of Painting*. Quiere que el recorrido tenga sentido y que alguien pueda explicar su criterio.

**Tu problema:** ¿cómo organizarías cuatro salas por lo que aparece en los cuadros, y qué evidencia te haría cambiar de opinión?

Trabaja en equipo de 2–3 personas. Tienen **60 minutos** y pueden usar Codex o Claude para inspeccionar datos, escribir código y ejecutarlo. La elección de variables, la lectura de resultados y la recomendación final corresponden al equipo. No es necesario escribir Python a mano.

No hay etiquetas de “estilo verdadero” ni una única partición correcta. La evaluación se centra en la evidencia y las decisiones, no en replicar los números de otro equipo.

## Lo que recibirás

- `data/elements-by-episode.csv`: datos reales, guardados localmente.
- `data/manifest.json`: fuente, edición y hash para comprobar el archivo.
- Un agente con acceso a archivos y capacidad de ejecutar Python. No necesita conectarse a APIs ni usar una clave de OpenAI.

Cada fila es un episodio. `EPISODE` sirve para encontrarlo y `TITLE` para interpretarlo después. Un 1 indica que el productor registró un elemento; un 0 indica que no lo registró. `TREES` no es una cantidad de árboles.

Si trabajas dentro del repositorio completo, abre sólo este documento y los datos durante la actividad. El docente tiene un paquete separado con una solución de referencia; leerla antes elimina parte del problema que vamos a discutir.

## 1. Decide antes de pedir código · 0–18 minutos

Escribe tres frases antes de ejecutar clustering:

1. Dos cuadros se parecen para esta exposición cuando…
2. Una columna numérica que dejaríamos fuera es… porque…
3. Cuatro grupos significa…; no significa…

Mira seis episodios y haz una agrupación manual provisional. Conserva un caso ambiguo. Pregunta al docente por las tarjetas de la demo si no estás trabajando con imágenes.

Pide al agente una inspección, no una conclusión:

> Lee el CSV local y el manifiesto. Antes de modelar, dime cuántas filas y columnas hay, qué representa una fila, si los IDs son únicos, qué etiquetas no son binarias y si faltan valores. Muéstrame seis registros reales. Distingue elementos del paisaje, metadatos, artistas y tipos de marco. No uses títulos para deducir etiquetas ni imputes datos silenciosamente. Propón variables y espera nuestra decisión antes de entrenar.

Comprobad lo que responde. Una tabla impresa por el agente debe proceder del archivo, no de su memoria.

## 2. Construye una representación · 18–25 minutos

Para la comparación común usaremos los episodios con `GUEST == 0` y doce familias binarias. Si el equipo propone otra representación, documentadla; sus resultados no tienen por qué coincidir con la referencia.

| Familia | Etiquetas originales combinadas mediante OR |
| --- | --- |
| Árboles | TREE, TREES |
| Montañas | MOUNTAIN, MOUNTAINS, SNOWY_MOUNTAIN |
| Lagos | LAKE, LAKES |
| Ríos | RIVER |
| Mar | OCEAN |
| Nieve | SNOW, SNOWY_MOUNTAIN |
| Cascadas | WATERFALL |
| Estructuras | STRUCTURE |
| Nubes | CLOUDS |
| Rocas | ROCKS |
| Sol | SUN |
| Flores | FLOWERS |

OR significa “aparece al menos una”. Si `TREE=1` y `TREES=1`, Árboles sigue siendo 1. Nieve y montañas comparten una etiqueta: no estamos suponiendo que las familias sean independientes.

¿Qué pierde esta representación? No incluye composición, posición de objetos, color, tamaño ni parecido visual completo. Un episodio sin ninguno de esos doce motivos no equivale a un cuadro vacío.

## 3. Pide una propuesta verificable · 25–42 minutos

> Implementa K-means con k=4, semilla 42 y n_init=50 sobre las doce familias aprobadas, sin estandarizar. El ID, el título, la temporada y los artistas quedan fuera de X. k=4 viene del número de salas, no de descubrir cuatro estilos naturales. Ejecuta el código. Entrega tamaños, conteos y proporciones de cada motivo por grupo, el centro de cada grupo y un episodio real representativo. Busca también un episodio que complique la descripción de cada grupo. Guarda los resultados en archivos y explícame cómo reproducirlos sin red. No llames precisión a una métrica sin categorías de referencia.

Antes de aceptar los grupos, responded:

- ¿Los tamaños suman exactamente la población usada?
- ¿Qué significa un centro con valor 0.8 en una variable binaria?
- ¿El representante es un episodio real o un promedio inventado?
- ¿Qué episodios del mismo grupo no encajan con su nombre propuesto?
- ¿Qué nombres pondríais vosotros a las salas? No aceptéis una etiqueta sólo porque suena convincente.

## 4. Intenta romper tu resultado · 42–54 minutos

Elegid una comprobación y explicad qué permite concluir:

> Compara k entre 2 y 8. Reporta silhouette usando el mismo espacio y distancia, tamaños y el grupo más pequeño. Explica si el mejor valor resuelve por sí solo el encargo de las cuatro salas.

> Cambia varias semillas manteniendo las variables. Compara las membresías con ARI, sin confundir la numeración de los grupos con cambios reales. Después quita la familia Árboles y repite: ¿estabilidad de la semilla equivale a estabilidad del criterio?

El docente revelará otro experimento deliberadamente incorrecto: añadir un ID secuencial grande como variable. Antes de verlo, anotad qué esperáis que ocurra.

## 5. Firma tu decisión · 54–60 minutos

Entregad `decision.md`, máximo 150 palabras, y los archivos de evidencia. Debe contener:

- Una propuesta de organización y el criterio que la justifica.
- Un conteo con su denominador y un ID de episodio concreto.
- Una limitación o un caso que desafíe vuestra interpretación.
- Una comprobación adicional antes de recomendar abrir la exposición.

Inicio sugerido:

> Organizaríamos… La evidencia es… El episodio… complica esta lectura. No afirmamos… Antes de abrir verificaríamos…

**Transferencia:** al agrupar clientes, sucursales o tiendas, ¿qué columna cómoda podría producir grupos nítidos y llevaros a responder otra pregunta?

Los datos son de FiveThirtyEight, bajo CC BY 4.0. La licencia de datos no implica derechos sobre pinturas o vídeos. El encargo no mide calidad artística ni las preferencias del público.
