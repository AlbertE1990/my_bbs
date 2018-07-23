$(function(){

    //格式化字符串
    String.prototype.format = function(args) {
    var result = this;
    if (arguments.length < 1) {
        return result;
    }

    var data = arguments;       //如果模板参数是数组
    if (arguments.length == 1 && typeof (args) == "object") {
        //如果模板参数是对象
        data = args;
    }
    for (var key in data) {
        var value = data[key];
        if (undefined != value) {
            result = result.replace("{" + key + "}", value);
        }
    }
    return result;
    };

    //从网页链接获取版块id
    function get_board_id() {
        var current_url = location.href;
        var p = /bd=(\d)/;
        var board_id_reg = p.exec(current_url);

        if (board_id_reg){
            var board_id = parseInt(board_id_reg[1])
        }else{
            board_id=0
        }
        return board_id

    };

    var bd = $('.list-group ');
    var board = get_board_id();

    var current_bd = bd.find('a[board={0}]'.format(board));
    current_bd.siblings().removeClass('active');
    current_bd.addClass('active');


    $('.post-head li').click(function (e) {
        e.preventDefault();
      $(this).siblings().removeClass('active');
      $(this).addClass('active');
      var order = $(this).attr('order');
      var board = get_board_id();
      location.href = '/?bd={0}&order={1}'.format(board,order)


    });


});