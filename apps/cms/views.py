# -*- coding:utf-8 -*-
from flask import Blueprint,render_template,request,session,redirect,url_for,g
from flask.views import MethodView
from .forms import LoginForm,ResetPasswordForm
from .modles import CMSUser
from utils import restful
from config import CMS_USER_ID
from .decorators import login_required
import os

bp = Blueprint('cms',__name__,url_prefix='/cms')

import os
base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))



@bp.route('/')
@login_required
def index():

    return render_template('cms/cms_index.html')


#登陆
class LoginView(MethodView):

    def get(self):
        return render_template('cms/cms_login.html')

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[CMS_USER_ID] = user.id
                session.permanent = remember
                return restful.success(message='登录成功!')
            else:
                return restful.params_error(message='邮箱或者密码错误!')
        else:
            return restful.params_error(message= '邮箱或者密码格式错误！')

#注销
@bp.route('/logout')
@login_required
def logout():
    del session[CMS_USER_ID]
    return redirect(url_for('cms.login'))


@bp.route('/profile')
@login_required
def profile():

    return render_template('cms/cms_profile.html')

#修改密码
class ResetPasswordView(MethodView):

    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetPasswordForm(request.form)
        if form.validate():
            raw_pwd = form.raw_pwd.data
            new_pwd = form.new_pwd1.data
            if g.user.check_password(raw_pwd):
                g.user.password = new_pwd
                return restful.success('密码修改成功！')
            else:
                return restful.params_error('原始密码错误！')
        else:
            return restful.params_error('原始密码错误!')

bp.add_url_rule('/resetpwd',view_func=ResetPasswordView.as_view('resetpwd'))



@bp.route('/resetemail')
@login_required
def reset_email():

    return render_template('cms/cms_resetemail.html')


@bp.route('/profile_ajax')
@login_required
def profile_ajax():
    file = os.path.join(base_path, 'templates/cms/cms_profile_ajax.html')
    with open(file,'r',encoding='utf-8') as f:
        profile_ajax_doc = f.read()
    return profile_ajax_doc


@bp.route('/profile_iframe')
@login_required
def profile_iframe():
    data = 'this is profile'
    return data



bp.add_url_rule('/login/',endpoint='login',view_func=LoginView.as_view('login'))

