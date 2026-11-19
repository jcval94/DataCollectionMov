# Doce arcos de investigación — preguntas no superficiales

**No son resultados comprobados.** Son rutas de investigación priorizables a partir del dataset y la historia real de Bob Ross. O2/O3 se activan **solo después de ejecutar** el nodo anterior.

## 1. ¿Hay una historia de evolución estética en las 31 temporadas?

**Familia:** Evolución y rupturas · **Estado:** `PROPOSED_UNEXECUTED`

- **Orden 1:** ¿La combinación de motivos cambia de manera gradual o atraviesa rupturas durante la serie?
- **Orden 2, si el resultado lo justifica:** Si aparece un cambio: ¿está concentrado en ciertas temporadas, invitados o familias de motivos?
- **Orden 3, si existe evidencia:** Si persiste: ¿qué explicación rival se sostiene al incorporar fechas de emisión/grabación, paletas, decisiones de producción y contexto de vida? ¿Qué NO podemos atribuir a salud?

**Datos:** Etiquetas + episodios por temporada; paleta y cronología externas pendientes.

**Visual decisivo:** heatmap estacional normalizado + change-point con incertidumbre.

## 2. ¿Coincide algún cambio pictórico tardío con acontecimientos personales documentados?

**Familia:** Contexto biográfico y límites causales · **Estado:** `BLOCKED_EXTERNAL_DATES; NO_CAUSAL_CLAIM`

- **Orden 1:** ¿Hay cambios detectables de motivos, variedad y paleta hacia el tramo final de la serie?
- **Orden 2, si el resultado lo justifica:** Si los hay: ¿aparecen antes, durante o después de las fechas externas verificadas, o solo parecen sincronizados por usar temporadas?
- **Orden 3, si existe evidencia:** ¿Se explican igual de bien por fechas de grabación, programación de episodios, artistas invitados, selección de obras o artefactos de etiquetado? ¿Podemos descartar que la atribución a salud sea injustificable?

**Datos:** Dataset + cronología corroborada + fechas grabación/emisión + paleta (no disponibles completas).

**Visual decisivo:** serie temporal de cambios con eventos documentados y bandas de incertidumbre.

## 3. ¿Qué episodio rompe el patrón y qué temporada lo hace aún más?

**Familia:** Outliers multiescala · **Estado:** `DATA_FEASIBLE_METHOD_PENDING`

- **Orden 1:** ¿Cuáles son los episodios inusuales por combinación de motivos y cómo se define rareza?
- **Orden 2, si el resultado lo justifica:** ¿Se concentra la rareza en temporadas enteras o solo en casos individuales, al cambiar de episodio a temporada y a era?
- **Orden 3, si existe evidencia:** ¿La rareza resiste bootstrap, normalización por tamaño y una taxonomía alternativa; o es un error de codificación/escasez del muestreo?

**Datos:** Etiquetas 403 + 12 familias + temporadas.

**Visual decisivo:** matriz episodio×motivo + ranking de anomalía por temporada + tooltips.

## 4. ¿Cuánto Alaska hay realmente en los paisajes de Bob Ross?

**Familia:** Historia e iconografía · **Estado:** `CONTEXT_RESEARCH_REQUIRED`

- **Orden 1:** ¿Qué prevalencia tienen montañas, nieve, bosques y agua en la serie, y cómo varía a través del tiempo?
- **Orden 2, si el resultado lo justifica:** ¿Aumentan o disminuyen los paisajes nevados según temporada, después de controlar invitaciones y correlaciones mecánicas?
- **Orden 3, si existe evidencia:** ¿La asociación histórica con Alaska queda respaldada por declaraciones documentadas o es una lectura retrospectiva no demostrable a partir del CSV?

**Datos:** Motivos + entrevistas/biografía, cronología; no hay geolocalización física de cuadros.

**Visual decisivo:** small multiples de iconografía + citas verificadas.

## 5. ¿Era el pintor de los árboles felices... o hay otra cara?

**Familia:** Mitos versus medición · **Estado:** `DESCRIPTIVE_COUNTS_VERIFIED; CULTURAL_CLAIM_NEEDS_SOURCE`

- **Orden 1:** ¿Hasta qué punto la asociación popular con árboles representa su repertorio?
- **Orden 2, si el resultado lo justifica:** ¿Las excepciones sin árboles comparten motivos/temporadas o forman un repertorio propio?
- **Orden 3, si existe evidencia:** Si parecen formar un grupo: ¿sobrevive esa conclusión a otro esquema de codificación o la imagen popular simplifica deliberadamente un repertorio más diverso?

**Datos:** TREE/TREES + motivos + referencias externas para demostrar la creencia.

**Visual decisivo:** mosaico de 381 episodios con contraejemplos focalizados.

## 6. ¿Qué paisajes combinaba de formas que casi nunca esperaríamos?

**Familia:** Combinaciones inesperadas · **Estado:** `DATA_FEASIBLE_METHOD_PENDING`

- **Orden 1:** ¿Qué pares o tríos de motivos coocurren mucho más o mucho menos que sus frecuencias marginales?
- **Orden 2, si el resultado lo justifica:** ¿Las combinaciones raras pertenecen a temporadas, invitados o grupos concretos?
- **Orden 3, si existe evidencia:** ¿Las asociaciones desaparecen al corregir multiplicidad y dependencias creadas por OR, o hay una combinación estable y visualmente interpretable?

**Datos:** Matriz binaria y diccionario, confusiones de SNOWY_MOUNTAIN.

**Visual decisivo:** heatmap de lift frente a esperado + red con umbrales + casos extremos.

## 7. ¿Cambian las pinturas cuando el pincel lo toma un invitado?

**Familia:** Heterogeneidad y composición · **Estado:** `DESCRIPTIVE_COUNTS_VERIFIED; CAUSAL_BLOCKED`

- **Orden 1:** ¿Qué combinaciones de motivos diferencian episodios con GUEST=1 y los demás?
- **Orden 2, si el resultado lo justifica:** ¿La diferencia global desaparece al comparar solo temporadas con invitados?
- **Orden 3, si existe evidencia:** ¿Es una diferencia de artista, de encargo, de época o del criterio de selección? ¿Qué datos permitirían distinguirlo?

**Datos:** GUEST 22 episodios, temporada y etiquetas; identidad del artista opcional.

**Visual decisivo:** dotplots porcentuales con n y modelos de incertidumbre por grupo.

## 8. La obra invisible: ¿qué dejó fuera el conteo de 403 episodios?

**Familia:** Lo que los datos no muestran · **Estado:** `CONTEXT_ONLY; ORIGINAL_DATA_INCOMPLETE`

- **Orden 1:** ¿A qué universo pertenece la muestra de 403 episodios y qué versiones de cada pintura deja fuera?
- **Orden 2, si el resultado lo justifica:** ¿Cómo alteraría el relato considerar las pinturas de referencia, las variantes para libros y las siete obras preparadas para una temporada 32?
- **Orden 3, si existe evidencia:** ¿Cambiarían los patrones al construir un corpus con imágenes y permisos, o el supuesto de un estilo por episodio seguiría siendo equivocado?

**Datos:** Fuentes externas de producción, Smithsonian, AP, pinturas con derechos.

**Visual decisivo:** diagrama de cobertura de corpus y capas de versiones.

## 9. ¿La paleta cambió mientras los motivos permanecían?

**Familia:** Evolución de color · **Estado:** `BLOCKED_EXTERNAL_DATA`

- **Orden 1:** ¿Cómo cambió la diversidad de colores declarados entre temporadas?
- **Orden 2, si el resultado lo justifica:** ¿Persisten cambios de paleta dentro de paisajes comparables (ej., montañas sin nieve) o son resultado de motivos distintos?
- **Orden 3, si existe evidencia:** ¿El cambio refleja técnica, metadatos de la paleta o fuente de color diferente? Contrastar con imagen licenciada o catálogo de materiales.

**Datos:** Paletas de jwilber / Bob Ross y join season+episode; derechos externos.

**Visual decisivo:** río cromático temporal / small multiples controlados.

## 10. Si el algoritmo encuentra estilos, ¿encontró algo de verdad?

**Familia:** Metodología e interpretabilidad · **Estado:** `EXISTING_CLUSTERING; HUMAN_ART_VALIDATION_PENDING`

- **Orden 1:** ¿Qué estructura tienen los grupos al representar episodios mediante familias de motivos?
- **Orden 2, si el resultado lo justifica:** ¿Cuántos episodios cambian de sala al variar Jaccard, Euclídea o el peso de árboles?
- **Orden 3, si existe evidencia:** Si la estructura parece estable: ¿la validarían evaluadores humanos con pinturas licenciadas o solo reproduce nuestras definiciones de features?

**Datos:** Matriz doce motivos + clustering ya implementado, evaluación externa no disponible.

**Visual decisivo:** alluvial de membresías + hover por episodio + representantes.

## 11. ¿Y si las fechas que vemos no fueran las fechas de creación?

**Familia:** Errores temporales e historias falsas · **Estado:** `BLOCKED_EXTERNAL_DATES`

- **Orden 1:** ¿Cuándo se grabó versus cuándo se emitió cada episodio, y en qué cambia esa diferencia el relato histórico?
- **Orden 2, si el resultado lo justifica:** ¿Los puntos de cambio se desplazan al usar grabación, emisión o solo ordinal de temporada?
- **Orden 3, si existe evidencia:** ¿Qué hipótesis biográfica deja de ser viable ante errores de fechamiento o censura del corpus?

**Datos:** Necesita calendario validado de grabación/emisión; CSV solo ID temporada.

**Visual decisivo:** dos líneas paralelas con conexiones y grados de certeza.

## 12. ¿Los «accidentes felices» eran realmente improvisación?

**Familia:** Espontaneidad versus preparación · **Estado:** `BIOGRAPHIC_ONLY; NOT_MEASURABLE_IN_CSV`

- **Orden 1:** ¿Qué fuentes muestran cómo Ross preparaba las obras antes de grabarlas, y cuál era su grado de planificación?
- **Orden 2, si el resultado lo justifica:** ¿Existe evidencia de que la improvisación didáctica y la composición planificada pudieran coexistir?
- **Orden 3, si existe evidencia:** ¿Qué datos independientes (grabaciones, guiones, tres versiones) permitirían poner a prueba la espontaneidad en vez de asumirla por su imagen pública?

**Datos:** Entrevistas NPR, archivos de producción, videos/transcripciones con permiso.

**Visual decisivo:** diagrama verificado de tres versiones de la obra y ciclo de producción.

## Selección editorial inicial

Prioridad para investigar primero: **EVOL → HEALTH** como un solo arco histórico con cautela causal; **OUTLIER** en episodios, temporadas y eras; **CLUSTER** con imágenes únicamente autorizadas; **MYTH** como entrada accesible. El episodio empieza con la historia de Bob Ross, no con `COUNT(*)`.

La primera guía científica debe narrar investigación abierta, métodos y resultados reales. Ningún guion o video antes de su aprobación.
