$(document).on('submit', '#profile_edit_form', function(event){

  event.preventDefault();
  //method = $(this).attr('method');

  image = $('#id_image').get(0).files[0];
  formdata = new FormData();
  formdata.append("image", image);

  $.ajax({
      url     : "/users/update_profile_info/",
      type    : 'post',
      dataType: 'json',
      data    : $(this).serialize(),
      success : function(data) {

        $('#username_navbar').html(data.username);
        $('#profile_name_tag').html(data.username);
        $('#profile_name_tag').data().name = data.username;

        $.ajax({
            url         : "/users/update_profile_image/",
            type        : 'POST',
            enctype     : "multipart/form-data",   //it is done inside jquery
            data        : formdata,
            cache       : false,
            contentType : false,
            processData : false,
            success : function(data) {
              $("#profile_picture").attr('src',data.profile_picture);
              $('#profile_picture').data().name = data.profile_picture;
            },
            error: function(data) {
              console.log('upload image failed');
            }
        });

      },
      error: function(data) {
          console.log('info-fail');
      }
  });


   // close modal window and show controls
   modal1.style.display = "none";
   $(".geo-panel").show();
   $("#search_places").show();
   $(".navigate-panel").show();
   $(".profile_section").show();

});
