$(function () {

  //初始化iframe的高度
  var iframe_body_heigth = $(document).height();
  parent.$('iframe').height(iframe_body_heigth);


  //修改密码开始
   var raw_pwdE = $('#raw-pwd');
   var new_pwd1E = $('#new-pwd1');
   var new_pwd2E = $('#new-pwd2');

   //密码验证
  function validate_pwd() {
    var raw_pwd = raw_pwdE.val();
    var new_pwd1 = new_pwd1E.val();
    var new_pwd2 = new_pwd2E.val();
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

  //清空密码输入框
   function clear_pwd(){
     raw_pwdE.val('');
     new_pwd1E.val('');
     new_pwd2E.val('');
   }

  //点击submit
    $('#reset-pwd').click(function (e) {
      e.preventDefault();
      var raw_pwd = raw_pwdE.val();
      var new_pwd1 = new_pwd1E.val();
      var new_pwd2 = new_pwd2E.val();
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
              xtalert.alertSuccessToast(data.message)
              clear_pwd()
            } else {
              xtalert.alertErrorToast(data.message)
               clear_pwd()
            }
          }
        })
      }


    });

    //点击取消
    $('#cancel-pwd').click(function(){
      clear_pwd()
     });

    //修改密码结束

  $('#cancel').click(function(){
    $(this).parents('form').find('input').val('');
  });
  //添加个人详情

  $('#sumbit-profile').click(function(e){
    e.preventDefault();
    var gender = $('#gender').find('input[name="gender"]:checked').val();
    var birth = $('#date-of-birth').val();
    var phone = $('#phone').val();
    var intro = $('#description').val();
    var name = $('#name').val();

    myajax.post({
      'url':'/cms/profile',
      'data':{
        'name':name,
        'gender':gender,
        'birthday':birth,
        'phone':phone,
        'intro':intro
      },
      'success':function(data){
        if(data.code == 200){
          xtalert.alertSuccessToast(data.message);


        }else{
          xtalert.alertSuccessToast(data.message)
         }
      }
    })


  });




});



