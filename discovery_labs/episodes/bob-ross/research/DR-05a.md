# DR-05a · síntesis adversarial intermedia

Checkpoint del 19-11-2026. Lectura de O1 guardadas en `results/o1_results.json` después de contrastar DR-01/02/03 en `SOURCE_REVIEW.md` y 54 registros de evidencia. No es DR-05b ni aprobación humana. Su alcance es la evidencia de etiquetas: fuentes históricas y visuales no resueltas siguen pendientes.

| Arco | Evidencia O1 y objeción | Decisión de progresión |
|---|---|---|
| BR-14 / H8 | 10,000 permutaciones × tres poblaciones, cuatro motivos. Ninguna prueba primaria de inhibición sobrevive Holm; OCEAN tiene 0 adyacencias pero esperanza solo 1.38. Menos de lo esperado no basta para demostrar programación. | O1 INCONCLUSIVE respecto a inhibición; no equivalencia ni refutación definitiva. No abrir la O2 heredada sobre distribución de rachas sin señal robusta y sin fechas de emisión verificadas. |
| BR-07 / H9 | CABIN–WINTER: 28/381 conjunta frente a 11.96 bajo independencia; lift 2.342, IC bootstrap temporadas 1.795–2.895. Permutación condicionada por temporada p≈.0001, límite de resolución Monte Carlo. R5 composición/técnica y R3 anotación siguen plausibles. | O1 exploratoria apoyada como asociación, no como simbolismo/causa. La O2 canónica requiere estabilidad de asociaciones por épocas; puede estudiarse después. La O2 H9 sobre habitantes exige corpus autorizado. No activar ahora. |
| BR-09 / H6 | k=4 Jaccard: 236/106/36/3. El grupo de tres es exactamente el de filas sin etiquetas; aparece en cada k de 2 a 6. ARI Jaccard–Euclídea .109; bootstrap condicional .069–.163. R3 representación es una explicación medible. | **Activar únicamente BR-09-O2**, anidada en BR-09. El trigger canónico de cuatro grupos se cumple y hay desacuerdo observado entre distancias. Ejecutar cambios con matching de etiquetas, grid sin filas vacías y leave-one-season-out. |
| BR-10 / H1/H7 | Join 403/403 factible. MIT de BobRossColors no verifica derechos de upstream; paleta declarada no es color de píxel. La idea Burnt Umber/Dark Sienna ya aparece en Flourish. | BLOCKED_RIGHTS para ejecución de paletas en esta ronda; acceso técnico probado, no originalidad demostrada. |

## Excepción contextual explícita para BR-09

La revisión temprana de los tres DR está hecha de forma focalizada, no exhaustiva. La O2 activada no utiliza diagnóstico, fechas biográficas, créditos de invitados o imágenes: depende exclusivamente de CSV, reglas de transformación y algoritmo preservados. Estas fuentes centrales sí están auditadas. Los pendientes históricos no se convierten en hechos ni bloquean una comparación de matrices binarias sin calendario. Esta delimitación sustituye un falso «DR-01/02/03 totalmente verificados».

## BR-09-O2 · protocolo fijado después de O1 y antes de su ejecución

- `parent_id=BR-09-O1`; evidencia que activa: `results/o1_results.json#/BR-09` y asignaciones guardadas. Estado inicial DATA_FEASIBLE; resultado aún no escrito al fijar este checkpoint.
- **Cómo:** matching exacto de etiquetas para k=4 (24 permutaciones) antes de contar cambios; nunca comparar IDs de cluster literalmente. ARI para todo k=2…6. Reajustar grid Jaccard sobre 378 episodios quitando solo tres filas de 67 ceros. Añadir 31 reajustes dejando una temporada fuera, predecir todos los episodios por medoid más cercano y comparar con partición completa; estos resultados son sensibilidad algorítmica, no rendimiento OOS frente a verdad artística. Comparar además 12 familias frente a 64 etiquetas sin tres flags de autoría. Contraste independiente ya ejecutado: bootstrap por temporadas del acuerdo entre métricas, condicional a particiones fijas. No llamar a ese IC estabilidad de reajuste; los 31 nuevos reajustes atienden por separado ese punto.
- **Por qué:** distinguir efecto de filas vacías, cambio de métrica y pérdida de una temporada. Una sala vacía puede venir de datos faltantes en vez de un género artístico.
- **Para qué:** hacer visible qué decisiones de medición producen los grupos y qué casos cambian; no elegir «estilo verdadero» por el máximo silhouette.
- O3 sigue CONDITIONAL: la pregunta canónica exige evaluadores humanos y obras autorizadas, ausentes. La evaluación computacional de R3 permite formularla, pero no ejecutarla ni publicarla como respondida.

## Límites que se mantienen

La evidencia es un censo del snapshot, no una muestra aleatoria de la obra de Ross. Fisher/permutaciones describen un nulo hipotético; no muestrean autores ni espectadores. BH supone condiciones de dependencia que no se demostraron para las 12 familias: se conserva tabla completa y se interpreta de modo exploratorio, con una pareja condicionada fijada por DR-03. No hay nuevas anotaciones, corpus visual, validación humana ni prueba de prioridad bibliográfica. La búsqueda de k es exploratoria; no atribuir el máximo a arte o intención. Salud, ventas, recepción y ritmo de creación permanecen fuera de identificación.
