"""Inspections are surveillance events, not a rat census. All rules are explicit and auditable."""
import textwrap
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from .common import load as read_source, profile, BLUE, RED, GOLD, COLORS
from v3.data import require

CASE='nyc-ratas'
PREFIX='D04'
SEED=1729
TITLE='¿Más ratas o más oportunidades de encontrarlas?'
HOOK='Dos distritos presentan números distintos de hallazgos. Una persona propone dirigir todos los recursos al que tiene más positivos; otra pregunta cuántos predios se visitaron y cuántas visitas fueron seguimientos de un problema previo. Hoy no contaremos la población de ratas: investigaremos lo que un sistema de inspección permite observar. Elige una pregunta, un denominador y una predicción que estés dispuesto a revisar.'
BOROUGHS=['Bronx','Brooklyn','Manhattan','Queens','Staten Island']
BBL_BOROUGH={'1':'Manhattan','2':'Bronx','3':'Brooklyn','4':'Queens','5':'Staten Island'}
POSITIVE=['Failed for Rat Activity','Failed for Rat Activity and Other Reason']
OUTCOMES=POSITIVE+['Passed','Failed for Other Reason']
TYPES=['Initial','Compliance','Treatments','Stoppage','Clean Ups']
SPECS=[('inspection-scope',['D04-B','D04-E'],'type_counts'),('borough-positivity',['D04-B','D04-E'],'policy_rates'),
       ('month-heatmap',['D04-C','D04-D1'],'monthly'),('season-comparison',['D04-D1'],'season_rates'),
       ('paired-seasons',['D04-D1'],'paired_sensitivity'),('ranking-denominator',['D04-B','D04-E'],'borough_summary'),
       ('monthly-volume',['D04-C','D04-E'],'monthly')]
STORIES={
 'D04-B':('El distrito que cambia al contar predios','¿Elegirías por hallazgos, visitas o primeros predios positivos?',
     'Repetir inspecciones pondera más a unos predios; faltan o discrepan algunas llaves catastrales.',
     'Compara eventos iniciales, eventos con llave coherente y la primera inspección por predio, declarando los cambios de universo.',
     '¿Cómo distinguirías más accidentes de una mayor vigilancia en carreteras?'),
 'D04-C':('El calendario de lo que sí se inspeccionó','¿Una subida mensual de hallazgos implica más animales?',
     'El volumen de visitas cambia por mes; sólo tenemos un año observado de vigilancia dirigida.',
     'Contrasta conteos con proporciones y separa boroughs; no extrapoles un ciclo estacional general.',
     '¿Cómo interpretarías una subida de fallas cuando se duplicó el número de pruebas?'),
 'D04-D1':('El verano bajo una segunda lupa','¿Esperas mayor positividad en verano aun comparando los mismos predios?',
     'Invierno agrupa enero, febrero y diciembre de 2024; no es una secuencia temporal única y la cohorte pareada es selectiva.',
     'Compara tasas por borough, pesos iguales y predios observados en ambas estaciones; revisa el cruce pareado y su incertidumbre condicional.',
     '¿Qué cambiaría al comparar ventas de las mismas tiendas frente a todas las tiendas abiertas?'),
 'D04-E':('El ranking que dependía del denominador','¿Puede el distrito con más positivos tener una tasa menor?',
     'Seguimientos y tratamientos responden a decisiones previas; mezclarlos con visitas iniciales cambia el significado de la métrica.',
     'Cambia la política de visitas y el denominador, conserva los recuentos y explica qué cambió en cada paso.',
     '¿Cuándo un ranking de reseñas mide popularidad, calidad o intensidad de participación?')}


def load(): return read_source(CASE)


def prepare(raw,manifest):
    d=raw.copy();checks=[]
    def check(rule,condition,detail):
        require(bool(condition),rule+': '+detail);checks.append(dict(rule=rule,passed=True,detail=detail))
    d['inspection_date']=pd.to_datetime(d.inspection_date,format='ISO8601',errors='raise')
    check('calendar_window',d.inspection_date.ge('2024-01-01').all() and d.inspection_date.lt('2025-01-01').all(),'Closed calendar 2024, floating timestamps, no invented UTC offset.')
    check('categories',d.borough.isin(BOROUGHS).all() and d.inspection_type.isin(TYPES).all(),'Unknown categories stop this version rather than disappear.')
    check('administrative_id',d.job_id.ne('').all(),'Administrative job ID present; not a unique event by itself.')
    check('minimal_projection',not set(raw).intersection({'house_number','street_name','latitude','longitude','observations'}),'No addresses, precise coordinates or free text requested.')
    d['duplicate_exact']=raw.duplicated()
    keys=['job_id','inspection_date','inspection_type','bbl']
    distinct=d[~d.duplicate_exact]
    check('business_conflicts',not distinct.duplicated(keys).any(),'Conflicting rows with same business key would stop instead of choosing an outcome.')
    d['bbl_valid']=d.bbl.str.fullmatch(r'[1-5]\d{9}')
    d['bbl_borough_match']=d.bbl.str[0].map(BBL_BOROUGH).eq(d.borough)&d.bbl_valid
    d['known_outcome']=d.result.isin(OUTCOMES)
    d['positive']=d.result.isin(POSITIVE).where(d.known_outcome,np.nan).astype('Float64')
    check('initial_outcomes',d.loc[d.inspection_type.eq('Initial'),'known_outcome'].all(),'All Initial results map explicitly to rat-sign binary outcome.')
    d['initial_eligible']=d.inspection_type.eq('Initial') & d.known_outcome & ~d.duplicate_exact
    d['property_eligible']=d.initial_eligible & d.bbl_borough_match
    d['month']=d.inspection_date.dt.month
    d['season']=np.select([d.month.isin([1,2,12]),d.month.isin([6,7,8])],['Winter','Summer'],default='Other')
    check('record_conservation',len(d)==len(raw),'All original records retained in Silver, including exact duplicates and unresolved keys.')
    transformations=[
        dict(step='exact_duplicates',affected_rows=int(d.duplicate_exact.sum()),action='Flag in Silver; one copy only in Gold event denominators.',statistical_consequence='Avoid double-counting the same received event.'),
        dict(step='not_initial',affected_rows=int((~d.inspection_type.eq('Initial')).sum()),action='Keep all in Silver and type profile; exclude follow-ups/treatment from main comparisons.',statistical_consequence='Main denominator describes initial surveillance, not all interventions.'),
        dict(step='invalid_bbl',affected_rows=int((~d.bbl_valid).sum()),action='Retain in event analyses; exclude only from property matching.',statistical_consequence='Property and all-event universes differ; report both.'),
        dict(step='bbl_borough_disagreement',affected_rows=int((d.bbl_valid&~d.bbl_borough_match).sum()),action='Flag; do not relocate or repair from cadastral prefix; exclude from property matching.',statistical_consequence='Do not silently join a property to contradictory geography.'),
        dict(step='first_initial_per_property',affected_rows=int(d.property_eligible.sum()-d.loc[d.property_eligible,'bbl'].nunique()),action='For property policy choose earliest Initial date, then lexicographic job ID; never choose by result.',statistical_consequence='One observed initial event per property; not an estimate for uninspected properties.')]
    p=profile(raw,d,manifest,keys,{'inspection_date':'NYC floating local calendar; no offset supplied','bbl':'10-digit public tax-lot code, kept as string'})
    p['temporal']=dict(min=d.inspection_date.min().isoformat(),max=d.inspection_date.max().isoformat(),frequency='Irregular events; all 12 months present.',
        timezone='Floating producer timestamps; use calendar month, do not claim timezone conversion.')
    p['coverage']=dict(duplicate_exact=int(d.duplicate_exact.sum()),invalid_bbl=int((~d.bbl_valid).sum()),
        bbl_borough_disagreement=int((d.bbl_valid&~d.bbl_borough_match).sum()),initial_events=int(d.initial_eligible.sum()),property_eligible_events=int(d.property_eligible.sum()),
        unique_property_keys=int(d.loc[d.property_eligible,'bbl'].nunique()))
    p['target_and_leakage']='No forecasting or supervised target. Follow-ups selected by prior outcomes are excluded from main surveillance denominator; no causal intervention effect or rat-population estimate.'
    return d,p,transformations,checks


def paired_statistics(frame,repetitions=500):
    require(len(frame)>0 and frame[['Winter','Summer']].isin([0,1]).all().all(),'Invalid or empty paired cohort')
    diff=frame.Summer.to_numpy(dtype=float)-frame.Winter.to_numpy(dtype=float)
    rng=np.random.default_rng(SEED);boot=[]
    for _ in range(repetitions):boot.append(float(rng.choice(diff,len(diff),replace=True).mean()))
    low,high=np.quantile(boot,[.025,.975])
    return dict(properties=len(frame),winter_positive=int(frame.Winter.sum()),summer_positive=int(frame.Summer.sum()),
        winter_fraction=float(frame.Winter.mean()),summer_fraction=float(frame.Summer.mean()),difference=float(diff.mean()),
        bootstrap_percentile95=[float(low),float(high)],repetitions=repetitions,seed=SEED,
        assumption='Resampling the selected paired properties as IID units; spatial dependence and nonrandom inspection selection are not corrected. Conditional uncertainty only, not population coverage.')


def first_property_events(valid,by_season=False):
    return valid.sort_values(['inspection_date','job_id','bbl']).drop_duplicates(['bbl','season'] if by_season else ['bbl'],keep='first')


def analyze(d):
    unique=d[~d.duplicate_exact].copy();initial=d[d.initial_eligible].copy();valid=d[d.property_eligible].copy()
    first=first_property_events(valid)
    any_positive=valid.groupby(['borough','bbl'],sort=True).positive.max().reset_index()
    comparable=unique[unique.inspection_type.isin(['Initial','Compliance'])&unique.known_outcome]
    policies=[]
    for label,frame in [('All Initial events',initial),('Key-consistent Initial events',valid),('First Initial per property',first),
                        ('Any positive per property',any_positive),('Initial + Compliance events',comparable)]:
        for borough,g in frame.groupby('borough',sort=True):
            policies.append(dict(policy=label,borough=borough,positive=int(g.positive.sum()),denominator=len(g),fraction=float(g.positive.mean())))
    policies=pd.DataFrame(policies)
    summary=policies[policies.policy.eq('All Initial events')][['borough','positive','denominator','fraction']].rename(columns={'positive':'initial_positive','denominator':'initial_events','fraction':'initial_fraction'})
    p=policies[policies.policy.eq('First Initial per property')][['borough','positive','denominator','fraction']].rename(columns={'positive':'first_positive','denominator':'first_properties','fraction':'first_fraction'})
    summary=summary.merge(p,on='borough',validate='one_to_one').sort_values('borough')
    # Ties get the same rank; do not invent an ID tie-break ranking.
    summary['rank_positive_count']=summary.initial_positive.rank(method='min',ascending=False).astype(int)
    summary['rank_first_property_fraction']=summary.first_fraction.rank(method='min',ascending=False).astype(int)
    monthly=initial.groupby(['borough','month']).positive.agg(positive='sum',denominator='size').reset_index()
    monthly['positive']=monthly.positive.astype(int);monthly['fraction']=monthly.positive/monthly.denominator
    require(len(monthly)==60,'Missing borough/month cell; do not interpolate surveillance coverage')
    season=initial[initial.season.ne('Other')].groupby(['borough','season']).positive.agg(positive='sum',denominator='size').reset_index()
    season['positive']=season.positive.astype(int);season['fraction']=season.positive/season.denominator
    selected=first_property_events(valid[valid.season.ne('Other')],by_season=True)
    paired=selected.pivot(index='bbl',columns='season',values='positive').dropna(subset=['Winter','Summer'])
    paired=paired.astype(int);paired_result=paired_statistics(paired)
    more_resamples=paired_statistics(paired,repetitions=2000)
    early_keys=selected.loc[selected.season.eq('Winter')&selected.month.ne(12),'bbl']
    paired_without_december=paired_statistics(paired.loc[paired.index.isin(early_keys)])
    cross=pd.crosstab(paired.Winter,paired.Summer).reindex(index=[0,1],columns=[0,1],fill_value=0)
    crossed=pd.DataFrame([dict(winter=w,summer=s,properties=int(cross.loc[w,s])) for w in [0,1] for s in [0,1]])
    weights=[]
    for label in ['Winter','Summer']:
        g=season[season.season.eq(label)]
        weights.append(dict(policy='Observed event mix',season=label,fraction=float(g.positive.sum()/g.denominator.sum()),events=int(g.denominator.sum())))
        weights.append(dict(policy='Equal borough weights',season=label,fraction=float(g.fraction.mean()),events=int(g.denominator.sum())))
    weights=pd.DataFrame(weights)
    pooled=weights[weights.policy.eq('Observed event mix')].set_index('season')
    contrasts=[dict(policy='Iniciales',difference=float(pooled.loc['Summer','fraction']-pooled.loc['Winter','fraction']),
        lower=np.nan,upper=np.nan,unit='events',denominator_winter=int(pooled.loc['Winter','events']),denominator_summer=int(pooled.loc['Summer','events']),repetitions=0)]
    for label,result in [('Pareados 500',paired_result),('Pareados 2000',more_resamples),('Sin diciembre',paired_without_december)]:
        contrasts.append(dict(policy=label,difference=result['difference'],lower=result['bootstrap_percentile95'][0],upper=result['bootstrap_percentile95'][1],
            unit='paired properties',denominator_winter=result['properties'],denominator_summer=result['properties'],repetitions=result['repetitions']))
    borough_contrasts=season.pivot(index='borough',columns='season',values='fraction')
    type_counts=unique.groupby('inspection_type').size().rename('events').reset_index()
    require(int(monthly.denominator.sum())==len(initial) and int(crossed.properties.sum())==len(paired),'Aggregate reconciliation failed')
    source=dict(rows=len(d),deduplicated_events=len(unique),initial_events=len(initial),property_eligible_events=len(valid),
        first_properties=len(first),property_excluded_initial_events=len(initial)-len(valid),
        initial_positive=int(initial.positive.sum()),first_property_positive=int(first.positive.sum()))
    claims={
        'D04-B':dict(**source,geographic_scope='Boroughs only, not neighborhoods; operational narrowing of catalogue question.',
            by_borough=summary[['borough','first_positive','first_properties','first_fraction']].to_dict('records'),
            interpretation='Positivity among first observed Initial inspections of key-consistent properties in 2024; not prevalence in all properties.'),
        'D04-C':dict(**source,months=12,borough_month_cells=60,monthly_total=monthly.groupby('month')[['positive','denominator']].sum().reset_index().to_dict('records'),
            interpretation='One observed calendar year. Temporal/geographic surveillance pattern, not recurring seasonality or rat population.'),
        'D04-D1':dict(**source,year=2024,winter_months=[1,2,12],summer_months=[6,7,8],
            borough_differences={str(k):float(v) for k,v in (borough_contrasts.Summer-borough_contrasts.Winter).items()},
            weighting_sensitivity=weights.to_dict('records'),paired=paired_result,
            paired_bootstrap2000=more_resamples,paired_winter_jan_feb_only=paired_without_december,
            paired_cross=crossed.to_dict('records'),paired_first_winter_december=int(selected[selected.season.eq('Winter')&selected.bbl.isin(paired.index)].month.eq(12).sum()),
            interpretation='Descriptive seasonal contrast in 2024, not causal heat effect. Jan/Feb/Dec winter is not a chronological transition; paired cohort is selected.'),
        'D04-E':dict(**source,rank_count_vs_property_fraction_spearman=float(spearmanr(summary.initial_positive,summary.first_fraction).statistic),
            rankings=summary.to_dict('records'),policies=policies.to_dict('records'),
            interpretation='Counts, event rates and first-property rates answer different surveillance questions. No claim about total rats or uninspected locations.')}
    return dict(type_counts=type_counts,policy_rates=policies,borough_summary=summary,monthly=monthly,season_rates=season,
        season_weights=weights,paired_cross=crossed,paired_summary=pd.DataFrame([paired_result]),paired_sensitivity=pd.DataFrame(contrasts)),claims


def draw(name,ax,t,c,mobile):
    s=c['D04-B']
    if name=='inspection-scope':
        z=t['type_counts'].sort_values('events').copy();labels={'Initial':'Inicial','Compliance':'Seguimiento','Treatments':'Tratamientos','Stoppage':'Sellado','Clean Ups':'Limpieza'}
        y=np.arange(len(z));ax.barh(y,z.events,color=[BLUE if x=='Initial' else '#bfcbd0' for x in z.inspection_type])
        ax.set_yticks(y,[labels[x] for x in z.inspection_type],fontsize=9);ax.set_xlabel('Eventos únicos recibidos')
        ax.set_xlim(right=float(z.events.max())*1.22)
        if mobile:ax.set_xticks([0,50000,100000,150000],['0','50 mil','100 mil','150 mil'])
        for i,r in enumerate(z.itertuples()):ax.text(r.events,i,f' {r.events:,}',va='center',fontsize=8)
        return ('Primero, distinguir qué se hizo',f'{s["deduplicated_events"]:,} eventos tras retirar copias exactas de {s["rows"]:,} filas. Azul: universo principal.',
            'Seguimiento, tratamiento, sellado y limpieza no son visitas iniciales intercambiables. La escala es lineal y conserva acciones pequeñas.',
            'Barras de conteos por tipo de intervención muestran por qué el análisis principal se limita a inspecciones iniciales.')
    if name=='borough-positivity':
        policies=t['policy_rates'];y=np.arange(5)
        for label,color,marker,offset in [('All Initial events',GOLD,'x',-.12),('Key-consistent Initial events',BLUE,'o',0),('First Initial per property',RED,'s',.12)]:
            z=policies[policies.policy.eq(label)].set_index('borough').reindex(BOROUGHS)
            ax.scatter(100*z.fraction,y+offset,color=color,marker=marker,label={'All Initial events':'Eventos iniciales','Key-consistent Initial events':'Eventos con llave coherente','First Initial per property':'Primera visita por predio'}[label],s=35)
        z=t['borough_summary'].set_index('borough').reindex(BOROUGHS)
        ax.set_yticks(y,[f'{b}\n{int(z.loc[b,"first_positive"])}/{int(z.loc[b,"first_properties"])} predios' for b in BOROUGHS],fontsize=7 if mobile else 9)
        ax.set(xlim=(0,100),xlabel='Con señales de ratas (%)');ax.legend(loc='upper center',bbox_to_anchor=(.5,-.27),fontsize=7.5,frameon=False,ncol=1 if mobile else 3)
        return ('El mismo nombre, tres denominadores',f'Iniciales: {s["initial_events"]:,} eventos; política por predio: {s["first_properties"]:,} llaves coherentes, primera visita observada.',
            'La política intermedia separa el filtro de llaves de la deduplicación por predio. No se estima prevalencia fuera de lo inspeccionado.',
            'Puntos por borough comparan positividad de eventos iniciales, eventos con llave coherente y primeras visitas por predio; etiquetas muestran numerador y denominador de predios.')
    if name=='month-heatmap':
        z=t['monthly'].pivot(index='borough',columns='month',values='fraction').reindex(BOROUGHS)
        upper=float(np.ceil(z.to_numpy(dtype=float).max()*10)*10)
        image=ax.imshow(100*z.to_numpy(dtype=float),vmin=0,vmax=upper,cmap='cividis',aspect='auto')
        ax.set_yticks(range(5),[b.replace('Staten Island','Staten\nIsland') for b in BOROUGHS],fontsize=8)
        ax.set_xticks(range(12),list('EFMAMJJASOND'),fontsize=8);ax.set_xlabel('Mes de inspección, 2024')
        ax.figure.colorbar(image,ax=ax,orientation='horizontal',fraction=.08,pad=.30,label='Positividad (%)')
        return ('Un año de vigilancia, mes a mes',f'60 celdas borough/mes; cada tasa usa positivos / inspecciones iniciales del mismo borough/mes. Total {s["initial_events"]:,}.',
            f'Escala común 0–{upper:g}%; cada celda conserva su denominador en CSV. Un solo año no demuestra un ciclo recurrente ni abundancia de animales.',
            'Heatmap de positividad de inspecciones iniciales para cinco boroughs y doce meses con escala lineal común declarada y denominadores en tabla.')
    if name=='season-comparison':
        z=t['season_rates'].pivot(index='borough',columns='season',values='fraction').reindex(BOROUGHS);y=np.arange(5)
        diff=100*(z.Summer-z.Winter)
        ax.scatter(diff,y,color=BLUE,s=40)
        for i,value in enumerate(diff):ax.annotate(f'{value:.2f}',(value,i),xytext=(7,7),textcoords='offset points',fontsize=9)
        ax.set_yticks(y,[b.replace('Staten Island','Staten\nIsland') for b in BOROUGHS],fontsize=8);ax.set(xlim=(0,100),xlabel='Positividad inicial (%)')
        ax.set(xlim=(-10,10),xlabel='Verano menos invierno (puntos porcentuales)');ax.axvline(0,color=GOLD,linestyle='--',linewidth=1)
        return ('La diferencia dentro de cada distrito',f'Visitas iniciales de 2024. Verano: jun/jul/ago; invierno: ene/feb/dic. Diferencia de tasas, no conteo de animales.',
            'Cada estación conserva su denominador. Invierno no es una secuencia cronológica única; se contrasta composición y cohorte pareada en tablas.',
            'Diagrama de diferencias verano menos invierno dentro de cada borough en puntos porcentuales; línea de referencia en cero y sin interpretación causal.')
    if name=='paired-seasons':
        z=t['paired_sensitivity'];labels=[]
        for i,r in enumerate(z.itertuples()):
            if r.repetitions:
                ax.errorbar([100*r.difference],[i],xerr=[[100*(r.difference-r.lower)],[100*(r.upper-r.difference)]],fmt='o',color=BLUE,capsize=4)
                labels.append(f'{r.policy}\nn={r.denominator_winter:,}')
            else:
                ax.scatter([100*r.difference],[i],color=GOLD,marker='x',s=50)
                labels.append(f'Iniciales\n{r.denominator_winter:,}/{r.denominator_summer:,}')
        ax.set(yticks=range(len(z)),yticklabels=labels,xlim=(-8,3),xlabel='Verano menos invierno (pp)')
        ax.tick_params(axis='y',labelsize=7 if mobile else 9);ax.axvline(0,color='#777777',linestyle='--',linewidth=1)
        return ('Comparar los mismos predios cambia la pregunta',f'Iniciales: visitas invierno/verano. Pareados: primera visita por estación en {c["D04-D1"]["paired"]["properties"]:,} predios; sin diciembre cambia la cohorte.',
            'Intervalos bootstrap 95% condicionales, supuesto IID. 500/2000 usan la misma cohorte; sin diciembre usa enero/febrero. Iniciales: sólo punto descriptivo, sin intervalo. No causalidad.',
            'Gráfico de diferencias e intervalos compara eventos iniciales con los mismos predios, 500 y 2000 remuestreos, y una cohorte sin diciembre; denominadores y línea cero visibles.')
    if name=='ranking-denominator':
        z=t['borough_summary'].set_index('borough').reindex(BOROUGHS);y=np.arange(5)
        ax.scatter(z.rank_positive_count,y,color=GOLD,marker='x',s=45,label='Conteo de iniciales positivas')
        ax.scatter(z.rank_first_property_fraction,y,color=RED,marker='s',s=35,label='Tasa de primeros predios')
        ax.set_yticks(y,[b.replace('Staten Island','Staten\nIsland') for b in BOROUGHS],fontsize=8)
        ax.set(xlim=(.5,5.5),xticks=range(1,6),xlabel='Posición (1 = mayor valor)')
        ax.legend(loc='upper center',bbox_to_anchor=(.5,-.22),fontsize=8,frameon=False,ncol=1 if mobile else 2)
        return ('Un ranking depende de lo que cuentas',f'Cinco boroughs; conteo de positivos sobre {s["initial_events"]:,} eventos frente a fracción en {s["first_properties"]:,} primeros predios.',
            'Las métricas y universos cambian explícitamente; la tabla conserva números y políticas intermedias. Ranking de vigilancia, no población de ratas.',
            'Comparación de posiciones por conteo de inspecciones iniciales positivas y por tasa de positividad de la primera inspección por predio.')
    if name=='monthly-volume':
        z=t['monthly'].groupby('month')[['positive','denominator']].sum()
        ax.plot(z.index,z.denominator,color=BLUE,marker='o',label='Iniciales únicas');ax.plot(z.index,z.positive,color=RED,marker='o',label='Iniciales positivas')
        ax.set(xlim=(.5,12.5),ylim=(0,None),xticks=range(1,13),xlabel='Mes de 2024',ylabel='Inspecciones (conteo)')
        ax.legend(loc='upper center',bbox_to_anchor=(.5,-.22),fontsize=8,frameon=False,ncol=1 if mobile else 2)
        return ('Más hallazgos también pueden ser más visitas',f'Cada punto suma los cinco boroughs. Total anual: {s["initial_positive"]:,} positivas / {s["initial_events"]:,} iniciales únicas.',
            'Se muestran conteos con el mismo eje; las tasas por mes están en el heatmap y CSV. No se imputa actividad entre meses ni se ajusta por clima.',
            'Dos líneas con una sola escala comparan volumen mensual de inspecciones iniciales y positivas, conservando el denominador visible.')
    raise ValueError('Unregistered figure: '+name)
