from flask import render_template, request, jsonify
from . import bp
from utils import restful


@bp.app_errorhandler(403)
def forbidden(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        return restful.permission_error()
    return render_template('errors/front_403.html'), 403


# @bp.app_errorhandler(404)
# def page_not_found(e):
#     if request.accept_mimetypes.accept_json and \
#             not request.accept_mimetypes.accept_html:
#         return restful.page_not_found()
#     print('404')
#     return render_template('errors/front_404.html'), 404


@bp.app_errorhandler(500)
def internal_server_error(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        return restful.server_error()
    return render_template('errors/front_500.html'), 500
