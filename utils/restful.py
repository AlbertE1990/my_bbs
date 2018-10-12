# -*- coding:utf-8 -*-
from flask import jsonify


class HttpCode():
    ok = 200
    notfound = 404
    unautherror = 401
    permissionerror = 403
    paramserror = 400
    servererror = 500


def restful_result(code,message,data):
    return jsonify(code=code,message=message,data=data)


def success(message=None,data=None):
    return restful_result(code=HttpCode.ok,message=message,data=data)


def unauth_error(message='未认证通过',data=None):
    return restful_result(code=HttpCode.unautherror, message=message, data=data)


def server_error(message="服务器内部错误",data=None):
    return restful_result(code=HttpCode.servererror, message=message, data=data)


def permission_error(message="无此权限",data=None):
    return restful_result(code=HttpCode.permissionerror, message=message, data=data)


def params_error(message='参数错误',data=None):
    return restful_result(code=HttpCode.paramserror, message=message, data=data)


def page_not_found(message='未找到此页面',data=None):
    return restful_result(code=HttpCode.notfound,message=message,data=data)

