// function for drawing manager (draw circle)
function drawCircle(){
 closeAll();
 drawingManager = new google.maps.drawing.DrawingManager({
    drawingMode: google.maps.drawing.OverlayType.CIRCLE,
    drawingControl: false,
    drawingControlOptions: { drawingModes: ['circle'] },
    circleOptions: {
      fillColor: 'transparent',
      fillOpacity: 1,
      strokeWeight: 3,
      clickable: true,
      editable: false,
      zIndex: 1
    }
  });
  drawingManager.setMap(map);
}
