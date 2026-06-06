function doGet() {
  return HtmlService.createTemplateFromFile('Index')
    .evaluate()
    .setTitle('Rutas de atencion por incidente')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function getInitialData() {
  return APP_DATA;
}

function getSecurityPostalCentroids(cp) {
  var key = String(cp || '').trim();
  return {
    cp: key,
    centroids: SECURITY_CENTROIDS_BY_CP[key] || []
  };
}

function getSecurityPostalRoute(cp) {
  var key = String(cp || '').trim();
  var points = orderCentroidsByNearestNeighbor(SECURITY_CENTROIDS_BY_CP[key] || []);
  if (points.length < 2) {
    return { cp: key, status: 'not_enough_points', segments: [], orderedCentroids: points };
  }

  var segments = [];
  var start = 0;
  while (start < points.length - 1) {
    var end = Math.min(start + 24, points.length - 1);
    var chunk = points.slice(start, end + 1);
    segments.push(routeChunkWithMaps(chunk));
    start = end;
  }

  return {
    cp: key,
    status: segments.some(function (s) { return s.status === 'ok'; }) ? 'ok' : 'fallback',
    segments: segments,
    orderedCentroids: points
  };
}

function routeChunkWithMaps(points) {
  try {
    var finder = Maps.newDirectionFinder()
      .setOrigin(formatPoint(points[0]))
      .setDestination(formatPoint(points[points.length - 1]))
      .setMode(Maps.DirectionFinder.Mode.DRIVING);

    for (var i = 1; i < points.length - 1; i++) {
      finder.addWaypoint(formatPoint(points[i]));
    }

    var directions = finder.getDirections();
    var route = directions.routes && directions.routes[0];
    if (!route || !route.overview_polyline || !route.overview_polyline.points) {
      return { status: 'no_route', encodedPolyline: null };
    }
    return {
      status: 'ok',
      encodedPolyline: route.overview_polyline.points,
      distanceText: route.legs ? route.legs.map(function (leg) { return leg.distance && leg.distance.text; }).join(' + ') : '',
      durationText: route.legs ? route.legs.map(function (leg) { return leg.duration && leg.duration.text; }).join(' + ') : ''
    };
  } catch (err) {
    return { status: 'error', encodedPolyline: null, message: String(err).slice(0, 180) };
  }
}

function orderCentroidsByNearestNeighbor(points) {
  var remaining = points.slice().sort(function (a, b) { return b.events - a.events; });
  if (remaining.length <= 2) return remaining;
  var ordered = [remaining.shift()];
  while (remaining.length) {
    var last = ordered[ordered.length - 1];
    var bestIndex = 0;
    var bestDistance = Infinity;
    for (var i = 0; i < remaining.length; i++) {
      var d = haversineMeters(last.lat, last.lng, remaining[i].lat, remaining[i].lng);
      if (d < bestDistance) {
        bestDistance = d;
        bestIndex = i;
      }
    }
    ordered.push(remaining.splice(bestIndex, 1)[0]);
  }
  return ordered;
}

function formatPoint(point) {
  return point.lat + ',' + point.lng;
}

function haversineMeters(lat1, lon1, lat2, lon2) {
  var radius = 6371000;
  var phi1 = lat1 * Math.PI / 180;
  var phi2 = lat2 * Math.PI / 180;
  var dPhi = (lat2 - lat1) * Math.PI / 180;
  var dLambda = (lon2 - lon1) * Math.PI / 180;
  var a = Math.sin(dPhi / 2) * Math.sin(dPhi / 2) +
    Math.cos(phi1) * Math.cos(phi2) *
    Math.sin(dLambda / 2) * Math.sin(dLambda / 2);
  return radius * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}
