# Implementación: primera entrega

Se instalaron cuatro skills personales, verificadas en sus rutas guardadas. Las skills conservan procedimiento y criterios; el código de análisis y los resultados pertenecen a este repo.

| Skill | Acceso |
| --- | --- |
| integrar-fuentes-publicas | [Abrir skill](https://chatgpt.com/skills?skill_id=6aec094837b48191be11e4363dd64c01) |
| analizar-territorio-mexico | [Abrir skill](https://chatgpt.com/skills?skill_id=6aec09630070819187372c72e60e7c39) |
| investigar-corpus-con-evidencia | [Abrir skill](https://chatgpt.com/skills?skill_id=6aec09822a6c8191a5c39b445cd8a8c2) |
| comparar-versiones-documentales | [Abrir skill](https://chatgpt.com/skills?skill_id=6aec09a2278c81918012376271d3b695) |

## Arnés y piloto ejecutado

[Retail: resultados, tests, ejemplos y gráfica](../../examples/retail_discovery/README.md). El ejecutor `scripts/run_discovery.py` implementa por ahora un adaptador de retail: ingesta acotada o snapshot local, contrato, cálculo Decimal, sensibilidad y README. Las 72 fuentes conservan su plan y sus pruebas de acceso anteriores.

- Datos completos leídos: 541,909 filas; 536,429 elegibles con la política publicada.
- Ocho pruebas de comportamiento pasaron, además del esquema del archivo y los cuadres de ambas variantes.
- Caso medido: código 23843, segundo por bruto, 168,469.60 GBP positivos y la misma cifra negativa; neto cero. No se atribuye una causa comercial sin evidencia adicional.
- Se conservan faltantes de cliente; se identificaron 5,268 duplicados exactos y se calculó una variante sin ellos.
- La gráfica se produce con matplotlib y se incrusta en el README. Manifiesto, fecha y hash completo permiten cotejar el original.

## Herramientas y alcance

Se utilizaron HTTP, archivos y Python disponibles. No se configuraron servidores MCP adicionales: Docling y LangGraph siguen siendo opciones pendientes de una prueba que justifique incorporarlos. No se ejecutaron modelos de IA ni se programaron nuevas recolecciones.

## Qué sigue

1. Revisar comercialmente la política de códigos de producto y las líneas de crédito; distinguir devoluciones enlazadas de ajustes.
2. Aplicar GEO a una zona y fecha acotadas con capas completas; registrar CRS, bordes y no emparejados.
3. Aplicar CORPUS/VERSION al caso DOF, ampliando la evidencia por artículo y transitorio.
4. Elegir un corpus histórico accesible y una muestra anotada antes de escalar a OCR o clasificación.

Las cuatro skills pasaron validación de estructura; la integración tiene una prueba real en retail. La calidad metodológica de geografía y corpus requiere sus propios pilotos, todavía pendientes.
