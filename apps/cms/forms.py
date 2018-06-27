# -*- coding:utf-8 -*-
from wtforms import Form,StringField,BooleanField
from wtforms.validators import Email,Length,EqualTo

class LoginForm(Form):
    email = StringField(validators=[Email(message="邮箱格式不正确!")])
    password = StringField(validators=[Length(min=6,message='请输入6位以上的密码！')])
    remember = BooleanField()

class ResetPasswordForm(Form):
    raw_pwd = StringField(validators=[Length(min=6, message='请输入6位以上的密码！')])
    new_pwd1 = StringField(validators=[Length(min=6, message='请输入6位以上的密码！')])
    new_pwd2 = StringField(validators=[EqualTo('new_pwd1')])