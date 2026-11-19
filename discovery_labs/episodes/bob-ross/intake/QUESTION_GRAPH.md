# Banco de preguntas multinivel — Bob Ross

**Estado:** 12 arcos candidatos, no aprobados; son investigaciones, no respuestas. El CSV solo tiene etiquetas de episodios; cualquier biografía, cronología de grabación, imágenes o situación de salud requiere evidencia externa. **No** reescribir aún las seis tarjetas de `episode.html` hasta que los arcos se prueben y se aprueben.

## 1. ¿Pintaba el mismo mundo al final de su vida que al principio?

**Gancho:** Dos cuadros separados por once años pueden parecer hermanos. ¿Lo son?

**Primer orden:** ¿Cómo evoluciona la combinación de motivos en las 31 temporadas y qué diferencias persisten más allá de una línea de tendencia?

**Segundo orden:**
- ¿Cambian el número de motivos por episodio y sus coocurrencias o solo cambia la frecuencia de árboles?
- ¿Sobreviven los cambios al excluir episodios con invitados y usar ventanas móviles/prevalencias por temporada?

**Tercer orden:** Si existe un punto de cambio, ¿se mantiene en períodos alternativos, distintas definiciones de motivos y al comparar contra la variación natural entre temporadas?

**Método:** Tasas por temporada, composición multivariante, cambio de punto con corrección por selección, bootstrap por temporada y sensibilidad a ventanas

**Visualización deseada:** Río de motivos por temporada + heatmap de 31×12 + tira de episodios representativos con imágenes solo autorizadas

**Refutación / riesgo:** Cambiar agregación temporada/era/episodio; controlar múltiples comparaciones; la fecha de emisión NO es fecha de creación

**Fuentes adicionales:** cronología de producción/emisión validada; contexto de cambios en el programa

**Transferible a:** Evolución, adaptación y cambios de régimen

**Estado:** CANDIDATA_NO_EJECUTADA

---

## 2. ¿Dejó su salud una huella en su obra?

**Gancho:** La vida de quien crea una obra no está dentro de una tabla de etiquetas. ¿Podemos encontrar su rastro?

**Primer orden:** ¿Existen cambios descriptivos en los motivos hacia el final de la serie?

**Segundo orden:**
- ¿Qué fechas biográficas y de grabación están documentadas, frente a fechas de transmisión o simples rumores?
- ¿Se observan cambios comparables en temporadas anteriores sin un evento biográfico conocido?

**Tercer orden:** ¿Es identificable un efecto de enfermedad con la secuencia temporal y la disponibilidad de obras posdiagnóstico o debemos clasificar la causalidad como no demostrable?

**Método:** Mapa de evidencia temporal → análisis descriptivo → evaluación de identificación causal/negativa, sin pruebas clínicas ni inferencia psicológica

**Visualización deseada:** Timeline de tres carriles: vida verificada / grabación / emisión / intervalos de incertidumbre y cobertura del CSV

**Refutación / riesgo:** El diagnóstico se sitúa cerca del final de la serie; riesgo de cero pos-evento comparable, confundidores y sesgo de supervivencia

**Fuentes adicionales:** fechas documentadas de diagnóstico, contexto de vida y muerte; fechas reales de grabación, no solo emisión; cuadros posteriores a la serie y su procedencia

**Transferible a:** Impacto de eventos de vida en procesos creativos/productivos con guardas causales

**Estado:** NO_IDENTIFICABLE_HASTA_DEEP_RESEARCH

---

## 3. ¿Cuál fue la temporada más extraña de Bob Ross?

**Gancho:** ¿Y si la temporada menos reconocible explica más que la más popular?

**Primer orden:** ¿Qué episodios y temporadas son atípicos por frecuencia y combinación de motivos?

**Segundo orden:**
- ¿La temporada rara sigue si agregamos motivos por familias o usamos las 67 etiquetas originales?
- ¿El supuesto outlier es una obra genuinamente diferente, un grupo de invitados, un error de etiqueta o una consecuencia de n=13?

**Tercer orden:** ¿Sigue siendo excepcional cuando se compara contra nulos permutados que preservan frecuencias y se ajusta por buscar máximos entre 31 temporadas?

**Método:** Rareza multivariante, scores robustos, permutaciones con estratos, niveles episodio/temporada/era y revisión de registros

**Visualización deseada:** Mapa de calor de anomalías por temporada + ranking de 10 episodios raros + inspector de hover con miniatura autorizada

**Refutación / riesgo:** Vigilar falsos positivos por 31 búsquedas, motivos casi constantes y duplicación de etiquetas

**Fuentes adicionales:** evidencia visual autorizada para verificar un subconjunto de casos extremos

**Transferible a:** Anomalías multiescala y explicación de extremos

**Estado:** CANDIDATA_NO_EJECUTADA

---

## 4. ¿Era Bob Ross siempre el mismo artista?

**Gancho:** Parecerse no es repetirse. ¿Podemos medir la originalidad sin juzgar belleza?

**Primer orden:** ¿Con qué frecuencia se repiten exactamente perfiles de motivos y cómo cambia su novedad por temporada?

**Segundo orden:**
- ¿Se reutilizan combinaciones pero cambian los elementos raros o los invitados?
- ¿Qué parte de la repetición proviene de que las etiquetas comprimen cuadros visualmente distintos?

**Tercer orden:** Si incorporamos descriptores visuales legalmente disponibles, ¿se mantiene la aparente repetición o era una ilusión de la representación tabular?

**Método:** Índice de novedad respecto de episodios anteriores, unicidad de perfiles, diversidad de Shannon y ablation etiquetas vs píxeles

**Visualización deseada:** Mosaico de perfiles repetidos con capas de novedad y miniaturas solo cuando estén autorizadas

**Refutación / riesgo:** Un perfil binario idéntico no implica la misma pintura ni menor creatividad; concept drift del etiquetador

**Fuentes adicionales:** imágenes licenciadas o permiso explícito; metadatos de 3 versiones de pinturas por episodio

**Transferible a:** Originalidad, repetición y diversidad de productos/contenidos

**Estado:** CANDIDATA_NO_EJECUTADA

---

## 5. ¿De verdad su mundo estaba lleno de árboles?

**Gancho:** Lo recordamos por los árboles. ¿Qué pintaba cuando no estaban?

**Primer orden:** ¿Cuáles son los contraejemplos de la afirmación «siempre pinta árboles» dentro de las etiquetas?

**Segundo orden:**
- ¿Qué motivos reemplazan a los árboles en esos episodios y cómo se distribuyen por temporadas?
- ¿Los paisajes sin árboles forman comunidades coherentes o son anomalías dispersas?

**Tercer orden:** ¿La asociación entre ausencia de árboles y agua/mar se mantiene al controlar por temporada e invitados, o se invierte dentro de segmentos?

**Método:** Condicionales, odds ratios descriptivos con intervalos apropiados, coocurrencia por subgrupo, control de mezcla/Simpson

**Visualización deseada:** 403 episodios como puntos; filtrar árboles, revelar paisajes alternativos y revisar casos atípicos mediante inspector

**Refutación / riesgo:** No igualar etiqueta faltante con ausencia física comprobada en una imagen

**Fuentes adicionales:** fuente verificable que demuestre la difusión de la creencia, si se presenta como popular

**Transferible a:** Revisión profunda de estereotipos/creencias mediante subpoblaciones

**Estado:** BASE_DESCRIPTIVA_PREEXISTENTE; CAPAS_Q2_Q3_PENDIENTES

---

## 6. ¿Sus montañas tenían que estar nevadas?

**Gancho:** Nuestra imaginación dibuja nieve en la montaña. ¿Y los datos?

**Primer orden:** ¿Qué proporción de episodios con montaña codificada no incluyen nieve?

**Segundo orden:**
- ¿Cambian las combinaciones montaña/nieve en temporadas y motivos circundantes?
- ¿En qué medida SNOWY_MOUNTAIN induce mecánicamente la asociación observada?

**Tercer orden:** Al redefinir ambas familias sin la etiqueta solapada, ¿cuánto de la relación permanece y qué implica sobre nuestra primera conclusión?

**Método:** Tablas cruzadas, sensibilidad de diccionario, intervalos en subgrupos y recodificación adversarial

**Visualización deseada:** Dos mitades del mismo paisaje: matriz de categorías solapadas antes/después de separar variables

**Refutación / riesgo:** La feature SNOWY_MOUNTAIN contribuye a numerador y denominador; medir dependencia por construcción

**Fuentes adicionales:** imagen autorizada para comprobar casos extremos y errores de etiqueta

**Transferible a:** Dependencias artificiales debidas a ingeniería de variables

**Estado:** BASE_DESCRIPTIVA_PREEXISTENTE; CAPAS_Q2_Q3_PENDIENTES

---

## 7. ¿Cuántos Bob Ross viven dentro del mismo Bob Ross?

**Gancho:** Cuatro salas de museo, cuatro versiones de la misma historia. ¿Hay una correcta?

**Primer orden:** ¿Qué familias de paisajes aparecen si organizamos los 381 episodios por 12 motivos?

**Segundo orden:**
- ¿Cómo cambian representantes y tamaños al comparar Jaccard, Euclídea y sin árboles?
- ¿Qué episodios cambian de sala y cuáles son los puentes entre perfiles?

**Tercer orden:** Al confrontar las particiones con imágenes legalmente accesibles y con nuevas familias, ¿qué grupos siguen siendo interpretables por humanos sin convertir un score en verdad artística?

**Método:** k-medoids/k-means con métodos explícitos, ARI y estabilidad, prototipos y puntos frontera

**Visualización deseada:** Scatter/proyección prudente + grupos conectados y inspector hover/foco del episodio, título, motivos y posible pintura autorizada

**Refutación / riesgo:** Evitar inferir estilos naturales; k=4 es restricción del museo; proyecciones 2D distorsionan

**Fuentes adicionales:** vínculos episodio→obra y permisos de previsualización

**Transferible a:** Segmentación de entidades con interpretación, sensibilidad y ejemplos

**Estado:** BASE_CLUSTERING_PREEXISTENTE; QA_VISUAL_PENDIENTE

---

## 8. ¿Quién rompe las reglas: el artista o el editor?

**Gancho:** Un invitado puede convertir una pauta aparentemente universal en excepción.

**Primer orden:** ¿Qué motivos son más distintos entre episodios con invitado y sin invitado?

**Segundo orden:**
- ¿La diferencia viene de uno o dos invitados, de una temporada concreta o de los propios temas de emisión?
- ¿Qué cambia al comparar tasas, no números absolutos, y representar la incertidumbre de n=22?

**Tercer orden:** ¿Podemos separar el efecto de ser invitado de la selección editorial y temporal, o faltan características del proceso de producción?

**Método:** Comparación de grupos no aleatorios, tasas por subgrupo, intervalos exploratorios y análisis de selección

**Visualización deseada:** Small multiples de motivos para anfitrión/invitados y timeline de apariciones, n siempre visible

**Refutación / riesgo:** N pequeño, no inferencia sobre rasgos personales, causalidad o superioridad artística

**Fuentes adicionales:** lista y nombres de invitados, producción y criterios editoriales documentados

**Transferible a:** Efecto de composición, selección y paneles desbalanceados

**Estado:** BASE_DESCRIPTIVA_PREEXISTENTE; CAPAS_Q2_Q3_PENDIENTES

---

## 9. ¿El programa enseñaba a pintar o enseñaba a mirar?

**Gancho:** Dos cuadros iguales como motivos pueden contar historias distintas para sus espectadores.

**Primer orden:** ¿Qué patrones de composición se priorizan como ejemplos didácticos a lo largo de la serie?

**Segundo orden:**
- ¿Los motivos frecuentes se relacionan con cambios documentados en técnicas/guiones del programa?
- ¿El patrón observado responde a restricciones pedagógicas, comerciales o artísticas?

**Tercer orden:** ¿Qué predicciones diferencian la hipótesis «pedagógica» de «preferencia personal» y qué pruebas audiovisuales, guiones o manuales necesitaríamos?

**Método:** Triangulación cualitativa, codificación de técnicas enseñadas y pruebas de hipótesis rivales, sin inferir motivaciones

**Visualización deseada:** Línea paralela motivos ↔ segmentos de instrucción verificados (sin reproducir videos protegidos)

**Refutación / riesgo:** Una asociación entre dos corpus no prueba intención artística ni ventas

**Fuentes adicionales:** transcripciones subtituladas licenciadas; entrevistas; manuales y programación de PBS

**Transferible a:** Comportamiento observado vs intención y contexto del sistema

**Estado:** REQUIERE_NUEVAS_FUENTES

---

## 10. ¿Y si la tendencia es un espejismo de la escala?

**Gancho:** A veces el dato cambia de historia cuando cambiamos la unidad de tiempo.

**Primer orden:** ¿Cómo se describe la frecuencia de cada motivo por episodio, temporada y tercio de la serie?

**Segundo orden:**
- ¿Hay una inversión de tendencia entre niveles de agregación, aun con grupos de invitados definidos?
- ¿La concentración de episodios atípicos en ciertas temporadas domina los promedios?

**Tercer orden:** ¿Resiste el hallazgo un análisis jerárquico que considere variación dentro y entre temporadas, incertidumbre y corrección por búsquedas exploratorias?

**Método:** Estadística multinivel descriptiva, varianza por temporada, resúmenes ponderados y permutation controls

**Visualización deseada:** Zoom semántico episodio→temporada→era, mismos datos diferentes agregaciones, intervalos/denominadores visibles

**Refutación / riesgo:** No tratar filas de episodios correlacionados como ensayos IID ni atribuir cambio de agregación a causalidad

**Fuentes adicionales:** fechas de producción para no tratar emisión como creación

**Transferible a:** Simpson, errores de agregación y estructura multinivel

**Estado:** CANDIDATA_NO_EJECUTADA

---

## 11. ¿Qué paisajes casi nunca se atreve a pintar?

**Gancho:** Lo más revelador no siempre es lo frecuente, sino lo que casi nunca ocurre.

**Primer orden:** ¿Qué pares o combinaciones de motivos son extraordinariamente raros frente a sus tasas individuales?

**Segundo orden:**
- ¿Estas rarezas cambian por temporada o se concentran en capítulos invitados?
- ¿Cuánto de la rareza proviene de etiquetas parecidas o ausentes?

**Tercer orden:** Tras preservar las frecuencias marginales en un modelo nulo, ¿qué combinaciones son realmente inesperadas y cuáles aparentaban serlo por baja frecuencia?

**Método:** Null models de permutación, coocurrencias robustas, ranking por sorpresa condicionado al marginal, control FDR

**Visualización deseada:** Red de combinaciones raras + revelación de episodios excepcionales y fichas con controles de calidad

**Refutación / riesgo:** Evitar poner como descubrimiento una combinación rara solo porque uno de sus elementos casi nunca aparece

**Fuentes adicionales:** revisión autorizada de cuadros para verificar etiquetas y casos excepcionales

**Transferible a:** Sorprendencia condicionada, nichos y anomalías de combinaciones

**Estado:** CANDIDATA_NO_EJECUTADA

---

## 12. ¿Cuánto de la obra de Bob Ross quedó fuera del dataset?

**Gancho:** Un programa no es toda una vida creativa; y una etiqueta no es un cuadro.

**Primer orden:** ¿Qué representa exactamente cada fila y qué obras/versiones quedan fuera?

**Segundo orden:**
- ¿Qué fuentes documentan las versiones previas/durante/después de grabar y obras sin episodio?
- ¿Cambian las conclusiones al ampliar el universo más allá de las 403 filas?

**Tercer orden:** ¿Qué sesgo de selección introduce usar solo obras televisadas para hablar de la evolución de toda su producción artística y qué datos lo reducirían?

**Método:** Análisis de cobertura, tabla de universos, sample-selection audit, missing-not-at-random conceptual

**Visualización deseada:** Diagrama de universo: todas las obras→obras televisadas→403 etiquetas→12 motivos usados

**Refutación / riesgo:** No usar estas 403 filas como censo de todas las obras de su vida

**Fuentes adicionales:** Smithsonian, obras originales, libros, pinturas inéditas, procedencia y derechos

**Transferible a:** Sesgo de cobertura y lo invisible del dataset

**Estado:** REQUIERE_NUEVAS_FUENTES
