$(function () {

    String.prototype.format = function(args) {
        if (arguments.length > 0)
        {
            var result = this;
            if (arguments.length == 1 && typeof (args) == "object")
            {
                for (var key in args)
                {
                    var reg = new RegExp("({" + key + "})", "g");
                    result = result.replace(reg, args[key]);
                }
            }
            else
            {
                for (var i = 0; i < arguments.length; i++)
                {
                    if (arguments[i] == undefined)
                    {
                        return "";
                    }
                    else
                    {
                        var reg = new RegExp("({[" + i + "]})", "g");
                        result = result.replace(reg, arguments[i]);
                    }
                }
            }
            return result;
        }
        else
        {
            return this;
        }
    };

  //初始化iframe的高度
  function init_iframe_height(){
    var parent_window_height = parent.window.innerHeight;
    var parent_doc_height = parent.$('html').height();
    var html_height = $('html').height();


    if (parent_window_height-162 > html_height){
       parent.$('iframe').height(parent_window_height-162);
    }else{
      parent.$('iframe').height(html_height);
    };
  };

  init_iframe_height();

  //点击取消按钮执行函数
  function reset() {
    $('form').find('input').val('');
  };

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
  };

  //清空密码输入框
   function clear_pwd() {
     raw_pwdE.val('');
     new_pwd1E.val('');
     new_pwd2E.val('');
   };

  //更改密码点击submit
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
              parent.xtalert.alertSuccessToast(data.message);
              reset();
            } else {
              parent.xtalert.alertErrorToast(data.message);
              reset();
            }
          }
        })
      }


    });

    //点击取消
    $('#cancel').click(function(){
      reset();

     });

    //修改密码结束


  //个人详情页面

  var db_gender = $('#gender').attr('data-gender');

  if(db_gender == '1'){
    $('#gender > label:nth-child(1)').addClass('active')
  };
  if(db_gender == '0'){
    $('#gender > label:nth-child(2)').addClass('active')
  };
  //点击submit
  $('#sumbit-profile').click(function(e){
    e.preventDefault();
    var gender = $('input[name="gender"]:checked').val();
    var birth = $('#date-of-birth').val();
    var phone = $('#phone').val();
    var intro = $('#description').val();
    var name = $('#name').val();

    myajax.post({
      'url':location.href,
      'data':{
        'name':name,
        'gender':gender,
        'birthday':birth,
        'phone':phone,
        'intro':intro
      },
      'success':function(data){
        if(data.code == 200){
          parent.xtalert.alertSuccessToast(data.message);
          location.reload();
        }else{
          parent.xtalert.alertSuccessToast(data.message)
         }
      }
    })

  });


  //修改邮箱
  $('#reset-email').click(function (e) {
    e.preventDefault();
    var raw_pwd = $('#raw-pwd').val();
    var new_email = $('#new-email').val();
    var captcha = $('#email-captcha').val();
    myajax.post({
      'url':location.href,
      'data':{
        'pwd':raw_pwd,
        'email':new_email,
        'captcha':captcha
      },
      'success':function (data) {
        if (data.code == 200){
          parent.xtalert.alertSuccessToast(data.message)
        }else{
          parent.xtalert.alertErrorToast(data.message)
        };
      }
    })

  });

  //点击获取验证码
  $('#captcha-btn').click(function (e) {
    console.log('点击了验证码');
    var new_email = $('#new-email').val();
    myajax.get({
      'url':'/email_captcha/',
      'data':{
        'email':new_email
      },
      'success':function (data) {
                if (data.code == 200){
                    parent.xtalert.alertSuccessToast(data.message)
                }else{
                    parent.xtalert.alertInfo(data.message);
                    
                }
      },
      'fail':function () {
          parent.xtalert.alertNetworkError()
      }

    });

  });

  //注册CMS新用户
  $('#register-submit').click(function (e) {
      var new_pwd1 = $('#new-pwd1').val();
      var new_pwd2 = $('#new-pwd2').val();
      var email = $('#email').val();
      var username = $('#username').val();

      if (new_pwd1 != new_pwd2){
        console.log('两次密码不一至')
      }else{
        myajax.post({
          'url':'/cms_register/',
          'data':{
            'new_pwd1':new_pwd1,
            'new_pwd2':new_pwd2,
            'email':email,
            'username':username
          },
          'success':function (data) {
            if(data.code == 200){
              parent.xtalert.alertSuccessToast(data.message);
              $('#myModal2').modal('hide');
              location.reload()

            }else{
              parent.xtalert.alertErrorToast(data.message)
            }
          }
        })
      }

  });

});



