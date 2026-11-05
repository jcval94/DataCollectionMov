#!/usr/bin/env python3
"""Read-only, bounded public-source smoke tests; never loads credentials.

Stdlib for HTTP/JSON/CSV/HTML; optional pypdf/openpyxl for PDF/XLSX.
Exit 0: report produced. --strict exits 1 if any defined check fails.
This intentionally separates a readable portal from an actual data sample.
"""
from __future__ import annotations
import argparse
import concurrent.futures
import csv
import hashlib
import io
import os
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
UA = 'DataCollectionMov-source-check/1.0 (+https://github.com/jcval94/DataCollectionMov)'
LABELS = {'DATA_SAMPLE':'Registros recuperados', 'CACHED_SAMPLE':'Registros del repo',
          'DOCUMENT_SAMPLE':'Documento recuperado', 'DOC_ONLY':'Sólo portal/documentación',
          'METADATA_SAMPLE':'Sólo catálogo/manifiesto', 'BLOCKED':'Acceso bloqueado',
          'HTTP_ERROR':'Error HTTP', 'NETWORK_ERROR':'Error de red', 'PARSE_ERROR':'Formato/esquema inesperado',
          'LIMIT_REACHED':'Límite de descarga', 'EMPTY':'Respuesta sin registros',
          'DEPENDENCY_MISSING':'Falta lector opcional', 'MEDIA_SAMPLE':'Cabecera de medio verificada',
          'INTERNAL_ERROR':'Error del verificador'}

def now(): return datetime.now(timezone.utc).isoformat(timespec='seconds')
def norm(s): return ''.join(c for c in unicodedata.normalize('NFD',str(s)).lower() if unicodedata.category(c)!='Mn')
def brief(value, n=120):
    if isinstance(value,str): return value if len(value)<=n else value[:n]+'…'
    if isinstance(value,dict): return {k:brief(v,n) for k,v in list(value.items())[:12]}
    if isinstance(value,list): return [brief(v,n) for v in value[:8]]
    return value
def getpath(obj,path):
    for part in path.split('.') if path else []:
        if not isinstance(obj,dict) or part not in obj:return None
        obj=obj[part]
    return obj
def pick(row, fields):
    if not isinstance(row,dict):return brief(row)
    fields=fields or list(row)[:10]
    return {k:brief(getpath(row,k)) for k in fields if getpath(row,k) is not None}

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.skip=0; self.parts=[]; self.links=[]; self.title=[]; self.in_title=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in ('script','style','noscript'):self.skip+=1
        if tag=='title':self.in_title=True
        if tag=='a' and a.get('href'):self.links.append(a['href'])
        if tag in ('p','div','br','h1','h2','h3','li','tr'):self.parts.append('\n')
    def handle_endtag(self,tag):
        if tag in ('script','style','noscript'):self.skip=max(0,self.skip-1)
        if tag=='title':self.in_title=False
    def handle_data(self,data):
        if not self.skip:self.parts.append(data)
        if self.in_title:self.title.append(data)
    def text(self):return re.sub(r'[ \t]+',' ',''.join(self.parts)).strip()

def fetch(url, timeout, limit, prefix=False):
    if urllib.parse.urlsplit(url).scheme not in ('http','https'):raise ValueError('Non-HTTP URL')
    req=urllib.request.Request(url,headers={'User-Agent':UA,'Accept-Encoding':'identity'})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        data=r.read(limit+1)
        truncated=len(data)>limit
        data=data[:limit]
        result=dict(requested_url=url,final_url=r.url,http_status=r.status,
                    content_type=r.headers.get('Content-Type',''),last_modified=r.headers.get('Last-Modified'),
                    bytes_read=len(data),truncated=truncated,sha256=hashlib.sha256(data).hexdigest(),
                    hash_scope='response_prefix' if truncated else 'complete_response')
        if truncated and not prefix:result['limit_exceeded']=True
        return data,result

def decode(data):
    for enc in ('utf-8-sig','cp1252'):
        try:return data.decode(enc)
        except UnicodeDecodeError:pass
    return data.decode('utf-8','replace')

def run_check(spec,args):
    out=dict(checked_at_utc=now(),kind=spec['kind'],scope=spec.get('scope','live_public'),sample=[])
    start=time.monotonic()
    kind=spec['kind']
    prefix=kind in ('csv','text','noaa_fixed','media','gsm_jsonl','amc') and not spec.get('full_read')
    limit=65536 if prefix else args.max_bytes
    try:
        data,metadata=fetch(spec['url'],args.timeout,limit,prefix)
        out.update(metadata)
        if metadata.get('limit_exceeded'):
            out.update(status='LIMIT_REACHED',detail='Respuesta supera el límite; no se validó el documento completo.');return out
        text=decode(data)
        lower=text[:10000].lower()
        if any(s in lower for s in ('<title>just a moment','<title>access denied','<title>403 forbidden','<title>502 bad gateway','<title>503 service unavailable','verify you are human')):
            out.update(status='BLOCKED',detail='HTTP exitoso con página de bloqueo/error; no se acepta como dato.');return out
        if kind in ('json','geojson','nasa_rows','gbfs','ckan'):
            obj=json.loads(text)
            if kind=='gbfs':
                langs=obj.get('data',{})
                feeds=langs.get('feeds') or next((v.get('feeds',[]) for v in langs.values() if isinstance(v,dict) and v.get('feeds')),[])
                target=next((x['url'] for x in feeds if x.get('name')==spec.get('feed','station_information')),None)
                if not target:raise ValueError('GBFS no incluye el feed solicitado')
                child=run_check(dict(url=target,kind='json',path='data.stations',fields=['station_id','name','lat','lon','capacity']),args)
                out.update(status=child['status'],sample=child['sample'],child=child,detail='Descubrimiento GBFS y validación del catálogo de estaciones.');return out
            if kind=='ckan':
                if not obj.get('success'):raise ValueError('CKAN success=false')
                result=obj.get('result',{})
                resources=result.get('resources',[])
                out.update(status='METADATA_SAMPLE',sample=[pick(result,['name','title','metadata_modified'])],detail=f'{len(resources)} recursos declarados; no son registros del fenómeno.')
                resource=next((r for r in resources if (str(r.get('format','')).lower() in ('csv','geojson') or str(r.get('url','')).lower().endswith(('.csv','.geojson')))),None)
                if spec.get('follow_resource') and resource:
                    url=resource['url']; k='geojson' if 'geojson' in (str(resource.get('format',''))+url).lower() else 'csv'
                    child=run_check(dict(url=url,kind=k),args)
                    out['child']=child
                    if child['status'] in ('DATA_SAMPLE','DOCUMENT_SAMPLE'):out.update(status=child['status'],sample=child['sample'],detail='Recurso enlazado desde metadatos CKAN.')
                return out
            if kind=='geojson':
                if obj.get('type')!='FeatureCollection':raise ValueError('No es GeoJSON FeatureCollection')
                rows=obj.get('features',[]); out['reported_count']=len(rows)
            elif kind=='nasa_rows':
                fields=obj.get('fields',[])
                if not fields or not isinstance(obj.get('data'),list):raise ValueError('Faltan fields/data de CNEOS')
                rows=[dict(zip(fields,row)) for row in obj['data']]
                out['signature']=obj.get('signature')
            else:
                rows=getpath(obj,spec.get('path',''))
                if rows is None:raise ValueError('No existe ruta JSON: '+spec.get('path',''))
                if isinstance(rows,dict):rows=[rows]
                if not isinstance(rows,list):raise ValueError('Se esperaba lista/objeto de registros')
            if not rows:out.update(status='EMPTY',detail='Estructura válida, muestra vacía.');return out
            for field in spec.get('required',[]):
                if any(not isinstance(r,dict) or getpath(r,field) in (None,'') for r in rows[:2]):raise ValueError('Falta campo requerido: '+field)
            count=min(3,max(1,spec.get('sample_rows',2)))
            out.update(status=spec.get('sample_status','DATA_SAMPLE'),sample=[pick(r,spec.get('fields')) for r in rows[:count]],observed_rows=len(rows),detail='Formato y campos de la muestra validados; no implica calidad de toda la fuente.')
            if not any(out['sample']):raise ValueError('La selección no encontró campos de ejemplo')
            if spec.get('follow_media'):
                target=getpath(rows[0],spec['follow_media'])
                if target:
                    out['child']=run_check(dict(url=target,kind='media'),args)
                    out['detail']+=' Se probó además la cabecera del medio enlazado; ver resultado del recurso.'
        elif kind=='csv':
            if '<html' in lower or '<!doctype html' in lower:raise ValueError('Se esperaba CSV y se recibió HTML')
            if out['truncated']:text=text.rsplit('\n',1)[0]
            dialect=csv.Sniffer().sniff(text[:16000],delimiters=',;\t|')
            reader=csv.DictReader(io.StringIO(text),fieldnames=spec.get('columns'),dialect=dialect)
            rows=[]
            for row in reader:
                rows.append(row)
                if len(rows)==2:break
            if not rows:out.update(status='EMPTY',detail='CSV sin registros de muestra.');return out
            if len(reader.fieldnames or [])<2:raise ValueError('CSV sin estructura multicolumna')
            for f in spec.get('required',[]):
                if f not in reader.fieldnames:raise ValueError('Columna requerida ausente: '+f)
            out.update(status='CACHED_SAMPLE' if spec.get('scope')=='repository_snapshot' else 'DATA_SAMPLE',columns=reader.fieldnames,sample=[pick(r,spec.get('fields')) for r in rows],detail='Primeras filas completas del archivo; no se contó el total ni se comprobaron llaves globales.')
        elif kind=='gsm_jsonl':
            first=next((line for line in text.splitlines() if line.strip()),None)
            row=json.loads(first or '{}')
            if not isinstance(row.get('question'),str) or '####' not in row.get('answer',''):raise ValueError('No se reconoce esquema question/answer de GSM8K')
            out.update(status='DATA_SAMPLE',sample=[dict(question_excerpt=' '.join(row['question'].split()[:18]),answer_numeric=row['answer'].split('####')[-1].strip())],detail='Una línea JSONL real: fragmento breve de pregunta y respuesta final de referencia, sin ejecutar un modelo ni evaluar todo el benchmark.')
        elif kind in ('sru','tei'):
            root=ET.fromstring(data)
            if kind=='sru':
                records=root.findall('.//{*}recordData')
                if not records:raise ValueError('SRU sin recordData; revisar diagnósticos o consulta')
                rows=[]
                for record in records[:2]:
                    rows.append({field:[brief(e.text or '') for e in record.findall('.//{http://purl.org/dc/elements/1.1/}'+field)][:2] for field in ['title','creator','date','identifier']})
                out.update(status='METADATA_SAMPLE',sample=rows,detail='XML SRU válido con metadatos bibliográficos; no se recuperó OCR ni el contenido completo de los volúmenes.')
            else:
                if root.tag.split('}')[-1]!='TEI':raise ValueError('La raíz no es TEI')
                titles=root.findall('.//{*}titleStmt/{*}title')
                speakers=root.findall('.//{*}speaker')
                paragraphs=root.findall('.//{*}body//{*}p')
                excerpt=' '.join(' '.join(paragraphs[0].itertext()).split()[:20]) if paragraphs else ''
                out.update(status='DOCUMENT_SAMPLE',sample=[dict(title=' '.join(titles[0].itertext()) if titles else '',speaker_examples=[' '.join(e.itertext()) for e in speakers[:2]],passage_excerpt=excerpt)],detail='Documento TEI con título e intervenciones; no se calculó todavía la red completa de personajes.')
        elif kind=='amc':
            if ':DEGREES' not in text:raise ValueError('No se encontró cabecera AMC en grados')
            lines=text.splitlines();frame=next((i for i,line in enumerate(lines) if line.strip().isdigit()),None)
            if frame is None:raise ValueError('AMC sin frame numérico')
            samples=[]
            for line in lines[frame+1:frame+3]:
                values=line.split();samples.append(dict(channel=values[0],values=[float(x) for x in values[1:]]))
            out.update(status='DATA_SAMPLE',sample=samples,detail='Prefijo AMC de un frame; interpretar canales con el esqueleto ASF correspondiente.')
        elif kind=='noaa_fixed':
            rows=[]
            for line in text.splitlines()[:2]:
                if len(line)<71:raise ValueError('Registro de estación demasiado corto')
                rows.append(dict(station_id=line[:11],latitude=float(line[12:20]),longitude=float(line[21:30]),elevation_m=float(line[31:37]),name=line[41:71].strip()))
            out.update(status='METADATA_SAMPLE',sample=rows,detail='Catálogo de estaciones de ancho fijo; observaciones meteorológicas no probadas.')
        elif kind=='gdelt_index':
            rows=[]
            for line in text.splitlines()[:3]:
                size,md5,url=line.split(maxsplit=2)
                if not url.endswith('.zip') or len(md5)!=32:raise ValueError('Manifiesto GDELT inesperado')
                rows.append(dict(bytes=int(size),md5=md5,url=url))
            out.update(status='METADATA_SAMPLE',sample=rows,detail='Manifiesto recuperado; archivos de eventos/mentions/GKG no descargados.')
        elif kind=='pdf':
            if not data.startswith(b'%PDF'):raise ValueError('La respuesta no tiene firma PDF')
            try:from pypdf import PdfReader
            except ImportError:out.update(status='DEPENDENCY_MISSING',detail='PDF descargado; falta pypdf para extraer texto.');return out
            pdf=PdfReader(io.BytesIO(data)); page=min(spec.get('pdf_page',0),len(pdf.pages)-1)
            words=(pdf.pages[page].extract_text() or '').split()
            if not words:raise ValueError('PDF válido, sin texto extraíble en la página seleccionada')
            out.update(status='DOCUMENT_SAMPLE',sample=[dict(page=page+1,excerpt=' '.join(words[:20]))],pages=len(pdf.pages),detail='Firma PDF y extracción de una página validadas; sin OCR ni auditoría de todas sus tablas.')
        elif kind=='xlsx':
            if not data.startswith(b'PK'):raise ValueError('La respuesta no tiene contenedor ZIP/XLSX')
            try:from openpyxl import load_workbook
            except ImportError:out.update(status='DEPENDENCY_MISSING',detail='Falta openpyxl para leer XLSX.');return out
            wb=load_workbook(io.BytesIO(data),read_only=True,data_only=True)
            rows=iter(wb.worksheets[0].values); header=None
            for _ in range(30):
                row=next(rows,())
                if any(norm(x).strip()=='clues' for x in row):header=[str(x).strip() for x in row];break
            if not header:raise ValueError('No se encontró cabecera CLUES en las primeras 30 filas')
            fields=[f for f in header if any(norm(term) in norm(f) for term in spec.get('fields_matching',[]))][:8]
            sample=[]
            for _ in range(2):sample.append(pick(dict(zip(header,next(rows))),fields))
            wb.close()
            out.update(status='DATA_SAMPLE',columns=header,sample=sample,detail='Cabecera CLUES y primeras dos filas del primer sheet; no se validó completitud del catálogo.')
        elif kind=='media':
            fmt='JPEG' if data.startswith(b'\xff\xd8') else 'PNG' if data.startswith(b'\x89PNG\r\n\x1a\n') else 'WAV' if data.startswith(b'RIFF') and data[8:12]==b'WAVE' else 'MP3' if data.startswith(b'ID3') or (len(data)>2 and data[0]==255 and data[1]&224==224) else 'OGG' if data.startswith(b'OggS') else None
            if not fmt:raise ValueError('No se reconoce firma JPEG/PNG/WAV/MP3/OGG en el prefijo')
            out.update(status='MEDIA_SAMPLE',sample=[dict(format=fmt,bytes_checked=len(data),complete_file=not out['truncated'])],detail='Sólo firma binaria y acceso al prefijo: no se decodificó, reprodujo ni validó el medio completo.')
        elif kind=='text':
            if '<html' in lower:raise ValueError('Se esperaba texto plano y se recibió HTML')
            if spec.get('expected') and spec['expected'].lower() not in text.lower():raise ValueError('No aparece contenido esperado')
            if spec.get('excerpt_start'):
                passage_match=re.search(spec['excerpt_start'],text,re.I)
                if not passage_match:raise ValueError('No se encontró el comienzo del pasaje esperado')
                text=text[passage_match.start():]
            excerpt=' '.join(text.split()[:60 if spec.get('public_domain') else 20])
            out.update(status='DOCUMENT_SAMPLE',sample=[dict(excerpt=excerpt)],detail='Prefijo de documento real; no se descargó el corpus completo.')
        else:
            page=Page();page.feed(text)
            content=page.text();title=' '.join(''.join(page.title).split())
            if spec.get('expected') and norm(spec['expected']) not in norm(content):raise ValueError('No aparece contenido esperado')
            if len(content)<60 and not title:raise ValueError('Página vacía sin título ni contenido suficiente')
            if kind=='dof':
                if not all(x in norm(content) for x in ('articulo 76','doce dias','2023')):raise ValueError('Nota DOF distinta del decreto esperado')
                out.update(status='DOCUMENT_SAMPLE',sample=[dict(codigo='5675889',titulo='Decreto de reforma de los artículos 76 y 78 de la LFT',publicacion='2022-12-27',nuevo_minimo_dias=12,entrada_vigor='2023-01-01')],detail='Texto real de nota histórica; campos extraídos/normalizados para la demostración.')
            elif kind=='discover_csv':
                target=next((urllib.parse.urljoin(spec['url'],x) for x in page.links if re.search(spec['link_pattern'],x)),None)
                if not target:raise ValueError('No se encontró enlace mensual esperado en la página oficial')
                child=run_check(dict(url=target,kind='csv',fields=spec.get('fields')),args)
                out.update(status=child['status'],sample=child['sample'],child=child,detail='Descarga CSV descubierta en página oficial, muestreo por prefijo.');return out
            else:
                example=title or ' '.join(content.split()[:16])
                out.update(status='DOC_ONLY',sample=[dict(page_title=' '.join(example.split()[:18]))],detail='Ejemplo de página; no son registros del dataset. Los enlaces pueden requerir JavaScript, sesión o descarga adicional.')
        return out
    except urllib.error.HTTPError as e:
        out.update(requested_url=spec['url'],http_status=e.code,status='BLOCKED' if e.code in (401,403,429) else 'HTTP_ERROR',detail=f'HTTP {e.code}: {e.reason}. No se sorteó el bloqueo ni se usaron credenciales personales.')
    except (urllib.error.URLError,TimeoutError,OSError) as e:
        out.update(requested_url=spec['url'],status='NETWORK_ERROR',detail=str(e)[:240])
    except Exception as e:
        out.update(requested_url=spec['url'],status='PARSE_ERROR',detail=f'{type(e).__name__}: {str(e)[:240]}')
    finally:out['elapsed_seconds']=round(time.monotonic()-start,3)
    return out

def run_source(spec,args):
    checks=[run_check(s,args) for s in spec['checks']]
    preference=['DATA_SAMPLE','CACHED_SAMPLE','DOCUMENT_SAMPLE','MEDIA_SAMPLE','METADATA_SAMPLE','DOC_ONLY','EMPTY','LIMIT_REACHED','DEPENDENCY_MISSING','BLOCKED','HTTP_ERROR','NETWORK_ERROR','PARSE_ERROR']
    status=next((s for s in preference if any(x['status']==s for x in checks)),'PARSE_ERROR')
    return dict(id=spec['id'],name=spec['name'],status=status,note=spec['note'],checks=checks)

def write_report(results,path,meta):
    counts=Counter(r['status'] for r in results)
    lines=['# Prueba de acceso y muestras de fuentes','',f"Ejecución: **{meta['started_at_local']}** (America/Mexico_City). Fin UTC: `{meta['finished_at_utc']}`.",'',
    f"Se probaron **{len(results)} fuentes** del catálogo mediante GET públicos, con timeout de {meta['timeout_seconds']} s por operación, {meta['workers']} fuentes en paralelo y un límite de {meta['max_bytes']} bytes para documentos completos. CSV/TXT se muestrean por prefijo de 64 KiB.",'',
    '**Qué comprueba:** acceso desde este entorno, formato, campos mínimos y ejemplos recuperados. **Qué no comprueba:** disponibilidad futura, calidad estadística completa, autenticación de APIs protegidas, decodificación/reproducción integral de multimedia, ni salud de los workflows existentes. Una página HTTP 200 no se cuenta como un dataset recuperado.','',
    'Los ejemplos se tomaron de las respuestas; los datos no disponibles no se sustituyen por filas inventadas. `CACHED_SAMPLE` identifica CSVs ya publicados por el repo, separados de las APIs en vivo. `METADATA_SAMPLE` prueba un catálogo/manifiesto, no los eventos u observaciones que referencia.','',
    '## Resultados','', '| Resultado | Fuentes |','| --- | ---: |']
    for k,n in sorted(counts.items()):lines.append(f'| {k}: {LABELS[k]} | {n} |')
    lines+=['','## Índice de las pruebas','', '| Fuente | Resultado más útil | Capas con fallo o límite |','| --- | --- | --- |']
    def all_failures(check):
        failures=[] if check['status'] in ('DATA_SAMPLE','CACHED_SAMPLE','DOCUMENT_SAMPLE','MEDIA_SAMPLE','METADATA_SAMPLE','DOC_ONLY') else [check['status']]
        return failures+(all_failures(check['child']) if check.get('child') else [])
    for r in results:
        failures=[failure for check in r['checks'] for failure in all_failures(check)]
        lines.append(f"| [{r['id']}](#{r['id']}) | {r['status']} | {', '.join(failures) or '—'} |")
    lines+=['','## Interpretación y siguientes correcciones','',
    '- Registros recuperados permiten comenzar una exploración de esa muestra; no prueban representatividad ni unicidad global.',
    '- Portales, índices y documentación requieren un segundo paso para obtener la base. Consultar cada ficha para autenticación, licencia y unidad de análisis.',
    '- Un bloqueo/error queda registrado con URL, código y hora. Reintentar sólo esa fuente desde otro momento o entorno autorizado; no afirmar que el sitio está caído globalmente.',
    '- Las muestras por prefijo no dan un conteo total ni una muestra aleatoria. Un hash de prefijo no identifica el archivo completo.',
    '- En fuentes mixtas se indica la capa probada. Una URL de imagen o audio presente no demuestra descarga o reproducción del medio.',
    '- Para citar resultados científicos, de encuestas o territoriales, añadir una validación del diseño, calidad y cobertura antes de inferir conclusiones.',
    '', '## Reproducir','', 'Desde la raíz del repo (Python 3.10+; `pypdf` y `openpyxl` son lectores opcionales):','',
    '```bash','python -m pip install pypdf openpyxl','python scripts/probe_catalog_sources.py','python scripts/probe_catalog_sources.py --only dof-publicaciones usgs-sismos','```','',
    'No lee secrets ni activa tareas programadas. Sin `--strict`, el código de salida 0 significa que el informe se produjo; los fallos permanecen visibles. Con `--strict` devuelve 1 si falla cualquier comprobación definida, incluidos recursos enlazados. Un `DOC_ONLY` válido pasa su comprobación de página, pero sigue sin acreditar ingesta de registros.', '',
    'La selección `--only` guarda resultados en un subdirectorio `selected/` para conservar la última corrida completa. Se puede cambiar con `--output`. El informe y results.json se generan juntos.','',
    '## Ejemplos y evidencia por fuente','']
    for r in results:
        lines += [f"### {r['id']}",'',f"**{r['name']}** — `{r['status']}`.",'',r['note'],'']
        for idx,check in enumerate(r['checks'],1):
            lines += [f"Prueba {idx}: [{check['kind']}]({check['requested_url']}) — `{check['status']}`; HTTP `{check.get('http_status','sin respuesta')}`; {check.get('elapsed_seconds','?')} s.",'',check['detail'],'']
            if check.get('child'):
                child=check['child']
                lines += [f"Recurso enlazado: [{child['kind']}]({child['requested_url']}) — `{child['status']}`, HTTP `{child.get('http_status','sin respuesta')}`.",'',child['detail'],'']
                if child.get('sample') and child['sample']!=check['sample']:
                    lines+=['```json',json.dumps(child['sample'],ensure_ascii=False,indent=2),'```','']
            if check['sample']:
                lines+=['```json',json.dumps(check['sample'],ensure_ascii=False,indent=2),'```','']
            else:lines+=['Sin registros o ejemplos recuperados para esta prueba.','']
    probes_link=Path(os.path.relpath(ROOT/'catalogs/source_probes.json',path.parent)).as_posix()
    catalog_link=Path(os.path.relpath(ROOT/'docs/CATALOGO_DATASETS_REALES.md',path.parent)).as_posix()
    lines += ['## Evidencia legible por máquina','', f'[results.json](results.json) contiene cada petición y su timestamp; código HTTP, content-type, bytes, hash y su alcance cuando están disponibles; además de muestras y errores. [Definición de pruebas]({probes_link}). [Catálogo]({catalog_link}).','']
    path.write_text('\n'.join(lines))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--only',nargs='+');p.add_argument('--output',type=Path)
    p.add_argument('--timeout',type=int,default=18);p.add_argument('--workers',type=int,default=4)
    p.add_argument('--max-bytes',type=int,default=8*1024*1024);p.add_argument('--strict',action='store_true')
    args=p.parse_args()
    specs=json.loads((ROOT/'catalogs/source_probes.json').read_text())['probes']
    catalog=json.loads((ROOT/'catalogs/datasets_reales_mexico.json').read_text())
    ids=[x['id'] for x in specs]
    assert len(ids)==len(set(ids)) and set(ids)=={d['id'] for d in catalog['datasets']}, 'Catalog/probe IDs differ'
    if args.only:
        unknown=set(args.only)-set(ids)
        if unknown:p.error('IDs desconocidos: '+','.join(sorted(unknown)))
        specs=[s for s in specs if s['id'] in args.only]
    output=args.output or ROOT/'source_tests'/('selected' if args.only else '')
    output.mkdir(parents=True,exist_ok=True)
    meta=dict(started_at_utc=now(),started_at_local=datetime.now(ZoneInfo('America/Mexico_City')).isoformat(timespec='seconds'),timeout_seconds=args.timeout,workers=args.workers,max_bytes=args.max_bytes,python_version=sys.version.split()[0],probe_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),probe_definitions_sha256=hashlib.sha256((ROOT/'catalogs/source_probes.json').read_bytes()).hexdigest())
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures={pool.submit(run_source,s,args):s for s in specs}
        for future in concurrent.futures.as_completed(futures):
            try:r=future.result()
            except Exception as exc:
                spec=futures[future]
                r=dict(id=spec['id'],name=spec['name'],status='INTERNAL_ERROR',note='Excepción interna del verificador; no es un dictamen sobre la fuente.',checks=[dict(kind='internal',requested_url=spec['checks'][0]['url'],status='INTERNAL_ERROR',sample=[],detail=f'{type(exc).__name__}: {str(exc)[:240]}',checked_at_utc=now())])
            results.append(r);print(r['id']+': '+r['status'],flush=True)
    order={s['id']:i for i,s in enumerate(specs)};results.sort(key=lambda r:order[r['id']])
    meta['finished_at_utc']=now()
    payload=dict(schema_version='1.0',run=meta,summary=dict(Counter(r['status'] for r in results)),results=results)
    (output/'results.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    write_report(results,output/'README.md',meta)
    print(json.dumps(payload['summary'],ensure_ascii=False),flush=True)
    def failed(check):
        return check['status'] not in {'DATA_SAMPLE','CACHED_SAMPLE','DOCUMENT_SAMPLE','MEDIA_SAMPLE','METADATA_SAMPLE','DOC_ONLY'} or bool(check.get('child') and failed(check['child']))
    return int(args.strict and any(failed(check) for r in results for check in r['checks']))
if __name__=='__main__':raise SystemExit(main())
