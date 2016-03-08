$(function(){
    $(".my-tabs").each(function(index,ele){
        $ele = $(this);
        $ele.children(".my-tabs-nav").find("li").on('mouseenter', function(event) {
            event.preventDefault();
            var i = $(this).index();
            $(this).siblings().removeClass("my-tabs-active");
            $(this).addClass("my-tabs-active");
            $ele.children(".my-tabs-bd").find('.my-tabs-panel').removeClass("my-tabs-active")
            $ele.children(".my-tabs-bd").find('.my-tabs-panel').eq(i).addClass('my-tabs-active')
        });
    });
});