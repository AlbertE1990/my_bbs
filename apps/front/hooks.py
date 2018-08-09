from flask import g,session,request,render_template,redirect,url_for
from .views import bp
import config
from .models import FrontUser

@bp.before_request
def before_request():
    user_id = session.get(config.FRONT_USER_ID)
    print('front hooks print front_user_id:',user_id)
    if user_id:
        user = FrontUser.query.get(user_id)
        if user:
            g.front_user = user
        if not user.confirm \
                and request.endpoint != 'front.unconfirm' \
                and request.endpoint != 'front.resend_confirmation' \
                and request.endpoint != 'front.confirm' \
                and request.endpoint != 'static':
            return redirect(url_for('front.unconfirm'))


@bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('front/front_404.html'),404