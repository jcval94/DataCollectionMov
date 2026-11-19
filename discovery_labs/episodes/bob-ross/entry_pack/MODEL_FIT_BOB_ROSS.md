# Ajuste de modelos — exclusivamente Bob Ross

Este documento conserva **solo criterios específicos de Bob Ross**. El catálogo canónico está integrado en `main` en `discovery_labs/shared/model_catalog/MODEL_SET.md` (PR #11 ya fusionado). No hay copia de 24 modelos en el episodio.

**Población y variables:** 403 episodios, 381 sin GUEST y 22 con invitado, 31 temporadas ordinales, 67 etiquetas binarias originales y 12 familias OR; no existen en el CSV fecha exacta de grabación, enfermedad, audiencias, costes ni colores. No extraer causa clínica, estilo artístico verdadero o ingresos de estas variables.

**Criterios de exclusión:** LSTM/transformers M16 con 31 temporadas insuficientes; riesgo colectivo M22 sin frecuencia y severidad de pérdidas; RL M23 sin acciones/recompensa; diferencia-en-diferencias M20 sobre enfermedad sin identificación ni cronología. Optuna M18 solo en fase posterior con suficiente dato, target, CV adecuado y autorización de entrenamiento.

## Mapear métodos a las preguntas (sin entrenar)

- **Historia/evolución:** M01 + IC/test de tendencia, M02/M03 si se justifica; temporal ordinal.
- **Hipótesis de salud:** M03 solo para cambios descriptivos con fechas verificadas; M20 **bloqueado**, no atribución clínica.
- **Outliers:** M05 + bootstrap/ranking robusto; comparar rareza episodio/temporada/era.
- **Mitos:** M01 o M12 y test binomial/intervalos, más grupos y variantes de definición.
- **Coocurrencia:** M10 + Fisher/FDR y contraste contra base-rate; diagramas de lift.
- **Clustering:** M07/M08 + estabilidad por bootstrap/ARI, más panel de representantes.
- **Invitados:** M19 + test exacto de Fisher e IC con n=22; no causal.
- **Paleta externa:** M09/M12 + pruebas de distribución/color solo tras join y permiso.
- **Cobertura:** M17 (escenarios de sensibilidad) + análisis de selección/missingness, sin inventar datos de pinturas ocultas.
- **Museo ficticio:** M21 + simulaciones de balance/redistribución, indicando hipótesis.

## Rutas y validaciones del episodio

Los 14 arcos canónicos están en `QUESTIONS_MASTER.md` + `questions_master.json`. Cada uno señala un modelo Mxx, un ejercicio estadístico separado, sus requerimientos y su estado `PLAN_ONLY`. La sección técnica de `research_guide.html` debe reflejar su evidencia, y las fechas externas en `CONTEXT_CLAIMS.md` no deben usarse como variables clínicas observadas.

## Dependencia de integración

- Motor compartido: [PR #11](https://github.com/jcval94/DataCollectionMov/pull/11).
- Episodio Bob Ross: [PR #5](https://github.com/jcval94/DataCollectionMov/pull/5) y [PR #10](https://github.com/jcval94/DataCollectionMov/pull/10).
- Integrar shared primero; después reemplazar los dos archivos heredados de catálogo/skill por stubs o referencias, sin romper el validador.
