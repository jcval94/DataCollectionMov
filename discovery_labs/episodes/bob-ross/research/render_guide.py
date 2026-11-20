#!/usr/bin/env python3
"""Generate one scientific guide from canonical questions and measured artifacts."""
import csv
import hashlib
import html
import json
from pathlib import Path
from audit import audit, HERE, ROOT

def esc(s): return html.escape(str(s))
def read(p): return json.loads(p.read_text())

def figures(o1,o2):
    folder=HERE/'figures';folder.mkdir(exist_ok=True)
    head='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 400" role="img" aria-labelledby="t d"><rect width="900" height="400" fill="#fffdf8"/>'
    seq=[head,'<title id="t">Adyacencias frente al nulo condicionado</title><desc id="d">403 episodios y 372 transiciones. Banda gris: nulo 95 por ciento. Azul: esperanza exacta. Rojo: observado.</desc>',
         '<text x="35" y="38" font-family="sans-serif" font-size="21">¿Cero repeticiones es una sorpresa?</text>']
    sx=lambda x:210+float(x)*35
    for i,r in enumerate(o1['BR-14']['results'][:4]):
        y=105+i*65;lo,hi=r['null_interval_95'];obs=r['observed_11'];ex=r['expected_11_exact']
        seq.extend([f'<text x="35" y="{y+5}" font-family="sans-serif" font-size="16">{r["motif"]}</text>',
                    f'<line x1="{sx(lo)}" x2="{sx(hi)}" y1="{y}" y2="{y}" stroke="#b7c6c2" stroke-width="12"/>',
                    f'<circle cx="{sx(ex)}" cy="{y}" r="7" fill="#225d69"/>',
                    f'<path d="M{sx(obs)},{y-9} l9,9 l-9,9 l-9,-9 z" fill="#a7482f"/>',
                    f'<text x="745" y="{y+5}" font-family="sans-serif" font-size="14">{obs} / {ex:.2f} esper.</text>'])
    for x in range(0,19,3):
        seq.append(f'<text x="{sx(x)-5}" y="355" font-family="sans-serif" font-size="13">{x}</text>')
    seq.append('<text x="35" y="385" font-family="sans-serif" font-size="13">Pares 1→1 · gris: nulo 95% · azul: esperado · rojo: observado · no es IC de efecto</text></svg>')
    (folder/'sequence_null.svg').write_text('\n'.join(seq))
    cl=[head,'<title id="t">Silhouette con y sin tres filas vacías</title><desc id="d">Misma distancia Jaccard. 381 frente a 378 episodios. El máximo del grid cambia de k=2 a k=3; no valida estilos.</desc>',
        '<text x="35" y="38" font-family="sans-serif" font-size="21">Tres filas vacías cambian el máximo del grid</text>']
    for tick in [0,.1,.2,.3,.4]:
        y=320-tick*600
        cl.append(f'<line x1="90" x2="830" y1="{y}" y2="{y}" stroke="#e1e5df"/><text x="40" y="{y+5}" font-family="sans-serif" font-size="13">{tick:.1f}</text>')
    for g,color,dx in [(o1['BR-09']['k_grid'],'#225d69',-18),(o2['complete_case_grid'],'#a7482f',18)]:
        for i,r in enumerate(g):
            x=150+i*155+dx;v=r['silhouette_same_jaccard_space'];h=v*600
            cl.append(f'<rect x="{x-14}" y="{320-h}" width="28" height="{h}" fill="{color}"/><text x="{x-15}" y="{310-h}" font-family="sans-serif" font-size="11">{v:.3f}</text>')
    for i in range(5):cl.append(f'<text x="{140+i*155}" y="347" font-family="sans-serif" font-size="14">k={i+2}</text>')
    cl.append('<text x="95" y="385" font-family="sans-serif" font-size="14" fill="#225d69">Azul: 381 · incluye tres filas vacías</text><text x="520" y="385" font-family="sans-serif" font-size="14" fill="#a7482f">Rojo: 378 · sin esas filas</text></svg>')
    (folder/'cluster_sensitivity.svg').write_text('\n'.join(cl))

def main():
    o1=read(HERE/'results/o1_results.json');o2=read(HERE/'progressive_results/br09_o2.json')
    bank=read(ROOT/'entry_pack/questions_master.json')['questions']
    registry=read(HERE/'execution_registry.json');data,rows=audit()
    figures(o1,o2)
    seq=o1['BR-14']['results'][:4];cw=o1['BR-07']['cabin_winter'];cl=o1['BR-09']
    all_pairs=list(csv.DictReader((HERE/'results/associations.csv').open()))
    result={}
    tr=''.join(f'<tr><th>{r["motif"]}</th><td>{r["observed_11"]}</td><td>{r["expected_11_exact"]:.2f}</td><td>{r["p_inhibition_holm"]:.3f}</td></tr>' for r in seq)
    result['BR-14']=f'''<h3>O1 medida · inhibición no demostrada</h3>
<p>403 episodios y 372 transiciones dentro de 31 temporadas. Ninguna de las cuatro pruebas cumple el criterio de H8 tras Holm. OCEAN tiene cero repeticiones, pero el nulo espera solo 1.38: cero no basta para inferir alternancia deliberada.</p>
<img src="research/figures/sequence_null.svg" alt="Adyacencias, esperanza y banda nula 95 por ciento de cuatro motivos" width="900" height="400">
<div class="scroll"><table><caption>10,000 permutaciones por temporada; prueba unilateral</caption><tr><th>Motivo</th><th>Observadas</th><th>Esperadas</th><th>p Holm</th></tr>{tr}</table></div>
<p>Sensibilidades sin invitados y sin tres filas vacías: 330 y 324 transiciones, sin puentear huecos. Tampoco apoyan inhibición corregida. No demostrar efecto no prueba equivalencia ni ausencia de intención.</p>
<p><strong>Cómo:</strong> tablas Markov y permutación de vectores completos con totales por temporada fijos. <strong>Por qué:</strong> controlar rareza y diferencias entre temporadas. <strong>Para qué:</strong> evitar confundir ausencia llamativa con programación. Modelo descriptivo; no se evaluó predicción futura.</p>'''
    pairrows=''.join(f'<tr><td>{esc(r["motif_a"])} / {esc(r["motif_b"])}</td><td>{r["n11"]}/{r["n"]}</td><td>{float(r["lift"]):.3f}</td><td>{float(r["q_bh_66"]):.3g}</td><td>{esc(r["shared_input_columns"]) or "—"}</td></tr>' for r in all_pairs)
    result['BR-07']=f'''<h3>O1 parcial medida · cabañas e invierno</h3>
<p>En 381 episodios GUEST=0, CABIN y WINTER coinciden en <strong>28</strong>, frente a {cw['expected_n11']:.2f} bajo independencia: lift <strong>{cw['lift']:.2f}</strong>, OR {cw['odds_ratio']:.2f}. IC percentil de lift remuestreando temporadas: {cw['lift_season_bootstrap_interval_95'][0]:.2f}–{cw['lift_season_bootstrap_interval_95'][1]:.2f}.</p>
<div class="scroll"><table><caption>Episodios observados, n=381</caption><tr><th></th><th>WINTER=1</th><th>WINTER=0</th></tr><tr><th>CABIN=1</th><td>28</td><td>40</td></tr><tr><th>CABIN=0</th><td>39</td><td>274</td></tr></table></div>
<p>Permutar WINTER dentro de temporada da p≈0.0001, resolución mínima de 10,000 réplicas. Excluir las tres filas vacías conserva lift {cw['complete_case_sensitivity']['lift']:.2f}. Pareja motivada por H9; resultado exploratorio, sin probar simbolismo, habitantes o efecto climático.</p>
<p><strong>Cómo:</strong> independencia/lift, Fisher y contraste condicionado por temporada. <strong>Por qué:</strong> separar prevalencia y afinidad. <strong>Para qué:</strong> investigar composición sin inventar mecanismos. Las 66 asociaciones se publican completas; montaña–nieve comparte SNOWY_MOUNTAIN y no se interpreta como descubrimiento independiente. H3 sobre tiempo y los tríos siguen sin ejecutar.</p>
<details><summary>Inspeccionar los 66 pares y su FDR exploratoria</summary><p>Fisher bilateral y BH sobre 66 pares. Dependencias del diccionario limitan alcance confirmatorio.</p><div class="scroll"><table><tr><th>Par</th><th>Coincidencias</th><th>Lift</th><th>q BH</th><th>Columna compartida</th></tr>{pairrows}</table></div></details>'''
    changes=o2['aligned_changes_k4']
    result['BR-09']=f'''<h3>O1 parcial medida · un grupo de datos vacíos</h3>
<p>k=4 Jaccard produce tamaños <strong>236, 106, 36 y 3</strong>. El último grupo contiene S09E10, S15E04 y S26E10: ninguna etiqueta positiva. Reaparece para cada k=2…6. Es una propiedad de esta codificación y algoritmo; no identifica un estilo artístico.</p>
<p>ARI Jaccard–Euclídea <strong>{cl['ari_jaccard_euclidean_k4']:.3f}</strong>; IC bootstrap por temporadas {cl['conditional_ari_bootstrap_interval_95'][0]:.3f}–{cl['conditional_ari_bootstrap_interval_95'][1]:.3f}, condicionado a particiones fijas. No mide estabilidad tras reajustar.</p>
<section class="progressive" aria-labelledby="br09-o2-title"><h3 id="br09-o2-title">Sensibilidad calculada antes del protocolo HF · pendiente de revisión humana</h3>
<p>Padre histórico: BR-09-O1. Cálculos ejecutados antes del merge de HF; decisión actual HF-02 PENDING. Evidencia anterior y <a href="research/DR-05a.md">DR-05a</a>; trigger: cuatro grupos aparentes y desacuerdo observado entre métricas.</p>
<p>Con matching exacto de nombres de grupo, Euclídea cambia <strong>{changes['euclidean']['changed_n']}/381</strong> asignaciones; retirar árbol cambia <strong>{changes['without_tree']['changed_n']}/381</strong>. Pasar de 12 familias a 64 etiquetas sin autoría da ARI {o2['representation_sensitivity']['ari_12_families_vs_64_non_author_labels']:.3f}.</p>
<img src="research/figures/cluster_sensitivity.svg" alt="Al excluir tres filas vacías, el máximo de silhouette del grid cambia de k igual a dos a k igual a tres" width="900" height="400">
<p>El máximo del grid cambia de k=2 (378+3) a k=3 (236+106+36) al excluir vacíos. En cambio, los <strong>31 reajustes dejando fuera una temporada</strong> reproducen la partición de 381 (ARI=1). Los grupos resisten esa perturbación temporal, pero dependen de matriz y distancia.</p>
<p><strong>Cómo:</strong> matching, grid con/sin vacíos y 31 reajustes. <strong>Por qué:</strong> distinguir medición y variación entre temporadas. <strong>Para qué:</strong> auditar representación antes de validar categorías artísticas. Heurística determinista, sin garantía de óptimo global.</p></section>
<p>O3 sigue condicional: faltan obras autorizadas y evaluadores humanos. H6 híbrida, KMeans/Bernoulli y validación artística no se ejecutaron.</p>'''
    cards=[]
    for q in bank:
        ident=q['id'];execution=registry['executions'].get(ident)
        state=execution['o1_status'] if execution else 'PLAN_ONLY / '+q['status']
        evidence='<div class="result">'+result[ident]+'</div>' if ident in result else ''
        cards.append(f'''<details class="story-arc" id="{ident.lower()}" {'open' if execution else ''}>
<summary><span>{ident} · {esc(state)}</span><br>{esc(q['title'])}</summary>
<p><strong>O1:</strong> {esc(q['o1'])}</p><p><strong>Denominador:</strong> {esc(q['estimand']['denominator'])}</p>
<p><strong>Modelo del diseño:</strong> {esc(q['model'])} · {esc(q['model_name'])}. {esc(q['model_why'])}</p>
<p><strong>Contraste del diseño:</strong> {esc(q['stat'])}</p><p><strong>Rival:</strong> {esc(q['rival_hypothesis'])}</p>
<p><strong>Datos y puertas:</strong> {esc(q['data'])}</p>{evidence}
<p><a href="entry_pack/questions_master.json">Ficha canónica y planes internos</a> · <a href="research/PROTOCOL.md">Protocolo ejecutado: alcance y diferencias frente al diseño</a></p></details>''')
    assigns={r['episode']:r for r in csv.DictReader((HERE/'results/cluster_assignments.csv').open())}
    points=[]
    for r in rows:
        if not r['guest']:
            a=assigns[r['id']];points.append({'id':r['id'],'title':r['title'],'season':r['season'],
                'motifs':[k for k,v in r['motifs'].items() if v], 'raw_positive_marks':sum(r['flags'].values()),
                'jaccard':int(a['jaccard_k4'])+1,'euclidean':int(a['euclidean_k4'])+1,'without_tree':int(a['without_tree_k4'])+1})
    payload=json.dumps(points,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    options=''.join(f'<option value="{r["id"]}">{r["id"]} · {esc(r["title"])}</option>' for r in points)
    css='''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f8f5ee;color:#152e34;font:17px/1.65 system-ui,sans-serif}main,header,footer{max-width:1100px;margin:auto;padding:28px 24px}header{padding-bottom:0}h1,h2{font-family:Georgia,serif;line-height:1.15}h1{font-size:clamp(2.3rem,6vw,4.4rem)}h2{font-size:2rem;margin-top:0}h3{line-height:1.35}a{color:#17576a}nav{display:flex;flex-wrap:wrap;gap:14px;border-block:1px solid #c3cec8;padding:16px 0}section{margin:34px 0}summary{cursor:pointer;font-weight:700}summary span{font:12px system-ui;color:#4a6268}details{border:1px solid #becdc6;border-radius:9px;padding:20px;margin:18px 0;background:#fffdf8}details details{background:#f3f5ef}.result{border-left:4px solid #226070;padding-left:18px;margin:20px 0}.progressive{border-top:2px solid #b4c5bf;padding-top:15px}.status{background:#e9e1cf;padding:14px;border-left:4px solid #9a502f}img{max-width:100%;height:auto}table{border-collapse:collapse;width:100%;font-size:15px}caption{text-align:left;padding:12px 0;font-weight:600}th,td{border-bottom:1px solid #c7d3cd;padding:10px;text-align:left;vertical-align:top}.scroll{overflow-x:auto}button,input,select{font:inherit;padding:10px;border:1px solid #557477;border-radius:4px;max-width:100%;width:100%}label{display:block;margin:12px 0}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#153039;color:#eef5ef;padding:20px;font-size:14px}code{overflow-wrap:anywhere}p{max-width:85ch}.intro{font-size:19px}.meta{font-size:13px;color:#4f6367}.skip{position:absolute;left:-999px}.skip:focus{left:10px;top:10px;background:white}:focus-visible{outline:3px solid #a34b2d;outline-offset:3px}#episode-detail{border:1px solid #a8bdb5;border-radius:8px;padding:20px;background:white;min-height:180px}@media(max-width:580px){main,header,footer{padding:20px 15px}body{font-size:16px}.result{padding-left:10px}details{padding:14px}.scroll table{min-width:520px}h2{font-size:1.7rem}}@media print{body{background:white}nav,.skip,input,select{display:none}details{break-inside:avoid}pre{background:#eee;color:black}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}'''
    page=f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Bob Ross · Guía científica V4 · AI Discovery Labs</title><meta name="description" content="Auditoría, secuencias, asociaciones y sensibilidad del agrupamiento: investigación reproducible de Bob Ross."><style>{css}</style></head>
<body><a class="skip" href="#contenido">Saltar al contenido</a><header><p class="meta">AI DISCOVERY LABS · AUGMENTED D. LAB · 19 NOV 2026 · V4</p></header>
<main id="contenido"><p class="intro">Entre 1983 y 1994, <em>The Joy of Painting</em> convirtió la pintura de paisajes en una experiencia televisiva accesible. Walt Hickey/FiveThirtyEight codificó motivos de 403 episodios; ese archivo registra etiquetas, no fotografías, fechas de grabación ni información clínica. Aquí investigamos qué patrones y excepciones podemos defender, cómo dependen de nuestras decisiones de análisis y qué fuentes harían falta para ir más allá.</p>
<h1>¿Qué nos cuentan las etiquetas de Bob Ross?</h1><section id="resumen"><h2>Resumen ejecutivo</h2><p>La auditoría confirma 3,221 marcas positivas y corrige supuestos sobre columnas, títulos duplicados y filas vacías. Tres investigaciones ya tienen cálculos reproducibles: las pruebas secuenciales no respaldan inhibición tras corregir comparaciones; cabañas e invierno se asocian; y tres episodios sin etiquetas forman un grupo aparente en todos los k probados. La sensibilidad cambia al modificar distancia y representación, aunque los 31 reajustes que omiten una temporada mantienen la partición. Son resultados del snapshot y del método, sin validar estilos artísticos ni causas históricas. Desde el paquete de entrada avanzamos a evidencia y nulos medidos. Recomiendo revisar primero el artefacto de datos vacíos y resolver permisos antes de ampliar color o imágenes. El PR #17 incorporó checkpoints humanos durante esta sesión: los cálculos previos se conservan, HF-02 sigue pendiente y ninguna aprobación se infiere. Falta QA visual de navegador, móvil y teclado.</p></section><p class="status">FASE 1 · PENDIENTE DE APROBACIÓN. O1 exploratorias ejecutadas y sensibilidad pendiente de HF-02. Storyboard, guion audiovisual y video BLOQUEADOS.</p>
<nav aria-label="Índice"><a href="#objetivo">Objetivo</a><a href="#datos">Datos</a><a href="#preguntas">Investigaciones</a><a href="#inspector">Inspector</a><a href="#limites">Límites</a><a href="#reproducir">Reproducir</a></nav>
<section id="objetivo"><h2>Objetivo y utilidad</h2><p><strong>Cómo:</strong> auditar CSV, fijar nulos, ejecutar offline y guardar resultados, incertidumbre y sensibilidad. <strong>Por qué:</strong> patrones llamativos pueden depender de filas vacías, prevalencias o distancias. <strong>Para qué:</strong> distinguir resultados reproducibles de interpretaciones injustificadas y convertirlos en un laboratorio de unos 45 minutos.</p></section>
<section id="datos"><h2>Los datos y su frontera</h2><p>Snapshot original: <strong>403 × 69; 67 indicadores</strong>, 66,315 bytes y <strong>3,221 marcas positivas</strong>. 381 episodios GUEST=0 y 22 GUEST=1; no sustituyen créditos independientes. SHA-256: <code>{data['sha256']}</code>.</p>
<ul><li>PERSON existe: S03E10. CHIMNEY no existe.</li><li>Dos títulos repetidos: MOUNTAIN WATERFALL y LAKESIDE CABIN. La llave es EPISODE.</li><li>Tres filas de 67 ceros: S09E10, S15E04, S26E10. Se conservan; al excluirlas como la viñeta R se pasa de 381 a 378.</li><li>Subtipos no siempre activan su etiqueta superior. No se corrigieron valores sin evidencia visual.</li><li>12 familias mediante OR, definidas en run.py; montaña y nieve comparten SNOWY_MOUNTAIN.</li></ul>
<p>La publicación de Graten et al. presenta 3,324 en su resumen y 3,224 en su sección de datos. El CSV fijado suma 3,221; la causa histórica sigue sin resolverse. <a href="research/SOURCE_REVIEW.md">Fuentes y contradicciones</a> · <a href="research/evidence/data_audit.json">Auditoría completa</a>.</p>
<p>Etiquetas: CC BY 4.0, atribución a Walt Hickey/FiveThirtyEight; publicamos transformaciones y resultados propios. Sin permisos transferidos sobre obras, videos o transcripciones. Paletas externas: cobertura técnica 403/403, modelado bloqueado por permisos pendientes.</p></section>
<section id="preguntas"><h2>Un banco · 14 investigaciones</h2><p>Las fichas conservan su diseño canónico. O1 medidas de BR-07, BR-09 y BR-14 con límites explícitos; BR-10 bloqueada. BR-09 conserva cálculos de sensibilidad realizados antes de integrarse el protocolo HF. Su promoción editorial está retenida hasta HF-02; ninguna decisión humana se infiere.</p>{''.join(cards)}</section>
<section id="inspector"><h2>Inspeccionar episodios y grupos</h2><p>381 episodios GUEST=0. Los números de grupo son locales a cada método: compararlos literalmente induce cambios falsos. Las cifras 179 y 75 usan matching exacto; este inspector muestra etiquetas originales sin alinear.</p><label for="episode">Episodio<select id="episode">{options}</select></label>
<div id="episode-detail" role="status" aria-live="polite"><strong>S01E01</strong><p>Huella de atributos, no reproducción de pintura. Usa el selector para inspeccionar el resto.</p></div>
<noscript><p>El inspector requiere JavaScript; <a href="research/results/cluster_assignments.csv">descarga las 381 asignaciones</a>. Las preguntas y resultados anteriores siguen siendo legibles.</p></noscript></section>
<section id="limites"><h2>Interpretación adversarial</h2><p>Tres filas sin etiquetas producen un grupo aparente y cambian el máximo del grid de k. Cambiar distancia altera muchas asignaciones; retirar una temporada no las altera en las 31 pruebas. Evidencia de sensibilidad a representación, no taxonomía artística.</p>
<p>La secuencia no respalda inhibición corregida. Cabañas e invierno se asocian, pero composición, selección didáctica y anotación siguen como rivales. No se midieron habitantes implícitos, efectos del linfoma, duelo, gustos ni rentabilidad.</p>
<p>Diagnóstico disputado y fechas de grabación no recuperadas. Ball State PBS corrobora traslado de estudio en 1988 sin episodio preciso. NPR/KPBS recoge testimonio de tres versiones, sin localizar tres obras por cada fila.</p>
<p><a href="research/DR-05a.md">DR-05a y activación</a> · <a href="research/evidence/source_claim_matrix.csv">54 registros con estado independiente</a>. DR-04 y DR-05b diferidos. O3 exige evidencia nueva; BR-09 necesita imágenes autorizadas y evaluadores.</p></section>
<section id="reproducir"><h2>Reproducibilidad y siguiente decisión</h2><pre>cd discovery_labs/episodes/bob-ross
python research/audit.py
python research/reconcile.py
python research/experiments.py
python research/progressive.py
python research/render_guide.py
python -m unittest discover -s tests -v
python entry_pack/validate_pack.py</pre>
<p>Python ≥3.11, biblioteca estándar y sin red para repetir. Semilla 20261119; 10,000 permutaciones y 2,000 bootstrap. Bandas nulas no son IC de efecto. Remuestrear 31 temporadas no las convierte en muestra aleatoria de toda su obra.</p>
<p><a href="research/results/o1_results.json">O1</a> · <a href="research/progressive_results/br09_o2.json">O2</a> · <a href="research/evidence/reconciliation.csv">Conciliación</a> · <a href="research/evidence/ranking.json">Ranking</a> · <a href="research/README.md">Informe</a> · <a href="research/QA.md">QA ejecutado</a>.</p>
<p class="meta">V3 era estática con rutas superiores expuestas. V4 ofrece resultados trazables y cálculos de sensibilidad pendientes de HF-02. Historial anterior en Git. Aprobación humana del commit PENDIENTE; audiovisual BLOQUEADO.</p></section></main>
<footer>Walt Hickey / FiveThirtyEight · Datos CC BY 4.0 · AI Discovery Labs · REM[AI]N HUMAN</footer>
<script type="application/json" id="research-data">{payload}</script>
<script>
const data=JSON.parse(document.getElementById('research-data').textContent);
const choose=document.getElementById('episode'),detail=document.getElementById('episode-detail');
function inspect(){{const r=data.find(x=>x.id===choose.value);const title=document.createElement('strong');title.textContent=r.id+' · '+r.title;const p=document.createElement('p');p.textContent='Temporada '+r.season+' · '+(r.motifs.join(', ')||'Sin motivos positivos')+' · '+r.raw_positive_marks+' marcas originales.';const groups=document.createElement('p');groups.textContent='Grupo Jaccard: '+r.jaccard+' · Euclídea: '+r.euclidean+' · Sin árbol: '+r.without_tree+'. Números locales sin alinear.';const note=document.createElement('small');note.textContent='Representación textual del CSV; no es la pintura ni valida estilo artístico.';detail.replaceChildren(title,p,groups,note);}}
choose.addEventListener('change',inspect);inspect();
</script></body></html>'''
    (ROOT/'research_guide.html').write_text(page,encoding='utf-8')
    artifacts=[ROOT/'research_guide.html',*(HERE/'figures').glob('*.svg')]
    (HERE/'guide_build.json').write_text(json.dumps({
        'version':'V4','renderer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'inputs':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'entry_pack/questions_master.json',HERE/'results/o1_results.json',HERE/'progressive_results/br09_o2.json',HERE/'execution_registry.json']},
        'outputs':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in artifacts},
    },indent=2)+'\n')
    print('V4: 14 cards, 3 measured O1, legacy sensitivity pending HF02, no active O3')

if __name__=='__main__':main()

