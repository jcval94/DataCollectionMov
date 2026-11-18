# Diccionario · NYC Rodent Inspection

Consulta completa de 2024 para seis campos de p937-wjvj; 234, 596 filas, reconciliadas con un conteo independiente del mismo filtro. No es toda la base histórica. La geografía disponible es borough: no se responde a escala de barrio. No se solicitaron direcciones, coordenadas exactas, nombres ni observaciones libres.

| Campo | Tipo / grano | Regla |
| --- | --- | --- |
| job_id | Texto administrativo | No es único por sí mismo: un caso puede tener múltiples visitas |
| inspection_date | Timestamp flotante del productor | Calendario 2024; no inventar zona UTC. Se analiza mes, no intervalos horarios |
| inspection_type | Initial, Compliance, Treatments, Stoppage, Clean Ups | Seguimientos y tratamientos no intercambiables con iniciales |
| borough | Uno de cinco distritos | No es barrio ni medida de cobertura poblacional |
| result | Categoría del productor | Positivo: Failed for Rat Activity o Failed for Rat Activity and Other Reason. Negativo comparable: Passed o Failed for Other Reason. Bait applied y otras acciones no se codifican como negativos |
| bbl | Llave pública de predio, texto | Diez dígitos, prefijo1–5 coherente con borough. Vacío, inválido o discordante no se repara; no se usa para emparejar predios |

Silver conserva todas las filas, incluidas diez copias exactas posteriores a la primera. `duplicate_exact` evita duplicarlas sólo en Gold. La llave de negocio candidata es job_id+inspection_date+inspection_type+bbl; si dos filas no idénticas comparten esa llave, el adaptador se detiene.

`known_outcome` distingue resultados binarios comparables de acciones. `initial_eligible` exige tipo Initial, resultado conocido y primera copia exacta. `property_eligible` agrega BBL válido y coherencia geográfica. `positive` es1/0 sólo para resultados comparables y vacío para otras acciones; no se usa para convertir tratamientos en resultados negativos.

Política por predio: primera inspección Initial observada en 2024, ordenada por fecha y job_id, sin seleccionar por resultado. Se compara con eventos iniciales en el mismo universo de llaves y con cualquier positivo por predio. Es la primera visita observada en la ventana, no la primera de la historia.

Invierno: enero, febrero y diciembre del mismo2024. Verano: junio–agosto. Para la cohorte pareada se elige primera visita de cada estación por BBL, sólo si ambas existen. El cruce de resultados invierno/verano **no es una transición cronológica**: algunas primeras visitas de invierno ocurren en diciembre. Bootstrap: 500 remuestreos de predios pareados, semilla 1729; incertidumbre condicional con supuesto IID, sin corregir selección o dependencia espacial.

Gold sólo contiene agregados de borough, mes, estación o política. No hay mapas de predios ni recomendaciones de control sanitario. No inspeccionado no equivale a ausencia de ratas. Ninguna tasa estima número de animales, infestación poblacional, causalidad o eficiencia monetaria.
