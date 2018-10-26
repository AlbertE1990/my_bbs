$(function(){

    function init_select(){
        var current_url = document.URL;
        var current_board = current_url.match(/board_id=(\d+)/);
        var current_per_page = current_url.match(/per_page=(\d+)/);
        current_board = current_board?current_board[1]:0;
        current_per_page = current_per_page?current_per_page[1]:10;
        $('#per-page option[value={0}]'.format(current_per_page)).prop("selected", true);
        $('#board option[value={0}]'.format(current_board)).prop("selected", true);
    }
    init_select();
     //选择框选项改变事件
    $('select').change(function () {
      var per_page = $('#per-page').val();
      var board_id = $('#board').val();
      var base_url = "/posts/?per_page={per_page}&board_id={board_id}";
      var next= base_url.format({per_page:per_page,board_id:board_id});
      location.href=next;

    });

    var delete_btn = $('.delete-btn');
    var highlight_btn = $('.highlight-btn');

    highlight_btn.click(function () {
        var post_id = $(this).parent().parent().attr('data-id');
        var type = $(this).attr('data-type');
        myajax.post({
            'url':'/hpost/',
            'data':{
                'post_id':post_id,
                'type':type
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

    delete_btn.click(function () {
         var post_id = $(this).parent().parent().attr('data-id');
         parent.xtalert.alertConfirm({
             'confirmText':'删除',
             'confirmCallback':function () {
                 myajax.post({
            'url':'/dpost/',
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

    //顶置处理
    $('.top-post-btn').click(function (e) {
        console.log('顶置程序');
        var post_id = $(this).parent().parent().attr('data-id');
        var type = $(this).attr('data-type');
        myajax.post({
            'url':'/tpost/',
            'data':{
                'post_id':post_id,
                'type':type
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


})