function set_ads_marker(){

  closeAll();

   var position = new google.maps.LatLng(53.164939179132,  8.21971260292969);

   event_marker = new google.maps.Marker({
     map: map,
     position: position,
     draggable: true,
   });

    content =
          '<div style="background-color:AliceBlue ">' +   // for resizing the info window
          "<h3> Amazon Fashion </h3>" +
          "<br><h4> The latest deal </h4>" +
          '<br><img src="https://scontent-ams3-1.xx.fbcdn.net/v/t1.0-9/40066416_10211760354596439_2909789413317804032_n.jpg?_nc_cat=0&oh=012012deb307616cac48ac532be3a639&oe=5BF9183A" img>' +
          '<br><br><h4> $34,99 </h4>' +
          '<br><br><button class="btn btn-default" type="button"> Inspect </button>' +
          '<button class="btn btn-default" type="button"> Buy now! </button>' +
          '</div>';


   infowindow = new google.maps.InfoWindow({
    content: content,
    });

    infowindow.open(map, event_marker);

    google.maps.event.addListener(event_marker,'click',function(){
      event_marker.setMap(null);
    });

}
