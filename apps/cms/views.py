# -*- coding:utf-8 -*-
from flask import Blueprint,render_template,request,session,redirect,url_for,g
from flask.views import MethodView
from .forms import LoginForm,ResetPasswordForm,ProfileForm,ResetEmailForm,validate_email,RegisterForm
from .modles import CMSUser,CMSUserDetail
from utils import restful,my_redis
from config import CMS_USER_ID
from .decorators import login_required
from exts import db,mail
import string
import random
from flask_mail import Message

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
                return restful.params_error(message='邮箱或者密码错误！')

        else:
            print(form.errors)
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
        return render_template('cms/cms_profile.html')

    def post(self):
        #有待优化
        detail = g.user.detail
        form = ProfileForm(request.form)
        if form.validate():
            data = {}
            data['uid'] = g.user.id
            data['name'] = form.name.data
            data['phone'] = form.phone.data
            data['birthday'] = form.birthday.data
            data['gender'] = form.gender.data
            data['intro'] = form.intro.data
            data['avatar'] = form.avatar.data
            d = {}
            for k, v in data.items():
                if v != '':
                    d[k] = v
            if detail:
                detail.name = d.get('name')
                detail.phone = d.get('phone')
                detail.birthday = d.get('birthday')
                detail.gender = d.get('gender')
                detail.intro = d.get('intro')
                detail.avatar = d.get('avatar')
            else:
                detail = CMSUserDetail(**d)
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



#修改邮箱
class ResetEmailView(MethodView):

    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            g.user.email = form.email.data
            db.session.commit()
            return restful.success(message='邮箱修改成功！')
        else:
            print(form.errors)
            return restful.params_error(message='数据错误！')


#邮箱验证码
@bp.route('/email_captcha/')
@login_required
def email_captcha():
    email = request.args.get('email')
    validate_res = validate_email(email)
    if not validate_res['flag']:
        return restful.params_error(message=validate_res['message'])

    source = list(string.ascii_lowercase) + list(string.digits)
    captcha = "".join(random.sample(source, 6))
    body = '您的验证码是：%s,验证码有效期为5分钟' % captcha
    message = Message('CMS管理后台邮件发送', recipients=[email], body=body)
    my_redis.set(email,captcha,ex=300)
    print('生成的验证码',captcha)

    try:
        mail.send(message=message)
    except:
        return restful.server_error()
    return restful.success(message="邮件发送成功请注意查收！")


#cms用户管理
@bp.route('/cms_users/')
@login_required
def cms_users():
    users = CMSUser.query.all()
    return render_template('cms/cms_user_manage.html',users=users)


#注册cms用户

def create_cms_user(username,password,email):
    user = CMSUser(username=username,password=password,email=email)
    db.session.add(user)
    db.session.commit()


@bp.route('/cms_register/',methods=['post'])
@login_required
def cms_register():
    form = RegisterForm(request.form)
    if form.validate():
        username = form.username.data
        email = form.email.data
        password = form.new_pwd1.data
        create_cms_user(username=username, password=password, email=email)
        return restful.success(message='添加新用户成功！')
    else:
        print(form.errors)
        return restful.params_error(message='注册数据有问题')






bp.add_url_rule('/resetpwd',view_func=ResetPasswordView.as_view('resetpwd'))
bp.add_url_rule('/resetemail',view_func=ResetEmailView.as_view('resetemail'))
bp.add_url_rule('/login/',endpoint='login',view_func=LoginView.as_view('login'))

