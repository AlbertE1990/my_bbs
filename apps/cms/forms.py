# -*- coding:utf-8 -*-
from wtforms import Form,StringField,BooleanField,IntegerField
from wtforms.validators import Email,Length,EqualTo,DataRequired,Regexp
import re

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
    captcha = StringField(validators=[Length(min=4,max=4, message='请输入4位验证码！')])


def validate_email(email):
    r = re.compile("^[a-zA-Z0-9_]+@[a-zA-Z0-9_]+\.[a-zA-Z]{1,4}$")
    if re.match(r, email):
        return True
    return False
