/**

 */

$(function () {

   var window_h = $(window).height();

  $('.sub-menu li').click(function () {
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
  })


});