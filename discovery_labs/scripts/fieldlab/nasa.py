"""Default PS parameter sets: selection bias, descriptive radius audit and exploratory clusters."""
import textwrap
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score, silhouette_score
from sklearn.preprocessing import StandardScaler, RobustScaler

from .common import load as read_source, profile, BLUE, RED, GOLD, COLORS
from v3.data import require

CASE='nasa-exoplanetas'
PREFIX='D05'
SEED=1729
TITLE='Los mundos que nuestros instrumentos dejan ver'
HOOK='Imagina un museo de mundos lejanos: caben gigantes, planetas pequeños y órbitas extremas. Pero la colección no llegó al museo al azar. Un instrumento ve sombras y otro mide el movimiento de una estrella. Antes de agrupar planetas o buscar una Tierra, decidamos qué cuenta como semejanza y qué parte del catálogo pudo seleccionar el instrumento. Tu primera apuesta puede cambiar cuando veamos lo que falta.'
SPECS=[('coverage',['D05-C','D05-E'],'coverage'),('period-radius',['D05-C','D05-E'],'clustered'),
       ('cluster-method',['D05-E'],'method_mix'),('cluster-sensitivity',['D05-C','D05-E'],'cluster_sensitivity'),
       ('earth-radius',['D05-D1'],'radius_share'),('radius-uncertainty',['D05-D1'],'radius_audit'),
       ('discovery-timeline',['D05-C'],'annual')]
STORIES={
 'D05-C':('El museo de los mundos posibles','¿Agruparías por tamaño, tiempo de órbita o temperatura?',
     'La temperatura modelada falta en gran parte del archivo; los grupos describen sólo casos completos.',
     'Compara tres grupos con dos/cuatro, otro escalado y los mismos planetas sin temperatura.',
     '¿Cómo afectaría una cámara que sólo detectara objetos brillantes a un catálogo de animales?'),
 'D05-D1':('Una Tierra, ¿según qué regla?','¿Un radio parecido basta para llamarlo una Tierra?',
     'Radio puntual, límite y error asimétrico son tres cosas distintas; tampoco hay radio para todos.',
     'Cambia el rango de radios y el denominador; revisa los intervalos publicados cerca del umbral.',
     '¿Qué ocurre al llamar saludable a una persona usando una sola medida?'),
 'D05-E':('¿Familias naturales o huellas del telescopio?','¿Esperas que los grupos coincidan con el método que encontró cada planeta?',
     'La asociación con el método no identifica su efecto causal; faltan las poblaciones que se buscaron sin detección.',
     'Contrasta asociación con etiquetas de método barajadas y cambia representación en los mismos casos completos.',
     '¿Una app de fotos aprendería especies o diferencias entre cámaras?')}


def load(): return read_source(CASE)


def prepare(raw,manifest):
    d=raw.copy();checks=[];transforms=[]
    def check(rule,ok,detail):
        require(bool(ok),rule+': '+detail);checks.append(dict(rule=rule,passed=True,detail=detail))
    strings={'pl_name','hostname','discoverymethod','disc_facility','pl_bmassprov','pl_refname','st_refname','sy_refname','rowupdate'}
    for c in d:
        if c not in strings:d[c]=pd.to_numeric(d[c].replace('',np.nan),errors='raise')
    check('unique_planet',d.pl_name.ne('').all() and not d.pl_name.duplicated().any(),'PS default_flag=1 must have exactly one row per planet.')
    check('default_parameter_set',d.default_flag.eq(1).all(),'No mixing reference rows or composite columns.')
    check('discovery_year',d.disc_year.between(1900,2025).all(),'Discovery years <=2025; measurements are at acquisition date, not a historical 2025 snapshot.')
    check('required_metadata',d.hostname.ne('').all() and d.discoverymethod.ne('').all() and d.pl_refname.ne('').all(),'Host, discovery method and parameter publication retained.')
    check('controversy_flag',d.pl_controv_flag.isin([0,1]).all(),'Preserve controversial status.')
    for c in ['pl_rade','pl_orbper','pl_eqt','pl_bmasse']:
        check(c+'_finite_positive',np.isfinite(d[c].dropna()).all() and d[c].dropna().gt(0).all(),'Positive values only; unexpected values stop rather than silently vanish.')
        check(c+'_limit_domain',d[c+'lim'].dropna().isin([-1,0,1]).all(),'0 measurement; +/-1 limits. Missing flag is not a measurement.')
        d[c+'_measured']=d[c].notna() & d[c+'lim'].eq(0)
        d[c+'_errors_usable']=d[c+'_measured'] & d[c+'err1'].ge(0) & d[c+'err2'].le(0) & (d[c]+d[c+'err2']).gt(0)
        transforms.append(dict(step=c+'_measurement_policy',affected_rows=int((~d[c+'_measured']).sum()),
            action='Retain all rows in Silver; exclude missing/limit/unknown flag only from analyses needing that measurement.',
            statistical_consequence='Complete cases depend on detection method; no imputation or completeness correction.'))
    d['cluster_eligible']=d[['pl_rade_measured','pl_orbper_measured','pl_eqt_measured']].all(axis=1)
    d['radius_central_in_range']=d.pl_rade_measured & d.pl_rade.between(.8,1.25)
    for c in ['pl_rade','pl_orbper','pl_eqt']:d['log10_'+c]=np.log10(d[c].where(d[c+'_measured']))
    check('record_conservation',len(d)==len(raw),'Every original row remains in Silver.')
    units={'pl_rade':'Earth radii','pl_orbper':'days','pl_eqt':'kelvin; modeled equilibrium temperature, not surface temperature','pl_bmasse':'Earth masses; provenance retained','sy_dist':'parsec','disc_year':'year'}
    p=profile(raw,d,manifest,['pl_name'],units)
    p['temporal']=dict(discovery_year_min=int(d.disc_year.min()),discovery_year_max=int(d.disc_year.max()),
        rowupdate_min=str(d.rowupdate.min()),rowupdate_max=str(d.rowupdate.max()),frequency='Irregular discoveries, updates at acquisition; no forecasting.')
    p['coverage']=dict(radius_measured=int(d.pl_rade_measured.sum()),cluster_complete=int(d.cluster_eligible.sum()),
        mass_provenance_counts={str(k):int(v) for k,v in d.pl_bmassprov.value_counts().items()})
    p['target_and_leakage']='Unsupervised/descriptive only. No training target, no forecast, no prevalence of undiscovered planets. Temperature is model-derived and can correlate mechanically with orbit.'
    return d,p,transforms,checks


def fit_groups(frame,k=3,scaler='standard',columns=None):
    columns=columns or ['log10_pl_rade','log10_pl_orbper','log10_pl_eqt']
    x=frame[columns].to_numpy()
    require(len(x)>k and np.isfinite(x).all(),'Insufficient or non-finite cluster features')
    z=(StandardScaler() if scaler=='standard' else RobustScaler()).fit_transform(x)
    model=KMeans(n_clusters=k,n_init=20,random_state=SEED).fit(z)
    # Label order is a display convention, not a physical rank.
    order=sorted(range(k),key=lambda label:float(frame.loc[model.labels_==label,'log10_pl_rade'].mean()))
    labels=np.array([{old:new for new,old in enumerate(order)}[label] for label in model.labels_])
    score=float(silhouette_score(z,labels,sample_size=min(800,len(x)),random_state=SEED))
    return labels,score


def analyze(d):
    total=len(d); eligible=d[d.cluster_eligible].copy().reset_index(drop=True)
    labels,score=fit_groups(eligible);eligible['cluster']=labels
    coverage=[]
    for method,g in d.groupby('discoverymethod',sort=True):
        coverage.append(dict(method=method,total=len(g),radius_measured=int(g.pl_rade_measured.sum()),
            period_measured=int(g.pl_orbper_measured.sum()),temperature_measured=int(g.pl_eqt_measured.sum()),complete=int(g.cluster_eligible.sum())))
    coverage=pd.DataFrame(coverage)
    sensitivity=[]
    for k,scale,columns,label in [(2,'standard',None,'k=2'),(3,'standard',None,'k=3 base'),(4,'standard',None,'k=4'),
        (3,'robust',None,'Escala robusta'),(3,'standard',['log10_pl_rade','log10_pl_orbper'],'Sin temperatura')]:
        alt,sil=fit_groups(eligible,k,scale,columns)
        sensitivity.append(dict(policy=label,k=k,scaler=scale,features=','.join(columns or ['log10_pl_rade','log10_pl_orbper','log10_pl_eqt']),
            rows=len(eligible),ARI_vs_base=float(adjusted_rand_score(labels,alt)),silhouette=sil))
    mix=pd.crosstab(eligible.cluster,eligible.discoverymethod).stack().rename('planets').reset_index().rename(columns={'discoverymethod':'method'})
    rng=np.random.default_rng(SEED);methods=eligible.discoverymethod.to_numpy()
    observed=float(normalized_mutual_info_score(methods,labels))
    null=pd.DataFrame({'repetition':range(50),'NMI':[float(normalized_mutual_info_score(rng.permutation(methods),labels)) for _ in range(50)]})
    radius=[]
    for method,g in [('Todos',d),*list(d.groupby('discoverymethod',sort=True))]:
        measured=g[g.pl_rade_measured]
        for lo,hi in [(.9,1.1),(.8,1.25),(.75,1.5)]:
            n=int(measured.pl_rade.between(lo,hi).sum());unknown=len(g)-len(measured)
            radius.append(dict(method=method,lower_radius=lo,upper_radius=hi,in_range=n,measured=len(measured),total=len(g),unknown=unknown,
                measured_fraction=n/len(measured) if len(measured) else 0,
                all_rows_lower=n/len(g),all_rows_upper=(n+unknown)/len(g),
                has_measured_denominator=bool(len(measured))))
    radius=pd.DataFrame(radius);main=radius[(radius.method=='Todos')&radius.lower_radius.eq(.8)].iloc[0]
    errors=d[d.pl_rade_errors_usable].copy()
    errors['lower_radius']=errors.pl_rade+errors.pl_radeerr2;errors['upper_radius']=errors.pl_rade+errors.pl_radeerr1
    errors['definitely_in_range']=errors.lower_radius.ge(.8)&errors.upper_radius.le(1.25)
    errors['overlaps_range']=errors.lower_radius.le(1.25)&errors.upper_radius.ge(.8)
    # A reproducible illustrative sample, explicitly not a representative sample.
    errors['distance_to_one']=(errors.pl_rade-1).abs()
    audit=errors.sort_values(['distance_to_one','pl_name']).head(12)[['pl_name','pl_rade','lower_radius','upper_radius','definitely_in_range','overlaps_range','pl_refname']]
    annual=d.groupby(['disc_year','discoverymethod']).size().rename('planets').reset_index().rename(columns={'discoverymethod':'method'})
    claims={
        'D05-C':dict(rows=total,complete_cases=len(eligible),excluded_from_clustering=total-len(eligible),
            k=3,seed=SEED,silhouette_sample800=score,cluster_counts={str(k):int(v) for k,v in eligible.cluster.value_counts().sort_index().items()},
            feature_columns=['log10_pl_rade','log10_pl_orbper','log10_pl_eqt'],
            sensitivity=sensitivity,interpretation='Exploratory groups of observed complete cases, not proven physical families. No external validity or occurrence rate.'),
        'D05-D1':dict(in_range=int(main.in_range),measured_denominator=int(main.measured),fraction=float(main.measured_fraction),
            more_than_half=bool(main.measured_fraction>.5),total=total,unmeasured_or_limits=int(main.unknown),
            missing_value_bounds_all_rows=[float(main.all_rows_lower),float(main.all_rows_upper)],
            radius_interval=[.8,1.25],with_usable_asymmetric_errors=len(errors),
            published_intervals_wholly_in_range=int(errors.definitely_in_range.sum()),published_intervals_overlapping_range=int(errors.overlaps_range.sum()),
            interpretation='Descriptive archive fraction, no sampling confidence or habitability inference. Error columns are as published, not a common calibrated probability interval.'),
        'D05-E':dict(complete_cases=len(eligible),NMI_cluster_discovery_method=observed,permutation_repetitions=50,
            shuffled_NMI_mean=float(null.NMI.mean()),shuffled_NMI_min=float(null.NMI.min()),shuffled_NMI_max=float(null.NMI.max()),
            seed=SEED,interpretation='Association and sensitivity audit, not causal explanation or detection-completeness correction. Shuffling preserves labels/counts and is exploratory, not a confirmatory p-value.')}
    require(int(coverage.total.sum())==total and int(mix.planets.sum())==len(eligible),'Aggregate reconciliation failed')
    return dict(coverage=coverage,clustered=eligible,cluster_sensitivity=pd.DataFrame(sensitivity),method_mix=mix,
        shuffled_method=null,radius_share=radius,radius_audit=audit,annual=annual),claims


def draw(name,ax,t,c,mobile):
    if name=='coverage':
        z=t['coverage'].sort_values(['total','method'],ascending=[False,True]).head(5).iloc[::-1];y=np.arange(len(z))
        ax.barh(y,z.total,color='#c9d2d6',label='Catálogo seleccionado');ax.barh(y,z.complete,color=BLUE,label='Tres medidas utilizables')
        names=z.method.str.replace('Radial Velocity','Velocidad radial').str.replace('Transit Timing Variations','Tiempos de tránsito')
        ax.set_yticks(y,[textwrap.fill(x,12 if mobile else 25) for x in names],fontsize=8 if mobile else 10)
        ax.set_xlabel('Planetas (conteo)');ax.legend(loc='upper center',bbox_to_anchor=(.5,-.20),fontsize=8,frameon=False)
        return ('Lo que falta también selecciona',f'{c["D05-C"]["rows"]:,} planetas; cinco métodos de descubrimiento con más registros. Barras sobre el mismo universo.',
            'Casos completos exigen radio, periodo y temperatura positivos con lim=0. No se rellenan faltantes.',
            'Barras por método comparan todos los planetas del catálogo seleccionado con los que tienen las tres variables utilizables.')
    if name=='period-radius':
        z=t['clustered']
        for k,g in z.groupby('cluster'):ax.scatter(g.pl_orbper,g.pl_rade,s=9,alpha=.4,color=COLORS[k],label=f'G{k+1}: n={len(g)}',edgecolor='none')
        ax.set(xscale='log',yscale='log',xlabel='Periodo orbital (días, log)',ylabel='Radio (radios terrestres, log)')
        ax.legend(fontsize=8,loc='upper center',bbox_to_anchor=(.5,-.22),ncol=1 if mobile else 3,frameon=False)
        return ('Un mapa de semejanzas observadas',f'{len(z):,} casos completos. K-means k=3 sobre log10 de radio, periodo y temperatura, estandarizados.',
            'Sólo se proyectan dos de tres variables. Temperatura de equilibrio modelada; grupos exploratorios sin validación física externa.',
            'Dispersión logarítmica de radio y periodo, coloreada por tres grupos exploratorios y con conteos; no dibuja planetas a escala.')
    if name=='cluster-method':
        mix=t['method_mix'];methods=t['coverage'].sort_values(['total','method'],ascending=[False,True]).method.head(3).tolist()
        wide=mix.assign(method=mix.method.where(mix.method.isin(methods),'Otros')).groupby(['cluster','method']).planets.sum().unstack(fill_value=0)
        denom=wide.sum(axis=1);bottom=np.zeros(len(wide))
        for i,method in enumerate(methods+['Otros']):
            values=100*wide.get(method,pd.Series(0,index=wide.index))/denom
            ax.bar(np.arange(len(wide)),values,bottom=bottom,color=COLORS[i],label=method.replace('Radial Velocity','Vel. radial'));bottom+=values
        ax.set(ylim=(0,100),xticks=range(len(wide)),xticklabels=[f'G{k+1}\nn={int(denom.loc[k])}' for k in wide.index],ylabel='Método dentro de cada grupo (%)')
        ax.legend(loc='upper center',bbox_to_anchor=(.5,-.25),fontsize=8,ncol=1 if mobile else 4,frameon=False)
        return ('La huella del método de descubrimiento',f'Mismos {int(denom.sum()):,} casos completos. Cada barra suma 100%; grupos ordenados por radio medio logarítmico.',
            f'NMI observada {c["D05-E"]["NMI_cluster_discovery_method"]:.3f}; media de 50 barajados {c["D05-E"]["shuffled_NMI_mean"]:.3f}. Asociación, no efecto causal.',
            'Barras apiladas muestran la mezcla de métodos de descubrimiento dentro de cada grupo, con tamaño y denominador por barra.')
    if name=='cluster-sensitivity':
        z=t['cluster_sensitivity'];y=np.arange(len(z));ax.scatter(z.ARI_vs_base,y,color=BLUE,s=40)
        ax.set_yticks(y,[x.replace('Escala robusta','Escala\nrobusta').replace('Sin temperatura','Sin\ntemperatura') for x in z.policy],fontsize=9)
        ax.set(xlim=(-.05,1.08),xlabel='ARI frente a tres grupos base');ax.axvline(1,color='#999999',linewidth=.5)
        return ('¿Cuánto depende de nuestra regla?',f'Los mismos {c["D05-C"]["complete_cases"]:,} planetas en cada política; cambia k, escala o uso de temperatura.',
            'ARI mide acuerdo de asignaciones, no verdad física. Silhouette y parámetros completos están en la tabla; no se elige k después de ver una historia.',
            'Diagrama de puntos compara el acuerdo de grupos bajo cinco decisiones de modelado manteniendo fijo el conjunto de planetas.')
    if name=='earth-radius':
        z=t['radius_share'].query("method=='Todos'");y=np.arange(len(z))
        ax.hlines(y,100*z.all_rows_lower,100*z.all_rows_upper,color='#b5c2c8',linewidth=6,label='Cotas por radio no medido')
        ax.scatter(100*z.measured_fraction,y,color=RED,label='Sólo radio medido',zorder=3)
        ax.set_yticks(y,[f'{r.lower_radius:g}–{r.upper_radius:g}\n{r.in_range}/{r.measured}' for r in z.itertuples()],fontsize=9)
        ax.set(xlim=(0,100),xlabel='Dentro del rango de radio (%)');ax.axvline(50,color=GOLD,linestyle='--',linewidth=1)
        ax.legend(loc='upper center',bbox_to_anchor=(.5,-.24),fontsize=8,frameon=False)
        return ('Parecido en radio, según el umbral',f'Puntos: {c["D05-D1"]["measured_denominator"]:,} radios medidos. Cotas: {c["D05-D1"]["total"]:,} filas, asignando todos los no medidos fuera/dentro.',
            'Cotas por datos no medidos, no intervalos de confianza. Radio similar no implica agua, atmósfera ni habitabilidad. Línea: 50%.',
            'Tres definiciones de radio parecido muestran fracciones entre los medidos y cotas al cambiar el denominador al catálogo completo.')
    if name=='radius-uncertainty':
        z=t['radius_audit'].head(8 if mobile else 12).iloc[::-1];y=np.arange(len(z))
        ax.errorbar(z.pl_rade,y,xerr=[z.pl_rade-z.lower_radius,z.upper_radius-z.pl_rade],fmt='o',color=BLUE,capsize=3)
        ax.axvspan(.8,1.25,alpha=.10,color=GOLD);ax.set_yticks(y,z.pl_name,fontsize=7 if mobile else 9)
        ax.set_xlabel('Radio y errores publicados (R Tierra)')
        return ('Cerca del umbral, mira los errores',f'{len(z)} planetas más próximos a 1 R Tierra con errores utilizables; selección ilustrativa, no muestra aleatoria.',
            'Errores asimétricos conservados de cada referencia, sin asumir mismo nivel de confianza. Sombreado: rango 0.8–1.25.',
            'Intervalos asimétricos de radios publicados para una selección explícita de planetas cerca del radio terrestre; umbrales sombreados.')
    if name=='discovery-timeline':
        z=t['annual'];methods=t['coverage'].sort_values(['total','method'],ascending=[False,True]).method.head(3).tolist()
        for i,method in enumerate(methods):
            g=z[z.method.eq(method)].set_index('disc_year').planets.reindex(range(int(z.disc_year.min()),2026),fill_value=0)
            ax.plot(g.index,g.values,color=COLORS[i],label=method.replace('Radial Velocity','Vel. radial'),linewidth=1.5)
        ax.set(xlabel='Año de descubrimiento',ylabel='Planetas del catálogo por año',ylim=(0,None))
        ax.legend(loc='upper center',bbox_to_anchor=(.5,-.24),fontsize=8,frameon=False,ncol=1 if mobile else 3)
        return ('La colección cambió con el tiempo',f'Tres métodos más numerosos. Años hasta 2025 en el catálogo recibido; año de descubrimiento, no recuento de anuncios diarios.',
            'Las mediciones por defecto pueden haberse actualizado después del descubrimiento. Saltos de catálogo no son frecuencia de formación de planetas.',
            'Líneas de conteos anuales por tres métodos de descubrimiento, mostrando cambios en la composición temporal del archivo seleccionado.')
    raise ValueError('Unregistered figure: '+name)
