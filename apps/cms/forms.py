# -*- coding:utf-8 -*-
from wtforms import Form,StringField,BooleanField,IntegerField
from wtforms.validators import Email,Length,EqualTo,DataRequired,Regexp,ValidationError,InputRequired
import re
from flask import g
from utils import my_redis
from .modles import CMSUser
from apps.forms import BaseForm


class LoginForm(Form):
    email = StringField(validators=[Email(message="邮箱格式不正确!")])
    password = StringField(validators=[Length(min=6,message='请输入6位以上的密码！')])
    remember = BooleanField()


class ResetPasswordForm(Form):
    raw_pwd = StringField(validators=[Length(min=6, message='请输入6位以上的密码！')])
    new_pwd1 = StringField(validators=[Length(min=6, message='请输入6位以上的密码！')])
    new_pwd2 = StringField(validators=[EqualTo('new_pwd1')])


class ProfileForm(Form):
    # uid = StringField(validators=[Required])
    name = StringField(validators=[DataRequired()])
    phone = StringField(validators=[DataRequired()])
    # birthday = StringField(validators=[Regexp('^\d{4}-\d{2}-\d{2}$')])
    birthday = StringField()
    gender = StringField()
    intro = StringField()
    avatar = StringField()

class ResetEmailForm(Form):

    pwd = StringField(validators=[Length(min=6, message='请输入6位以上的密码！')])
    email = StringField(validators=[Email(message='邮箱格式不正确！')])
    captcha = StringField(validators=[Length(min=6,max=6, message='请输入6位验证码！')])

    def validate_pwd(self,field):
        if not g.user.check_password(field.data):
            raise ValidationError('密码错误！')

    def validate_email(self,field):
        if field.data == g.user.email:
            raise ValidationError('要修改的邮箱和原邮箱一致，你确定是要修改邮箱?')

    def validate_captcha(self,field):
        email = self.email.data
        if field.data != my_redis.get(email).decode('utf-8'):
            raise ValidationError('验证码错误！')


def validate_email(email):
    r = re.compile("^[a-zA-Z0-9_]+@[a-zA-Z0-9_]+\.[a-zA-Z]{1,4}$")
    if not re.match(r, email):
        return {'flag':False,'message':'邮箱格式错误!'}
    if email == g.user.email:
        return {'flag':False,'message':'要修改的邮箱和原邮箱一致，你确定是要修改邮箱?'}
    return {'flag':True}


class RegisterForm(Form):

    email = StringField(validators=[Email(message="邮箱格式不正确!")])
    new_pwd1 = StringField(validators=[Length(min=6, message='请输入6位以上的密码！')])
    new_pwd2 = StringField(validators=[EqualTo('new_pwd1')])
    username = StringField(validators=[DataRequired(message="用户名不能为空！")])

    def validate_email(self,field):
        email = field.data
        if CMSUser.query.filter_by(email=email).first():
            raise ValidationError('该邮箱已经注册！')


class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图片名称！')])
    image_url = StringField(validators=[InputRequired(message='请输入轮播图片链接！')])
    link_url = StringField(validators=[InputRequired(message='请输入轮播图片跳转链接！')])
    priority = IntegerField(validators=[InputRequired(message='请输入轮播图片优先级！')])
    id = StringField()

class AddBoardForm(BaseForm):
    name = StringField(validators=[InputRequired('请输入板块名称！')])
    id = StringField()
