/**

 */

$(function () {

   var window_h = $(window).height();

  $('#nav li').click(function () {
      var src = $(this).attr('data-src');
      $('iframe[name=icms]').attr('src',src);
      $(this).addClass('current').siblings('li').removeClass('current');

  });

  //.wrapper 高度
  function wrapper_h() {
    var wrapperE = $('.wrapper');
    wrapperE.css('min-height',(window_h-114)+'px')

  };

  wrapper_h();

  $(window).resize(function () {
    // container_h()
  });

  //消除空格
  function Trim(str){
  return str.replace(/(^\s*)|(\s*$)/g,"");
  }

  // 自动隐藏没有权限的菜单
  function menu_hidden() {
    var menus =  $('#nav').children();

    menus.each(function (index, element) {
      var sub_menus = $(element).find('li');
      var menu_name = Trim($(element).children('a').text());
      if (sub_menus.length == 0 &&  menu_name!= '首页'){
        $(element).css('display','none')
      }
    })
  };

  menu_hidden()





});