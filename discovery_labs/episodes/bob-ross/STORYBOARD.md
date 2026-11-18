# Storyboard científico · Los árboles que faltaban

**Formato:** sesión guiada de 45 minutos o screencast largo de 55–60 minutos. **Tono:** curiosidad, humor moderado, rigor; no revelar la respuesta en el título. **Protagonista:** la decisión del grupo, no el algoritmo.

> *Una pintura parece simple desde lejos. Pero ¿qué pasa cuando intentas describir cientos de paisajes con unos cuantos ceros y unos?*

## Los siete actos

| Acto | Tiempo | Acción humana | Objeto visual / evidencia | Riesgo narrativo |
|---|---:|---|---|---|
| 1. Curiosidad | 0–5 | Presentar una pregunta elegible sin respuesta | Portada, seis tarjetas | No insinuar que son «estilos verdaderos» |
| 2. Apuesta | 5–10 | El público predice y define «todos», «más», «diferente» | Hipótesis escrita en pantalla | No mostrar resultados antes del voto |
| 3. Primer indicio | 10–14 | IA ayuda a elegir dos caminos, con límites | Ficha: grano, 403 episodios, 67 etiquetas | Un cero no cuenta objetos |
| 4. Fricción | 14–21 | Descubrir GUEST, OR de TREE/TREES y SNOWY_MOUNTAIN | Diccionario + Silver CSV | Una variable puede condicionar la respuesta |
| 5. Descubrimiento | 21–28 | Generar tabla/gráfica y discutir qué significa | SVG motivos / temporadas / denominadores / salas | No inventar «significancia» |
| 6. Giro crítico | 28–36 | Atacar conclusión con otro denominador o distancia | Contrastantes, contraejemplos, ARI | Una métrica no es una verdad universal |
| 7. Firma | 36–45 | Redactar afirmación cuantificada con límite y siguiente pregunta | Tarjeta de descubrimiento | No convertir hipótesis en hecho |

La duración no incluye descarga ni configuración del entorno. La versión screencast opcional expande principalmente los actos 4–6 para mostrar código y diagnósticos (hasta 60 minutos).

## Dirección visual

- **Apertura:** recrear paisaje con formas SVG abstractas (no copiar una pintura de Bob Ross). Una luna y montañas representan el tema, no los datos.
- **Primera prueba:** un contador **403 episodios**, después separar **381 anfitrión** y **22 invitados**.
- **Lupa estadística:** barras de 12 motivos; cada barra codifica presencia, no cantidad de objetos.
- **Comparación:** siempre mostrar n/N junto a porcentajes.
- **Giro:** dos particiones distintas del mismo conjunto bajo decisiones de método, o un contraejemplo claramente identificado.
- **Salida:** la mejor visualización es aquella que demuestra la magnitud **y la limitación** de la conclusión.

Paleta oscura, acento terracota, verde salvia y azul; contraste legible. Todo gráfico debe tener título, alternativa textual, fuente, unidad, filtro y supuestos visibles. No usar imágenes de las pinturas sin permiso.

## Tramas alternativas según la pregunta elegida

**A · Museo / negocio ficticio.** El grupo recibe cuatro salas vacías: ¿cómo repartir las obras? Primer acto: diseñar reglas. Segundo: ver tamaño de salas. Giro: una sala casi vacía indica que una regla operativa no equivale a una oferta comercial equilibrada. Final: solicitar datos nuevos sobre capacidad/demanda antes de hablar de ingresos.

**B · Social / representación.** Una persona afirma que todos los artistas pintan lo mismo. Contrastar 381 frente a 22 episodios con árboles. Giro: porcentajes y n pequeños; no atribuir intención ni identificar rasgos personales.

**C · Descubrimiento / agrupamiento.** Organizar cuatro salas por doce motivos. Giro: k-medoids con Jaccard y Euclídea puede cambiar representantes y tamaños. Pregunta final: ¿Qué haría falta para afirmar que son «estilos»?

**D1 · Árboles.** «¿De verdad salen árboles en todas?» El giro legítimo es encontrar contraejemplos codificados. Llevar al alumno a explicar qué significa etiqueta y qué no fue observado directamente.

**D2 · Nieve.** «Montaña» evoca nieve, pero la codificación no implica que todas estén nevadas. Giro: el denominador correcto es **episodios con montaña**, y la categoría SNOWY_MOUNTAIN está en ambas features.

**E · Detective.** Un algoritmo parece dar una agrupación más nítida al añadir un identificador enorme. Giro: hemos cambiado la pregunta; la agrupación ahora refleja cronología. Usar la **referencia ejecutada anteriormente** para el experimento artificial, sin inventar una reejecución en este paquete.

## Guion hablado de ejemplo (sin adelantar el desenlace)

**Gancho (0:00–0:45)**

«Mira este paisaje. Ahora imagina que necesitas ordenar cientos de episodios en un museo. Parece fácil: árboles aquí, montañas allá. Pero ¿qué significa realmente que dos pinturas se parezcan? Hoy no vas a recibir la respuesta de una IA. Vas a escoger la pregunta y a obligarnos a demostrarla».

**Justo antes de la visualización (aprox. 19:00)**

«Antes de dejar que el gráfico nos convenza, verifiquemos tres cosas: cada fila representa un episodio, estas etiquetas indican presencia y nuestra definición de montaña tiene un detalle importante. ¿Cuál creen que es?».

**Giro (aprox. 30:00)**

«Con la primera métrica parecía claro. Ahora cambiamos una decisión del análisis. ¿Sigue siendo válida la afirmación, o sólo era cómoda?».

**Cierre (últimos 90 segundos)**

«Una investigación no termina cuando sale una gráfica bonita. Termina cuando podemos decir exactamente qué sabemos, cómo lo sabemos y qué todavía no podemos afirmar».

## Bifurcaciones honestas

- Si la respuesta inicial era correcta, mostrar evidencia que **la apoye**, no forzar una contradicción.
- Si no hay tamaño de muestra suficiente, presentar el límite como hallazgo metodológico.
- Si el clustering produce salas muy desbalanceadas, no ocultarlo con etiquetas bonitas.
- Si falla el entorno, usar \`episode.html\` offline con resultados embebidos y decir que no se calculan de nuevo en ese momento.
- Si un alumno cuestiona la definición TREE/TREES, abrir el diccionario y mostrar el OR.

## Nota editorial

El storytelling está subordinado a la evidencia. **No se manipulan números, períodos, gráficas ni datos para construir un giro dramático.** Si el giro no aparece, el episodio debe reconocerlo y mostrar qué aprendimos de la ausencia de un resultado sorprendente.
