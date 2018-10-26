$(function(){
  var replyE = $('#reply');
  var submit = $('#reply-btn');
  var post_id = replyE.attr('data-post');
  //快速评论
  submit.click(function () {
    var content = replyE.val();
    myajax.post({
      'url':'/acomment/',
      'data':{
        'post_id':post_id,
        'content':content
      },
      'success':function (data) {
        if(data.code ==200){
          location.reload()
        }else{
          xtalert.alertError(data.message)
        }
      }
    })
  });

  //收藏功能
  $('div.post-head-group > div > a > span').click(function (e) {
    e.preventDefault();
    var book_status = $(this).attr('data-book');
    myajax.get({
      'url':'/mark/',
         'headers': {
            "X-Requested-Accept": 'json'
        },
      'data':{
        'post_id':post_id,
        'book_status':book_status
      },
      'success':function (data) {
        if(data.code ==200){
          location.reload()
        }else{
          xtalert.alertError(data.message)
        }
      }
    })
  });

  //关注功能
  $('.follow').click(function (e) {
    e.preventDefault();
    var url = $(this).attr('data-href');
    myajax.get({
      'url':url,
      'success':function (data) {
        if(data.code ==200){
          location.reload()
        }else{
          xtalert.alertError(data.message)
        }
      }
    })
  });

  //申请功能
    $('.apply').click(function (e) {
        var type = $(this).attr('data-type');
        myajax.post({
            'url':'/apply/',
            'data':{
                'type':type,
                'pid':post_id
            },
            'success':function (data) {
                if (data.code == 200){
                    xtalert.alertSuccessToast(data.message)
                }else{
                    xtalert.alertErrorToast(data.message)
                }
            }
        })
    });

    //顶置处理
    $('.top-post').click(function (e) {
        console.log('顶置处理');
        var type = $(this).attr('data-type');
        var url = $(this).attr('data-url');
        console.log(type);
        myajax.post({
            'url':url,
            'data':{
                'type':type,
                'post_id':post_id
            },
            'success':function (data) {
                if(data.code == 200){
                    xtalert.alertSuccessToast(data.message)
                }else{
                    xtalert.alertErrorToast(data.message)
                }
            }
        })
    })

})