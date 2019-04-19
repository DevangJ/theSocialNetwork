$(document).ready(function() {
    // Like and Unlike
    $(".like-btn, .unlike-btn").click(function(){
      var post_id = this.id.split("-")[2];
      var clicked_btn = this.id.split("-")[0];
      if(clicked_btn == "like"){
        $.ajax({
        url: '/like/'+ post_id,
        type: 'get',
        success: function(){
          $("#like-btn-"+ post_id).toggleClass('like-btn unlike-btn');
          var html_in_btn = '<span class="badge badge-light" id="like-count-'+ post_id +'">'+ (parseInt($("#like-count-"+ post_id).text()) + 1) +'</span> Unlike';
          $("#like-btn-"+ post_id).html(html_in_btn);
          $('#like-btn-'+ post_id).attr("id","unlike-btn-"+post_id);
        }
      })
      } else{
        $.ajax({
        url: '/unlike/'+ post_id,
        type: 'get',
        success: function(){
          $("#unlike-btn-"+ post_id).toggleClass('unlike-btn like-btn');
          var html_in_btn = '<span class="badge badge-light" id="like-count-'+ post_id +'">'+ (parseInt($("#like-count-"+ post_id).text()) - 1) +'</span> Like';
          $("#unlike-btn-"+ post_id).html(html_in_btn);
          $('#unlike-btn-'+ post_id).attr("id","like-btn-"+post_id);
        }
      })
    }
  });
  // Delete
  $(".delete-btn").click(function(){
    var post_id = this.id.split("-")[2];
    $.ajax({
        url: '/delete/'+ post_id,
        type: 'get',
        success: function(){
          $("#post-"+ post_id).remove();
        }
      });
  });
  // Edit
  $(".edit-btn").click(function(){
    var post_id = this.id.split("-")[2];
    window.location = "/edit/"+ post_id;
  });
  // View More
  $(".view-btn").click(function(){
    var post_id = this.id.split("-")[2];
    console.log(post_id);
    window.location = "/post/"+ post_id;
  });
  // Delete Comment
  $(".delete-comment-btn").click(function(){
    var comment_id = this.id.split("-")[3];
    $.ajax({
        url: '/delete_comment/'+ comment_id,
        type: 'get',
        success: function(){
          $("#comment-"+ comment_id).remove();
        }
      });
  });
  // Load Links
  function unique(list) {
    var result = [];
    $.each(list, function(i, e) {
        if ($.inArray(e, result) == -1) result.push(e);
    });
    return result;
  }
  $(".post-text").each(function(){
    // external links
    var urlRegex = /(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;
    var photoRegex = /(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|]).(?:jpg|gif|png)/ig;
    var post_id = this.id.split("-")[2];
    var url_url= $('#post-text-'+ post_id).html().match(urlRegex);
    url_url = unique(url_url);
    var url_photo= $('#post-text-'+ post_id).html().match(photoRegex);
    url_photo = unique(url_photo);
    var j = 0;
    $.each(url_url, function(i, value){
      var convert_url='<a href="'+url_url[i]+'">'+url_url[i]+'</a>';
      if(url_url[i] == url_photo[j]){
        var convert_photo='<img src="'+url_photo[j++]+'" style="max-width:75%; max-height:75%;" alt="Nba">';
        $('#post-text-'+ post_id).html(function(){
          return $(this).html().replace(RegExp(url_url[i], "g"), convert_url +"<br>"+ convert_photo);
        });
      }else{
        $('#post-text-'+ post_id).html(function(){
          return $(this).html().replace(RegExp(url_url[i], "g"), convert_url);
        });
      }
    });

    // uploaded files
    // var fileRegex = /\b(static\/img\/post-[0-9]*[0-9]-img[0-9]*[0-9])[.](?:png|jpg|gif)/ig;
    // var url_file= $('#post-text-'+ post_id).html().match(fileRegex);
    // $.each(url_url, function(i, value))
    // console.log(url_file);
  });
  
});