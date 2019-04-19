$(document).ready(function(){
    $(".follow-btn, .unfollow-btn").click(function(){
        var user_id = this.id.split("-")[2];
        var clicked_btn = this.id.split("-")[0];
        if(clicked_btn == "follow"){
          $.ajax({
          url: '/follow/'+ user_id,
          type: 'get',
          success: function(){
            $("#follow-btn-"+ user_id).toggleClass('follow-btn unfollow-btn');
            $("#follow-btn-"+ user_id).toggleClass('btn-outline-success btn-outline-danger');
            $("#follow-btn-"+ user_id).text('Unfollow');
            $('#follow-btn-'+ user_id).attr("id","unfollow-btn-"+ user_id);
            if($("#follower-count").length){
              $("#follower-count").text(parseInt($("#follower-count").text())+1);
            }
          }
        })
        } else{
          $.ajax({
          url: '/unfollow/'+ user_id,
          type: 'get',
          success: function(){
            $("#unfollow-btn-"+ user_id).toggleClass('unfollow-btn follow-btn');
            $("#unfollow-btn-"+ user_id).toggleClass('btn-outline-danger btn-outline-success');
            $("#unfollow-btn-"+ user_id).text('Follow');
            $('#unfollow-btn-'+ user_id).attr("id","follow-btn-"+ user_id);
            // url is https://{domain}/stream_members/following
            if(window.location.href.split("/")[4] == "following"){
              $("#user-"+ user_id).remove();
            }
            //
            if($("#follower-count").length){
              $("#follower-count").text(parseInt($("#follower-count").text())-1);
            }
            
          }
        })
      }
    });

  });