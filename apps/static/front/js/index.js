$(function(){

    //格式化字符串
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


    //从网页链接获取版块id
    function get_sort() {
        var current_url = location.href;
        var p = /sort=(\d)/;
        var sort_reg = p.exec(current_url);

        if (sort_reg){
            var sort = parseInt(sort_reg[1])
        }else{
            sort=0
        }
        return sort

    };

    //从网页链接获取sort
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
    //给板块加上active
    var bd = $('.list-group ');
    var board = get_board_id();

    var current_bd = bd.find('a[board={0}]'.format(board));
    current_bd.siblings().removeClass('active');
    current_bd.addClass('active');
    //
    //给分类加上active
    var current_sort =  get_sort();
    console.log(current_sort);
    $(".post-sort ").find('li[sort={0}]'.format(current_sort)).addClass('active');

    //点击分类按钮
    $('.post-head li').click(function (e) {
        e.preventDefault();
      $(this).siblings().removeClass('active');
      $(this).addClass('active');
      var sort = $(this).attr('sort');
      var board = get_board_id();
      location.href = '/?bd={0}&sort={1}'.format(board,sort)


    });


});