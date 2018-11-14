function geocodeAddress(geocoder, resultsMap) {

  var address = document.getElementById('geo-address').value;

  geocoder.geocode({'address': address}, function(results, status) {
    if (status === 'OK') {
      resultsMap.setCenter(results[0].geometry.location);
      var marker = new google.maps.Marker({
        map: resultsMap,
        position: results[0].geometry.location
      });

      map.setZoom(6);

      marker.newWindow = new google.maps.InfoWindow({
        content: 'here!',
      });
      marker.newWindow.open(map, marker);

      google.maps.event.addListener(marker,'click',function(){
        marker.setMap(null);
      });


    } else {
      alert('Navigating to the given address was not successful: ' + status);
    }

  });
}
