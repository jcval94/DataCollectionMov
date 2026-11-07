# Guía docente · Cuatro salas para Bob Ross

## La decisión didáctica

**Pregunta central:** ¿cómo organizar cuatro salas por los elementos representados y defender la decisión, sin convertir los grupos en “estilos verdaderos”?

Duración recomendada: **60 minutos**. Equipos de 2–3. Los alumnos ya saben abrir una carpeta, conversar con Codex/Claude, permitir ejecución local y localizar archivos de salida. No necesitan escribir código ni aprender las ecuaciones de K-means durante la actividad.

El caso empieza con un encargo concreto: un museo ficticio dispone de cuatro salas. El alumno formula qué considera parecido, dirige al agente y evalúa la propuesta. El docente revela resultados después de que el grupo haya firmado un criterio provisional.

**Conceptos a reforzar:** unidad de análisis; tipo de dato frente a significado; representación; distancia; objetivo del clustering; centroides como proporciones; selección de k; validación; límites de métricas y de explicaciones de IA. No se introduce visión artificial: se agrupan etiquetas de presencia, no imágenes.

**Resultado observable:** el alumno justifica una representación, interpreta un centro con numerador y denominador y detecta una variable que mejora una métrica mientras desvía el análisis del encargo. Repartir roles de curador, operador del agente y verificador de evidencia; intercambiarlos al pasar de modelado a refutación. En parejas, el curador también verifica.

## Encaje con el curso

Encaja principalmente en **C17, “Encontrar lo raro”**, tras introducir similitud, segmentación y agrupación exploratoria. Aprovecha la asignación de Bob Ross al [plan docente](../../docs/exploration/PLAN_DOCENTE_DATASETS.md#c17), con una adaptación: esta demo trabaja **motivos** y ejecución E1 con Python, en lugar del piloto de paletas/visión E4 que allí estaba propuesto.

La versión de 35 minutos cabe en aquella cápsula. La de 60 ocupa un tercio de una sesión de 180 minutos y permite que los alumnos dirijan el análisis. Es una alternativa preparada; no modifica los casos principales ni el calendario del curso. También puede reutilizarse al hablar de calidad de datos, selección de variables e interpretación de modelos, cambiando la pregunta de cierre.

## Qué preparar

1. Abrir `demo.html` en un navegador y volver al paso 1. Todo el texto, datos y gráficos del ejercicio están incrustados. Las cuatro reproducciones son enlaces remotos opcionales; verificar conexión si se quieren mostrar. La clase funciona con tarjetas de rasgos si no cargan.
2. Entregar el [material del alumno](ALUMNO.md) y el CSV. Para evitar enviar soluciones, generar un paquete separado con `python examples/bob_ross_clustering/build_student_kit.py`. No hace falta clonar todo el repositorio de históricos.
3. Tener una terminal preparada con las dependencias de `requirements.txt`. El análisis no llama a ningún LLM ni descarga datos. Codex/Claude actúan como asistentes de programación del alumno.
4. Leer el [README de evidencia](reference/README.md), comprobar el caso representativo y el caso difícil de cada sala y ensayar la revelación del ID.
5. Elegir una contingencia: si un agente tarda, usar la referencia calculada y pedir al equipo que la audite. La actividad no se aprueba por la velocidad del asistente ni por coincidir con una semilla.

Preparación humana estimada, con el paquete listo: **20–30 minutos** para ejecutar, revisar y ensayar. La primera instalación o configuración de agentes puede añadir tiempo; realizarla antes de la sesión, no dentro del presupuesto de 60 minutos. No se requiere contratar un MCP ni configurar una API del proveedor.

## Guion de 60 minutos

| Tiempo | Docente | Alumnos | Evidencia que debe quedar |
| --- | --- | --- | --- |
| 0–8 | Presentar el encargo. Preguntar “¿qué debe tener en común una sala?” Evitar mencionar resultados. | Proponer un criterio y una predicción. | Tres frases: similitud, una columna que excluirían y significado de cuatro grupos. |
| 8–18 | Abrir las seis tarjetas. Mostrar títulos sólo después de la primera agrupación. | Repartirlas a mano y justificar un caso ambiguo. Inspeccionar grano y etiquetas con el agente. | Reparto provisional, población propuesta y columnas excluidas. |
| 18–25 | Acordar representación y filtro. Explicar OR y la pérdida de detalle. | Aprobar o corregir la propuesta de variables; decir qué no podrá inferirse. | Contrato de 12 familias, sin ID ni título en X. |
| 25–30 | Pedir una ejecución y artefactos, no una historia atractiva. Si tarda, abrir referencia. | Dirigir K-means y comprobar los archivos. | Tamaños que suman n, proporciones y representantes. |
| 30–42 | Revelar los cuatro perfiles y las reproducciones opcionales. Pedir un nombre y un contraejemplo por sala. | Interpretar un centro, recontar una celda y discutir una excepción. | Un numerador/denominador y un episodio que desafía la etiqueta. |
| 42–49 | Mostrar k=2…8. Preguntar si mayor silhouette autoriza ocho salas. | Distinguir encargo, métrica y decisión; elegir una prueba de sensibilidad. | Justificación de k y limitación de la métrica. |
| 49–54 | Antes del botón, pedir una predicción sobre añadir el ID. Revelar la trampa. | Explicar por qué la métrica puede subir agrupando por cronología. | Diagnóstico del error y regla para futuras variables. |
| 54–60 | Pedir recomendación breve y transferencia a clientes/tiendas. | Firmar decisión con evidencia, contraejemplo y próximo control. | `decision.md`, hasta 150 palabras. |

## Resultados esperables y preguntas que los ponen a prueba

La edición fijada contiene **403 episodios**. Excluir los 22 con `GUEST=1` deja **381**; el modelo usa doce familias binarias. Hay **122 perfiles únicos** y tres perfiles con ceros en esas doce familias. Dos cuadros diferentes pueden tener distancia cero: esta representación los hace indistinguibles.

Con K-means, semilla 42 y 50 inicializaciones, las salas de referencia tienen **124, 118, 100 y 39 episodios**. La numeración se ordena por tamaño únicamente para presentarla: no es una clase ni un rango de calidad.

| Sala | Interpretación humana posible | Evidencia a pedir | Episodio representativo |
| --- | --- | --- | --- |
| 1 · 124 | Ríos entre árboles | 123/124 tienen ríos; 124/124, árboles. No todos son paisajes simples de río. | S01E01 · A Walk in the Woods |
| 2 · 118 | Paisajes arbolados sin río | 115/118 tienen árboles; 0/118, ríos. Lagos y estructuras no están presentes en todos. | S15E10 · Forest Dawn Oval, según el CSV de elementos |
| 3 · 100 | Montañas y lagos | 96/100 tienen montañas; 78/100, lagos. No llamarla “todos los lagos”. | S01E07 · Autumn Mountains |
| 4 · 39 | Costas y cielos | 33/39 tienen mar; 36/39, nubes. Seis no tienen la marca OCEAN. | S09E02 · Surf's Up |

Estos nombres no salieron como etiquetas verdaderas de un algoritmo. Son propuestas que deben compararse con frecuencias, ejemplos y decisiones del museo. Los representantes son **medoides**: episodios reales con menor distancia media a los miembros de su sala. Un centroide es el promedio de las variables y puede no coincidir con ningún episodio.

La referencia conserva un caso distante del medoide por sala. Por ejemplo, **S11E05, Towering Glacier**, pertenece a la sala 1 y contiene montañas, nieve, cascadas, nubes y rocas además de árboles/río. Sirve para frenar una descripción demasiado simple del grupo. “Caso distante” no es un diagnóstico formal de anomalía ni un error de asignación.

**Lectura del centro:** en la sala 1, el centro para Ríos es 123/124 ≈ 0.992. Significa proporción de episodios con ese motivo; no “0.992 ríos por pintura”, ni probabilidad predictiva validada de una pintura nueva.

### El giro que conviene ensayar

En el espacio original, silhouette con k=4 es **0.22698**. Dentro de la exploración acotada k=2…8, el valor más alto está en **k=8, 0.27075**. No se exploró todo k posible y no existe un umbral universal que transforme estas cifras en aprobación de la exposición.

El experimento deliberadamente incorrecto añade `10 × (temporada × 13 + episodio)` a las doce familias. Ese número construido domina las distancias. Silhouette pasa a **0.57132 en ese otro espacio**, mientras que el acuerdo con la partición por motivos es **ARI=0.01023**. La visualización muestra franjas cronológicas.

No comparar los dos silhouette como si midieran la misma calidad: cambió la representación y la métrica está evaluando esa nueva geometría. La enseñanza es que una puntuación favorable puede recompensar un criterio que no responde al encargo.

Preguntas de facilitación:

- “¿Qué separa ahora a los episodios: el paisaje o su posición en la serie?”
- “¿El ID dejó de ser identificador por poder convertirlo en número?”
- “¿Qué cifra te estaba dando tranquilidad? ¿Qué observación la puso en duda?”
- “Si usamos esos grupos para tomar una decisión, ¿qué perderíamos?”

### Sensibilidad: resultado estable no equivale a criterio correcto

Diez semillas adicionales dan ARI mínimo **0.96952** frente a la referencia. Quitar Árboles da **0.75794**. Incluir invitados y comparar sólo los 381 episodios comunes da **0.96952**. ARI compara membresías ignorando los números arbitrarios de los grupos; no mide exactitud ni calidad artística.

No enseñar ARI en detalle si aún no se ha visto: basta con “acuerdo entre dos agrupaciones; cerca de 1, más parecido”. Los valores y las condiciones quedan en la evidencia para revisión posterior.

## Preguntas frecuentes y correcciones breves

| Si alguien dice… | Repregunta o corrección |
| --- | --- |
| “Encontramos los cuatro estilos de Bob Ross.” | ¿Qué referencia define estilos y qué detalles visuales hemos omitido? Son cuatro grupos bajo una representación y una restricción. |
| “Todo lo numérico sirve.” | ¿Qué significa la columna? El identificador numérico sigue identificando; también puede dominar por escala. |
| “Estandarizar siempre es obligatorio.” | En binarios modifica la ponderación relativa de motivos comunes y raros. Debe ser una decisión, no un hábito automático. |
| “El centroide es la pintura promedio.” | Aquí es un vector de proporciones de etiquetas; no una imagen ni un episodio real. |
| “Dos cuadros del mismo grupo son iguales.” | ¿Cuántos perfiles únicos hay y qué información no medimos? |
| “El agente lo ejecutó; ya está validado.” | ¿Dónde están la fuente, el conteo, el archivo de salida y el contraejemplo? |
| “Hay una accuracy del clustering.” | ¿Contra qué categorías de referencia? Sin ellas no usar ese término. |
| “Converger o cambiar poco de semilla prueba que es correcto.” | ¿También se mantendría al cambiar las variables o el objetivo del encargo? |

No imponer Jaccard, otro algoritmo o visión como requisito adicional a mitad de la sesión. Son extensiones posteriores. Cambiar distancia **y** algoritmo simultáneamente no permite atribuir la diferencia a uno solo.

## Evaluación breve · 10 puntos

| Criterio | Puntos | Señal observable |
| --- | ---: | --- |
| Define la unidad y población | 2 | Distingue episodios, filtro de invitados y tamaño final. |
| Justifica variables y similitud | 2 | Excluye metadatos, explica OR y una pérdida de información. |
| Interpreta evidencia | 2 | Usa un conteo con denominador y explica un centro correctamente. |
| Intenta refutar | 2 | Revisa un caso difícil o prueba de sensibilidad y limita la conclusión. |
| Decide y transfiere | 2 | Recomendación concreta, límite y próximo control; detecta una posible trampa equivalente fuera del arte. |

No puntuar cantidad de prompts, velocidad de escritura ni parecido de nombres con esta guía. Si dos equipos usan representaciones distintas y las defienden con evidencia, no hay razón para exigir idénticos grupos.

**Ticket de salida:** “Un clustering útil requiere… Una métrica alta puede engañarme cuando… Antes de usarlo para clientes verificaría…”.

## Versiones según el tiempo

- **35 minutos, demostración guiada:** encargo 4; tarjetas y variables 7; ejecución precalculada 4; perfiles y centro 8; trampa 7; decisión 5. El docente opera, los alumnos predicen y verifican. Es la variante que cabe en la cápsula de C17.
- **60 minutos, recomendada:** usa el guion anterior; una ejecución del agente por equipo, con contingencia de referencia.
- **90 minutos, laboratorio:** añade 15 para otro conjunto de variables y 15 para auditar ejemplos/representantes y comparar agrupaciones. No añadir scraping, embeddings ni fine-tuning para “hacerlo más avanzado”.

## Qué sigue abierto

No se verificaron visualmente las 403 codificaciones, ni se probaron preferencias de visitantes, calidad de curaduría, equivalencia de todas las reproducciones o generalización a otras obras. S15E10 figura como **Forest Dawn Oval** en elementos y **Forest Down Oval** en la fuente de imágenes; S01E07 también difiere en singular/plural. Se conservan ambos títulos y se cruza por episodio único, sin corregir silenciosamente. Es una oportunidad de calidad de datos, no motivo para afirmar que una fuente entera es falsa.

Un resultado final defendible sería una **propuesta de organización por motivos para esta exposición ficticia**, acompañada de ejemplos, límites y condiciones de revisión. La IA ayuda a producirla y cuestionarla; el equipo firma qué decisión puede respaldar.
