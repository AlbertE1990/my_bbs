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

})