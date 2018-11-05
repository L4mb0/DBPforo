function get_posts(){
    $.getJSON("/posts", function(data){
        var i = 0;
        $.each(data, function(){
            e = e+'<div>'+data[i]['content']+'</div>';
            e = e+'</div>';
            i = i+1;
            $("<div/>",{html:e}).appendTo("#postBox");
        })
    })
}
