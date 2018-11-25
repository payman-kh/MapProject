//function getProfile(username = 0){  //this is still not supported by IE, fuck you IE
function getProfile(username){
  if (!username){ username = 0 }

  //close results window
    $('.modal').hide();
    $(".geo-panel").show();
    $("#search_places").show();
    $(".navigate-panel").show();
    if (on_profile){
      $(".profile_section").show();
    }

  setCSRF();
  closeAll();

  on_profile = true;
  if (username){ UserName = username; }  // this variable is used for navigating through another user's profile
  else{ UserName = false; }


  if (username == 0){

    $('#profile_name_tag').html( $('#profile_name_tag').data().name );
    $("#profile_picture").attr('src', $('#profile_picture').data().name );
    $('#follow_button').css('display','none');
    $('#profile_edit_btn').css('display','block');

    //request the edit forms for the edit modal window via AJAX
    $.ajax({
       method: "POST",   // or 'type'
       url: "/users/profile_edit_window/",
       datatype: "json",
       success: function(data){
         $('#edit_forms').html(data);
       },
       error: function(data){
         console.log("fail");
       }
     });


  }else{

    $('#profile_name_tag').html(username);
    //get profile picture for this user
      $.ajax({
        method: "POST",
        url: "/users/user_profile_picture/",
        datatype:"json",
        data: {'username': username},
        success: function(data){
           $("#profile_picture").attr('src',data.profile_picture);
           $('#follow_button').css('display','block');
           $('#profile_edit_btn').css('display','none');
        },
        error: function(data){
            console.log('get-profile-picture-failed');
        }
      });

  } //end of else


  // fetch user's markers from the database
  $.ajax({
     method: "POST",   // or 'type'
     url: "/users/profile/",
     datatype: "json",
     data: {'username': username},
     success: function(data){
       if (data.markers_json){
         new_min_datetime = data.min_datetime;
         new_max_datetime = data.max_datetime;
         readNDisplayMarkers(JSON.parse(data.markers_json), data.number, JSON.parse(data.user_names),
          JSON.parse(data.image_urls), JSON.parse(data.ids), JSON.parse(data.num_likes), JSON.parse(data.liked));
       }
     },
     error: function(data){
       console.log("something went wrong");
     }
   });


  $(".profile_section").show();




} // getProfile
