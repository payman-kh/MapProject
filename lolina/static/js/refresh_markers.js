//---------------------------- NAVIGATE THROUGH MARKERS ------------------------------
// functions to navigate through markers (posts). check older or newer ones
$(document).on('submit', '#navigate_older', function(event){

  event.preventDefault();
  closeAll();

  if (!counter & !on_profile){
    min_datetime_raw  = $("#min_datetime").data();
    min_datetime = min_datetime_raw['name'];
    counter = 1;
  }else{
    min_datetime = String(new_min_datetime);
  }

    if (!on_profile){ url = "/homepage/"; }
    else if (on_profile) { url = "/users/navigate_profile/" }

    number = escape(document.getElementById('older_value').value);
    data = {'key': 'old', 'date': min_datetime, 'number': number, 'username': false}
    if (UserName){ data['username'] = UserName }

    setCSRF();
    $.ajax({
       method: "POST",
       url: url,
       datatype: "json",
       data: data,
       success: function(data){
         new_min_datetime = data.min_datetime;
         new_max_datetime = data.max_datetime;
         readNDisplayMarkers(JSON.parse(data.markers_json), data.number, JSON.parse(data.user_names),
          JSON.parse(data.image_urls), JSON.parse(data.ids), JSON.parse(data.num_likes), JSON.parse(data.liked));
       },
       error: function(data){
         console.log("something went wrong");
       }
     });

})


$(document).on('submit', '#navigate_newer', function(event){

  event.preventDefault();
  closeAll()

  if (!counter & !on_profile){
    max_datetime_raw  = $("#max_datetime").data();
    max_datetime = max_datetime_raw['name'];
    counter = 1;
  }else{
    max_datetime = String(new_max_datetime);
  }


  if (!on_profile ){ url = "/homepage/"; }
  else if (on_profile) { url = "/users/navigate_profile/"}

  number = escape(document.getElementById('newer_value').value);
  data = {'key': 'new', 'date': max_datetime, 'number': number, 'username': false}
  if (UserName){ data['username'] = UserName }

  setCSRF();
  $.ajax({
     method: "POST",
     url: url,
     datatype: "json",
     data: data,
     success: function(data){
       new_min_datetime = data.min_datetime;
       new_max_datetime = data.max_datetime;
       readNDisplayMarkers(JSON.parse(data.markers_json), data.number, JSON.parse(data.user_names),
        JSON.parse(data.image_urls), JSON.parse(data.ids), JSON.parse(data.num_likes), JSON.parse(data.liked));
     },
     error: function(data){
       console.log("something went wrong");
     }
   });

})
