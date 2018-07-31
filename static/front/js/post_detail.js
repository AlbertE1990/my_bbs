$(function(){
    var replyE = $('#reply');
    var submit = $('.submit-btn button');
    var post_id = replyE.attr('data-post');
    submit.click(function () {
        var user_id = replyE.attr('data-author');
        if (!user_id){
            xtalert.alertError('请先登录！');
            return false
        }
        var content = replyE.val();
        myajax.post({
            'url':'/acomment/',
            'data':{
                'author_id':user_id,
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

    $('div.post-head-group > div > a > span').click(function (e) {
      e.preventDefault();
      var book_status = $(this).attr('data-book');
      myajax.get({
        'url':'/mark/',
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

})