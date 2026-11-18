"""Airport maps and network diagnostics from exported Gold tables, with two honest display sizes."""
import textwrap

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.text import Text
import networkx as nx
import numpy as np
import pandas as pd

from v3.data import sha, write, require

BLUE, RED, GOLD = '#24546a', '#b84331', '#885f1d'
PALETTE = ['#24546a','#b84331','#6b7428','#79609a','#087f8c','#a26220','#614939','#28664a']
SPECS = [
    ('route-atlas',['D16-C'],'nodes'),
    ('community-network',['D16-C'],'community_flows'),
    ('community-sensitivity',['D16-C'],'community_stability'),
    ('community-null',['D16-C'],'null_modularity'),
    ('country-fragility',['D16-B'],'country_resilience'),
    ('degree-betweenness',['D16-D1'],'nodes'),
    ('ranking-sensitivity',['D16-D1','D16-E'],'nodes'),
    ('nearby-connections',['D16-D2'],'nearby_pairs'),
    ('metadata-sensitivity',['D16-D2','D16-E'],'metadata_sensitivity'),
    ('hub-removal',['D16-E','D16-B'],'hub_removal')]


def draw(name,ax,tables,claims,mobile):
    nodes = tables['nodes']
    if name == 'route-atlas':
        coordinates = nodes.set_index('airport_id')[['longitude','latitude']]
        e = tables['edges'].copy()
        degree = nodes.set_index('airport_id').unique_neighbors
        e['display_priority'] = e.source_id.map(degree)*e.destination_id.map(degree)
        e = e.sort_values(['display_priority','source_id','destination_id'],ascending=[False,True,True]).head(100 if mobile else 250)
        segments = []
        for row in e.itertuples():
            a = coordinates.loc[row.source_id].to_numpy(); b = coordinates.loc[row.destination_id].to_numpy()
            if abs(a[0]-b[0])<=180: segments.append([a,b])
        ax.add_collection(LineCollection(segments,colors='#7d8b90',linewidths=.35,alpha=.22))
        colors = [PALETTE[i] if i<8 else '#777777' for i in nodes.community]
        ax.scatter(nodes.longitude,nodes.latitude,c=colors,s=5 if mobile else 8,alpha=.75,linewidths=0)
        for i,color in enumerate(PALETTE+['#777777']):ax.scatter([],[],color=color,s=20,label=f'G{i+1}' if i<8 else 'Otras')
        ax.set(xlim=(-180,180),ylim=(-65,85),xlabel='Longitud (°)',ylabel='Latitud (°)')
        ax.grid(alpha=.2,linewidth=.5)
        ax.legend(loc='upper center',bbox_to_anchor=(.5,-.20),ncol=3 if mobile else 9,fontsize=8,frameon=False,handletextpad=.3,columnspacing=.7)
        return ('Un atlas de conexiones históricas',f'{len(nodes):,} aeropuertos activos; color por comunidad. Líneas: hasta {len(e)} aristas seleccionadas, sin cruces de antimeridiano.',
                'Equirectangular sin mapa base externo. Líneas esquemáticas, no trayectorias de vuelo. Rutas anteriores a julio 2014; metadata no es un censo de 2014.',
                'Mapa de aeropuertos por longitud y latitud, coloreados por comunidades. Las líneas muestran una selección de conexiones de alto grado, no todo el tráfico.')
    if name == 'community-network':
        flow=tables['community_flows'].copy(); summary=tables['communities']
        flow['a']=flow.source_community.map(lambda x:int(x) if x<8 else 8)
        flow['b']=flow.destination_community.map(lambda x:int(x) if x<8 else 8)
        grouped=flow.groupby(['a','b']).directed_edges.sum().reset_index()
        graph=nx.DiGraph();graph.add_nodes_from(range(9))
        strongest=grouped[grouped.a.ne(grouped.b)].sort_values(['directed_edges','a','b'],ascending=[False,True,True]).head(20)
        graph.add_weighted_edges_from((r.a,r.b,r.directed_edges) for r in strongest.itertuples())
        positions=nx.circular_layout(graph)
        counts=[int(summary.loc[summary.community.eq(i),'airports'].sum()) if i<8 else int(summary.loc[summary.community.ge(8),'airports'].sum()) for i in range(9)]
        sizes=[1000+3000*n/len(nodes) for n in counts]
        nx.draw_networkx_nodes(graph,positions,node_size=sizes,node_color=PALETTE+['#777777'],ax=ax)
        widths=[.25+3*graph[u][v]['weight']/max(nx.get_edge_attributes(graph,'weight').values()) for u,v in graph.edges()]
        nx.draw_networkx_edges(graph,positions,ax=ax,width=widths,edge_color='#7d8b90',alpha=.6,arrows=True,arrowsize=8,
                               connectionstyle='arc3,rad=0.08',node_size=sizes)
        labels={i:f'{"G"+str(i+1) if i<8 else "Otras"}\n{n}' for i,n in enumerate(counts)}
        nx.draw_networkx_labels(graph,positions,labels,font_size=8 if mobile else 10,font_color='white',ax=ax)
        ax.margins(.20);ax.set_aspect('equal');ax.set_axis_off()
        return ('La red vista a otra escala',f'20 flujos dirigidos mayores entre 8 comunidades principales y otras; cifras en nodos = aeropuertos.',
                'Anchura = conexiones distintas entre grupos, no pasajeros. Dibujo omite flujos menores y lazos internos; tabla conserva todas las aristas.',
                'Diagrama de los veinte mayores flujos dirigidos entre comunidades de aeropuertos. Nodos coloreados y con conteos; flechas y ancho representan conexiones únicas entre grupos.')
    if name == 'community-sensitivity':
        t=tables['community_stability'];ax.plot(t.resolution,t.ARI_vs_resolution1,color=BLUE,marker='o')
        for r in t.itertuples():ax.annotate(f'{r.communities} grupos',(r.resolution,r.ARI_vs_resolution1),xytext=(0,10),textcoords='offset points',ha='center',fontsize=9)
        ax.set(ylim=(0,1.15),xlim=(.72,1.28),xticks=[.8,1,1.2],xlabel='Resolución Louvain',ylabel='ARI frente a resolución 1.0')
        return ('¿Qué sobrevive al cambiar resolución?',f'Los mismos {len(nodes):,} nodos y {claims["D16-C"]["undirected_edges"]:,} conexiones no dirigidas; semilla fija.',
                'ARI mide acuerdo de asignaciones. Resolución 1.0 es una referencia elegida; no una clasificación geográfica verdadera.',
                'Curva de estabilidad de comunidades para tres resoluciones, con número de grupos y escala de acuerdo de cero a uno.')
    if name == 'community-null':
        t=tables['null_modularity'];observed=claims['D16-C']['modularity']
        average=float(t.modularity.mean());low=float(t.modularity.min());high=float(t.modularity.max())
        ax.errorbar([0],[average],yerr=[[average-low],[high-average]],fmt='o',color=BLUE,capsize=7)
        ax.scatter([1],[observed],color=RED,s=60)
        ax.annotate(f'media {average:.4f}\nrango [{low:.4f}, {high:.4f}]',(0,average),xytext=(0,18),textcoords='offset points',ha='center',fontsize=9)
        ax.annotate(f'{observed:.3f}',(1,observed),xytext=(0,12),textcoords='offset points',ha='center',fontsize=10)
        ax.set(xlim=(-.55,1.55),ylim=(-.05,.78),xticks=[0,1],xticklabels=['Aleatorias\nn=20','Louvain'],ylabel='Modularidad')
        return ('Una referencia que conserva tamaños',f'20 particiones aleatorias con los mismos tamaños de comunidades sobre el mismo grafo de {len(nodes):,} aeropuertos.',
                'Membresías aleatorias, no redes de vuelos simuladas. Contraste exploratorio después de optimizar Louvain; no p-valor confirmatorio.',
                'Dos puntos comparan modularidad: la media y rango de veinte particiones aleatorias frente al valor de Louvain, con anotaciones numéricas.')
    if name == 'country-fragility':
        t=tables['country_resilience'].sort_values(['loss_fraction','country'],ascending=[False,True]).head(6 if mobile else 10).iloc[::-1]
        y=np.arange(len(t));ax.scatter(100*t.loss_fraction,y,color=RED,marker='x',s=65,label='Retirar hub local')
        ax.scatter(100*t.baseline_mean_other_disconnected/t.remaining_denominator,y,color=BLUE,s=35,label='Retiro local aleatorio (media)')
        names=[f'{r.country}\nn restante={r.remaining_denominator}' for r in t.itertuples()]
        ax.set_yticks(y,names,fontsize=9);ax.set(xlim=(-4,104),xlabel='Otros aeropuertos fuera del gigante (%)')
        ax.legend(fontsize=8,loc='upper center',bbox_to_anchor=(.5,-.30 if mobile else -.17),frameon=False)
        return ('La conectividad depende de dónde se corta',f'{len(t)} países con mayor pérdida; universo con ≥5 aeropuertos dentro del gigante inicial. El nodo retirado no se cuenta como perdido.',
                'Referencia: hasta 20 retiros locales sin reemplazo. Lista ordenada exploratoriamente; topología histórica, sin volumen de personas afectadas.',
                'Dotplot por país: pérdida de accesibilidad de otros aeropuertos tras retirar el hub local frente a la media de retiros locales aleatorios; denominadores visibles.')
    if name == 'degree-betweenness':
        ax.scatter(nodes.unique_neighbors,nodes.betweenness_128,s=10,alpha=.35,color=BLUE,edgecolor='none')
        ids=set(nodes.nsmallest(3,'rank_unique_neighbors').airport_id)|set(nodes.nsmallest(3,'rank_betweenness_128').airport_id)
        for i,r in enumerate(nodes[nodes.airport_id.isin(ids)].sort_values('betweenness_128',ascending=False).itertuples()):
            offset=(5,10) if i%2==0 else (5,-13)
            ax.annotate(r.iata if r.iata!=r'\N' else r.airport_id,(r.unique_neighbors,r.betweenness_128),xytext=offset,textcoords='offset points',fontsize=9,arrowprops=dict(arrowstyle='-',linewidth=.5,color='#555555'))
        ax.set(xscale='log',xlabel='Vecinos distintos (escala log)',ylabel='Intermediación dirigida (aprox.)');ax.set_ylim(bottom=0)
        return ('Muchos vecinos, otra clase de importancia',f'Los mismos {len(nodes):,} aeropuertos. Grado exacto; intermediación con 128 pivotes y semilla fija.',
                f'Spearman = {claims["D16-D1"]["spearman_degree_betweenness"]:.3f}. No existe una importancia única; k=64 se contrasta en la tabla de sensibilidad.',
                'Dispersión del grado de vecinos y centralidad de intermediación aproximada por aeropuerto; se anotan líderes de cada métrica.')
    if name == 'ranking-sensitivity':
        t=nodes.nsmallest(6 if mobile else 10,'rank_betweenness_128').iloc[::-1];y=np.arange(len(t))
        for col,label,color,marker in [('rank_betweenness_128','Dirigida k=128',BLUE,'o'),('rank_betweenness_64','Dirigida k=64',GOLD,'x'),('rank_betweenness_undirected','Sin dirección k=128',RED,'s')]:
            ax.scatter(t[col],y,color=color,marker=marker,label=label,s=40)
        ax.set_yticks(y,t.iata,fontsize=10);ax.set_xlabel('Posición ordinal (1 = primera)');ax.set_xlim(left=0)
        ax.legend(fontsize=8,loc='upper center',bbox_to_anchor=(.5,-.17),frameon=False)
        return ('El ranking puesto a prueba',f'{len(t)} líderes de intermediación dirigida k=128; las tres columnas usan el universo completo de {len(nodes):,} aeropuertos.',
                'Cambian pivotes o dirección, no el conjunto de aeropuertos. Rangos con desempate por ID; consultar también valores numéricos y empates.',
                'Comparación de posiciones de los principales aeropuertos en tres versiones de intermediación: dirigida con 128 o 64 pivotes y proyección no dirigida.')
    if name == 'nearby-connections':
        t=tables['nearby_pairs'];ax.plot(t.threshold_km,100*t.fraction,color=BLUE,marker='o',label='Pares a distancia ≤ umbral')
        for i,r in enumerate(t.itertuples()):ax.annotate(f'{r.connected_either_direction:,}/{r.unordered_pairs:,}',(r.threshold_km,100*r.fraction),xytext=(0,12),textcoords='offset points',ha='left' if i==0 else 'right' if i==2 else 'center',fontsize=9)
        ax.axhline(100*claims['D16-D2']['world_fraction'],color=GOLD,linestyle='--',label='Todos los pares activos')
        ax.set(ylim=(0,100),xlim=(75,550),xticks=[100,250,500],xlabel='Umbral de distancia geodésica (km)',ylabel='Pares con conexión observada (%)');ax.legend(fontsize=8,loc='upper right')
        return ('Cerca en el mapa, ¿cerca en la red?',f'Pares no ordenados de {len(nodes):,} aeropuertos activos. Conexión = arista en al menos una dirección; umbral principal 250 km.',
                'Sensibilidad 100/500 km; distancia Haversine, no separación en pantalla. Red histórica y sin horarios; ausencia de arista no prueba ausencia de servicio actual.',
                'Fracción de pares cercanos con conexión observada para tres umbrales, con numeradores y denominadores; referencia de todos los pares activos.')
    if name == 'hub-removal':
        t=tables['hub_removal'];outside=t.remaining_nodes-t.largest_component
        ax.plot(t.removed_nodes,outside,color=RED,marker='o');ax.set_ylim(bottom=0)
        for i,(x,y,total) in enumerate(zip(t.removed_nodes,outside,t.remaining_nodes)):
            ax.annotate(f'{y}/{total}',(x,y),xytext=(0,-22) if i==1 else (0,10),textcoords='offset points',ha='left' if i<2 else 'center',fontsize=9)
        ax.set(xticks=[0,1,5,10],xlabel='Hubs retirados (ranking original)',ylabel='Aeropuertos restantes fuera del gigante');ax.margins(y=.25)
        return ('Después del corte, contar lo que queda',f'Retiros de 0/1/5/10 nodos de mayor grado original. Cada etiqueta usa el número de nodos restantes como denominador.',
                'No se retira el nodo y se lo cuenta como desconectado. No se recalcula la lista de hubs durante el ataque; no es una predicción de reacciones de aerolíneas.',
                'Curva del número de aeropuertos restantes fuera del mayor componente conectado tras retirar nodos del ranking original, con denominadores por escenario.')
    if name == 'metadata-sensitivity':
        t=tables['metadata_sensitivity'];values=100*t.nearby250_connected/t.nearby250_denominator
        ax.scatter([0,1],values,color=[BLUE,RED],s=65)
        for i,r in enumerate(t.itertuples()):ax.annotate(f'{r.nearby250_connected:,}/{r.nearby250_denominator:,}',(i,values.iloc[i]),xytext=(0,12),textcoords='offset points',ha='center',fontsize=9)
        ax.set(xlim=(-.5,1.5),ylim=(0,100),xticks=[0,1],xticklabels=['ID resuelto','ID y códigos\ncoincidentes'],ylabel='Pares próximos conectados (%)')
        return ('¿Cuánto cambia exigir códigos coincidentes?',f'Mismos {len(nodes):,} nodos y {int(t.nearby250_denominator.iloc[0]):,} pares a ≤250 km; cambia sólo política de aristas.',
                'IATA y metadata histórica pueden discrepar. No se remapean IDs a partir de códigos; ambas políticas se conservan, sin afirmar que una sea verdad completa.',
                'Dos proporciones comparan conectividad de pares próximos bajo llaves ID resueltas y bajo coincidencia adicional de códigos, con denominador fijo.')
    raise ValueError('Unknown figure: '+name)


def export(tables,claims,manifest,out,code_hash):
    metadata=[]
    for name,questions,table in SPECS:
        variants=[]
        for mobile in [False,True]:
            plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11 if mobile else 12,'svg.hashsalt':'ADL-OpenFlights-V3'})
            fig,ax=plt.subplots(figsize=(4.5,8.3) if mobile else (11.5,7.8))
            title,denominator,note,alt=draw(name,ax,tables,claims,mobile)
            fig.suptitle(textwrap.fill(title,26 if mobile else 80),x=.05,y=.98,ha='left',fontweight='bold',fontsize=15 if mobile else 19)
            width=46 if mobile else 122
            fig.text(.05,.89,textwrap.fill(denominator,width),va='top',fontsize=10 if mobile else 11)
            footer=f'Fuente: OpenFlights / Airline Route Mapper / OurAirports · ODbL-1.0\n{note}\nSnapshot {manifest["snapshot_sha256"][:12]} · código {code_hash[:12]} · ADL V3'
            fig.text(.05,.02,'\n'.join(textwrap.fill(line,width) for line in footer.splitlines()),va='bottom',fontsize=8 if mobile else 9)
            left=.36 if mobile and name=='country-fragility' else .20 if name=='country-fragility' else .15
            fig.subplots_adjust(left=left,right=.94,top=.74,bottom=.38 if mobile else .28)
            if mobile:
                ax.set_xlabel(textwrap.fill(ax.get_xlabel(),30))
                ax.set_ylabel(textwrap.fill(ax.get_ylabel(),35))
            fig.canvas.draw();renderer=fig.canvas.get_renderer();undrawn=set()
            for axis in fig.axes:
                for coord,limits in [(axis.xaxis,axis.get_xlim()),(axis.yaxis,axis.get_ylim())]:
                    low,high=sorted(limits)
                    for tick in coord.get_major_ticks()+coord.get_minor_ticks():
                        if not low<=tick.get_loc()<=high:undrawn.update([tick.label1,tick.label2])
            clipped=[]
            for t in fig.findobj(Text):
                if t not in undrawn and t.get_visible() and t.get_text():
                    box=t.get_window_extent(renderer)
                    if box.x0< -1 or box.y0< -1 or box.x1>fig.bbox.width+1 or box.y1>fig.bbox.height+1:clipped.append(t.get_text())
            require(not clipped,f'Figure clipping {name}/{mobile}: {clipped}')
            variant='mobile' if mobile else 'projection';prefix=out/f'{name}-{variant}'
            fig.savefig(prefix.with_suffix('.png'),dpi=120,metadata={'Software':'AI Discovery Labs V3 OpenFlights'})
            fig.savefig(prefix.with_suffix('.svg'),metadata={'Date':None,'Creator':'AI Discovery Labs V3','Description':alt})
            variants.append(dict(variant=variant,png=prefix.name+'.png',svg=prefix.name+'.svg',png_sha256=sha(prefix.with_suffix('.png')),
                                 svg_sha256=sha(prefix.with_suffix('.svg')),width=int(fig.get_figwidth()*120),height=int(fig.get_figheight()*120),
                                 denominator=denominator,note=note,text_bounds_pass=True))
            plt.close(fig)
        metadata.append(dict(id=name,question_ids=questions,title=title,denominator=denominator,note=note,alt=alt,
                             period=manifest['observed_time_scope'],source_url=manifest['source_url'],license=manifest['license'],
                             source_sha256=manifest['snapshot_sha256'],code_sha256=code_hash,table='gold/'+table+'.csv',
                             table_sha256=sha(out.parent/'gold'/f'{table}.csv'),variants=variants))
    write(out/'figures.json',metadata)
    return metadata
