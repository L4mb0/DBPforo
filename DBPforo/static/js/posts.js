var current_user;
var current_post_id

$.getJSON("/posts", function(data){
        var i = 0;
        $.each(data, function(){
            alert(data[i]['id']);
            e = '<div>'
            e = e+'<div class="container"><div class="col-md-5"><div class="panel panel-default"><div class="panel-body"><section class="post-heading"><div class="row"><div class="col-md-11"><div class="media"><div class="media-left"><a href="#"><img class="media-object photo-profile" src="https://banner2.kisspng.com/20180828/sxw/kisspng-clip-art-computer-icons-user-download-chamber-of-d-talonpaw-svg-png-icon-free-download-175238-on-5b84c95a116717.2809616615354289540713.jpg" width="40" height="40" alt="..."></a></div><div class="media-body"><a href="#" class="anchor-username"><h4 class="media-heading">'+data[i]['user_from']+'</h4></a><a href="#" class="anchor-time">'+data[i]['sent_on']+'</a></div></div></div><div class="col-md-1"><a href="#"><i class="glyphicon glyphicon-chevron-down"></i></a></div></div></section><section class="post-body"><p><strong>'+data[i]['title']+'</strong></p><p>'+data[i]['content']+'</p></section><section class="post-footer" id="post-footer"><hr><div class="post-footer-option container"> <ul class="list-unstyled"><li><a href="#"><i class="glyphicon glyphicon-thumbs-up"></i> Like</a></li><li><a href="#" onClick="commentForm(data[i][\'id\'])"><i class="glyphicon glyphicon-comment"></i> Comment</a></li> <li><a href="#"><i class="glyphicon glyphicon-share-alt"></i> Share</a></li></ul></div></section></div></div></div></div>';
            e = e+'</div>';
            i = i+1;
            $("<div/>",{html:e}).appendTo("#postBox");
        });
    });

$.getJSON("/comments", function(data){
    var i = 0;
    $.each(data, function(){
        if(current_post_id == data['post_id']){
        e = '<div>'
        e = e+'</div>';
        i = i+1;
        $("<div/>",{html:e}).appendTo("#post-footer");
        }
    });
});

function commentForm(id){
    e = '<div class="comment"><form action="/comments" method="post"><table><tr><td><input type="text" placeholder="Write a comment..." id="comment_content"></td><td><input type="submit" value="comment"></td></tr></table></form></div>';
    $("<div/>",{html:e}).appendTo("#post-footer");
}