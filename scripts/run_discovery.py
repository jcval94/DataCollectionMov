#!/usr/bin/env python3
"""First discovery harness: bounded retail snapshot, exact arithmetic and evidence."""
from __future__ import annotations
import argparse, csv, hashlib, io, json, re, tempfile, urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
URL='https://archive.ics.uci.edu/static/public/352/data.csv'
REQUIRED=['InvoiceNo','StockCode','Description','Quantity','InvoiceDate','UnitPrice','CustomerID','Country']
POLICY='Product-like StockCode: five digits plus optional letters; positive price, nonzero integer quantity. Quarantine positive quantity on C invoice. Retain missing customers and exact duplicate lines; sensitivity removes duplicates.'

def analyze(rows):
    totals=defaultdict(lambda:dict(gross=Decimal(0),credits=Decimal(0),lines=0,description=''))
    quality=Counter();seen=set();examples=[];dates=[];reversal_evidence=[]
    for row in rows:
        quality['input_rows']+=1
        if None in row or any(row.get(k) is None for k in REQUIRED):raise ValueError('Incomplete/misaligned CSV row')
        key=tuple(row[k] for k in REQUIRED)
        duplicate=key in seen;seen.add(key)
        quality['exact_duplicate_rows']+=duplicate
        quality['missing_customer_rows']+=not row['CustomerID'].strip()
        stamp=datetime.strptime(row['InvoiceDate'],'%m/%d/%Y %H:%M');dates.append(stamp)
        qty=Decimal(row['Quantity']);price=Decimal(row['UnitPrice'])
        if not qty.is_finite() or not price.is_finite() or qty!=qty.to_integral_value():raise ValueError('Invalid numeric value')
        code=row['StockCode'].strip();cancel=row['InvoiceNo'].upper().startswith('C')
        reason=('non_product_code' if not re.fullmatch(r'\d{5}[A-Za-z]*',code) else 'nonpositive_price' if price<=0 else 'zero_quantity' if qty==0 else 'cancel_positive_quantity' if cancel and qty>0 else None)
        if reason:quality['excluded_'+reason]+=1;continue
        quality['eligible_rows']+=1
        quality['negative_without_C']+=qty<0 and not cancel
        value=qty*price
        if code=='23843':reversal_evidence.append({k:row[k] for k in REQUIRED if k!='CustomerID'})
        for variant in ['retained_duplicates']+([] if duplicate else ['removed_duplicates']):
            t=totals[(variant,code)];t['lines']+=1;t['description']=row['Description']
            t['gross']+=max(value,Decimal(0));t['credits']+=max(-value,Decimal(0))
        if len(examples)<5:examples.append({k:row[k] for k in ['InvoiceNo','StockCode','Description','Quantity','UnitPrice']} )
    outputs={}
    for variant in ['retained_duplicates','removed_duplicates']:
        items=[dict(code=code,**t,net=t['gross']-t['credits']) for (v,code),t in totals.items() if v==variant]
        for metric in ['gross','net']:
            ranked=sorted(items,key=lambda t:(-t[metric],t['code']))
            for rank,item in enumerate(ranked,1):item['rank_'+metric]=rank
        for item in items:item['rank_loss']=item['rank_net']-item['rank_gross']
        sums={m:sum((t[m] for t in items),Decimal(0)) for m in ['gross','credits','net']}
        assert sums['gross']-sums['credits']==sums['net']
        outputs[variant]=dict(products=len(items),sums=sums,ranking=sorted(items,key=lambda t:t['rank_gross']))
    return dict(quality=dict(quality),date_min=min(dates).isoformat() if dates else None,date_max=max(dates).isoformat() if dates else None,examples=examples,reversal_evidence=reversal_evidence,variants=outputs)

def self_check():
    def r(invoice,code,qty,price,customer=''):
        return dict(zip(REQUIRED,[invoice,code,'fixture',qty,'12/1/2010 8:26',price,customer,'UK']))
    a=r('1','12345','10','0.1');b=r('C1','12345','-9','0.1');c=r('2','54321','5','0.1')
    result=analyze([a,b,c,a,r('C2','54321','1','0.1'),r('3','POST','1','2')])
    keep=result['variants']['retained_duplicates'];dedup=result['variants']['removed_duplicates']
    assert keep['sums']['gross']==Decimal('2.5') and keep['sums']['net']==Decimal('1.6')
    assert dedup['sums']['gross']==Decimal('1.5') and dedup['sums']['net']==Decimal('.6')
    assert result['quality']['excluded_cancel_positive_quantity']==1
    assert result['quality']['excluded_non_product_code']==1
    assert result['quality']['missing_customer_rows']==6
    assert next(t for t in dedup['ranking'] if t['code']=='12345')['rank_loss']==1
    try:analyze([{'InvoiceNo':'bad'}])
    except ValueError:pass
    else:raise AssertionError('Invalid schema accepted')
    return ['exact_decimal_arithmetic','signed_credits','duplicate_sensitivity','C_positive_quarantine','product_scope','missing_customers_retained','ranking_reversal','invalid_schema_rejected']

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--case',choices=['uci-retail'],default='uci-retail');p.add_argument('--input',type=Path);p.add_argument('--output',type=Path,default=ROOT/'examples/retail_discovery');p.add_argument('--self-check',action='store_true');args=p.parse_args()
    tests=self_check()
    if args.self_check:print(json.dumps(dict(status='PASS',checks=tests)));return
    started=datetime.now(timezone.utc).isoformat(timespec='seconds');request=None
    if args.input:
        if args.input.stat().st_size>64*1024*1024:raise ValueError('Input exceeds 64 MiB')
        data=args.input.read_bytes();scope='local_snapshot'
    else:
        with urllib.request.urlopen(urllib.request.Request(URL,headers={'User-Agent':'DataCollectionMov-discovery/1.0'}),timeout=30) as response:
            data=response.read(64*1024*1024+1);request=dict(http_status=response.status,final_url=response.url)
        if len(data)>64*1024*1024:raise ValueError('Download exceeds 64 MiB')
        scope='live_download';cache=Path(tempfile.gettempdir())/'datacollectionmov-retail.csv';cache.write_bytes(data)
    reader=csv.DictReader(io.StringIO(data.decode('utf-8-sig')))
    if reader.fieldnames!=REQUIRED:raise ValueError('Unexpected CSV schema (HTML is not data)')
    result=analyze(reader)
    if result['quality'].get('eligible_rows',0)==0:raise ValueError('No eligible rows')
    args.output.mkdir(parents=True,exist_ok=True)
    manifest=dict(source_id='uci-retail',source_url=URL,input_scope=scope,request=request,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),hash_scope='complete_file',attribution='Chen, D. (2015), Online Retail, UCI, doi:10.24432/C5BW33',license='CC BY 4.0')
    run=dict(question_id='uci-retail.q1',status='descriptive_measured',started_at_utc=started,finished_at_utc=datetime.now(timezone.utc).isoformat(timespec='seconds'),script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),policy=POLICY,currency='GBP',test_status='PASS',tests=tests,model_used=False)
    def write(name,value):(args.output/name).write_text(json.dumps(value,ensure_ascii=False,indent=2,default=str)+'\n')
    summary={k:v for k,v in result.items() if k!='variants'}
    summary['variants']={k:dict(products=v['products'],sums=v['sums'],top20=v['ranking'][:20]) for k,v in result['variants'].items()}
    write('inputs_manifest.json',manifest);write('run.json',run);write('metrics.json',summary)
    with (args.output/'product_ranking.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['code','description','lines','gross','credits','net','rank_gross','rank_net','rank_loss']);writer.writeheader();writer.writerows(result['variants']['retained_duplicates']['ranking'])
    with (args.output/'product_ranking_deduplicated.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['code','description','lines','gross','credits','net','rank_gross','rank_net','rank_loss']);writer.writeheader();writer.writerows(result['variants']['removed_duplicates']['ranking'])
    top=result['variants']['retained_duplicates']['ranking'][:20]
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    chart_items=top[:8];fig,ax=plt.subplots(figsize=(9,5))
    positions=list(range(len(chart_items)))
    ax.barh([y-.18 for y in positions],[float(t['gross']) for t in chart_items],height=.35,label='Bruto')
    ax.barh([y+.18 for y in positions],[float(t['net']) for t in chart_items],height=.35,label='Neto firmado')
    ax.set_yticks(positions,[t['code'] for t in chart_items]);ax.invert_yaxis();ax.set_xlabel('GBP');ax.set_title('Mismos productos: bruto frente a neto firmado');ax.legend();fig.tight_layout();fig.savefig(args.output/'gross_vs_net.png',dpi=130);plt.close(fig)
    lines=['# Piloto ejecutado: retail bruto frente a neto','', 'Pregunta: ¿qué productos cambian de posición al incorporar créditos/cancelaciones registrados? Este piloto calcula importes; no ejecuta un modelo de IA.','',f'Captura/ejecución UTC: `{started}`. Fuente: [UCI Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail), Daqing Chen, CC BY 4.0. [Manifiesto y hash completo](inputs_manifest.json).','',f'**{result["quality"]["input_rows"]:,} filas leídas**, **{result["quality"]["eligible_rows"]:,} elegibles**, {result["variants"]["retained_duplicates"]["products"]:,} códigos de producto. Periodo observado: {result["date_min"]} a {result["date_max"]}.','', '## Definiciones y límites','',POLICY,'','Bruto = suma de importes positivos; créditos = valor absoluto de importes negativos; neto firmado = bruto − créditos. Importes en GBP. Una línea negativa no prueba una devolución físicamente enlazada a la venta original; el neto no es utilidad ni ingreso auditado. Las facturas pueden repetirse por producto; no se inventa una llave única. Los códigos con cinco dígitos y letras se tratan como productos por una regla explícita, pendiente de validación comercial.','', 'Se conservan duplicados exactos porque podrían ser líneas legítimas; se compara una variante que los elimina. No se excluyen clientes faltantes. [Métricas completas y sensibilidad](metrics.json) · [Ranking completo](product_ranking.csv) · [Variante sin duplicados](product_ranking_deduplicated.csv).','','## Resultados: productos del top 20 bruto','','| Código | Bruto GBP | Créditos GBP | Neto GBP | Puesto bruto | Puesto neto |','| --- | ---: | ---: | ---: | ---: | ---: |']
    for t in top:lines.append(f'| {t["code"]} | {t["gross"]:,.2f} | {t["credits"]:,.2f} | {t["net"]:,.2f} | {t["rank_gross"]} | {t["rank_net"]} |')
    focus=next((t for t in result['variants']['retained_duplicates']['ranking'] if t['code']=='23843'),None)
    narrative=(f"Ejemplo medido: `23843` ocupa el puesto bruto {focus['rank_gross']}, con {focus['gross']:,.2f} GBP positivos y {focus['credits']:,.2f} negativos: neto {focus['net']:,.2f} GBP." if focus else 'El producto de contraste 23843 no está en este snapshot.')
    lines+=['','![Bruto y neto firmado para los ocho primeros productos por bruto](gross_vs_net.png)','',narrative+' Las líneas del producto se muestran abajo; no se atribuye una causa comercial. Los empates de ranking se ordenan por código y las descripciones son la última observada por producto.','','```json',json.dumps(result['reversal_evidence'],ensure_ascii=False,indent=2),'```','','## Sensibilidad a duplicados','','| Variante | Bruto GBP | Créditos GBP | Neto GBP |','| --- | ---: | ---: | ---: |']
    for k,v in result['variants'].items():lines.append(f'| {k} | {v["sums"]["gross"]:,.2f} | {v["sums"]["credits"]:,.2f} | {v["sums"]["net"]:,.2f} |')
    lines+=['','## Tests ejecutados','','| Comprobación | Resultado |','| --- | --- |']+[f'| {test} | PASS |' for test in tests]
    lines+=['| Esquema del archivo completo | PASS |','| Cuadre bruto − créditos = neto, ambas variantes | PASS |','','Calidad observada:','', '```json',json.dumps(result['quality'],indent=2),'```','','## Registros reales de ejemplo','','```json',json.dumps(result['examples'],ensure_ascii=False,indent=2),'```','','## Reproducir','','```bash','python -m pip install matplotlib','python scripts/run_discovery.py --self-check','python scripts/run_discovery.py --case uci-retail','# Sin red, usando una copia cuyo hash se coteja con el manifiesto:','python scripts/run_discovery.py --input /ruta/data.csv --output /ruta/resultados','```','','La descarga completa usa un límite de 64 MiB y timeout de 30 s. El original no se añade al repositorio; se identifica por hash para verificar futuras reproducciones. El ejecutor implementa el primer adaptador retail; los perfiles de otros métodos siguen siendo diseños.','']
    (args.output/'README.md').write_text('\n'.join(lines));print(json.dumps(dict(rows=result['quality']['input_rows'],products=len(result['variants']['retained_duplicates']['ranking']),output=str(args.output),tests='PASS')))

if __name__=='__main__':main()
