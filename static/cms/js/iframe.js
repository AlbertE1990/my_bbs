$(function () {

  //初始化iframe的高度
  var iframe_body_heigth = $(document).height();
  console.log('iframe_body_heigth:',iframe_body_heigth);
  parent.$('iframe').height(iframe_body_heigth);


  //修改密码

  //密码验证
  function validate_pwd() {
    var raw_pwd = $('#raw-pwd').val();
    var new_pwd1 = $('#new-pwd1').val();
    var new_pwd2 = $('#new-pwd2').val();
    if (new_pwd1 != new_pwd2) {

      $('fieldset > div:nth-child(3)').addClass('has-error');
      $('fieldset > div:nth-child(3) > div.col-sm-3').empty();
      $('fieldset > div:nth-child(3) > div.col-sm-3').append('<p class="help-block"><i class="icon-exclamation-sign"></i> 两次输入的密码不一样！</p>');
      console.log('两次密码不一样');
      return false
    }else if(new_pwd1.length < 6){
      $('fieldset > div:nth-child(3)').addClass('has-error');
      $('fieldset > div:nth-child(3) > div.col-sm-3').empty();
      $('fieldset > div:nth-child(3) > div.col-sm-3').append('<p class="help-block"><i class="icon-exclamation-sign"></i> 密码太短，必须大于6位！</p>');
      return false
    }else{
      $('fieldset > div:nth-child(3) > div.col-sm-3').empty();
      $('fieldset > div:nth-child(3)').removeClass('has-error');
      return true
    }
  }
    ;

  //点击submit
    var submitE = $('#reset-pwd');
    submitE.click(function (e) {
      e.preventDefault();
      var raw_pwd = $('#raw-pwd').val();
      var new_pwd1 = $('#new-pwd1').val();
      var new_pwd2 = $('#new-pwd2').val();
      if(validate_pwd()) {
        myajax.post({
          'url': '/cms/resetpwd',
          'data': {
            'raw_pwd': raw_pwd,
            'new_pwd1': new_pwd1,
            'new_pwd2': new_pwd2
          },
          'success': function (data) {
            if (data.code == 200) {
              console.log('密码修改成功！')
            } else {
              console.log(data.message)
            }
          }
        })
      };


    });
});



