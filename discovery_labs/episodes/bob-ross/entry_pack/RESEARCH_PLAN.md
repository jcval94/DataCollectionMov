# Plan de investigación — Bob Ross como una historia, no como una tabla

## Tesis editorial de trabajo (aún NO demostrada)
Bob Ross construyó durante más de una década un lenguaje visual y pedagógico reconocible. El dataset permite medir una parte: **motivos etiquetados por episodio**. La investigación debe explorar cómo se construyó, si evolucionó, dónde están sus excepciones y qué **no podemos** inferir sin otras fuentes.

El sujeto es **la historia documentada de Bob Ross y de su obra televisiva**. La unidad estadística del archivo es un episodio; no una pintura física, ni una audiencia, ni una fecha de ejecución del cuadro, ni un marcador de salud.

## Hipótesis históricas para investigar, sin resultados anticipados
1. **Evolución creativa:** entre S01 y S31 cambian combinaciones y diversidad de motivos; puede ser gradual o mostrar quiebres.
2. **Situación personal:** el diagnóstico de linfoma es un evento externo, cercano al cierre de la serie según fuentes biográficas. **No hay inferencia causal automática** y deben verificarse la fecha, el orden de grabación y explicaciones alternativas.
3. **Herencia de Alaska:** la relación con montañas/nieve es narrativa plausible; el CSV no trae el lugar real en que se inspira cada cuadro.
4. **Más allá del arquetipo:** hay 36 episodios del anfitrión sin TREE/TREES; estudiar quiénes son y por qué el arquetipo persiste.
5. **Obra no emitida:** existen siete pinturas preparadas para la temporada 32 (AP); no están necesariamente representadas en este CSV: una frontera de cobertura.
6. **Espontaneidad versus producción:** entrevistas cuentan que podía preparar tres versiones de un cuadro; el CSV no registra ensayos/guiones.

## Etapas de investigación dentro de Fase 1
| Lote | Trabajo | Salidas | Gate |
|---|---|---|---|
| 0. Ingesta | Repetir hash, 403×69, nulos, GUEST, conflictos de etiquetas y copy sample | QA y datadictionary actualizados | DATACHECKED |
| 1. Contexto | Ejecutar DR-01 y DR-03, conciliar biografía, temporización, mitos, antecedentes | timeline + claims registry | CONTEXT_REVIEWED |
| 2. Enriquecimiento | DR-02: fecha grabación/emisión, metadata paletas, cruce episodios; registrar no coincidencias | tabla de joins con cobertura | ENRICHED_OR_BLOCKED |
| 3. Diseño | Ejecutar Question Forge; puntuar 12 arcos; priorizar 3–5 y definir O1/O2/O3 condicionales | question_graph v2 + scoring | QUESTIONS_REVIEWED |
| 4. EDA y métodos | Tendencias, cambios, outliers multiescala, combinaciones, sensibilidad, control de invitados y anotaciones | scripts, figuras, resultados y pruebas | RESEARCH_REPRODUCIBLE |
| 5. Evidencia visual | DR-04, elegir 4–8 figuras y explorador de clusters con tarjetas hover/focus de episodios | capturas, QA mobile, derechos | VISUAL_REVIEWED |
| 6. Documento | Actualizar **research_guide.html** como ensayo científico sobre la historia real, con modo narrativo/técnico | HTML autónomo aprobado por QA | HUMAN_APPROVAL_PENDING |

**Stop:** no crear storyboard del video, guion de voz, intro, Remotion, MP4 ni material audiovisual hasta aprobación explícita de la guía científica.

## Métodos por tema
- **Trayectorias:** tasa de cada motivo por temporada, intervalos o bandas, small multiples, cambios observados con contraste contra modelo suave, sensibilidad a invitados y complejidad de etiquetas.
- **Cortes temporales:** usar temporada como ordinal; fechas de grabación/emisión solo si se consiguen y califican. No superponer «diagnóstico» sobre el episodio que lo sucede por índice.
- **Atípicos multiescala:** rareza por combinación frente a frecuencia base, tamaños de grupo, especificación de métrica y bootstrap por temporada; escalar episodio → temporada → era. Contrastar efectos espurios por denominadores pequeños.
- **Combinaciones:** lift y coocurrencias frente a esperados, corregir pruebas múltiples, separar dependencias constructivas como SNOWY_MOUNTAIN.
- **Clustering:** comparar con el KMeans ya existente y el k-medoids Jaccard; ARI, tamaño, medoids, estabilidad y asignaciones. Nunca «cuatro estilos verdaderos» sin evaluación externa.
- **Cultura e historia:** triangulación narrativa de por lo menos dos fuentes independientes, diferencias entre biografía y dataset, registrar versiones y contradicciones.
- **Causalidad salud-estilo:** describir hechos verificables y posibles cambios, sin atribución causal si no existen mediciones temporales y controles sólidos.

## Guía de prioridad
**Lote A:** evolución + outliers jerárquicos + mito de árboles (entradas narrativas accesibles). **Lote B:** clustering + paleta/imagen (necesita enriquecimiento, derechos y revisiones). **Lote C:** asociación biográfica y lagunas de cobertura (requiere varias fuentes externas).

Una buena pregunta queda **bloqueada honestamente** si no alcanza evidencia; eso es una lección, no un fracaso.

## Cómo debe verse el documento Fase 1
1. **Prólogo histórico documentado**: ¿quién era Bob Ross y por qué sus paisajes se volvieron reconocibles?
2. **El archivo y su frontera**: 403 episodios etiquetados; tres versiones de cuadros por episodio y obras de una temporada inconclusa como contexto.
3. **La primera impresión**: iconografía y representaciones frecuentes.
4. **Cuando avanzan los años**: evolución de motivos, sin inventar fechas.
5. **Las excepciones hablan**: análisis de outliers de tres niveles.
6. **La gran complicación**: invitaciones, codificación, paletas y clustering; qué cambia con otra definición.
7. **Capa biográfica**: qué eventos se conocen y qué hipótesis no podemos probar.
8. **Una respuesta más difícil**: hallazgos robustos, fronteras, nuevas preguntas O2/O3.
9. **Reproducibilidad total**: cifras, parámetros, enlaces, hashes, incidencias y scripts.
10. **Aprobación**: lista de puertas y versión del reporte; NO APROBADO hasta autorización.

## Definición de éxito visual
Una figura debe cambiar cómo entendemos algo: mostrar antes/después o grupo/composición; comparar absoluto/porcentaje; mostrar incertidumbre; permitir inspección individual y regreso al agregado. Toda interacción debe ser accesible vía teclado y focus, funcionar con fallback offline y nunca ofrecer una pintura como imagen integrada sin derechos verificados.

## Puertas de aprobación
- [ ] Investigación de contexto citada, fechas y afirmaciones conciliadas.
- [ ] Al menos tres arcos O1→O2→O3 revisados y ejecutados donde haya dato disponible (o marcados bloqueados).
- [ ] QA de datos y figures calculadas desde snapshots versionados.
- [ ] Explicaciones rivales, robustez, incertidumbre y categorías claras.
- [ ] Licencias de imágenes/hotlink verificados; fallback gráfico sin retratos ni pinturas.
- [ ] HTML narrativo/técnico con pruebas mobile, scroll, hover/focus/teclado y lectura accesible.
- [ ] Documento firmado por el usuario: `RESEARCH_APPROVED:<commit>`.

Solo al pasar **todas** las puertas necesarias y contar con aprobación humana puede arrancar el storytelling audiovisual.
