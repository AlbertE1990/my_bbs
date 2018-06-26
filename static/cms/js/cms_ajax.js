$(function () {

    $('#profile-ajax').click(function (e) {
        e.preventDefault();
        $(this).addClass('current');
        myajax.get({
            'url':'/cms/profile_ajax',
            'success':function (data) {
                $('.content').html('');
                $('.content').append(data);
            }
        });
    });

});