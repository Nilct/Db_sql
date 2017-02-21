function setLeaflet() {

    var googleStreet = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
        maxZoom: 20,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
    });

    var map = new L.Map('mapid', {
        center: new L.LatLng(48.8413019, 2.5876218),
        zoom: 14,
        layers: [googleStreet]
    });

    var marker = L.marker([48.8413019, 2.5876218]).addTo(map);

    marker.bindPopup("<b>ENSG</b><br>6 et 8 Avenue Blaise Pascal,<br> Cité Descartes, <br>77420 Champs-sur-Marne").openPopup();



    var popup = L.popup();

    function onMapClick(e) {
        popup
            .setLatLng(e.latlng)
            .setContent("You clicked the map at " + e.latlng.toString())
            .openOn(map);

        requestCompanies(e);

    }

    map.on('click', onMapClick);
}


function requestCompanies(e){
  var donnees = {
    "lon": e.latlng.lng,
    "lat": e.latlng.lat
  };
  $.ajax({
      url: "server/php/server.php",
      type: 'POST',
      dataType: "json",
      data: donnees

  }).done(function(response){
    console.log(response);
  })
}

$(function() {
    console.log("ready!");
    setLeaflet();


});
