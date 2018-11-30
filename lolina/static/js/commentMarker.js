$(document).on('submit', '#comment', function(event){ event.preventDefault(); })


function commentMarker(marker_pk){

  setCSRF();

  let comment = decodeURI(escape(document.getElementById('new_comment').value));

  $.ajax({
    url: '/commentMarker/',
    method: 'post',
    data: {'id': marker_pk, 'comment': comment},
    success: function(data){
      console.log(data.c);
    },
    error: function(err){
      console.log(err);
    }
  })

}
