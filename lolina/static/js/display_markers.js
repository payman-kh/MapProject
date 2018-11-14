function readNDisplayMarkers(markers_from_database, number, user_names, image_urls){
  // store the markers
  markers = [];
  marker_location = [];
  //infowindows = new Array();
  //var main_content = new Array();
  var bounds  = new google.maps.LatLngBounds();   // store coords for auto-zoom and auto-center
  var endpoint = markers_from_database.length;

  if (number== 1){
    markers_from_database[1] = []
    endpoint = 1;
  }

  //the blue marker icon
  var marker_icon = new google.maps.MarkerImage("http://maps.google.com/mapfiles/ms/micons/blue.png",
             new google.maps.Size(32, 32), new google.maps.Point(0, 0),new google.maps.Point(16, 32));



  // display markers one by one
  for(m=0; m<endpoint; m++){

    curr_marker = markers_from_database[m]['fields'];
    img_url = image_urls[m]
    user_name = user_names[m]

    if (curr_marker){

        lat = curr_marker.latitude;
        lng = curr_marker.longitude;

        // define marker attrs
        if (!curr_marker.was_there){
          markers[m] = new google.maps.Marker({
             icon: marker_icon,
             draggable: true,
           });
        }else{
          markers[m] = new google.maps.Marker({
            draggable: false,
          });
        }

        markers[m].setPosition({lat: parseFloat(lat), lng: parseFloat(lng)});
        markers[m].setMap(map);
        if (!on_profile ){ markers[m].draggable = false; }
        markers[m].index = m;

        // storing coords for auto-zoom/center
        marker_location = new google.maps.LatLng(lat, lng);
        bounds.extend(marker_location);


        //THUMBNAIL AND MAIN CONTENT
        // check image or video to get the tag and make thumbnail content with file.
        //if there is file (image/video) attached, it will be shown in the thumbnail content
        //otherwise if it has a youtube link attacehd to it, the youtube video will be shown
        //or just an empty thumbnail with only title
        if (curr_marker.attachment != ''){
          var format = curr_marker.attachment.split(".").pop();
          file_type = checkFileFormat(format);

            // content of the thumbnail with files
            if (file_type == 'image'){
              //thumbnail content with image tag
              thumbnail =
                  '<h4><img src="'+ img_url +'" title="'+ user_name +'"  width=20px; width=20px; class="img-circle" style="object-fit: contain;">&nbsp;'
                     +  curr_marker.title + '</h4><br>' +
                    //TODO: fix this url problem
                    '<img class="marker_thumbnail_image" src="'+ '/media/' + curr_marker.attachment +'" alt="could not load image" height="150" width="150">';

              //main content with image
              main_content =
                    '<h1><img src="'+ img_url +'" title="'+ user_name +'" width=30px; width=30px; class="img-circle" style="object-fit: contain;">&nbsp;'
                     + curr_marker.title + '</h1>' +
                      '<br><br>' + ( typeof curr_marker.body !="undefined" ? '<div id=marker_body" style="word-wrap: break-word; width:550px;"><h4>' + curr_marker.body + '</h4></div>':'null') +
                      '<img class="marker_main_image" src="'+ '/media/' + curr_marker.attachment +'" alt="could not load image" width=540px; height=340px;>';

            }else if (file_type == 'video'){
              //thumbnail content with video tag
              thumbnail =
                    '<h4><img src="'+ img_url +'" title="'+ user_name +'" width=20px; width=20px; class="img-circle" style="object-fit: contain;">&nbsp;'
                     + curr_marker.title + '</h4><br>' +
                    '<br><video id="marker_thumbnail_video" width="180" height="150" controls>' +
                      '<source src="' + '/media/' + curr_marker.attachment + '" type="video/' + format + '">' +
                      'Your browser does not support the video tag' +
                    '</video>';

              //main content with video
              main_content =
                    '<h1><img src="'+ img_url +'" title="'+ user_name +'" width=30px; width=30px; class="img-circle" style="object-fit: contain;">&nbsp;'
                    +  curr_marker.title + '</h1>' +
                    '<br><br>' + ( typeof curr_marker.body !="undefined" ? '<div style="width:550px"><h4>' + curr_marker.body + '</h4></div>':'null') +
                    '<video id="marker_main_video" width=540px; height=340px; controls>' +
                      '<source src="' + '/media/' + curr_marker.attachment + '" type="video/' + format + '">' +
                      'Your browser does not support the video tag' +
                    '</video>';

            }
        }else{
            // thumbnail content with or without youtube video
            thumbnail =
                      '<h4><img src="'+ img_url +'" title="'+ user_name +'"  width=20px; width=20px; class="img-circle" style="object-fit:contain;">&nbsp;'
                       +  curr_marker.title + '</h4><br>' +
                        ( typeof curr_marker.youtube_url != "undefined" ? '<iframe class="iframe" title="Youtube player" type="text/html" width=170px; height=90px; type="text/html" allow="encrypted-media" src="'
                                                          + curr_marker.youtube_url  + '" frameborder="0"></iframe>': 'null')


            // main content with/without attachemnt
            main_content =
                    '<h1><img src="'+ img_url +'" title="'+ user_name +'" width=30px; width=30px; class="img-circle" style="object-fit: contain;">&nbsp;'
                     + curr_marker.title + '</h1>' +
                      '<br><br>' + ( typeof curr_marker.body !="undefined" ? '<div style="width:400px"><h4>' + curr_marker.body + '</h4></div>':'null') +
                      ( typeof curr_marker.youtube_url != "undefined" ? '<iframe class="iframe" title="Youtube player" type="text/html" width=540px; height=340px; type="text/html" allow="encrypted-media" src="' +
                      curr_marker.youtube_url  + '" frameborder="0"></iframe>': 'null');


          } //check image/video

          if (curr_marker.was_there == true){
              thumbnail    = '<h5 style="background-color:Bisque;">'+ user_name +' was here!</h5><br>' + thumbnail;
              main_content = '<h4 style="background-color:Bisque;">'+ user_name +' was here!</h4><br>' + main_content;
          }

          main_content = main_content +
                          '<br><br><button id="like_button" type="button" class="btn btn-default" title="like (inactive)"><span class="glyphicon glyphicon-thumbs-up"></span></button>&nbsp' +
                          '<button id="share_button" class="btn btn-default" type="button" onclick="" title="share (inactive)"><span class="glyphicon glyphicon-share-alt"></span></button>&nbsp' +
                          '<button id="get_directions" class="btn btn-default" type="button" onclick="get_directions()" title="get directions"> <i class="material-icons" style="font-size:27px;color:red">place</i> </button>' +
                          '<br><input id="new_comment" class="new_comment" type=input placeholder="write a comment...">';
                          //'<br> <strong> Coordinates:&nbsp; </strong>' + lat + '<strong>,&nbsp;</strong> ' + lng + '<br><br>'

          //store and display thumbnail
          markers[m].thumbnail = new google.maps.InfoWindow({
           content: thumbnail,
           });
          markers[m].thumbnail.open(map,markers[m]);

          //store main content
          markers[m].main_content = new google.maps.InfoWindow({
           content: main_content,
           });

         // set left/right click event listners on markers
         setMarkerEvents(markers,m);

    }  // if curr_marker


  } //for loop

  if (endpoint){
    if (number > 1) {
      map.fitBounds(bounds);
    }   //auto-zoom
    else {
       map.setCenter(new google.maps.LatLng(lat, lng));
       var listener = google.maps.event.addListener(map, "idle", function() {
         map.setZoom(7);
         google.maps.event.removeListener(listener);
       });
      }  // center
  }


} //function

//------------------------------------------------------------------------------

function checkFileFormat(f){
  fileType = null;
  let ValidImageTypes = ["gif", "jpeg", "png",  "jpg"];
  let ValidVideoTypes = ["3g2", "3gp",  "3gpp", "asf", "avi", "dat",  "flv",
                         "gif", "mp4",  "mpeg", "mpg", "mpeg4", "wmv"];
    if ($.inArray(f, ValidImageTypes) > 0) {
      fileType = 'image';
    }else if ($.inArray(f, ValidVideoTypes) > 0){
      fileType = 'video';
    }
  return fileType
}

function setMarkerEvents(markers, m){
    // listner per click on the marker (close thumbnail/open content)
    google.maps.event.addListener(markers[m], 'click', function() {
          markers[m].thumbnail.close();
          markers[m].main_content.open(map,markers[m]);
          map.panTo(markers[m].getPosition());
    });

    // close content, open thumbnail
    google.maps.event.addListener(markers[m].main_content, 'closeclick', () => {
           markers[m].thumbnail.open(map,markers[m]);
    });

    // remove marker right click
    google.maps.event.addListener(markers[m], 'rightclick',  function(mouseEvent) {
         markers[m].setMap(null);
     });
}


//============================ get direction ==================================
//WARNING:
/** THIS FUNCTIONALITY WILL NOT WORK IF THERE ARE MORE THAN ONE MARKERS ON THE MAP **/

 // arrays to hold copies of the markers and html used by the side_bar
 // because the function closure trick doesnt work there
 var gmarkers = [];
 var htmls = [];
 // arrays to hold variants of the info window html with get direction forms open
 var to_htmls = [];
 var from_htmls = [];

 var infowindow


function get_directions() {

  infowindow = new google.maps.InfoWindow({
     size: new google.maps.Size(150, 50)
   });

   if (markers){
     //works only with 1 marker!
       markers[0].thumbnail.close();
       markers[0].main_content.close();
   }

   var i = gmarkers.length;
   latlng = marker_location;

   var i = gmarkers.length;
   latlng = marker_location;

   // The info window version with the "to here" form open
   to_htmls[i] = html + '<br>Directions: <b>To here<\/b> - <a href="javascript:fromhere(' + i + ')">From here<\/a>' +
     '<br>Start address:<form action="javascript:getDirections()">' +
     '<input type="text" SIZE=40 MAXLENGTH=40 name="saddr" id="saddr" value="" /><br>' +
     '<INPUT value="Get Directions" TYPE="button" onclick="getDirections()"><br>' +
     'Walk <input type="checkbox" name="walk" id="walk" /> &nbsp; Avoid Highways <input type="checkbox" name="highways" id="highways" />' +
     '<input type="hidden" id="daddr" value="' + latlng.lat() + ',' + latlng.lng() +
     '"/>';
   // The info window version with the "from here" form open
   from_htmls[i] = html + '<br>Directions: <a href="javascript:tohere(' + i + ')">To here<\/a> - <b>From here<\/b>' +
     '<br>End address:<form action="javascript:getDirections()">' +
     '<input type="text" SIZE=40 MAXLENGTH=40 name="daddr" id="daddr" value="" /><br>' +
     '<INPUT value="Get Directions" TYPE="SUBMIT"><br>' +
     'Walk <input type="checkbox" name="walk" id="walk" /> &nbsp; Avoid Highways <input type="checkbox" name="highways" id="highways" />' +
     '<input type="hidden" id="saddr" value="' + latlng.lat() + ',' + latlng.lng() +
     '"/>';
   // The inactive version of the direction info
   var html = '<br>Directions: <a href="javascript:tohere(' + i + ')">To here<\/a> - <a href="javascript:fromhere(' + i + ')">From here<\/a>';
   var contentString = html;

   //the direction infowindow pop up on the marker
   infowindow.setContent(contentString);
   infowindow.open(map, markers[0]);

   // save the info we need to use later for the side_bar
   gmarkers.push(markers[0])

}

// ===== request the directions =====
function getDirections() {
  directionsService = new google.maps.DirectionsService();
  directionsDisplay = new google.maps.DirectionsRenderer();
  directionsDisplay.setMap(map);
  directionsDisplay.setPanel(document.getElementById("directionsPanel"));

  // ==== Set up the walk and avoid highways options ====
  var request = {};
  if (document.getElementById("walk").checked) {
    request.travelMode = google.maps.DirectionsTravelMode.WALKING;
  } else {
    request.travelMode = google.maps.DirectionsTravelMode.DRIVING;
  }

  if (document.getElementById("highways").checked) {
    request.avoidHighways = true;
  }
  // ==== set the start and end locations ====
  var saddr = document.getElementById("saddr").value;
  var daddr = document.getElementById("daddr").value;

  request.origin = saddr;
  request.destination = daddr;
  directionsService.route(request, function(response, status) {
    if (status == google.maps.DirectionsStatus.OK) {
      directionsDisplay.setDirections(response);
    } else alert("Directions not found:" + status);
  });
}

// This function picks up the click and opens the corresponding info window
function myclick(i) {
  google.maps.event.trigger(gmarkers[i], "click");
}

// functions that open the directions forms
function tohere(i) {
  // gmarkers[i].openInfoWindowHtml(to_htmls[i]);
  infowindow.setContent(to_htmls[i]);
  infowindow.open(map, gmarkers[i]);
}

function fromhere(i) {
  // gmarkers[i].openInfoWindowHtml(from_htmls[i]);
  infowindow.setContent(from_htmls[i]);
  infowindow.open(map, gmarkers[i]);
}
