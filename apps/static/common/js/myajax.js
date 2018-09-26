/**
 * Created by albert on 2017/11/10.
 */
// 对jquery的ajax的封装

'use strict';
var myajax = {
	'get':function(args){
		args['method'] = 'GET';
		this._ajax(args)
	},
	'post':function (args) {
		args['method'] = 'POST';
		this._ajax(args)
    },
	'_ajax':function (args) {
		this._ajaxSetup();
		$.ajax(args);
    },
	'_ajaxSetup':function () {
		$.ajaxSetup({
			'beforeSend':function (jqXHR,settings) {
				if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    var csrftoken = $('meta[name=csrf_token]').attr('content');
                    jqXHR.setRequestHeader("X-CSRFToken", csrftoken)
                }
            }
		})
    }

};
