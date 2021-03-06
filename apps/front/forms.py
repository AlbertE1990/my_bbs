from apps.forms import BaseForm
from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,IntegerField,SubmitField,PasswordField,Form
from wtforms.validators import Regexp,InputRequired,EqualTo,Length,ValidationError,Email
from utils import my_redis
from flask import session
from ..models import User


class SignupForm(FlaskForm):

    telephone = StringField('电话',validators=[Regexp(r"1[345789]\d{9}",message='请输入正确的手机号码！')])
    username = StringField('用户名',validators=[Length(min=2,max=20,message='用户名长度为2-20个字符！')])
    password1 = PasswordField('密码',validators=[Length(min=6,max=20,message='密码长度为6-20个字符！')])
    password2 = PasswordField('重复密码',validators=[EqualTo('password1',message='两次密码不相等')])
    email = StringField('邮箱',validators=[Email()])
    graph_captcha = StringField('验证码',validators=[Regexp(r"[0-9a-zA-Z]{4}",message='验证码格式错误！')])
    submit = SubmitField('注册')

    def validate_graph_captcha(self,field):
        graph_captcha = field.data
        singup_captcha = session.get('signup_captcha')
        if not singup_captcha:
            raise ValidationError('图形验证码发生错误')
        if graph_captcha.lower() != singup_captcha.lower():
            raise ValidationError('验证码错误')

    def validate_email(self,field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('该邮箱已经注册')

    def validate_telephone(self,field):
        user = User.query.filter_by(telephone=field.data).first()
        if user:
            raise ValidationError('该手机已经注册')




class LoginForm(FlaskForm):

    telephone = StringField(validators=[Regexp(r"1[345789]\d{9}", message='请输入正确的手机号码！')])
    password = PasswordField(validators=[Length(min=6,max=20,message='密码长度为6-20个字符！')])
    graph_captcha = StringField()
    remember = BooleanField('记住我')
    submit = SubmitField('登陆')

    def validate_graph_captcha(self, field):
        graph_captcha = field.data
        graph_captcha_session = session.get('login_captcha')
        if not graph_captcha_session:
            raise ValidationError('图形验证码发生错误')
        if graph_captcha.lower() != graph_captcha_session.lower():
            raise ValidationError('验证码错误')


class AddPostForm(FlaskForm):
    title = StringField(validators=[InputRequired(message='请输入标题！')])
    content = StringField(validators=[InputRequired(message='请输入内容！')])
    board_id = IntegerField(validators=[InputRequired(message='请输入板块ID！')])


class AddCommentForm(BaseForm):
    content = StringField(validators=[InputRequired(message='请输入内容！')])
    post_id = IntegerField(validators=[InputRequired(message='系统没有获取到帖子ID！')])
    # author_id = StringField(validators=[InputRequired(message='系统没有获取到用户ID不！')])


#重置密码验证邮箱
class PasswordResetRequestForm(FlaskForm):
    email = StringField('电子邮箱：',validators=[Email(message='请输入正确的电子邮箱！'),InputRequired()])
    submit = SubmitField('点击验证')


#
class PasswordResetForm(FlaskForm):
    password = PasswordField('新密码：', validators=[InputRequired(), EqualTo('password2', message='两次密码不相等！'),Length(min=6,message='密码长度必须不小于6!')])
    password2 = PasswordField('再次确认', validators=[InputRequired()])
    submit = SubmitField('重置密码')