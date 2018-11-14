$(document).on('submit', '#search_form', function(event){
  // send search query to the server
  // at the moment just search for users !!

event.preventDefault();

query = escape(document.getElementById('search_value').value);

if (query){

  setCSRF();
  closeAll();

  $.ajax({
     method: "GET",
     url: "/search/",
     datatype: "json",
     data: {'q' : query},
     success: function(data){
       if (data.users != null){
         $('#search_results').empty();   //empty the container first
         data.users.forEach(function(user){
             username = user.username;
             $('#search_results').append('<li class="list-group-item" style="width:20%"><a href="#" onclick="getProfile(\''
                                          + username + '\')">' + username + '</a></li>');
         });
       }else{
         $('#search_results').html('<div align="center"><h4> No users found! </h4></div>')
       }
     },
     error: function(data){
       console.log("search failed");
     }
   });

   is_query = true;
 }

});



/*
counter = 1;
on_profile = false;

query = escape(document.getElementById('search_value').value);

if (query){
  doAjaxStuff();
  closeAllMarkersSearch();
  $.ajax({
     method: "POST",
     url: "/first_results/",
     datatype: "json",
     data: {'q': query},

     success: function(data){
      new_markers = JSON.parse(data.markers_json);
      new_min_datetime = data.min_datetime;
      new_max_datetime = data.max_datetime;
      readNDisplayMarkers(new_markers, data.number);

     },
     error: function(data){
       console.log("something went wrong");
     }
   });

   is_query = true;
 }

})*/
