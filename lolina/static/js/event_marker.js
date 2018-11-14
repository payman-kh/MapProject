function set_event_marker(){

  closeAll();

   var position = new google.maps.LatLng(53.164939179132,  8.21971260292969);

   event_marker = new google.maps.Marker({
     map: map,
     position: position,
     draggable: true,
   });

    content =
          '<div style="background-color:AliceBlue ">' +   // for resizing the info window
          "<h1>  Payman's Birthday party </h1>" +
          '<br><div><h4 style="color:grey"> Private· Hosted by</h4> <h4 style="color:blue"> Peyman Kheiri </h4></div>' +
          '<br><img src="https://scontent-ams3-1.xx.fbcdn.net/v/t1.0-9/34017790_10211174101740484_3819504598037561344_n.jpg?_nc_cat=0&_nc_eui2=AeEHC20Go_wKtrLMT6tWH_kK9g5Oc1OPF-M6LuYQ9AvCPmf-62DCxGkhYGxdboqub77vF7nStvqaLkOsjHRR9r3oXTrIFrbdLBwD0RudEaJjLw&oh=876631a6353e7ca3a836bd025d7ebfd7&oe=5BC0BE05" img>' +
          '<br><br><h4> Am Salzmarkt 1, 49074 Osnabrück, Deutschland </h4>' +
          '<br><h4> Friday, June 8 at 9 PM </h4>' +
          '<br><h4 style="color:grey"> Next Week · 16–27° Sunny </h4>' +
          '<br><br><button class="btn btn-default" type="button"> Going </button>' +
          '<button class="btn btn-default" type="button"> Not going </button>' +
          '<button class="btn btn-default" type="button"> Get Direction </button>' +
          '</div>';


   infowindow = new google.maps.InfoWindow({
    content: content,
    });

    infowindow.open(map, event_marker);

    google.maps.event.addListener(event_marker,'click',function(){
      event_marker.setMap(null);
    });

}
