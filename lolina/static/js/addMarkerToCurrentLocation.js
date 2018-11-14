function addMarkerToCurrentLocation(){
  closeAll();

  was_there = true;

  temp_marker = new google.maps.Marker({
    map: map,
    animation: google.maps.Animation.DROP,
  });

  // fetch invisible form
  var form_1 =	$("#iw-add_marker").clone().show();
  var infowindow_content_1 = form_1[0];
  temp_marker.newWindow = new google.maps.InfoWindow({
    content: infowindow_content_1
  });


    // Try HTML5 geolocation.
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
        var pos = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };

        temp_marker.setPosition(pos);
        map.setCenter(pos);
      }, function() {
        handleLocationError(true, temp_marker, map.getCenter());
      });
    } else {
      // Browser doesn't support Geolocation
      handleLocationError(false, temp_marker, map.getCenter());
    }


    temp_marker.newWindow.open(map, temp_marker);

   // Listener for window close:
   google.maps.event.addListener(temp_marker.newWindow,'closeclick',function(){
     temp_marker.setMap(null);
   });




  function handleLocationError(browserHasGeolocation, temp_marker, pos) {
    temp_marker.setPosition(pos);
    temp_marker.setContent(browserHasGeolocation ?
                          'Error: The Geolocation service failed.' :
                          'Error: Your browser doesn\'t support geolocation.');
    temp_marker.open(map);
  }

}
