"""Route-specific narrative decisions; revelations always refer to computed evidence."""
from v3.data import write

NARRATIVES={
    'D16-B':dict(title='El corte que cambia el mapa',
        hook='Imagina que debes explicar la dependencia de una región sin tener datos de pasajeros. Puedes retirar un aeropuerto del mapa histórico y observar qué conexiones quedan. Pero ¿contarías como desconectado al mismo aeropuerto que acabas de retirar? Antes de ver una tabla, elige una definición de accesibilidad y predice si todos los países reaccionarían igual. La investigación mide una estructura; el grupo decidirá qué pregunta humana aún queda sin responder.',
        first='Localizar un país y contar sus nodos dentro del componente gigante inicial; contrastar con el total de aeropuertos de su metadata.',
        complication='Retirar un nodo cambia el denominador. Además, estar fuera del componente gigante no mide cuántos pasajeros pierden un viaje.',
        discovery='Abrir country_resilience.csv. Señalar el hub retirado, los otros aeropuertos desconectados y el número restante del país.',
        adversary='Comparar el hub con los retiros locales de referencia y con 1/5/10 hubs globales del ranking original. ¿La región y el mundo reaccionan igual?',
        transfer='¿Qué fuentes necesitarías para convertir fragilidad topológica en personas o suministros afectados?',
        tables=['gold/country_resilience.csv','gold/hub_removal.csv']),
    'D16-C':dict(title='Fronteras que el algoritmo no conoce',
        hook='Tienes un mapa de aeropuertos y una lista de conexiones, pero el algoritmo que formará grupos no recibe países ni continentes. ¿Qué fronteras esperas que aparezcan? Cada persona apuesta por una división y explica por qué. Luego el grupo elegirá cómo definir cercanía: compartir una conexión, estar cerca físicamente o pertenecer al mismo país. Esas definiciones no son equivalentes. Al final habrá que distinguir una clasificación útil de una verdad que los datos nunca prometieron.',
        first='Leer el mapa por coordenadas y los conteos de nodos/aristas, antes de nombrar las comunidades.',
        complication='El número de comunidades cambia con resolución. La red se proyecta sin dirección para este método y no tiene pesos de tráfico.',
        discovery='Relacionar route-atlas, community-network y communities.csv; las ocho comunidades mayores se distinguen de Otras sin borrar nodos del análisis.',
        adversary='Contrastar ARI en resolución 0.8/1/1.2 y modularidad frente a 20 particiones de igual tamaño. La referencia no es una prueba confirmatoria.',
        transfer='¿Qué cambiaría al representar una red de amistades, coautorías o estaciones de bicicleta?',
        tables=['gold/communities.csv','gold/community_stability.csv','gold/null_modularity.csv','gold/community_flows.csv']),
    'D16-D1':dict(title='¿Quién merece el primer puesto?',
        hook='Imagina que dos analistas deben elegir un aeropuerto importante. Uno cuenta destinos distintos; el otro busca los nodos por los que pasan conexiones entre muchas partes de la red. Ambos pueden calcular bien y aun así discrepar. Antes de ver los nombres, define para qué serviría tu ranking y apuesta si habría un único ganador. La misión no es decidir qué analista tiene razón en general: es descubrir qué pregunta responde cada número y qué cambia al aproximarlo.',
        first='Verificar dos aeropuertos en nodes.csv y contar sus vecinos únicos a partir de edges.csv; no sumar aerolíneas como destinos nuevos.',
        complication='Intermediación no es un conteo de vuelos y aquí se aproxima con pivotes. Un orden de ranking tampoco muestra la magnitud de la diferencia.',
        discovery='Comparar valores, líderes y top10 de grado e intermediación, apoyándose en degree-betweenness y nodes.csv.',
        adversary='Repetir la lectura con k=64 frente a k=128 y con dirección eliminada. Separar sensibilidad del muestreo de un cambio de definición.',
        transfer='¿Usarías el mismo ranking para elegir dónde añadir capacidad y dónde estudiar dependencia de conexiones?',
        tables=['gold/nodes.csv','gold/edges.csv']),
    'D16-D2':dict(title='Vecinos en la Tierra, vecinos en la red',
        hook='Dos puntos pueden estar muy cerca en un mapa y no compartir una conexión directa en el archivo. ¿Te parecería una anomalía? Antes de buscar ejemplos, fija qué significa cerca y qué significa conectado. El grupo decidirá qué evidencia podría contradecir la afirmación. Después cambiará el umbral de distancia y revisará el denominador. El cierre debe explicar lo que esta red histórica permite saber y por qué una ruta ausente no es una oportunidad comercial demostrada.',
        first='Localizar un par de aeropuertos y cotejar sus coordenadas y sus IDs en la tabla original.',
        complication='La distancia de pantalla engaña en una proyección; usar Haversine. Cambiar de 100 a 500 km agrega muchos pares al denominador.',
        discovery='Leer los conteos de nearby_pairs.csv y localizar contraejemplos exportados en nearby_counterexamples.csv.',
        adversary='Comparar 100/250/500 km y la base de todos los pares activos. Exigir además coincidencia de códigos con metadata, manteniendo el denominador. Comprobar el antimeridiano.',
        transfer='¿Qué conclusiones exigirían añadir transporte terrestre, horarios, población o demanda?',
        tables=['gold/nearby_pairs.csv','gold/nearby_counterexamples.csv','gold/metadata_sensitivity.csv']),
    'D16-E':dict(title='El ranking que sobrevivió a sus supuestos',
        hook='Una tabla con posiciones precisas puede parecer definitiva. Hoy tu trabajo será intentar debilitarla. Puedes conservar o quitar la dirección de las conexiones y retirar nodos de la red. Antes de ejecutar, explica qué cambio considerarías relevante y qué esperas que permanezca estable. Puede que la red resista mejor de lo esperado o que cambien varios puestos: ninguno de esos desenlaces está exigido por el guion. La conclusión debe apoyarse en la prueba que realmente se ejecutó.',
        first='Elegir un ranking inicial y registrar la lista de hubs antes de simular retiros.',
        complication='Si se recalcula a cada paso qué hub retirar, cambia el experimento. La dirección y los desacuerdos entre códigos de rutas y metadata también cambian el grafo.',
        discovery='Leer ranking-sensitivity y hub_removal.csv; distinguir nodos retirados de nodos restantes fuera del gigante.',
        adversary='Comparar escenarios 0/1/5/10, usando siempre el ranking original y los denominadores restantes. No atribuir a compañías una reacción que no fue modelada.',
        transfer='¿Qué supuesto pondrías a prueba primero en un ranking entregado por otra IA?',
        tables=['gold/nodes.csv','gold/hub_removal.csv','gold/metadata_sensitivity.csv'])}


def enrich(out,stories):
    for story in stories:
        route=NARRATIVES[story['question_id']]
        story['title']=route['title'];story['hook_30_60_seconds']=route['hook']
        for index,key in [(2,'first'),(3,'complication'),(4,'discovery'),(5,'adversary')]:
            story['acts'][index]['facilitation']=route[key]
            story['acts'][index]['tables']=route['tables']
        story['acts'][6]['audience_question']=route['transfer']
        story['narrative_policy']='Escenario de investigación, sin incidente histórico inventado ni sorpresa exigida. Revelaciones ligadas a tablas y resultados ejecutados.'
    write(out/'education/storyboards.json',stories)
    # Facilitation includes the authored route hooks; never copied into the learner archive.
    text=(out/'teacher/FACILITACION.md').read_text()
    for story in stories:
        text+=f'\n## {story["question_id"]} · {story["title"]}\n\n{story["hook_30_60_seconds"]}\n\n'
        for act in story['acts']:text+=f'{act["act"]}. {act["name"]}: {act["facilitation"]}\n\n'
        text+='Transferencia: '+NARRATIVES[story['question_id']]['transfer']+'\n'
    (out/'teacher/FACILITACION.md').write_text(text)
    return stories
