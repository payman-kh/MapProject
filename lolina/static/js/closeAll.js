function closeAll(){

  // delete markers (if any)
  if (markers){
    markers.forEach(function(marker) {
      marker.setMap(null);
    });
  }
  if (temp_marker != null){
    temp_marker.setMap(null);
  }

  // delete the route (if any)
  if (directionsDisplay != null && directionsDisplay !== '') {
    directionsDisplay.setMap(null);
    directionsDisplay = null;
  }

  // delete place markers (if any)
  if (place_markers){
    place_markers.forEach(function(place_marker) {
      place_marker.setMap(null);
    });
  }

  //delete circles (if any)
  if(drawingManager != null && drawingManager != '' && drawingManager != []) {
    drawingManager.setDrawingMode(null);
    //drawingManager.setMap(null);
  }

}
