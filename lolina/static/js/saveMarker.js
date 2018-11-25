$(document).on('submit', '#add_marker_form', function(event){

  event.preventDefault();

  closeAll_saveMarker();
  setCSRF();

  on_profile = true;

  var FILE_DATA = false;

  // title
  let title = decodeURI(escape(document.getElementById('marker_title').value));
  // coordinates
  let latitude = temp_marker.getPosition().lat();
  let longitude = temp_marker.getPosition().lng();
  // csrf token
  let csrfmiddlewaretoken =  $("#add_marker_form").find("input[name='csrfmiddlewaretoken']" ).val();

  let DATA = { 'title': title,
               'latitude': latitude,
               'longitude': longitude,
               'csrfmiddlewaretoken': csrfmiddlewaretoken,
               'was_there': was_there
          };

  was_there = false;

  // body
  let body = document.getElementById('body');
  if (body != null){
    body = decodeURI(escape(body.value));
    DATA = Object.assign(DATA, {'body': body});
  }

  // youtube link
  let youtube_url = document.getElementById('youtube_url').value;
  if (youtube_url){
    youtube_url = "https://www.youtube.com/embed/" + getYoutubeId(youtube_url);
    DATA = Object.assign(DATA, {'youtube_url': youtube_url});
   }

  //attachment (image/video)
  let attachment = $('#uploaded_files').get(0).files[0];
  if (attachment != null){
    var formdata = new FormData();
    var fileType = attachment["type"];
    var ValidFileTypes = ["image/gif", "image/jpeg", "image/png", "image/jpg", "video/3g2", "video/3gp", "video/3gpp", "video/asf",
                          "video/avi", "video/dat", "video/flv", "video/gif", "video/mp4", "video/mpeg", "video/mpg", "video/mpeg4",
                          "video/wmv"];
    if ($.inArray(fileType, ValidFileTypes) > 0) {
       formdata.append("attachment", attachment);
       FILE_DATA = true;
    }else{
        console.log('invalid file format');
        alert('invalid file format');
        return
    }
  }

 DATA = Object.assign(DATA, {'file_data': FILE_DATA});


 $.ajax({
   method  : "POST",
   url     : "/saveMarker1/",
   datatype: "json",
   data    : DATA,
   success : function(data){

       if(FILE_DATA){
             $.ajax({
               method     : "POST",
               url        : "/saveMarker2/",
               datatype   : "json",
               data       : formdata,
               cache      : false,
               processData: false,
               contentType: false,
               success: function(data){
                   console.log('second ajax done');
                   //get the markers of the user
                   new_min_datetime = data.min_datetime;
                   new_max_datetime = data.max_datetime;
                   readNDisplayMarkers(JSON.parse(data.markers_json), data.number, JSON.parse(data.user_names),
                    JSON.parse(data.image_urls), JSON.parse(data.ids), JSON.parse(data.num_likes), JSON.parse(data.liked));
               },
               error: function(err){
                 console.log(err);
               }
             }) //second ajax

        }else{
            //get the markers of the user
            new_min_datetime = data.min_datetime;
            new_max_datetime = data.max_datetime;
            readNDisplayMarkers(JSON.parse(data.markers_json), data.number, JSON.parse(data.user_names),
             JSON.parse(data.image_urls), JSON.parse(data.ids), JSON.parse(data.num_likes), JSON.parse(data.liked));
        }

        //redirect to user profile
        if (UserName == false){
          $('#profile_name_tag').html( $('#profile_name_tag').data().name );
          $("#profile_picture").attr('src', $('#profile_picture').data().name );
        }
        $(".profile_section").show();
        UserName = false;
        //close form and marker
        temp_marker.newWindow.close();
        temp_marker.setMap(null);

   },
   error: function(err){
     console.log(err);
   }

 }) // first ajax


}) // document


function getYoutubeId(url){
 var videoid = url.match(/(?:https?:\/{2})?(?:w{3}\.)?youtu(?:be)?\.(?:com|be)(?:\/watch\?v=|\/)([^\s&]+)/);
 if(videoid == null) {
   console.log(url + " is not a valid YouTube url");
 }
   return videoid[1];
 }


function closeAll_saveMarker(){
  // delete markers
    if (markers){
      markers.forEach(function(marker) {
        marker.setMap(null);
      });
    }

    // delete the route (if any)
    if (directionsDisplay != null) {
      directionsDisplay.setMap(null);
      directionsDisplay = null;
  }

  // delete place markers
  if (place_markers){
    place_markers.forEach(function(place_marker) {
      place_marker.setMap(null);
    });
  }
}
