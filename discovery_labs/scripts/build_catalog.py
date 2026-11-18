#!/usr/bin/env python3
"""Build the reconciled research bank without promoting editorial metadata to evidence."""
from pathlib import Path
import csv,hashlib,json,re,collections

BASE=Path(__file__).resolve().parents[1]
REPO=BASE.parent
DATE='2026-11-16'
ROUTES=['A','B','C','D1','D2','E']
# This reconstructs the archived V2 catalog. V3 adapters apply typed overlays through agent_tools.
# A new manifest must not inherit the old single-table schema, 538 license evidence or question readiness.
LEGACY_SNAPSHOT_CASES={'uci-retail','nba-elo','bob-ross-elementos'}
def read(p):return json.loads(Path(p).read_text())
def write(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def pending(how):return {'status':'PENDIENTE','how_to_obtain':how}
def export_csv(path,rows):
    fields=list(dict.fromkeys(k for row in rows for k in row))
    with Path(path).open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for row in rows:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in row.items()})

NEW={
'bts-kpop-musica':dict(publisher='MetaBrainz / MusicBrainz; anotación comunitaria',grain='Artista MBID, release-group y relaciones; no reproducciones',coverage='Catálogo internacional de BTS',variables=['MBID','nombre','release-group','first-release-date','relaciones'],formats=['JSON'],reference_period='Catálogo observado al corte; fechas por edición',access='API pública con User-Agent identificable; respetar rate limit documentado; no descarga de audio',usage_terms='MusicBrainz distingue datos centrales CC0 y datos suplementarios CC BY-SA; PENDIENTE identificar campos de esta extracción y atribución aplicable.',url='https://musicbrainz.org/artist/0d79fe8e-ba27-4859-bb8c-2f255f346853'),
'kpop-idols':dict(publisher='onlyrohit (Kaggle); paquete SouthKoreAPIs de Renzo Caceres Rossi como derivación',grain='Idol; no trayectoria longitudinal comprobada',coverage='K-pop; cobertura de países dependiente de la selección',variables=['stage name','fecha de nacimiento','grupo','país'],formats=['RDA'],reference_period='PENDIENTE: corte del dataset original de Kaggle',access='Paquete archivado en CRAN; localizar archivo original y licencia antes de ejecutar código',usage_terms='PENDIENTE licencia del dataset Kaggle; la licencia del paquete no garantiza derechos de los datos.',url='https://www.kaggle.com/datasets/onlyrohit/all-kpop-idols'),
'peliculas-taquilla':dict(publisher='The Movie Database / contribuyentes',grain='Película y versión de metadatos',coverage='Catálogo internacional, cobertura no censal',variables=['id','budget','revenue','release_date','genres','original_language'],formats=['JSON'],reference_period='Según película y captura',access='API con clave; no solicitar credenciales al alumno. Preparar muestra sólo con autorización de uso correspondiente.',usage_terms='TMDB exige atribución; uso comercial requiere licencia comercial. PENDIENTE autorización para curso de pago. Budget y revenue no equivalen a margen.',url='https://developer.themoviedb.org/docs/faq'),
'mundial-futbol-2026':dict(publisher='FIFA Training Centre (primario); Alamyy/Worldcup26 (derivado)',grain='Partido; otras tablas de eventos deben verificarse por separado',coverage='Copa Mundial 2026',variables=['match_id','home_team','away_team','home_score','away_score','date','group','source_url'],formats=['CSV','PDF'],reference_period='Mundial 2026; fechas efectivas PENDIENTE cotejo con FIFA',access='CSV público derivado; cotejar muestra contra reportes FIFA y revisar derechos de redistribución',usage_terms='PENDIENTE derechos FIFA y licencia de la extracción; repositorio público no equivale a permiso.',url='https://github.com/Alamyy/Worldcup26'),
'cop31-2026':dict(publisher='UNFCCC',grain='Documento y versión, párrafo o compromiso codificado',coverage='Conferencia internacional',variables=['document_id','versión','fecha','tipo documental','texto','compromiso','monto','plazo'],formats=['HTML','PDF'],reference_period='COP31; corte 16 noviembre 2026, conferencia en curso según página oficial',access='Documentos públicos; congelar versiones y distinguir borradores, acuerdos y pagos',usage_terms='PENDIENTE política de reproducción UNFCCC por documento; no redistribuir corpus sin revisarla.',url='https://unfccc.int/cop31'),
'huggingface-modelos-2026':dict(publisher='Hugging Face y autores de repositorios',grain='Repositorio de modelo y snapshot de metadatos',coverage='Hub, no universo de modelos usados en producción',variables=['id','downloads','likes','tags','pipeline_tag','lastModified','cardData.license'],formats=['JSON'],reference_period='Captura 2026; no reconstruye descargas históricas por sí sola',access='API pública paginada; límites por cuenta y ventana. No descargar pesos ni ejecutar código remoto.',usage_terms='PENDIENTE política para metadatos; licencia de cada modelo se revisa aparte y no se infiere de la palabra abierto.',url='https://huggingface.co/docs/hub/api'),
'elecciones-eeuu-2026':dict(publisher='Oficinas electorales estatales (resultados); FEC (financiamiento y compilación posterior)',grain='Candidato-distrito-elección-corte; separar resultados y gasto',coverage='Elecciones federales EE.UU. 2026',variables=['candidate_id','district','votes','status','certification_date','disbursements'],formats=['CSV','PDF','JSON'],reference_period='Elección 3 noviembre 2026; PENDIENTE certificación por estado y publicación FEC',access='La URL federalelections2026.pdf es una propuesta no confirmada. Usar oficinas estatales para votos y FEC para gasto con cortes compatibles.',usage_terms='PENDIENTE términos y derechos de cada archivo estatal; no usar reportes provisionales como certificados.',url='https://www.fec.gov/introduction-campaign-finance/election-results-and-voting-information/'),
'agentes-ia-mcp-2026':dict(publisher='Autores de repositorios GitHub; GitHub como plataforma',grain='Repositorio único y commit; documentación no prueba ejecución',coverage='Consulta topic:mcp; no censo de agentes',variables=['id','full_name','fork','stargazers_count','pushed_at','license','topics'],formats=['JSON','texto','código'],reference_period='Corte 2026; consulta y paginación limitan cobertura',access='Search API pública o token de mínimo permiso; la investigación sólo lee metadatos/código; no ejecutar herramientas ajenas.',usage_terms='Licencia de software por repositorio; PENDIENTE ToS de metadatos y licencias ausentes. Estrellas no validan calidad.',url='https://docs.github.com/en/rest/search/search')
}

REVISIONS={
'D01-A':'¿Qué estaciones acumulan más salidas netas en el mes observado y cuáles justificarían medir demanda no atendida antes de reforzarlas?',
'D01-D1':'¿Más del 80% de viajes registrados comienza de lunes a viernes entre 7–10 o 17–20 horas? Es un proxy de horario laboral, no del motivo del viaje.',
'D02-D1':'¿Gana al menos el 80% de las partidas completas quien hizo la jugada individual de mayor puntuación?',
'D02-D2':'¿Una apertura definida antes del análisis como agresiva se asocia con mayor tasa de victoria, ajustando nivel rival?',
'D03-D1':'¿Carlsen tiene la mayor tasa de puntos dentro de un corpus con época, control y mínimo de partidas comparables? No compara todas las épocas con un solo campeonato.',
'D04-D1':'¿Es mayor la positividad de inspecciones iniciales en verano que en invierno al comparar los mismos boroughs y años?',
'D05-D1':'¿Más de la mitad de planetas con radio medido en la tabla seleccionada tiene radio entre 0.8 y 1.25 radios terrestres? Este rango operativo no prueba habitabilidad.',
'D05-D2':'¿La aparente abundancia de planetas grandes se mantiene tras corregir la completitud de detección con una fuente externa?',
'D09-D1':'¿Coinciden los rankings por victorias y puntos dentro de una misma temporada? Ninguno define por sí solo al mejor piloto.',
'D10-D1':'¿Gana todas las series el equipo con mayor Elo previo al primer partido? Una serie perdida refuta la versión universal en el corpus.',
'D14-D2':'¿Persiste una diferencia en precio anunciado en Condesa al comparar tipo de alojamiento, capacidad y fecha?',
'D15-D2':'¿Todos los establecimientos con grade A carecen de infracciones críticas en la misma inspección? No mezclar estrellas de consumidores con grado sanitario.',
'D20-D1':'¿Supera el 50% la proporción de entradas con referencias políticas según un manual de anotación previo? No representa a toda la población del siglo XVII.',
'D25-D2':'¿La frecuencia de un sismo de mayor magnitud en una ventana de 24 horas supera una línea base temporal comparable? No permite predicción individual ni avisos.',
'D31-A':'¿Qué productos lideran el importe neto firmado de las líneas de la muestra tras incorporar importes negativos registrados? No equivale a rentabilidad.',
'D31-E':'¿Qué productos cambian de puesto al ordenar por importe bruto positivo o por neto firmado, con y sin duplicados exactos?',
'D31-B':'¿Cuánto cambia la fracción de datos sin ID de cliente al contar líneas o facturas? No permite describir perfiles individuales de clientes.',
'D35-D2':'¿Persisten diferencias de destino según origen al comparar variables observadas compatibles? La encuesta no mide esfuerzo individual suficiente para afirmar que basta o no basta.',
'D38-A':'¿Qué metadatos de lanzamiento de BTS están disponibles y qué serie externa de atención haría falta para comparar duración del interés?',
'D42-B':'¿Qué grupos vulnerables aparecen en los documentos oficiales disponibles al 16 de noviembre de 2026? Los borradores no se tratan como documentos finales.',
'D42-C':'¿Qué cambios de lenguaje aparecen entre versiones oficiales disponibles al corte? La comparación con un texto final queda bloqueada mientras no se publique.',
'D43-E':'¿Cambia el ranking de modelos al usar descargas de la misma ventana y actividad de actualización? No etiquetar el campo downloads como acumulado sin verificar su definición.',
'D44-D2':'¿Qué correlación tienen los errores de encuestas entre distritos en una muestra de elecciones comparables con resultados certificados? Una elección aislada no basta.'
}

def technique(s,route,metric):
    text=(metric+' '+s['name']+' '+s['grain']).lower()
    if any(x in text for x in ['ocr','texto','carta','pasaje','documento','diario','obra–edición']):return 'NLP y revisión documental'
    if any(x in text for x in ['red ','modularidad','centralidad','repertorio']):return 'Redes'
    if any(x in text for x in ['silueta','cluster','perfiles','jaccard']):return 'Clustering'
    if any(x in text for x in ['brier','exactitud','macro f1','clasificador','precisión cae']):return 'Evaluación predictiva'
    if any(x in text for x in ['ponderad','encuesta','quintil','decil']):return 'Encuestas ponderadas'
    if any(x in text for x in ['polígono','distancia','geometr','cobertura territorial','ageb']):return 'Análisis geoespacial'
    if any(x in text for x in ['temporal','serie','tendencia','trimestr','fecha']):return 'Series temporales'
    return 'Comparación y auditoría estadística'

METHODS={
'NLP y revisión documental':('Construir una tabla de pasajes con página/offset, separar voz y notas; contar tras anotar una muestra a mano.','Comparar TF-IDF o red de términos contra etiquetas humanas; medir precisión/recall, incluyendo negativos y ambiguos.','Mapa de términos y tabla de pasajes cotejados','Cambiar edición, excluir notas y cotejar OCR con imagen; contar autores/obras independientes además de menciones.'),
'Redes':('Crear tabla de aristas con definición explícita; contar nodos, componentes y grado antes de algoritmos.','Comparar comunidades o centralidad con red permutada y otra definición de arista.','Red filtrada y barras de centralidad','Retirar el nodo dominante, modificar definición de arista y revisar estabilidad; no interpretar copresencia como conversación.'),
'Clustering':('Revisar unidades, escalar sólo con justificación y comparar distancia apropiada con un resumen por grupos simples.','Probar k y semillas fijadas; medir silueta, estabilidad por remuestreo y dependencia de variables.','Heatmap de perfiles y diagnóstico de estabilidad','Retirar ID, fecha y proxy del resultado; alterar distancia, semillas y faltantes; ausencia de grupos estables es resultado válido.'),
'Evaluación predictiva':('Fijar corte temporal y test separado; comparar con línea base sin entrenar con resultados futuros.','Comparar por grupo con Brier, calibración o macro F1 según objetivo; intervalos por unidad independiente.','Calibración o matriz de confusión y tamaños por grupo','Separar sujetos/sitios/fechas; buscar fuga en variables posteriores, duplicados y transformaciones ajustadas con test.'),
'Encuestas ponderadas':('Identificar tablas, llaves, pesos, estratos y UPM; obtener estimación ponderada y tamaños sin ponderar.','Intervalos con diseño de encuesta o réplicas oficiales; armonizar cohortes y definiciones antes de comparar.','Transiciones ponderadas y brechas con incertidumbre','Comparar con/sin pesos y pérdida de cobertura en joins; no usar bootstrap iid donde el diseño exige conglomerados.'),
'Análisis geoespacial':('Validar CRS, llaves y edición; computar conteos y tasas en áreas compatibles antes de hacer el mapa.','Comparar distancias de red/rectas o agregaciones territoriales; contrastar con marco externo.','Mapa de tasas y dispersión con tamaño de población','Cambiar escala territorial, fronteras y denominador; revisar puntos fuera y sesgo de observadores. No exponer domicilios sensibles.'),
'Series temporales':('Fijar periodo común y frecuencia; mostrar huecos y exposición junto a la serie, sin rellenar cero por defecto.','Comparar ventanas, estacionalidad o baseline con validación temporal y bloques contiguos.','Serie con cobertura y comparación de ventanas','Cambiar ventana, revisar revisiones históricas y cortes; retirar último periodo incompleto y probar estabilidad.'),
'Comparación y auditoría estadística':('Construir tabla con numerador, denominador y exclusiones; calcular dos casos a mano y una comparación descriptiva.','Estratificar por exposición y repetir con política alternativa de duplicados/faltantes; usar intervalos sólo si hay diseño defendible.','Barras o dispersión con denominadores y tabla de sensibilidad','Cambiar denominador y política de exclusión; comprobar unidades, fechas, selección y confusores; no atribuir causalidad.')
}

def main():
    inv=read(BASE/'imports/inventory_v2.json');orig={x['id']:x for x in read(REPO/'catalogs/datasets_reales_mexico.json')['datasets']}
    reconciliation=read(BASE/'catalog/reconciliation.json')
    assert set(orig)==set(reconciliation['original_ids']), 'El catálogo original cambió: reconciliar antes de regenerar.'
    previous={x['id']:x for x in read(REPO/'source_tests/results.json')['results']}
    current={x['id']:x for x in read(BASE/'evidence/probes_78_current.json')['results']}
    for x in read(BASE/'evidence/probes_8_current.json'):current[x['id']]=x
    qs={x['ID pregunta']:x['Pregunta a investigar'] for x in read(BASE/'imports/questions_270.json')}
    newq={int(t[0]):t[1:] for line in (BASE/'imports/new_questions.txt').read_text().splitlines() if line.strip() for t in [line.split('|')]}
    metrics={int(t[0]):t[1:] for line in (BASE/'imports/metric_contracts.txt').read_text().splitlines() if line.strip() for t in [line.split('|')]}
    sources=[];questions=[]
    for row in inv:
        n=row['N'];sid=row['ID canónico'];old=orig.get(sid);o=old or NEW[sid]
        checks=current.get(sid,{});fmt=o.get('formats',[])
        resource_type=('documento' if fmt and set(fmt)<={'PDF','HTML','texto','TXT'} else 'API' if 'JSON' in fmt else 'dataset descargable')
        if sid in ['gutenberg-quijote','pepys-diarios','napoleonica-cartas','dracor-teatro','wellcome-medicina-antigua']:resource_type='corpus'
        if sid in ['unam-colecciones','loc-prensa-historica','loc-mapas-historicos','gallica-napoleon','anuies-anuario','unam-agenda-estadistica','shcp-cuenta-publica']:resource_type='portal'
        if not old:resource_type='tema con fuente candidata' if sid in ['kpop-idols','peliculas-taquilla','elecciones-eeuu-2026'] else 'API' if sid in ['bts-kpop-musica','huggingface-modelos-2026','agentes-ia-mcp-2026'] else 'corpus documental' if sid=='cop31-2026' else 'dataset derivado'
        s=dict(id=sid,inventory_number=n,name=row['Fuente / caso'],description=o.get('analysis_ideas',[row['Fuente / caso']])[0],publisher=o['publisher'],macrocategory=row['Macrocategoría principal'],original_category=old['category'] if old else 'Propuesta posterior',origin='initial_selection' if sid in reconciliation['initially_selected_ids'] else 'originally_omitted' if old else 'later_proposal',resource_type=resource_type,primary_url=o.get('url') or o['sources'][0]['url'],direct_url=(old['sources'][0].get('resource_url') if old else None),original_inventory_url=row['URL fuente / recurso'],sources_declared=old.get('sources',[]) if old else [],coverage=o['coverage'],grain=o['grain'],reference_period_declared=o['reference_period'],frequency_declared=o.get('source_frequency','PENDIENTE: verificar productor'),formats_declared=fmt,variables_declared=o['variables'],keys_proposed=o.get('join_keys',['PENDIENTE: validar claves en el archivo concreto']),access=o['access'],usage_terms_declared=o['usage_terms'],caveats=o.get('caveats',[]),repository_paths=o.get('repository',{}).get('paths',[]),historical_probe=previous.get(sid),current_probe=checks,evidence_status=checks.get('status','PENDIENTE'),license=pending('Leer licencia del recurso y derechos por campo/medio; archivar URL y versión. '+o['usage_terms']),authentication=pending('Confirmar en documentación primaria. Acceso declarado: '+o['access']),quotas=pending('Consultar límites vigentes del endpoint; registrar fecha, cabeceras RateLimit y plan de cuenta sin guardar tokens.'),universe_size=pending('Descargar particiones completas autorizadas; contar filas, columnas, archivos y bytes sin confundir muestra ni metadatos con universo.'),start_date_verified=pending('Parsear fecha del fenómeno y registrar min, inválidas y zona horaria del archivo concreto.'),end_date_verified=pending('Parsear fecha del fenómeno; separar captura, publicación y revisión.'),last_updated_verified=pending('Consultar metadato del productor y ETag/Last-Modified; fecha de prueba no es fecha de actualización del fenómeno.'),quality=pending('Ejecutar perfil de nulos, duplicados por llave, rangos, valores extremos y muestreo manual; conservar decisiones y sesgos.'),schema_changes=pending('Comparar dos snapshots autorizados; registrar columnas, tipos, claves y revisiones de valores históricos.'),privacy=pending('Revisar cuasiidentificadores, granularidad territorial y derechos; minimizar y agregar antes de distribuir.'),snapshot=pending('Congelar bytes autorizados, SHA256 completo, consulta, versión, licencia y código de preparación.'),ready_for_class=False,human_45min_rehearsal=pending('Sesión observada de 45 min, con registro de tiempos, incidentes, decisiones y firma del facilitador.'))
        if sid=='bts-kpop-musica':s['entity_disambiguation']='BTS, grupo musical, MBID 0d79fe8e-ba27-4859-bb8c-2f255f346853. No Bureau of Transportation Statistics.'
        if sid=='bts-puntualidad-vuelos':s['entity_disambiguation']='Bureau of Transportation Statistics, U.S. DOT. No grupo musical.'
        data=BASE/'pilots'/sid/'data/manifest.json'
        legacy_snapshot=data.exists() and sid in LEGACY_SNAPSHOT_CASES
        if legacy_snapshot:
            m=read(data);s['snapshot']={'status':'SNAPSHOT_HASHED','manifest_path':str(data.relative_to(BASE)),**m};s['license']={'status':'REVIEWED','name':m['license'],'url':m['license_url'],'evidence':'evidence/538-LICENSE.txt' if sid!='uci-retail' else 'https://archive.ics.uci.edu/dataset/352/online-retail','scope':'Sólo datos del snapshot, sin imágenes, vídeos ni otros medios.'};s['authentication']={'status':'VERIFIED','value':'Sin autenticación para snapshot offline'}
            s['privacy']={'status':'REVIEWED','policy':m['personal_fields']};s['evidence_status']='SNAPSHOT_HASHED'
        sources.append(s)
        assert len(metrics[n])==6
        for i,route in enumerate(ROUTES):
            qid=f'D{n:02d}-{route}';original=qs.get(qid);text=REVISIONS.get(qid) or original or newq[n][i]
            contract=metrics[n][i];metric,denominator=contract.split(' / ',1)
            if qid=='D01-A':metric='salidas menos llegadas';denominator='estación y viajes con origen-destino válidos; no demanda no atendida'
            if qid=='D38-A':metric='completitud de fechas y obras';denominator='release-groups de BTS deduplicados; interés externo aún no observado'
            if qid=='D31-B':metric='fracción sin ID de cliente';denominator='líneas o facturas únicas, calculados por separado'
            if qid=='D85-C':denominator='episodios del anfitrión y 12 motivos seleccionados, no todos los 67 indicadores'
            tech=technique(s,route,metric);simple,advanced,visual,adversarial=METHODS[tech]
            block=[]
            if not legacy_snapshot:block.append('PENDIENTE: snapshot de alcance suficiente, derechos, esquema y QA para esta pregunta.')
            if re.search(r'extern[oa]|no presente|ausente|realmente vendid|riesgo|todos los|marco externo|censura|conciertos reales|costos|salario|rentabil|margen',contract+' '+text,re.I):block.append('PENDIENTE: dato adicional específico que exige el contrato de métrica/denominador; no estimarlo con un proxy sin aprobación.')
            if route=='A' and any(x in (contract+' '+text).lower() for x in ['costo','ingreso','rentab','salario','ahorro','inversión']):block.append('Decisión de negocio condicionada: costos, demanda o impacto causal no medidos no se convierten en ROI.')
            if sid in ['cop31-2026','elecciones-eeuu-2026']:block.append('PENDIENTE: identificar versión final o certificado oficial por unidad; corte provisional debe quedar explícito.')
            if sid=='kpop-idols':block.append('PENDIENTE: archivo original y licencia; el paquete CRAN está archivado. No mide fecha de debut/carrera sólo por fecha de nacimiento.')
            if sid=='peliculas-taquilla':block.append('PENDIENTE: licencia comercial adecuada para curso pagado y acceso autorizado; recaudación no es utilidad.')
            if route in ['D1','D2']:
                universal=bool(re.search(r'tod[oa]s?|siempre|garant|nunca|necesaria',text,re.I))
                hypothesis=('H: la afirmación expresada en la pregunta se cumple en todas las unidades elegibles del snapshot. Alcance sólo al corpus observado; las condiciones y la métrica se fijan antes de contar.' if universal else f'H0: no hay diferencia ni asociación en {metric} entre los grupos definidos en la pregunta, usando {denominator}. H1: existe diferencia o asociación; fijar dirección antes del análisis.')
                refute=('Una unidad válida que contradiga la afirmación, cotejada manualmente en su registro original, refuta su versión universal dentro del corpus. Cero excepciones no prueba universalidad fuera del corpus.' if universal else f'Calcular magnitud y, si hay muestreo defendible, intervalo del contraste de {metric}; un intervalo que excluye el nulo refuta H0. Revisar multiplicidad si se abren más contrastes; falta de potencia es inconclusa.')
            elif route=='E':
                hypothesis=f'H: la conclusión cualitativa y el ranking de {metric} permanecen estables al aplicar la alternativa de medición de la pregunta.'
                refute='Refutar estabilidad si cambia la dirección del contraste o cambia el primer puesto entre las definiciones documentadas. Reportar también magnitud, Spearman y Jaccard top-k si corresponde; no ocultar empates.'
            elif route=='C':
                hypothesis=f'H: el patrón medido mediante {metric} tiene estructura más estable que una línea base simple que conserva la distribución marginal y el tamaño de {denominator}.'
                refute='Comparar con baseline permutado respetando bloques o relaciones permitidas y con cambios de representación. Si la señal no mejora la base o desaparece, declarar patrón no sustentado; no convertir exploración en confirmación.'
            else:
                hypothesis=f'H0: no existen diferencias en {metric} entre las unidades o segmentos comparables expresados en la pregunta, con denominador {denominator}.'
                refute='Fijar grupos, periodo y contraste antes de mirar resultados; medir diferencia y tabla por segmento. Rechazar H0 sólo con incertidumbre apropiada al diseño y revisión de confusores; la evidencia descriptiva no estima causalidad.'
            questions.append(dict(id=qid,canonical_id=sid+'.'+route,source_id=sid,route=route,perspective={'A':'Negocio / monetaria','B':'Social','C':'Exploración y descubrimiento','D1':'Creencia candidata 1','D2':'Creencia candidata 2','E':'Detective de datos'}[route],question=text,original_question=original,revision_reason='Operacionalización, alcance y límites de inferencia; no presupone respuesta.' if original else 'Nueva pregunta para fuente omitida; propuesta sometida a verificación.',hypothesis=hypothesis,objective={'A':'Orientar una decisión de priorización o una medición económica posterior; separar proxy y rentabilidad.','B':'Describir una brecha de cobertura o resultado con exposición comparable, sin atribuir rasgos individuales.','C':'Buscar estructura que sobreviva una explicación simple y perturbaciones del dato.','D1':'Contrastar una primera afirmación falsable con definiciones fijadas antes de ejecutar.','D2':'Contrastar otra afirmación sobre una variable o mecanismo distinto de D1.','E':'Detectar una conclusión que depende de una medición, denominador o dato futuro.'}[route],unit=s['grain'],population_scope='Sólo registros elegibles del corte verificado; no generalizar automáticamente al universo declarado: '+s['coverage'],metric=metric,denominator=denominator,period='Fijar ventana común antes de ejecución. Periodo declarado: '+s['reference_period_declared'],required_fields=s['variables_declared'],required_additional_data=contract if block else 'No adicional para el contraste descriptivo; revisar alcance del snapshot.',primary_source=s['primary_url'],technique=tech,difficulty='Inicial guiado' if tech=='Comparación y auditoría estadística' else 'Intermedio con copiloto',route_simple=simple,route_advanced=advanced,visualizations=visual,adversarial_test=adversarial,refutation_criterion=refute,possible_outcomes=['Evidencia compatible dentro del alcance medido','Contraejemplo o contraste que debilita/refuta la hipótesis','Inconcluso: faltan datos, potencia, cobertura, permiso o definición'],limitations=s['caveats']+['Distinguir muestra, marco de muestreo y universo; asociación no prueba causalidad.','No elegir retrospectivamente umbrales para fabricar descubrimientos.'],blockers=block,status='DESIGNED_UNTESTED',execution_evidence=None,belief_popularity_evidence=pending('Localizar encuesta, divulgación o cita que documente la popularidad; se presenta como afirmación candidata, no como consenso.') if route in ['D1','D2'] else None,estimated_minutes={'value':45,'status':'DISEÑO; no duración observada'}))
    assert len(sources)==86 and len({s['id'] for s in sources})==86
    assert len(questions)==516 and len({q['canonical_id'] for q in questions})==516
    assert sum(q['original_question'] is not None for q in questions)==270
    write(BASE/'catalog/sources.json',sources);write(BASE/'catalog/questions.json',questions)
    export_csv(BASE/'catalog/sources.csv',sources);export_csv(BASE/'catalog/questions.csv',questions)
    print(json.dumps({'sources':len(sources),'questions':len(questions),'revised':270,'new':246,'categories':dict(collections.Counter(s['macrocategory'] for s in sources))},ensure_ascii=False))

if __name__=='__main__':main()
