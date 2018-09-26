$(function(){
    var $onavmenu=$(".nav_menu"),
        $onavmenuItem=$onavmenu.find(".menu_item"),
        $onavlabel=$onavmenu.find(".nav_label"),
        top=$onavmenu.find(".current").position().top;
    $onavlabel.css({top:parseInt(top)});$onavmenu.on({mouseleave:function(){$onavlabel.animate({top:parseInt(top)},200)}});
    $onavmenuItem.on({mouseenter:function(){var top=$(this).position().top;
    $onavlabel.animate({top:parseInt(top)},200)},mouseleave:function(){$onavlabel.stop()}});
    var oImg=$(".head img");
    if(oImg.length>0&&typeof oImg.attr("data-original")!="undefined"){
        $(".head img").lazyload({effect:"fadeIn",threshold:100})}
});
