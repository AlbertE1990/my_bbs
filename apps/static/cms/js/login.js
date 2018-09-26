$(function () {
    var emailE = $('#email');
    var pwdE = $('#password');
    var rememberE = $('input[name="remember"]');

    function clear() {
        emailE.val('');
        pwdE.val('');
        rememberE.prop('checked',false);
    }

    $("button[type='submit']").click(function (event) {
        event.preventDefault();
        var email = emailE.val();
        var pwd = pwdE.val();
        var remember = rememberE.prop('checked');
        myajax.post({
            'url':'/login/',
            'data':{
                'email':email,
                'password':pwd,
                'remember':remember

            },
            'success':function(data){
                if(data.code == 200){
                    location.href='/'
                }else{
                    clear();
                }
            }

        })

    });

    //iframe注销带动主页面注销
  if (window.location.pathname == '/cms/login/'){
    if (parent.window != window){
      parent.window.location.href = (location.protocol+'//'+location.host + '/cms/login/');
    }

  }else{
    console.log('mei zhu xiao')
  };

});