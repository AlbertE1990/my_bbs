$(function () {
  var iframe_body_heigth = $(document).height();
  console.log('iframe_body_heigth:',iframe_body_heigth);
  parent.$('iframe').height(iframe_body_heigth);
});