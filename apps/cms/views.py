# -*- coding:utf-8 -*-
from flask import Blueprint,render_template,request,session,redirect,url_for,g
from flask.views import MethodView
from .forms import LoginForm,ResetPasswordForm,ProfileForm
from .modles import CMSUser,CMSUserDetail
from utils import restful
from config import CMS_USER_ID
from .decorators import login_required
from exts import db
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


#个人信息
class ProfileView(MethodView):
    decorators = [login_required]

    def get(self):
        ud = g.user.detail
        print(str(ud.birthday))
        print('avatar',ud.avatar)

        return render_template('cms/cms_profile.html')

    def post(self):
        print(request.form)
        form = ProfileForm(request.form)
        print(form)
        if form.validate():
            data={}
            data['uid'] = g.user.id
            data['name'] = form.name.data
            data['phone'] = form.phone.data
            data['birthday'] = form.birthday.data
            data['gender'] = form.gender.data
            data['intro'] = form.intro.data
            data['avatar'] = form.avatar.data
            detail = CMSUserDetail(**data)
            db.session.add(detail)
            db.session.commit()
            return restful.success('信息保存成功！')
        else:
            print(form.errors)
            return restful.params_error('信息保存失败！')

bp.add_url_rule('/profile', view_func=ProfileView.as_view('profile'))


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


bp.add_url_rule('/login/',endpoint='login',view_func=LoginView.as_view('login'))

