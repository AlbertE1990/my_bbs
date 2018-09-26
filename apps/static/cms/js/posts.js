$(function(){
    var delete_btn = $('.delete-btn');
    var highlight_btn = $('.highlight-btn');
    var unhighlight_btn = $('.unhighlight-btn');


    highlight_btn.click(function () {
        var post_id = $(this).parent().parent().attr('data-id');
        myajax.post({
            'url':'/cms/hpost/',
            'data':{
                'post_id':post_id
            },
            'success':function (data) {
                if(data.code == 200){
                    location.reload()
                }else{
                    xtalert.alertError(data.messsge)
                }
            },
            'fail':function () {
                xtalert.alertNetworkError()
            }
        })
    });

    unhighlight_btn.click(function () {
        var post_id = $(this).parent().parent().attr('data-id');
        myajax.post({
            'url':'/cms/uhpost/',
            'data':{
                'post_id':post_id
            },
            'success':function (data) {
                if(data.code == 200){
                    location.reload()
                }else{
                    parent.xtalert.alertError(data.messsge)
                }
            },
            'fail':function () {
                parent.xtalert.alertNetworkError()
            }
        })
    });

    delete_btn.click(function () {
         var post_id = $(this).parent().parent().attr('data-id');
         parent.xtalert.alertConfirm({
             'confirmText':'删除',
             'confirmCallback':function () {
                 myajax.post({
            'url':'/cms/dpost/',
            'data':{
                'post_id':post_id
            },
            'success':function (data) {
                if(data.code == 200){
                    location.reload()
                }else{
                    parent.xtalert.alertError(data.messsge)
                }
            },
            'fail':function () {
                parent.xtalert.alertNetworkError()
            }
        })
             }
         });

    });


})