from flask import request,render_template,redirect,url_for
from . import bp
from flask_login import current_user
from ..models import Permission,PermissionDesc,Group


@bp.before_request
def before_request():
    print("front before_request:", current_user)
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirm \
                and request.endpoint != 'front.unconfirm' \
                and request.endpoint != 'front.resend_confirmation' \
                and request.endpoint != 'front.confirm' \
                and request.endpoint != 'static':
            return redirect(url_for('front.unconfirm'))




@bp.app_context_processor
def inject_permissions():
    return dict(Permission=Permission,PermissionDesc=PermissionDesc,Group=Group)