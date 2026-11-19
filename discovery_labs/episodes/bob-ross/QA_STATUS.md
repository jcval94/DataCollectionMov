# Auditoría de alcance y estado de validación

## Nuevo paquete de entrada (18 de noviembre de 2026)

Se agregó `entry_pack/` como Fase 0 anterior a la guía científica: metadata/13 filas reales de muestra, 12 árboles de preguntas de 1.º→2.º→3.er orden, 24 ramificaciones condicionales, cinco prompts DR (cuatro especializados + síntesis), 12 URLs de investigación con estados de derechos, skill reusable, plan, brief visual y prompt de Fase 1.

**Comprobado mediante inspección del conector:** IDs de las 13 filas presentes en el CSV de 403 filas (sin duplicados), mismo blob Git del archivo original ya verificado, estructura de 12 árboles con dos ramas cada uno, cinco prompts y puertas de Fases 2–3 bloqueadas. **No se ejecutaron todavía los Deep Research externos ni los tests Python nuevos en GitHub Actions.** La lista de fuentes es un inicio a investigar, no 12 referencias con todas las afirmaciones corroboradas.

La vista de pintura al seleccionar un cluster es un **requisito para la guía HTML científica**, no una funcionalidad actualmente aprobada: depende de derechos de imágenes y de revisión de accesibilidad (hover + teclado + tap). Los antiguos números 36/48 siguen siendo resultados de etiquetas; no se ha probado cambio de estilo por enfermedad.



**Corte:** 17 de noviembre de 2026. **Ámbito exclusivo:** `discovery_labs/episodes/bob-ross/`.

## Comprobaciones realizadas y observadas

| Control | Resultado | Evidencia |
|---|---|---|
| Carpeta exclusiva | PASS | Archivos modificados del PR #5 tienen el prefijo exacto de esta carpeta; no se tocaron workflows ni otros casos. |
| Fuente íntegra | PASS | Blob SHA Git `c22fdf42b2323a6197a580d3ed1b446e1b5b659e` idéntico al archivo previo; SHA-256 original en `data/manifest.json`. |
| Cobertura | PASS | 403 filas, 67 etiquetas binarias, 381 anfitrión y 22 invitados. |
| Conteos verificados desde el CSV | PASS | Entre anfitrión, 345 con árboles, 36 sin árboles, 150 con montañas y 48 de esos sin nieve; invitados 16/22 con árboles. |
| Contrato de preguntas | PASS | Seis IDs únicos A/B/C/D1/D2/E, con métrica, hipótesis, dos caminos y adversario. |
| Bundle HTML | PASS sintáctico | JavaScript inline compilado mediante V8; 403 filas y seis preguntas incrustadas, sin elementos con ID duplicado o IDs de interfaz ausentes; no hay librerías ni peticiones remotas declaradas. |
| Visualizaciones estáticas | Generadas | Tres SVG de referencia desde el CSV: motivos, denominadores y museo hipotético. Sin arte ajeno ni reproducciones de pinturas. |

## Pruebas preparadas pero no acreditadas como ejecutadas

- **`python run.py --check`**: verifica hash, esquema, nulos binarios, duplicados, 381/22 y contraejemplos.
- **`python run.py --write`**: debe construir Silver CSV, Gold JSON y tres SVG dentro de `output/`.
- **`python clustering.py --write`**: debe generar k-medoids Jaccard/Euclídea, ARI, análisis sin árboles y el cuarto SVG.
- **`python -m unittest discover -s tests -v`**: 18 tests Python, creados pero todavía sin corrida registrada en este PR.
- **`node qa_static.cjs`**: control independiente de bundles y datos embebidos. El archivo está listo para ejecutar, no es una prueba de navegador real.

**GitHub Actions:** al comprobar el commit de esta rama no aparecieron ejecuciones asociadas al nuevo PR. Se respetó la restricción de no editar `.github/workflows` ni otro directorio. No se puede declarar CI verde sin una ejecución real.

## Puertas que siguen bloqueadas

1. Ejecutar y registrar los comandos anteriores sobre el SHA final de la rama.
2. Corregir cualquier fallo si apareciera, sin salir de esta carpeta.
3. Renderizar y revisar figuras en proyector y móvil; probar teclado y lector de pantalla.
4. Ensayo humano cronometrado de 45 minutos con alumnos principiantes.
5. Revisión docente independiente del guion, las preguntas y las interpretaciones.
6. Política de distribución de la guía docente: el repositorio es público.

**Estado editorial:** `TECHNICAL_DRAFT / CLASS_READY=false`. El PR permanece en borrador; no fusionar ni publicar en la plataforma hasta superar las puertas de calidad.

## Forma de reproducir

Desde la carpeta del episodio:

```bash
make check
make research
make clusters
make browser-qa  # requiere Node.js, sin npm
```

No se necesitan red, cuentas ni credenciales para los comandos; todos los archivos fuente están dentro de este directorio. Los tests y los scripts no alteran datos en otras carpetas del repositorio.
