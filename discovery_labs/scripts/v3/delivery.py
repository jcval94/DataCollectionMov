"""Evidence-linked teaching materials. Teacher references stay in ignored output."""
import base64
import html
import json
import shutil
import zipfile
from pathlib import Path

from .data import BASE, sha, write

TIMELINE = [(0, 5, 'Curiosidad y votación'), (5, 10, 'Apuesta y definición'),
            (10, 15, 'Dos caminos y primera evidencia'), (15, 28, 'Complicación y análisis'),
            (28, 36, 'Descubrimiento y giro crítico'), (36, 42, 'Debate'), (42, 45, 'Conclusión humana')]
HOOKS = {
    'uci-retail': ('La venta que cambió de puesto', 'Una tienda dispone de un espacio para destacar productos. Antes de elegir, ¿qué significa que un producto sea el mejor: unidades, importe registrado o ganancia? Hoy tenemos líneas de facturas, créditos y datos incompletos. El grupo decide qué pregunta puede investigar y qué dato se niega a inventar.'),
    'nba-elo': ('El partido contado dos veces', 'Imagina que debes explicar si un pronóstico merece confianza. La tabla ofrece miles de filas y probabilidades precisas. ¿Cada fila es un encuentro distinto? ¿Qué sabía el pronóstico antes del partido? Elige una pregunta y una predicción antes de consultar los resultados.'),
    'bob-ross-elementos': ('Un paisaje bajo sospecha', 'Debes organizar una pequeña exposición usando únicamente un archivo de etiquetas. Alguien recuerda árboles en todos los episodios y otra persona cree reconocer cuatro estilos. ¿Qué parte de esas intuiciones resiste una comprobación? Hoy la decisión es qué buscar, cómo representarlo y cuándo desconfiar del archivo.')}


def storyboard(contract, figure_ids, claim):
    """No surprise is asserted in advance. Every reveal points at an actual result."""
    qid = contract['id']; evidence = 'research/results.json#' + qid
    acts = [
        ('Curiosidad', contract['question'], '¿Qué decisión cambiaría tu respuesta?', None),
        ('Apuesta', contract['hypothesis'], 'Predice dirección o contraejemplo y qué te haría cambiar de opinión.', None),
        ('Primera evidencia', contract['metric_and_denominator'], 'Comprueba una fila y el denominador antes de interpretar.', 'quality/profile.json'),
        ('Complicación', contract['limitations'][0], '¿Qué parte de tu pregunta queda fuera de estos datos?', 'quality/transformations.json'),
        ('Descubrimiento', 'Consultar el resultado ejecutado; aceptar confirmación, refutación o ambigüedad.', '¿Qué patrón puedes señalar en una figura concreta?', evidence),
        ('Giro crítico', contract['adversarial_test'], '¿La conclusión cambia? Compara ambos resultados aunque no haya sorpresa.', evidence),
        ('Conclusión humana', 'Una respuesta, una figura, un argumento, un límite y una nueva pregunta.', '¿Qué afirmarías con tu nombre y qué dato pedirías después?', evidence)]
    return dict(question_id=qid, title=HOOKS[contract['source_id']][0], hook_30_60_seconds=HOOKS[contract['source_id']][1],
                evidence=evidence, figure_ids=figure_ids,
                acts=[dict(act=i+1, name=name, facilitation=text, audience_question=prompt,
                           transition='Antes de avanzar, el grupo explica qué dato necesita el siguiente paso.',
                           evidence=path, figures=figure_ids if i >= 4 else []) for i, (name, text, prompt, path) in enumerate(acts)],
                branches=dict(confirmed='Conservar alcance y buscar una sensibilidad que pueda debilitarlo.',
                              refuted='Mostrar el contraejemplo y revisar la predicción sin cambiar retroactivamente la hipótesis.',
                              inconclusive='Explicar qué falta y entregar un diagnóstico en lugar de un hallazgo inventado.'),
                class_timeline=[dict(start=a, end=b, activity=c) for a, b, c in TIMELINE],
                screencast=dict(minutes=55, segments=[dict(start=0, end=5, activity='Pregunta y predicción'),
                    dict(start=5, end=15, activity='Inspeccionar fuente, contrato y calidad'),
                    dict(start=15, end=30, activity='Ejecutar código y explicar decisiones reales'),
                    dict(start=30, end=42, activity='Interpretar figuras y tablas'),
                    dict(start=42, end=50, activity='Prueba adversarial y errores realmente observados'),
                    dict(start=50, end=55, activity='Conclusión con límites')],
                    rule='No representar errores, conflicto ni sorpresa que no ocurrieron.'))


def build(case, out, contracts, claims, figures):
    folder = out / 'education'; folder.mkdir(exist_ok=True)
    available = [c for c in contracts if c['execution_status'] == 'EXECUTABLE']
    stories = []
    for c in available:
        ids = [f['id'] for f in figures if c['id'] in f['question_ids']]
        stories.append(storyboard(c, ids, claims[c['id']]))
    write(folder/'storyboards.json', stories)
    title, hook = HOOKS[case]
    choices = '\n'.join(f'- {c["id"]}: {c["question"]}' for c in available)
    blocked = '\n'.join(f'- {c["id"]}: {c["blocking_reason"]}' for c in contracts if c['execution_status'] != 'EXECUTABLE') or 'Ninguna ruta bloqueada por datos en este snapshot.'
    (folder/'ALUMNO.md').write_text(f'''# {title}

{hook}

## Elige una ruta preparada

{choices}

Las otras perspectivas permanecen en el inventario y no entran a la votación:

{blocked}

## Tu registro (privado, sin enviarlo al repositorio)

1. Vota una pregunta y registra una predicción antes de abrir las figuras.
2. Escribe unidad, métrica, denominador y una observación que refutaría tu hipótesis.
3. Pide a tu IA dos caminos: el método descriptivo del contrato y su prueba adversarial. Decide tú.
4. Comprueba dos filas y un cálculo a mano; consulta silver.csv y el diccionario.
5. Ejecuta el script preparado o abre la evidencia offline tras registrar tu apuesta.
6. Contrasta una tabla con una figura y explica un límite de cobertura.
7. Entrega una respuesta, una figura, un argumento, un límite y una pregunta nueva.

Si se reinicia Python, vuelve a ejecutar desde el inicio. Si falla el entorno, abre index.html sin conexión.
No se necesitan cuentas, descargas ni instalaciones durante la clase. No hay calificación automática.
''')
    teacher = out/'teacher'; teacher.mkdir(exist_ok=True)
    (teacher/'FACILITACION.md').write_text(f'''# Facilitación · {title}

Material de preparación local; no incluir en el paquete de alumno.

Gancho de 30–60 segundos: {hook}

Rutas ejecutables: {', '.join(c['id'] for c in available)}. Revisar los contratos y sus límites antes de permitir votar.
No presentar seis rutas disponibles si una fuente sólo tiene tres ejecutables.

''' + '\n'.join(f'- {a}–{b} min: {c}.' for a,b,c in TIMELINE) + '''

En cada transición, pedir que el grupo explique qué sabe y qué le falta. La predicción puede fallar.
En el giro crítico, mostrar la sensibilidad aunque no cambie el resultado. Nunca inventar una sorpresa.
La conclusión pertenece al alumno: exigir magnitud, denominador, alcance y una objeción a la IA.

Revisar storyboards.json para los siete actos, preguntas al público, bifurcaciones y screencast de 55 minutos.
Las referencias calculadas de cada ruta se guardan en REFERENCIAS.json, fuera de la distribución del alumno.
''')
    write(teacher/'REFERENCIAS.json', claims)
    write(teacher/'ENSAYO.json', dict(status='NOT_OBSERVED', required=dict(observer='Identificador anónimo del observador independiente',
        date='Fecha real del ensayo', chosen_question='ID votado', actual_minutes_by_segment='Siete intervalos medidos',
        incidents='Fallos, confusiones y decisiones observadas', teacher_review='Decisión independiente y correcciones',
        accessible_mobile='Resultado de revisión con dispositivo', approval='Sólo después de corregir problemas críticos'),
        gates=dict(CLASS_READY=False, PUBLISHED=False)))
    return stories


def gallery(case, out, contracts, figures):
    cards = []
    for f in figures:
        p, m = f['variants']
        png = lambda name: 'data:image/png;base64,' + base64.b64encode((out/'visualization'/name).read_bytes()).decode()
        cards.append(f'''<article data-questions="{' '.join(f['question_ids'])}"><h2>{html.escape(f['title'])}</h2>
        <picture><source media="(max-width:600px)" srcset="{png(m['png'])}"><img src="{png(p['png'])}" alt="{html.escape(f['alt'], quote=True)}"></picture>
        <div class="projection"><p>{html.escape(p['denominator'])}</p><p>{html.escape(p['note'])}</p></div>
        <div class="mobile"><p>{html.escape(m['denominator'])}</p><p>{html.escape(m['note'])}</p></div>
        <details><summary>Procedencia y tabla</summary><p>{html.escape(f['source_url'])}</p><p>SHA256 {f['source_sha256']}</p>
        <a href="../gold/{f['table'].split('/')[-1]}">Tabla CSV</a></details></article>''')
    options = ''.join(f'<option value="{c["id"]}">{html.escape(c["id"]+" · "+c["question"])}</option>' for c in contracts if c['execution_status']=='EXECUTABLE')
    # A learning reveal, not an authorization mechanism. No reference answers or teacher notes in this file.
    page = '''<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>AI Discovery Labs · evidencia offline</title><style>
    *{box-sizing:border-box}body{font:18px/1.5 system-ui;margin:auto;max-width:1100px;padding:24px;color:#25313a;background:#f6f3ed}
    article,form{background:white;padding:20px;margin:24px 0;border:1px solid #a8b4ba;border-radius:12px}
    img{width:100%;height:auto;display:block}select,textarea,button{font:inherit;max-width:100%;width:100%;padding:12px;margin:8px 0}
    button{background:#24546a;color:white;border:0;cursor:pointer}p,a{overflow-wrap:anywhere}label{display:block;font-weight:600}
    [hidden]{display:none!important}.mobile{display:none}h1{font-size:clamp(1.5rem,5vw,2.5rem)}@media(max-width:600px){body{padding:12px}article{padding:8px}.projection{display:none}.mobile{display:block}}
    </style><main><h1>Una pregunta, una apuesta y evidencia</h1><p>Explorador técnico sin conexión. La aprobación de clase requiere ensayo humano y revisión docente.</p>
    <form id="vote"><label for="question">Pregunta preparada</label><select id="question" required><option value="">Elige una pregunta</option>__OPTIONS__</select>
    <label for="prediction">Tu predicción (no se guarda ni se envía)</label><textarea id="prediction" required minlength="5"></textarea>
    <button>Registrar apuesta y consultar figuras</button></form><p id="status" role="status"></p><section id="evidence" hidden>__CARDS__</section></main>
    <script>document.querySelector('#vote').addEventListener('submit',e=>{e.preventDefault();const q=document.querySelector('#question').value;
    const p=document.querySelector('#prediction').value.trim();if(!q||p.length<5)return;document.querySelector('#evidence').hidden=false;
    document.querySelectorAll('article').forEach(a=>a.hidden=!a.dataset.questions.split(' ').includes(q));
    document.querySelector('#status').textContent='Pregunta '+q+': comprueba la tabla, la figura y sus límites. La conclusión te corresponde.';});</script></html>'''
    (out/'education/index.html').write_text(page.replace('__OPTIONS__', options).replace('__CARDS__', ''.join(cards)))


def package(case, out):
    """Explicit allowlist, never copy a tree containing teacher/reference results."""
    destination = out/'student'; destination.mkdir(exist_ok=True)
    shutil.copy(out/'education/index.html', destination/'index.html')
    shutil.copy(out/'education/ALUMNO.md', destination/'ALUMNO.md')
    shutil.copy(BASE/'pilots'/case/'DICCIONARIO.md', destination/'DICCIONARIO.md')
    for filename in ['snapshot.csv', 'manifest.json']:
        shutil.copy(BASE/'pilots'/case/'data'/filename, destination/filename)
    # Figures and measured analytical CSVs are research artifacts, not a teacher answer key.
    # The portable gallery embeds figures; provide the linked CSVs at the expected relative location.
    text = (destination/'index.html').read_text().replace('../gold/', 'tables/')
    (destination/'index.html').write_text(text)
    tables = destination/'tables'; tables.mkdir(exist_ok=True)
    for source in (out/'gold').glob('*.csv'):
        shutil.copy(source, tables/source.name)
    # A runnable source slice accompanies the precomputed contingency, using only an allowlist.
    engine = destination/'research_engine/discovery_labs'
    sources = [BASE/'scripts/run_research.py', *sorted((BASE/'scripts/v3').glob('*.py')),
               BASE/'contracts/batch0.json', BASE/'requirements.txt',
               BASE/'evidence/pilot_runs'/f'{case}.json',
               BASE/'pilots'/case/'DICCIONARIO.md',
               BASE/'pilots'/case/'data/manifest.json', BASE/'pilots'/case/'data/snapshot.csv']
    for source in sources:
        dest = engine/source.relative_to(BASE); dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(source, dest)
    (destination/'EJECUTAR.md').write_text(f'''# Ejecutar la investigación

Preparar Python y requirements.txt antes de clase. Desde esta carpeta:

```sh
python research_engine/discovery_labs/scripts/run_research.py --case {case}
```

La ejecución no usa red. El código explicable y las políticas están en scripts/v3.
Las tablas se crean en research_engine/discovery_labs/output/v3/{case}/.
El modo offline precalculado es index.html. No registra ni transmite respuestas.
El paquete no incluye referencias docentes ni evaluación formal. Es un candidato técnico, sin aprobación de aula.
''')
    receipt = {str(p.relative_to(destination)):sha(p) for p in sorted(destination.rglob('*')) if p.is_file() and p.name!='package-manifest.json'}
    write(destination/'package-manifest.json', dict(distribution='student', files=receipt,
        teacher_reference_files_included=False, classroom_approved=False, published=False))
    # Fixed ZIP metadata avoids time-of-build differences.
    archive = out/'student-offline.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(destination.rglob('*')):
            if p.is_file():
                entry = zipfile.ZipInfo(str(p.relative_to(destination)), date_time=(2026,11,16,0,0,0))
                entry.compress_type = zipfile.ZIP_DEFLATED; entry.external_attr = 0o644 << 16
                z.writestr(entry, p.read_bytes())
    return archive
