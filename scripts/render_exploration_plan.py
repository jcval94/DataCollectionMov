#!/usr/bin/env python3
"""Validate the design catalogue and render its README, without network calls."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import hashlib
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / 'catalogs/exploration_plan.json'
README = ROOT / 'docs/exploration/README.md'

def validate(plan, catalog):
    expected = {d['id'] for d in catalog['datasets']}
    ids = [case['id'] for case in plan['cases']]
    assert len(ids) == len(set(ids)), 'IDs de fuente duplicados'
    assert set(ids) == expected, 'El plan no coincide con las fuentes del catálogo'
    question_ids = []
    question_texts = []
    for case in plan['cases']:
        assert case['plan_status'] in {'proposed_not_executed','partially_executed'}, case['id']
        assert len(case['questions']) >= 3, 'Faltan preguntas: ' + case['id']
        for question in case['questions']:
            assert question['id'].startswith(case['id'] + '.q'), question['id']
            assert question['text'].startswith('¿') and question['text'].endswith('?'), question['id']
            question_ids.append(question['id'])
            question_texts.append(question['text'].casefold())
        for field, registry in [('skills', 'skills'), ('tools', 'tools'), ('harnesses', 'harnesses')]:
            assert len(case[field]) == len(set(case[field])), (case['id'], field, 'duplicados')
            assert set(case[field]) <= set(plan[registry]), (case['id'], field, 'referencia inexistente')
        assert {'BASE', 'INGEST'} <= set(case['skills']), case['id']
        assert 'H0' in case['harnesses'] and len(case['harnesses']) >= 2, case['id']
        assert case['execution_harness'] in plan['execution_harnesses'], case['id']
        assert set(case['additional_source_ids']) <= expected, case['id']
        assert case['id'] not in case['additional_source_ids'], case['id']
        assert len(case['specific_checks']) >= 2, case['id']
        assert case['needed_inputs'] and case['access_gate'] and case['first_output'], case['id']
        assert case['source_test_link'] == 'source_tests/README.md#' + case['id'], case['id']
    assert len(question_ids) == len(set(question_ids)), 'IDs de pregunta duplicados'
    assert len(question_texts) == len(set(question_texts)), 'Preguntas textuales duplicadas'
    referenced = {r['id'] for r in plan['references']}
    assert all(set(tool['references']) <= referenced for tool in plan['tools'].values())
    return dict(sources=len(ids), questions=len(question_ids), categories=len({c['category'] for c in plan['cases']}),
                skill_routes='PASS', tool_routes='PASS', harness_routes='PASS', source_dependencies='PASS',
                question_uniqueness='PASS', scope='Validación estructural del plan, no validación de respuestas ni instalación de herramientas')

def cell(text):
    return html.escape(str(text)).replace('|', '&#124;').replace('\n', '<br>')

def refs(values, prefix):
    return ', '.join(f'[{v}](#{prefix}-{v.lower()})' for v in values)

def render(plan, receipt):
    groups = defaultdict(list)
    for case in plan['cases']:
        groups[case['category']].append(case)
    out = ['# De las fuentes a preguntas, herramientas y pruebas', '',
           f'Propuesta revisada el **{plan["reviewed_on"]}**, {plan["timezone"]}. **{receipt["sources"]} fuentes · {receipt["questions"]} preguntas · {receipt["categories"]} temáticas.**', '',
           'El objetivo es descubrir relaciones inesperadas usando IA y comprobarlas con datos. Esta propuesta conecta cada fuente con preguntas específicas, skills reutilizables, herramientas/MCP y un arnés de evaluación. Las preguntas siguen abiertas salvo los alcances ejecutados del piloto retail Q1 y la [demo acotada de clustering de Bob Ross](../../examples/bob_ross_clustering/README.md), que no verifica estilos ni otra medida de distancia. Ver [avance de implementación](IMPLEMENTACION.md) y [resultado retail](../../examples/retail_discovery/README.md).', '',
           '**Interpretación de la sigla:** se toma «MCC» como **MCP**, Model Context Protocol. Si la intención era otra, sólo habría que ajustar la capa de herramientas.', '',
           '[Catálogo de fuentes](../CATALOGO_DATASETS_REALES.md) · [Tests y muestras existentes](../../source_tests/README.md) · [Guía de descubrimientos](../GUIA_DESCUBRIMIENTOS_IA.md) · [Plan JSON](../../catalogs/exploration_plan.json)', '',
           f'Base de la propuesta: [commit {plan["based_on"]["commit"][:8]}](https://github.com/{plan["based_on"]["repository"]}/commit/{plan["based_on"]["commit"]}). El JSON conserva los hashes del catálogo y las evidencias consultadas.', '',
           '## Tres piezas que se complementan', '',
           '| Pieza | Para qué sirve | Ejemplo |', '| --- | --- | --- |',
           '| Skill | Procedimiento, decisiones y criterios que el agente debe aplicar. | Analizar encuestas respetando ponderadores y dominios. |',
           '| MCP o herramienta | Acceso a una capacidad: leer, consultar, extraer o ejecutar. | GitHub, HTTP de INEGI, lector PDF, Docling MCP, Python/SQL. |',
           '| Arnés | Entorno y contrato que ejecuta, registra y evalúa el trabajo. | Fijar datos y pregunta, correr código, contrastar con referencias y producir evidencia revisable. |', '',
           'La API de un productor, una biblioteca Python y un MCP son piezas distintas. Podemos usar las APIs actuales mediante adaptadores y herramientas nativas; añadir MCP donde facilite reutilizar capacidades entre clientes. El MCP por sí solo no garantiza corrección analítica.', '',
           '## Prioridad sugerida', '',
           'Reutilizar **BASE** y desarrollar primero **INGEST, GEO, CORPUS y VERSION**: cubren el trabajo ya iniciado con movilidad, fuentes públicas, documentos históricos y DOF. Especializar después SURVEY, VISION, GRAPH y MATH según el piloto elegido; AUDIO y MOTION necesitan corpus y dependencias específicos.', '',
           '| Piloto | Pregunta inicial | Qué lo vuelve interesante | Primer alcance revisable |', '| --- | --- | --- | --- |',
           '| Bob Ross | ¿Qué cambia al comparar pigmentos declarados, motivos y color de las reproducciones? | Unir etiquetas, imagen y estadística; ya hay CSV y un piloto de coocurrencias. | Una muestra de imágenes autorizadas y cruce por episodio; no asumir derechos ni concordancia. |',
           '| Retail | ¿Qué productos cambian de posición al descontar devoluciones? | Una decisión de negocio cambia al definir correctamente la métrica. | Ventas brutas/netas y tratamiento explícito de cancelaciones. |',
           '| DOF y Git | ¿Qué cambia cuando leemos transitorios y vigencia además del diff? | Enseñar versiones con un caso real y una trampa de interpretación. | Un artículo y sus documentos oficiales, con antes/después revisado. |',
           '| Matemáticas, GSM8K y CCH | ¿Un problema equivalente produce respuestas inconsistentes de IA? | Evaluar estabilidad, unidades y representaciones, además de acierto. | Pequeño conjunto con soluciones revisadas y variantes; no es evaluación de alumnos. |',
           '| Territorio en México | ¿Qué brechas cambian al pasar de CP a recorridos caminables? | Conectar DENUE, escuelas, población y movilidad con tu repo. | Una zona, cortes compatibles y evaluación de calidad de red/capas. |',
           '| Medicina histórica y diarios | ¿Vigilia nocturna significa costumbre, consejo o enfermedad? | Hallazgo potencial sorprendente con contraejemplos y contexto histórico. | Corpus delimitado de páginas y autores; hace falta recuperar contenido, no sólo portada. |',
           '| Napoleón y literatura | ¿La red de interlocutores cuenta otra historia que los temas más frecuentes? | Contrastar análisis de texto y estructuras de relaciones. | Una edición y periodo, con entidades y pasajes revisados. |', '',
           'Esta prioridad es una propuesta por acceso, utilidad didáctica y potencial de sorpresa; no es una estimación medida de costo o beneficio.', '',
           '## Skills reutilizables', '',
           '| ID | Skill | Situación | Cuándo conviene |', '| --- | --- | --- | --- |']
    for key, skill in plan['skills'].items():
        out.append(f'| [{key}](#skill-{key.lower()}) | {skill["name"]} | {skill["status"]} | {skill["priority"]} |')
    out += ['', 'La tabla distingue las cuatro skills instaladas de las especialidades propuestas; el detalle está en [implementación](IMPLEMENTACION.md). Una skill se justifica si captura decisiones repetidas y errores recurrentes. Las capacidades generales de Data ya disponibles cubren buena parte de BASE.', '']
    for key, skill in plan['skills'].items():
        out += [f'### skill-{key.lower()}', '', f'**{skill["name"]}**. {skill["scope"]}', '']
    out += ['## MCP y herramientas: situación real y propuesta', '',
            'Todos los casos usan GitHub, archivos/ejecución y acceso a la fuente. La columna de herramientas de cada ficha añade lectores documentales o multimedia según lo necesario. «Propuesto» no significa «conectado» ni «probado».', '']
    for key, tool in plan['tools'].items():
        out += [f'### tool-{key.lower()}', '', f'**{tool["name"]}** — {tool["kind"]}.', '',
                f'**Situación:** {tool["status"]}.', '', tool['use'], '']
    out += ['Un futuro MCP propio de datos públicos sólo tendría sentido si se reutilizan operaciones estables: listar recursos, recuperar un snapshot con manifiesto, consultar tablas permitidas, devolver una página y su localizador, o registrar evidencia. Sus nombres de herramientas y contratos se diseñarían entonces; no se presupone que existan servidores oficiales para cada fuente.', '',
            'Para un piloto basta un coordinador, ejecución reproducible y revisión de evidencia. La consulta se calcula con código; la IA ayuda a clasificar, proponer conexiones y explicar. Elegir modelos por la evaluación del piloto: modelo económico para extracción estructurada revisable; más capacidad de razonamiento para diseñar el método o revisar casos ambiguos; visión/ASR sólo cuando la pregunta lo requiera. Guardar modelo, versión, parámetros, costo y prompt de cualquier ejecución futura.', '',
           '## Arnés de ejecución por caso', '',
           'Aquí se distinguen dos niveles: el arnés de ejecución coordina herramientas, estado y artefactos; los perfiles de validación fijan las pruebas de método. Cada fuente tiene ambos asignados. Esta distinción permite empezar en el entorno actual y adoptar un runtime más complejo sólo donde haga falta.', '']
    for key, execution in plan['execution_harnesses'].items():
        out += [f'### execution-{key.lower()}', '', f'**{key}: {execution["name"]}**', '',
                execution['choice'], '', f'**Aplicar a:** {execution["when"]}', '',
                f'**Situación:** {execution["state"]}', '', f'**Aceptación:** {execution["acceptance"]}', '']
    out += ['LangGraph se propone para reanudar flujos de documentos y revisión con estado explícito, capacidades documentadas por su productor. No se presupone que su adopción mejore la calidad de una respuesta: eso lo prueba la evaluación del piloto. [Documentación primaria](https://docs.langchain.com/oss/python/langgraph/overview).', '',
            '## Arnés común y perfiles por método', '',
            'Propuesta de implementación gradual: CLI Python, snapshots inmutables, contratos por fuente y funciones de cálculo/evaluación. SQL local puede apoyar tablas; la extensión espacial de DuckDB es una opción, su instalación sigue pendiente. Elegir un framework de agentes después de que un piloto demuestre qué capacidades necesita.', '',
            '```mermaid', 'flowchart TD', '    Q["Pregunta y alcance"] --> A{"¿Datos suficientes?"}',
            '    A -->|No| P["Pendiente con evidencia"]', '    A -->|Sí| C["Cálculo y extracción"]',
            '    C --> V{"¿Pasa el arnés?"}', '    V -->|No| R["Revisar método o fuente"]',
            '    R --> C', '    V -->|Sí| D["Hallazgo delimitado y README"]', '```', '',
            '| Registro por ejecución | Contenido mínimo |', '| --- | --- |',
            '| run.json | Pregunta/ID, estado, fecha, código, entorno, parámetros y modelo/prompt si se usa IA. |',
            '| inputs/manifest.json | Fuente, acceso, edición, licencia, hash y alcance, cobertura y rutas de originales. |',
            '| contrato.json | Grano, llaves, unidades, diccionario y reglas de inclusión/exclusión. |',
            '| evidence.jsonl | Afirmación o etiqueta, registro/página/intervalo, evidencia localizable y estado de revisión. |',
            '| metrics.json y tablas | Fórmulas/código, denominadores, resultados de referencia y sensibilidad. |',
            '| evals/ y README.md | Casos de evaluación, errores/desacuerdos, imágenes cuando correspondan y límites del hallazgo. |', '',
            'Estas rutas describen el contrato propuesto para futuros experimentos; el documento no afirma que ya exista un ejecutor general que las produzca.', '']
    for key, harness in plan['harnesses'].items():
        out += [f'### harness-{key.lower()}', '', f'**{key}: {harness["name"]}**', '']
        out += [f'- {check}' for check in harness['checks']]
        out += ['', f'**Salida revisable:** {harness["output"]}.', '']
    out += ['## Qué se considera una prueba suficiente', '',
            '| Capa | Estado en este repo | Qué permite afirmar |', '| --- | --- | --- |',
            '| Acceso y ejemplos | Ya existen 72 fichas de prueba y nueve imágenes decodificadas. Cada petición conserva fecha y alcance. | Se recuperó el recurso/capa indicado, o se documentó el fallo. |',
            '| Integridad de este plan | Validada por el script de este documento. | Todas las fuentes tienen preguntas y rutas válidas a skills, herramientas y arneses. |',
            '| Método y datos completos | Primer piloto retail Q1 ejecutado; otros casos pendientes. | Grano, transformaciones y conclusiones resisten controles pertinentes. |',
            '| Calidad de la IA | Pendiente por piloto. | Una evaluación independiente muestra errores, estabilidad y límites en la tarea concreta. |', '',
            'Como punto de partida, diseñar un conjunto manual pequeño y estratificado: páginas con OCR bueno/malo y pasajes ambiguos; imágenes con reproducciones distintas; ejercicios equivalentes y casos negativos. El tamaño y los umbrales se fijan según uso y riesgo antes de confirmar una hipótesis. Evaluar tanto errores como cobertura; una puntuación de un modelo que se evalúa a sí mismo no basta.', '',
            'Pruebas negativas útiles: HTML con HTTP 200 donde se esperaba CSV; CP con cero inicial perdido; unión que duplica gasto; miles de pesos interpretados como pesos; página ausente; negación omitida; distintas fotos de la misma obra repartidas entre entrenamiento y prueba; fórmula o audio ilegible; instrucciones incrustadas en el corpus tratadas como texto. Son casos a implementar, no tests de método ya pasados.', '',
            '## Matriz por fuente', '',
            'En cada ficha, la fecha y estado de acceso proceden de las pruebas guardadas; no se volvieron a consultar las 72 fuentes para elaborar el plan. Todas las preguntas requieren validar los insumos indicados, incluso cuando una muestra ya existe. Las fuentes adicionales son dependencias propuestas; no se presupone un cruce válido.', '',
            '| Fuente | Skills adicionales a BASE/INGEST | Ejecución | Validación adicional a H0 | Acceso probado |', '| --- | --- | --- | --- | --- |']
    for case in plan['cases']:
        out.append(f'| [{case["id"]}](#{case["id"]}) | {", ".join(s for s in case["skills"] if s not in ("BASE", "INGEST")) or "BASE/INGEST"} | [{case["execution_harness"]}](#execution-{case["execution_harness"].lower()}) | {", ".join(h for h in case["harnesses"] if h != "H0")} | `{case["latest_source_test_status"]}` |')
    for category, cases in groups.items():
        out += ['', f'## {category}', '']
        for case in cases:
            out += [f'### {case["id"]}', '', f'**{case["name"]}**. Unidad: {case["grain"]}.', '',
                    f'**Skills:** {refs(case["skills"], "skill")} · **Herramientas/MCP:** {refs(case["tools"], "tool")}.', '',
                    f'**Arnés de ejecución:** [{case["execution_harness"]}](#execution-{case["execution_harness"].lower()}) · **Perfiles de validación:** {refs(case["harnesses"], "harness")}.', '',
                    f'**Acceso registrado:** `{case["latest_source_test_status"]}`. [Test y ejemplos](../../{case["source_test_link"]}). {case["access_gate"]}', '',
                    '**Preguntas:**', '']
            for index, question in enumerate(case['questions'], 1):
                out.append(f'{index}. {question["text"]} (`{question["id"]}`)')
            out += ['', f'**Insumos pendientes o que deben fijarse:** {case["needed_inputs"]}', '']
            if case['additional_source_ids']:
                out += ['**Cruces/contrastes propuestos:** ' + ', '.join(f'[{i}](#{i})' for i in case['additional_source_ids']) + '.', '']
            out += ['**Controles específicos:**', ''] + ['- ' + check for check in case['specific_checks']]
            out += ['', f'**Primer resultado revisable:** {case["first_output"]}', '']
    out += ['## Validación estructural de esta propuesta', '',
            '| Comprobación | Resultado |', '| --- | --- |',
            f'| Cobertura exacta del catálogo, sin IDs repetidos | PASS — {receipt["sources"]} fuentes |',
            f'| Tres preguntas como mínimo por fuente; IDs/textos únicos | PASS — {receipt["questions"]} preguntas |',
            '| Referencias a skills, herramientas y perfiles existentes en el plan | PASS |',
            '| Dependencias de otras fuentes pertenecen al catálogo | PASS |',
            '| Todas las fichas conservan estado propuesto o parcial, insumos, controles y salida | PASS |', '',
            'Esta comprobación valida el diseño y sus referencias. El piloto retail registra por separado sus pruebas de método; no certifica disponibilidad futura ni instala MCP.', '',
            'Reproducir desde la raíz, sin acceso a red:', '', '```bash',
            'python scripts/render_exploration_plan.py --check',
            'python scripts/render_exploration_plan.py', '```', '',
            '[Recibo JSON de validación](validation.json) · [Plan estructurado](../../catalogs/exploration_plan.json)', '',
            '## Documentación primaria consultada', '',
            'Las recomendaciones de método y las preguntas son propuestas de este proyecto. Las capacidades técnicas indicadas se contrastaron con documentación del productor; esto no sustituye una prueba local de compatibilidad.', '']
    for reference in plan['references']:
        out.append(f'- [{reference["id"]}]({reference["url"]}): {reference["purpose"]}')
    return '\n'.join(out) + '\n'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Validate only; do not rewrite files')
    args = parser.parse_args()
    plan = json.loads(PLAN.read_text())
    receipt = validate(plan, json.loads((ROOT / 'catalogs/datasets_reales_mexico.json').read_text()))
    receipt['plan_sha256'] = hashlib.sha256(PLAN.read_bytes()).hexdigest()
    receipt['validator_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    if not args.check:
        README.parent.mkdir(parents=True, exist_ok=True)
        README.write_text(render(plan, receipt))
        (README.parent / 'validation.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(receipt, ensure_ascii=False))

if __name__ == '__main__':
    main()
