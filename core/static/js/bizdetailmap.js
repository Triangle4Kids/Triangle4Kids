$(document).ready(function () {
    mapboxgl.accessToken = 'pk.eyJ1IjoidHJpYW5nbGU0a2lkcyIsImEiOiJjanFubWRwMGw3a2hjNGFtc3RrMWQ4OXl5In0.eZj0i5qyOBlmeY2oH6LWow';
    // TO DO: get ID from HTML 
    bizID = $('#business').attr("data-business-id");


    mapObject = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/light-v9',
        center: [-35.77, 78.63],
        zoom: 12
    });
    displayBizOnMap(bizID);
});

function displayBizOnMap(id) {

    const url = '/api/businesses/' + id;
    sendBizApiRequest("GET", url);
}

function sendBizApiRequest(method, url) {
    console.log("[Search Request] " + url);
    $.getJSON(url, null, handleBizApiResponse);
}

function handleBizApiResponse(data, status, xhr) {
    if (status == "success") {
        console.log("Got response, creating map...");
        var latitude = data["location"]["latitude"]
        var longitude = data["location"]["longitude"]
        console.log("Adding map marker at [" + latitude + ", " + longitude + "]")
        addLatLongMarker(mapObject, latitude, longitude);
        console.log("Map marker displayed...")
        console.log("Recentering map...")
        mapObject.flyTo({ center: [longitude, latitude] });
        console.log("Mapping complete...")
    }
    else {
        console.log("Bad response from BisApi: " + status)
    }
}

function addLatLongMarker(map, latitude, longitude) {
    console.log("plotting: " + latitude + ", " + longitude)
    // create a HTML element for each feature
    var el = document.createElement('div');
    el.className = 'marker';

    coords = [longitude, latitude]
    // make a marker for each feature and add to the map
    new mapboxgl.Marker(el)
        .setLngLat(coords)
        .addTo(map);
    console.log("plotting complete ")
}

