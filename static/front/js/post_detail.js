$(function(){
    var replyE = $('#reply');
    var submit = $('.submit-btn button');
    submit.click(function () {
        var user_id = replyE.attr('data_author');
        if (!user_id){
            xtalert.alertError('请先登录！');
            return false
        }
        var post_id = replyE.attr('data_post');
        var content = replyE.val();


        zlajax.post({
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
    })

})