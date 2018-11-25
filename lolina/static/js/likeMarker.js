function likeMarker(marker_pk){

  setCSRF();
  $.ajax({
    url: '/likeMarker/',
    method: 'post',
    data: {'pk': marker_pk},
    success: function(data){
      if (data.flag == 0){
        console.log('Marker unliked');
        $('#like_button').css('color','grey');
        $('#num_likes').html(data.num_likes + ' Likes');
      }
      else{
        console.log('Marker liked')
        $('#like_button').css('color','blue');
        $('#num_likes').html(data.num_likes + ' Likes');
      }
    },
    error: function(err){
      console.log(err);
    }
  });

}
