# Bob Ross · investigación científica ejecutable · 19-11-2026

Se auditó el snapshot, se conciliaron los tres DR y sus diez H con las 14 BR existentes, se ejecutaron tres O1 exploratorias y se activó/respondió únicamente BR-09-O2 tras DR-05a. No se inició audiovisual ni se aprobó la investigación. La revisión de fuentes fue focalizada, no exhaustiva; cada pendiente conserva ese estado.

## Estado real y procedencia

Base inspeccionada: `ce757809214fd6d38ffede9f4130d3c68feb2469`, main con commits automáticos de movilidad posteriores al merge Bob Ross. PR #12/#14/#15/#16 fusionados. CI específico de main tras #16: [run 44579116224](https://github.com/jcval94/DataCollectionMov/actions/runs/44579116224), success sobre `a8d157a384b6afebd85f8f796a0f5bdab5e1a580`; esto no certifica automáticamente todos los commits posteriores ni esta rama. PR abiertos #2/#4/#6/#7 ajenos a esta investigación permanecen fuera de alcance.

Ya existían `run.py` (conteos), `clustering.py` (cuatro salas didácticas), `examples/bob_ross_clustering` y un servicio MCP. No se reetiquetan como experimentos nuevos ni se modificó Render/MCP. La guía V3 exponía O2/O3 de antemano; V4 pasa a publicación progresiva con 14 fichas y una sola O2 activada.

Archivos originales: CSV de 66,315 bytes intacto, hash y blob coincidentes con upstream fijado; los diez blobs del archivo recibido coinciden con MANIFEST. Los tres informes literales no estaban en Git y no se reconstruyeron. El archivo recibido sigue intacto.

## Auditoría y contradicciones

| Aspecto | Verificado | Límite |
|---|---|---|
| Dimensiones | 403×69, 67 binarias, IDs únicos S01E01–S31E13, sin nulos | Calidad de esquema no valida anotación visual |
| Suma | 3,221 incluidos 34 flags de autoría; 3,187 sin esos flags | No se encontró definición que produzca 3,224/3,324 |
| Publicación académica | Resumen 3,324 y sección de datos 3,224 | Contradicción interna; versión histórica de datos no recuperada |
| PERSON | Existe, positiva en S03E10 | CHIMNEY no existe; una etiqueta no cubre todas las versiones físicas |
| Duplicados | Dos pares: MOUNTAIN WATERFALL y LAKESIDE CABIN | Nunca unir por título |
| Autoría | 381 GUEST=0, 22 GUEST=1; 11 Steve y 1 Diane | Diez invitados sin nombre en flags; créditos completos pendientes |
| Incompletas | S09E10/S15E04/S26E10, todas las etiquetas cero | Se conservan en población primaria; 378 como sensibilidad explícita |
| Ontología | Excepciones de nubes, montaña y marco | Se registran, sin reparación automática |
| Paletas externas | 403 claves únicas, join 403/403 viable | Licencia upstream pendiente; MIT del paquete derivado no da permiso de imágenes |

[Auditoría JSON](evidence/data_audit.json) · [403 episodios auditados](evidence/episode_audit.csv) · [Fuentes contrastadas](SOURCE_REVIEW.md) · [54 registros de evidencia](evidence/source_claim_matrix.csv).

## Conciliación sin segundo banco

| Insumo DR-03 | BR canónica de integración | Alcance |
|---|---|---|
| H1 | BR-10 | Paleta declarada; bloqueada por permisos |
| H2 | BR-01 | Cambio tardío descriptivo; clínica/rodaje no identificados |
| H3 | BR-07 | Subestudio compositivo; no se midieron duración ni cantidad de objetos |
| H4 | BR-08 | Invitados; créditos y curación editorial pendientes |
| H5 | BR-05 | Auditoría de medición de contraejemplos; nueva recodificación bloqueada |
| H6 | BR-09 | Motivos ejecutados parcialmente; híbrida y comparación completa pendientes |
| H7 | BR-10 | Calibración pigmentos/píxeles, requiere activos autorizados |
| H8 | BR-14 | Secuencia ordinal medida, sin calendario de grabación |
| H9 | BR-07 | Estructuras y clima; no simbolismo ni habitantes inferidos |
| H10 | BR-13 | Extensión de recepción con nuevo target externo; no sustituye target canónico |

[Matriz completa de las 14 BR](evidence/reconciliation.csv): O1, denominador, modelo, contraste, rivales, datos, derechos y siguiente acción. BR sin H equivalente se conserva, sin asociación forzada. [Banco canónico](../entry_pack/questions_master.json) mantiene diseños originales y añade referencias de ejecución; [registro](execution_registry.json) almacena estados, no un nuevo banco editorial.

## Priorización razonada

Rúbrica común de 100 puntos: curiosidad 15, anclaje histórico 10, falsabilidad 20, insight potencial 15, progresión 15, valor visual 10, factibilidad docente/coste 10, seguridad epistémica/derechos 5. Notas 0–5 y ponderación en [ranking.json](evidence/ranking.json). Una puerta bloqueante prevalece sobre la puntuación.

| Prioridad | Arco | Puntos | Método y decisión |
|---|---|---:|---|
| 1 | BR-14 / H8 | 91 | Markov + 10,000 permutaciones; CSV suficiente y nulo condicionado; ejecutado |
| 2 | BR-07 / H3/H9 | 85 | Lift + Fisher/BH, permutación por temporada y bootstrap; pares ejecutados |
| 3 | BR-09 / H6 | 83 | K-medoids + ARI/IC y sensibilidad; O1 parcial y O2 medida |
| 4 | BR-10 / H1/H7 | 85 | Paleta disponible técnicamente; bloqueada por permisos/calibración, pese a score alto |

La originalidad no está demostrada por un ranking. Agrupamiento, redes y evolución ya tienen antecedentes; no se anuncian como primicias. Esta ronda aporta un diseño reproducible y evidencia de sensibilidad, con coste de CPU local y cero APIs de pago. El protocolo fija el alcance antes de cada ejecución; no es preregistro independiente.

## Resultados medidos

### BR-14-O1 · la falta de repeticiones no demuestra alternancia

**Cómo:** cuatro motivos de H8, 372 transiciones dentro de 31 temporadas, Markov descriptivo y permutaciones intra-temporada moviendo vectores completos. Se preservan coocurrencias y totales; corrección Holm sobre cuatro pruebas.

| Motivo | Repeticiones 1→1 | Esperadas exactas | p Holm de inhibición |
|---|---:|---:|---:|
| OCEAN | 0 | 1.38 | .422 |
| OVAL_FRAME | 1 | 3.54 | .386 |
| WINTER | 6 | 9.69 | .386 |
| CABIN | 9 | 10.00 | .437 |

No alcanza evidencia para H8 en esta especificación. Sensibilidades anfitrión (330 transiciones) y anfitrión sin tres filas vacías (324) tampoco pasan Holm. No se puentean episodios eliminados ni temporadas. **Por qué:** un motivo raro puede no repetirse aun con orden aleatorio. **Para qué:** enseñar el valor del nulo condicionado. No equivale a demostrar ausencia de programación, intercambiabilidad o irrelevancia histórica.

### BR-07-O1 parcial · cabañas e invierno sí se asocian

**Cómo:** CABIN–WINTER, tabla 2×2 `[[28,40],[39,274]]` en 381 episodios. Coincidencias 28 frente a 11.96 bajo independencia, lift 2.342, OR 4.918. Fisher bilateral p=2.27e−7; al permutar WINTER dentro de temporada, p≈.0001, resolución mínima de 10,000 réplicas. Bootstrap de temporadas: lift 95% 1.795–2.895. Excluir vacíos da lift 2.323.

**Por qué:** la afinidad excede prevalencias y persiste con ese control estacional. R3 anotación y R5 composición siguen plausibles. **Para qué:** formular una pregunta sobre composición con límites claros. No prueba intención, casas habitadas, técnica, causa climática ni límite de 26 minutos.

Las 66 parejas de familias, con tabla, lift, OR y q BH, se conservan completas: 34 tienen q<.05, **no 34 descubrimientos independientes**. Hay dependencias entre familias y solapamiento explícito montaña–nieve. Tríos, modelo de H3, contrastes entre tipos de estructuras y recepción permanecen pendientes.

### BR-09-O1 y O2 · estabilidad depende de qué se perturba

**Cómo:** k-medoids heurístico determinista sobre 12 familias. Con 381 filas, todos los k=2…6 reservan un grupo a las tres filas sin etiquetas; el máximo de silhouette del grid es k=2 con tamaños 378+3. O1 detecta el artefacto; [DR-05a](DR-05a.md) activa la O2 canónica de cambios de asignación.

O2 reajusta y compara: sin los vacíos, el máximo del grid pasa a k=3, tamaños 236+106+36. Matching exacto de nombres: cambiar Jaccard por Euclídea altera 179/381 asignaciones (47.0%); quitar árbol altera 75/381 (19.7%). ARI entre métricas .109 (IC bootstrap condicional .069–.163); 12 familias frente a 64 etiquetas sin autoría: ARI .308. Pero 31 reajustes dejando fuera una temporada reproducen la partición completa (ARI=1 en cada uno).

**Por qué:** perturbación de muestra, métrica y ontología responden cosas diferentes; una partición puede resistir el primer cambio y ser sensible a los otros. **Para qué:** evitar elegir un número de estilos por silhouette y diseñar una validación de representación. El máximo del grid no es un estimador validado de categorías artísticas. El remuestreo del ARI de O1 usa particiones fijas, no reajuste; LOSO de O2 sí reajusta, pero compara contra etiquetas aprendidas, no verdad artística independiente. O3 humana permanece condicional y bloqueada por datos/derechos.

## Reproducir y revisar

Desde la raíz del episodio, Python ≥3.11 y biblioteca estándar:

```bash
python research/audit.py
python research/reconcile.py
python research/experiments.py
python research/progressive.py
python research/render_guide.py
python -m unittest discover -s tests -v
python entry_pack/validate_pack.py
```

O1 guarda 30,000 vectores nulos, 66 parejas y 381 asignaciones; O2 guarda comparaciones y los 31 reajustes. Manifiestos fijan hashes de entradas/código/salidas. El manifiesto O1 registra la versión del banco **anterior** a añadir estados: consultar commit `0f5b949bb51e31a075fe292dd74f455d8c1fed7f`; las actualizaciones de ejecución no alteran cálculos del CSV. El protocolo y código ejecutable siguen enlazados. La hora/plataforma del manifiesto cambia al repetir; los artefactos numéricos con la misma versión Python son deterministas.

No se requiere scipy para reproducir. Como verificación independiente durante desarrollo, los 66 Fisher se compararon con scipy: máximo error absoluto 2.22e−16. [QA](QA.md) registra pruebas reales y límites visuales, sin confundir validadores de estructura con verificación científica.

## Prioridades siguientes

1. Revisión de las tres filas sin etiquetas y de las excepciones jerárquicas contra versiones autorizadas y un libro de códigos; no tratar cero como ausencia visual validada.
2. Ampliar BR-09 con otras inicializaciones/algoritmos y consenso humano solo con derechos y protocolo ciego. DR-04 se especializa cuando se seleccionen las figuras para publicación; aún no se ejecutó como investigación profunda.
3. Resolver permiso/procedencia de paletas antes de BR-10/H1; documentar que BobRossColors y jwilber no son fuentes independientes.
4. Completar créditos/fechas únicamente si van a usarse en una pregunta; no fechar biografía con ordinal de episodio. Mantener otras O2/O3 condicionales.
5. DR-05b después de esos avances; aprobación explícita de un commit científico antes de audiovisual.
