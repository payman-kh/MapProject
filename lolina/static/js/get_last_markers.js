// load the homepage and dislplay the most recent markers
function get_last_markers() {
  counter = 0;
  on_profile = false;
  UserName = false;

  closeAll();
  setCSRF();

  $(".profile_section").hide();

  $.ajax({
     method: "POST",   // or 'type'
     url: "/get_latest_markers/",
     datatype: "json",
     success: function(data){
       if(data.markers_json){
         //new_markers = JSON.parse(data.markers_json);
         new_min_datetime = data.min_datetime;
         new_max_datetime = data.max_datetime;
         readNDisplayMarkers(JSON.parse(data.markers_json), data.number, JSON.parse(data.user_names),
          JSON.parse(data.image_urls), JSON.parse(data.ids), JSON.parse(data.num_likes), JSON.parse(data.liked));
       }
     },
     error: function(err){
       console.log(err);
     }
   });


}
