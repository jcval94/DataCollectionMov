#!/usr/bin/env python3
"""Render saved source and image evidence into browsable README files, offline."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import html
import json
import os
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
LABELS = {
    'DATA_SAMPLE': 'Registros recuperados', 'CACHED_SAMPLE': 'Registros publicados en el repo',
    'DOCUMENT_SAMPLE': 'Documento recuperado', 'METADATA_SAMPLE': 'Sólo catálogo o manifiesto',
    'DOC_ONLY': 'Sólo portal o documentación', 'HTTP_ERROR': 'Error HTTP',
    'BLOCKED': 'Acceso bloqueado', 'NETWORK_ERROR': 'Error de red',
    'PARSE_ERROR': 'Formato inesperado', 'EMPTY': 'Sin registros',
    'LIMIT_REACHED': 'Límite de descarga', 'DEPENDENCY_MISSING': 'Falta lector opcional',
    'MEDIA_SAMPLE': 'Cabecera de medio verificada', 'INTERNAL_ERROR': 'Error del verificador',
}

def relative(target, page):
    return Path(os.path.relpath(target, page.parent)).as_posix()

def slug(value):
    plain = ''.join(c for c in unicodedata.normalize('NFD', value.lower()) if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]+', '-', plain).strip('-')

def cell(value, limit=700):
    if value is None:
        return 'null'
    text = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list, bool)) else str(value)
    if len(text) > limit:
        text = text[:limit] + '… [ver JSON completo debajo]'
    return html.escape(text).replace('|', '&#124;').replace('\r', '').replace('\n', '<br>')

def samples(rows):
    if not rows:
        return ['Sin registros o ejemplos recuperados para esta prueba.', '']
    rows = [row if isinstance(row, dict) else {'valor': row} for row in rows]
    fields = list(dict.fromkeys(key for row in rows for key in row))
    out = ['| Campo | ' + ' | '.join(f'Ejemplo {i + 1}' for i in range(len(rows))) + ' |',
           '| --- | ' + ' | '.join('---' for _ in rows) + ' |']
    out.extend('| ' + cell(field) + ' | ' + ' | '.join(cell(row.get(field)) for row in rows) + ' |' for field in fields)
    # Keep exact machine-readable examples next to the readable table.
    out += ['', '<details>', '<summary>Ver los registros exactos en JSON</summary>', '',
            '```json', json.dumps(rows, ensure_ascii=False, indent=2), '```', '', '</details>', '']
    return out

def visuals():
    path = ROOT / 'catalogs/visual_examples.json'
    return json.loads(path.read_text())['examples'] if path.exists() else []

def figure(example, page, width=420):
    test = example.get('test', {})
    if test.get('status') != 'IMAGE_DECODED':
        return [f"Prueba visual: `{test.get('status', 'PENDIENTE')}` — {test.get('detail', '')}", '']
    src = relative(ROOT / example['local_path'], page) if example.get('local_path') else example['image_url']
    out = [f'<a href="{html.escape(example["record_url"], quote=True)}"><img src="{html.escape(src, quote=True)}" alt="{html.escape(example["alt"], quote=True)}" width="{width}"></a>', '',
           f'**{example["title"]}**. {example["attribution"]}. [Ficha original]({example["record_url"]}) · [Licencia y condiciones]({example["license_url"]}): {example["license"]}.', '',
           f'Prueba de imagen: **`{test["status"]}`**, HTTP `{test["http_status"]}`, `{test["format"]}`, **{test["width"]} × {test["height"]} px**, {test["bytes"]:,} bytes. Captura UTC: `{test["checked_at_utc"]}`.', '',
           example['display_scope'], '',
           'Archivo de imagen conservado en el repo.' if example.get('local_path') else 'Imagen incrustada desde el proveedor; su visualización depende de que esa URL siga disponible.', '',
           f'GET completo y decodificación de píxeles comprobados. SHA-256 completo: `{test["sha256"]}`. [Metadatos de origen]({example["metadata_url"]}).', '']
    return out

def check_lines(check, index):
    out = [f'**Prueba {index}: `{check["status"]}`** · [{check["kind"]}]({check["requested_url"]}) · HTTP `{check.get("http_status", "sin respuesta")}`.', '',
           f'Captura UTC: `{check.get("checked_at_utc", "no registrada")}`; duración: {check.get("elapsed_seconds", "?")} s.', '', check['detail'], '']
    if check.get('bytes_read') is not None:
        out += [f'Contenido: `{check.get("content_type", "no informado")}`; {check["bytes_read"]:,} bytes leídos; alcance del hash: `{check.get("hash_scope", "no informado")}`.', '']
    if check.get('archive_member'):
        member=check['archive_member']
        out += [f'Miembro del ZIP: `{member["name"]}`; {member["bytes_read"]:,} bytes leídos de {member["declared_bytes"]:,} declarados. SHA-256 `{member["sha256"]}`; alcance `{member["hash_scope"]}`. Se leyó dentro del archivo, sin extraer rutas al disco.', '']
    out += samples(check.get('sample', []))
    if check.get('child'):
        out += ['**Recurso enlazado: comprobación independiente**', '']
        out += check_lines(check['child'], str(index) + '.medio')
    return out

def source_lines(result, page, image_map):
    out = [f'### {result["id"]}', '', f'**{result["name"]}** — `{result["status"]}`.', '', result['note'], '']
    for index, check in enumerate(result['checks'], 1):
        out += check_lines(check, index)
    for example in image_map.get(result['id'], []):
        out += ['**Ejemplo visual y su test**', ''] + figure(example, page)
    return out

def render_report(payload, page):
    """Render one report; the full canonical report also gets thematic READMEs."""
    page = Path(page)
    page.parent.mkdir(parents=True, exist_ok=True)
    results = payload['results']
    counts = Counter(r['status'] for r in results)
    catalog = json.loads((ROOT / 'catalogs/datasets_reales_mexico.json').read_text())
    categories = {d['id']: d['category'] for d in catalog['datasets']}
    groups = defaultdict(list)
    for result in results:
        groups[categories[result['id']]].append(result)
    image_map = defaultdict(list)
    for example in visuals():
        image_map[example['dataset_id']].append(example)
    times = [c['checked_at_utc'] for r in results for c in r['checks'] if c.get('checked_at_utc')]
    full = page.resolve() == (ROOT / 'source_tests/README.md').resolve()
    lines = ['# Tests de fuentes: resultados, registros e imágenes', '',
             f'**{len(results)} fuentes comprobadas.** Fechas de las peticiones conservadas en este informe: `{min(times)}` a `{max(times)}` (UTC).' if times else f'**{len(results)} fuentes comprobadas.**', '',
             'Este README contiene las pruebas y sus ejemplos. Las tablas proceden de respuestas reales; los errores quedan visibles. Las imágenes tienen una prueba adicional de descarga completa y decodificación. Cada capa conserva su propia fecha: añadir una imagen no equivale a volver a probar toda la fuente.', '',
             '| Resultado más útil por fuente | Fuentes |', '| --- | ---: |']
    lines += [f'| `{status}` — {LABELS.get(status, status)} | {n} |' for status, n in sorted(counts.items())]
    lines += ['', 'Una página `DOC_ONLY` no acredita registros descargados. `METADATA_SAMPLE` sólo acredita metadatos. `CACHED_SAMPLE` usa archivos del repo. Una muestra por prefijo no es aleatoria ni prueba calidad global; su hash no identifica el archivo completo.', '',
              'Los errores/bloqueos describen estas peticiones desde este entorno, sin afirmar que el proveedor esté caído globalmente. No se inventan registros para sustituir datos inaccesibles.', '']
    if full:
        lines += ['## README por temática', '', '| Tema | Fuentes | Ejemplos visuales decodificados |', '| --- | ---: | ---: |']
        for category, members in groups.items():
            target = page.parent / 'by_topic' / slug(category) / 'README.md'
            image_count = sum(e.get('test', {}).get('status') == 'IMAGE_DECODED' for r in members for e in image_map.get(r['id'], []))
            lines.append(f'| [{category}]({relative(target, page)}) | {len(members)} | {image_count} |')
            topic = [f'# Tests: {category}', '', f'[Todas las pruebas]({relative(page, target)}) · [Catálogo]({relative(ROOT / "docs/CATALOGO_DATASETS_REALES.md", target)})', '',
                     'Resultados y ejemplos de las peticiones indicadas. Las imágenes se comprueban por separado; un portal accesible no equivale a datos ingeridos.', '']
            for result in members:
                topic += source_lines(result, target, image_map)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text('\n'.join(topic) + '\n')
    lines += ['', '## Índice de tests', '', '| Fuente | Resultado |', '| --- | --- |']
    lines += [f'| [{r["id"]}](#{r["id"]}) | `{r["status"]}` |' for r in results]
    lines += ['', '## Reproducir', '', 'Desde la raíz del repositorio:', '', '```bash',
              'python -m pip install pypdf openpyxl Pillow',
              '# Rehacer sólo los README a partir de la evidencia guardada (sin red):',
              'python scripts/render_source_readmes.py',
              '# Probar de nuevo las imágenes y actualizar los README:',
              'python scripts/check_visual_examples.py',
              'python scripts/render_source_readmes.py',
              '# Nueva prueba de acceso a todas las fuentes:',
              'python scripts/probe_catalog_sources.py',
              '# O sólo algunas, en selected/ para conservar el informe acumulado:',
              'python scripts/probe_catalog_sources.py --only dof-publicaciones bob-ross-paletas', '```', '',
              '`pypdf` y `openpyxl` son opcionales para PDF/XLSX; `Pillow` se usa para decodificar imágenes. El verificador de imágenes devuelve 1 si falla una imagen. En el verificador de fuentes, el código 0 sin `--strict` significa informe generado; `--strict` devuelve 1 si falla alguna comprobación, incluidos medios enlazados. No usa credenciales personales ni activa recolección programada.', '',
              '## Tests y ejemplos por fuente', '']
    for result in results:
        lines += source_lines(result, page, image_map)
    lines += ['## Evidencia y alcance', '',
              f'[Resultados JSON]({relative(page.parent / "results.json", page)}) · [Definiciones de tests]({relative(ROOT / "catalogs/source_probes.json", page)}) · [Manifest de pruebas visuales]({relative(ROOT / "catalogs/visual_examples.json", page)}) · [Catálogo]({relative(ROOT / "docs/CATALOGO_DATASETS_REALES.md", page)})', '',
              'El informe acumulado conserva las fechas y versiones del verificador en `results.json`: corrida inicial, ampliaciones y reintentos. Cada prueba visual guarda URL, HTTP, formato, dimensiones, bytes y hash de la respuesta completa. Decodificar una imagen no valida etiquetas, autenticidad histórica, OCR, contenido clínico ni representatividad de los datos.', '']
    page.write_text('\n'.join(lines))

def replace_block(path, name, block, before=None):
    start, end = f'<!-- {name}:START -->', f'<!-- {name}:END -->'
    content = path.read_text()
    replacement = start + '\n' + block.rstrip() + '\n' + end
    if start in content:
        content = re.sub(re.escape(start) + r'.*?' + re.escape(end), lambda _: replacement, content, flags=re.S)
    elif before:
        assert before in content, f'Ancla ausente: {before}'
        content = content.replace(before, replacement + '\n\n' + before, 1)
    else:
        content = content.rstrip() + '\n\n' + replacement + '\n'
    path.write_text(content)

def render_other_readmes(payload):
    examples = visuals()
    counts = Counter(r['status'] for r in payload['results'])
    passed = [e for e in examples if e.get('test', {}).get('status') == 'IMAGE_DECODED']
    root = ROOT / 'README.md'
    block = ['## Tests y ejemplos visibles', '',
             f'**{len(payload["results"])} fuentes probadas** y **{len(passed)} ejemplos visuales descargados y decodificados**. Resultados guardados con fecha, URL y evidencia; no todas las fuentes entregaron datos.', '',
             '| Resultado | Fuentes |', '| --- | ---: |']
    block += [f'| `{s}` — {LABELS.get(s, s)} | {n} |' for s, n in sorted(counts.items())]
    block += ['', '[Ver todos los tests, registros e imágenes](source_tests/README.md) · [Pruebas por temática](source_tests/README.md#readme-por-temática)', '',
              'Ejemplo de registros recuperados del CSV de paletas de Bob Ross:', '']
    palettes = next(r for r in payload['results'] if r['id'] == 'bob-ross-paletas')
    palette_rows = next((c['sample'] for c in palettes['checks'] if c.get('sample') and c['kind'] == 'csv'), [])
    block += ['| Título | Temporada | Episodio | Colores declarados |', '| --- | ---: | ---: | ---: |']
    block += [f'| {cell(r.get("painting_title"))} | {cell(r.get("season"))} | {cell(r.get("episode"))} | {cell(r.get("num_colors"))} |' for r in palette_rows]
    block += ['', 'Los tests de acceso y los de imágenes son independientes. A continuación, ejemplos reales de pintura, mapas, prensa y medicina histórica; los README temáticos también muestran producto, app, biodiversidad, sonograma y Bob Ross.', '']
    for dataset_id in ['met-arte', 'loc-mapas-historicos', 'loc-prensa-historica', 'wellcome-medicina-antigua']:
        block += figure(next(e for e in examples if e['dataset_id'] == dataset_id), root, width=300)
    replace_block(root, 'SOURCE_TESTS', '\n'.join(block), before='## Fuentes cubiertas')
    bob = ROOT / 'examples/bob_ross_discovery/README.md'
    image = next(e for e in examples if e['dataset_id'] == 'bob-ross-paletas')
    replace_block(bob, 'VISUAL_EXAMPLE', '\n'.join(['## Ejemplo visual de la fuente', '',
                  'La imagen siguiente procede del dataset de **paletas**. El cálculo de coocurrencias de este piloto usa el dataset de **elementos** de FiveThirtyEight; son fuentes distintas. Ver la imagen no constituye una nueva auditoría de las etiquetas del piloto.', ''] + figure(image, bob)))
    assets = ROOT / 'source_tests/assets/README.md'
    lines = ['# Imágenes de ejemplo conservadas en el repo', '',
             'Sólo se copian aquí los ejemplos seleccionados con dominio público o CC0 explícito. No se han editado las imágenes. Los otros ejemplos se incrustan desde el proveedor.', '',
             '| Imagen | Autor / colección | Condiciones | Test |', '| --- | --- | --- | --- |']
    for example in examples:
        if example.get('local_path'):
            lines.append(f'| [{example["title"]}]({Path(example["local_path"]).name}) | {example["attribution"]} | [{example["license"]}]({example["license_url"]}) | {example.get("test", {}).get("status", "PENDIENTE")} |')
    lines += ['', '[Tests, imágenes y registros completos](../README.md) · [URLs, dimensiones, hashes y fechas](../../catalogs/visual_examples.json)', '']
    assets.parent.mkdir(parents=True, exist_ok=True)
    assets.write_text('\n'.join(lines))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', type=Path, default=ROOT / 'source_tests/results.json')
    parser.add_argument('--output', type=Path, default=ROOT / 'source_tests/README.md')
    args = parser.parse_args()
    payload = json.loads(args.results.read_text())
    render_report(payload, args.output)
    if args.output.resolve() == (ROOT / 'source_tests/README.md').resolve():
        render_other_readmes(payload)
    print(f'README actualizado: {args.output}')

if __name__ == '__main__':
    main()
