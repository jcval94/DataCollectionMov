# Deep Research — cuatro investigaciones independientes y una síntesis

**Propósito:** generar contexto externo que permita preguntas verdaderamente importantes ANTES de preprocesar, graficar o contar una historia. **No es el guion de video ni un relato ficticio.** Cada investigación se puede ejecutar en un agente de investigación especializado; no reemplazar verificación de fuentes por una respuesta persuasiva.

**Insumos compartidos:** `metadata.json`, `data_sample.csv`, `QUESTION_BANK.md`, `PLANNING.md`, `data/manifest.json` y el CSV original en la carpeta padre. Publicar un informe con tabla de afirmaciones, evidencia en enlaces originales y niveles de confianza. Fechas de ejecución y fechas de los eventos por separado.

## DR-1 · BIOGRAFÍA, CRONOLOGÍA Y CONTEXTO DE BOB ROSS

**Pega este prompt en Deep Research:**

> Actúa como historiador audiovisual y verificador de hechos. Reconstruye la historia de Bob Ross en relación con la producción de *The Joy of Painting*: origen de su técnica, formación, carrera y su experiencia en Alaska, creación del programa, evolución de la televisión educativa, invitados, empresas colaboradoras, sucesos personales relevantes, enfermedad y etapa final. Diferencia nacimiento de la idea, grabación, fecha de emisión, reedición y publicación digital. Distingue biografía comprobada de recuerdos de terceros, especulación o mitos.
>
> Busca fuentes primarias (PBS, archivos, entrevistas, catálogos oficiales, periódicos de época) y secundarias independientes, sin depender únicamente de Bob Ross Inc. Genera una cronología con: fecha exacta o intervalo, acontecimiento, fuente primaria, segunda fuente si existe, calidad de respaldo, controversias, grado de certeza, correspondencia provisional con temporadas/episodios y sesgos.
>
> Estudia con sensibilidad la hipótesis: «¿La enfermedad de Bob Ross coincidió con un cambio medible en su obra televisiva?». No presupongas que sí ocurrió ni que un cambio sería consecuencia de la enfermedad. Averigua fechas con cautela y marca lo incierto. **No infieras diagnóstico, capacidad o estado mental desde pinturas o apariencia.** Incluye causas alternativas: selección de episodios, invitados, cambios de producción, guiones, tendencias previas, cambios de etiquetas, fechas de emisión diferentes de fechas de pintado.
>
> Entrega fuentes, citas breves, cronología y seis hipótesis testables; destaca qué datos no existen. No redactes un guion cinematográfico.

**Pistas iniciales para verificar (no autoridad exclusiva):**
- https://www.bobross.com/about-bob-ross/
- https://dos.fl.gov/cultural/programs/florida-artists-hall-of-fame/bob-ross/
- https://apnews.com/article/cd50203eb6b3cf4f1893364cfae472be
- https://people.com/bob-ross-death-what-to-know-7558507
- https://www.washingtonpost.com/arts-entertainment/2021/08/27/bob-ross-netflix-documentary/

**Nota crucial:** referencias públicas difieren en detalles y fechas de producción. No convertir año de estreno en fecha de pintura sin comprobar episodios. La aparición de nuevas producciones con pinturas preparadas para una supuesta temporada 32 NO es parte del CSV original de 403 episodios.

## DR-2 · INVESTIGACIONES, FUENTES DE DATOS Y ANTECEDENTES VISUALES

**Pega este prompt en Deep Research:**

> Investiga de forma exhaustiva qué han descubierto otros sobre las pinturas de *The Joy of Painting* y qué puede descubrirse de forma independiente. Localiza y evalúa críticamente análisis de Walt Hickey/FiveThirtyEight, artículos de visualización científica, análisis con R/Python, trabajos sobre coocurrencia de motivos, paletas de color, técnicas pictóricas y cronologías.
>
> Para cada antecedente: título, autor, año, DOI/URL, dataset utilizado, unidad de análisis, definición de variables, método, figuras, resultados, limitaciones, licencia y viabilidad de reproducirlo. Distingue trabajo primario, tutorial derivado, agregador y duplicado. Identifica al menos 5 vacíos de investigación que podamos cubrir sin exagerar novedad.
>
> Investiga datasets complementarios: jwilber/Bob_Ross_Paintings, Two Inch Brush, catálogo PBS, archivos de temporadas y fechas de emisión, entrevistas, reseñas y registros de imágenes. Para cada join propone claves (`season`, `episode`, `EPISODE`), unicidad, cobertura, ambigüedad de títulos y riesgos por licencia. No copies ni rehostees imágenes protegidas. Separa etiquetas humanas, píxeles, paleta de colores y recepción social.
>
> El resultado debe ser un **mapa de evidencia** y un ranking de enriquecimientos que realmente permiten preguntas de segundo y tercer orden, no una lista de enlaces.

**Pistas:**
- https://github.com/fivethirtyeight/data/tree/4c1ff5e3aef1816ae04af63218015066e186c147/bob-ross
- https://fivethirtyeight.datasettes.com/fivethirtyeight/bob-ross~2Felements-by-episode
- https://github.com/jwilber/Bob_Ross_Paintings
- https://asistdl.onlinelibrary.wiley.com/doi/10.1002/meet.2014.14505101084
- https://fivethirtyeightdata.github.io/fivethirtyeightdata/articles/bob_ross.html

## DR-3 · PREGUNTAS PROFUNDAS, EVENTOS EXTERNOS Y DISEÑO DE PRUEBAS

**Pega este prompt en Deep Research:**

> Actúa como investigador, metodólogo causal y diseñador de preguntas. Recibe la muestra, diccionario, cronología validada y antecedentes. Quiero preguntas con misterio real, importancia humana y suficiente profundidad para 45 minutos, no SQL trivial ni conteos sin historia.
>
> Aplica la skill `research-question-architect`: genera al menos 12 preguntas candidatas de orden 1, con ramificaciones de orden 2 activadas por resultados concretos y al menos un tercer orden que discuta explicaciones rivales. Incluye al menos: evolución por temporadas, cambio de régimen, eventos externos, anomalías de varios niveles, diversidad/entropía, falsación de creencias sofisticadas, diferencias invitados/anfitrión y un experimento adversarial sobre definición de similitud.
>
> Para cada una aporta tensión narrativa, variable/denominador, fuente original y datos externos, comparador, método y una visualización original; limita cualquier hipótesis causal a un análisis descriptivo si no existe identificación. Reserva resultados imaginarios como escenarios, no hallazgos.
>
> Evalúa individualmente las preguntas con 10 dimensiones y penaliza fuertemente afirmaciones que no se puedan verificar. Devuelve un árbol, matriz de viabilidad y una shortlist de 3–4 preguntas protagonistas. No produzcas el video ni el guion del video.

## DR-4 · DERECHOS, REPRESENTACIÓN VISUAL Y EXPERIENCIA DEL ESPECTADOR

**Pega este prompt en Deep Research:**

> Eres especialista en visualización científica, derechos de autor y diseño de interfaces accesibles. Investiga cómo mostrar cada pintura real de Bob Ross al pasar el cursor por un punto de un cluster, con alternativa por clic/tap, teclado y lector de pantalla. Proporciona enlaces de catálogo de imágenes por temporada/episodio, fecha de consulta, relación con los datos, titular/licencia/términos, restricciones de hotlinking y alternativas. No presupongas que el dataset CC BY 4.0 autoriza las imágenes.
>
> Propón: (a) mostrar imagen si existe permiso verificable, (b) vista previa desde URL remota cuando las condiciones lo permitan, con consentimiento de red y atribución, (c) ficha enlazada y placeholder sin copiar imagen cuando no exista permiso. Nunca evadir controles ni automatizar scraping de obras protegidas.
>
> Diseña un sistema de visualización para 31 temporadas y 403 episodios, con intervalos, pequeñas múltiples, anotaciones de eventos históricos con incertidumbre, outliers detectados en tres niveles de agregación, clusters interpretables con perfiles y medoids, conexiones entre motivos y una comparación de cambios robusta. Cada gráfico requiere unidad, denominador, limitaciones y alt text. Evalúa estética, legibilidad móvil, selección de color y animaciones útiles (no decorativas).
>
> Entrega un **brief visual verificable**, contratos de interacción, inventario de activos autorizados y criterios de QA. No desarrolles Remotion ni video en esta fase.

## DR-5 · SÍNTESIS / RED TEAM DE LOS CUATRO INFORMES

**Pega este prompt después de recibir DR-1 a DR-4:**

> Actúa como editor científico jefe y revisor adversarial. Dispones de cuatro informes: cronología, antecedentes y fuentes, preguntas profundas, y derechos/visualización. Cruza las afirmaciones por URL, fecha, unidad y método; detecta contradicciones y conclusiones injustificadas.
>
> Produce un `claims_registry`: id, afirmación, fuente, cita, fecha, estado (CONFIRMADO_EXTERNAMENTE / CALCULADO / HIPOTESIS / BLOQUEADO / CONFLICTO), variable disponible, contraargumento, uso permitido en texto, figura y posible prueba. No permitas que una afirmación de enfermedad se convierta en causa de cambio artístico por coincidencia temporal.
>
> Devuelve: cronología consolidada, gaps prioritarios, ocho+ preguntas con 1→2→3, plan de uniones de datos, storyboard CIENTÍFICO de visualizaciones (no audiovisual), riesgos de derechos y criterios de aprobación.
>
> Prepara material para **Fase 1: guía científica HTML**. No escribas Fase 2 (storytelling de video) ni Fase 3 (video) hasta aprobación humana explícita.

## Contrato mínimo de cada informe

- Resumen de hallazgos; fecha de investigación; fuentes primarias/secundarias.
- Tabla de afirmaciones importantes con enlaces reales; distinguir certeza factual y certeza causal.
- Material crítico faltante y plan concreto de obtención.
- Ideas originales derivadas del contexto, no del resultado que «sería bonito encontrar».
- Hallazgos negativos y controversias sin maquillar.
- Metodologías y pruebas que otro agente puede ejecutar.
- Dictamen honesto: ¿qué preguntas son aptas para el primer HTML y cuáles necesitan más datos?

**Regla de salida:** todos los informes quedan dentro del paquete de entrada hasta que la guía de investigación sea revisada y aprobada. El paquete puede tener múltiples DR; aquí recomendamos cuatro especializados y una síntesis adversarial.
