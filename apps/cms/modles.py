# -*- coding:utf-8 -*-
from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
import shortuuid
from config import SECRET_KEY
from flask import url_for



class CMSUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.String(50),primary_key=True)
    username = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(50),nullable=False,unique=True)
    _password = db.Column(db.String(150),nullable=False)
    join_time = db.Column(db.DateTime,default=datetime.now)

    def __init__(self,username,email,password):
        self.email = email
        self.username = username
        self.password = password
        self.id = shortuuid.uuid(email+str(SECRET_KEY))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,raw_password):
       self._password = generate_password_hash(raw_password)

    def check_password(self,raw_password):
        return check_password_hash(self.password,raw_password)

    def __repr__(self):
        return '<CMSUser username:%s>'%self.username

    __str__ = __repr__


class CMSUserDetail(db.Model):
    __tablename__ = 'cms_user_detail'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    uid = db.Column(db.String(50),db.ForeignKey('cms_user.id'))
    name = db.Column(db.String(50),nullable=True)
    phone = db.Column(db.String(20),nullable=True)
    birthday = db.Column(db.Date,nullable=True)
    gender = db.Column(db.Integer,nullable=True)
    intro= db.Column(db.Text,nullable=True)
    _avatar = db.Column(db.String(255),nullable=True)
    user= db.relationship('CMSUser',backref=db.backref('detail',uselist=False),uselist=False)


    @property
    def avatar(self):
        if not self._avatar:
            if self.gender == 1:
                avatar_img = url_for('static', filename='cms/images/d1.png')
            else:avatar_img = url_for('static', filename='cms/images/d0.png')
            return avatar_img
    @avatar.setter
    def avatar(self,avatar_img):
        self._avatar = avatar_img


    def __repr__(self):
        return '<CMSUserDetail:%s>'%self.name

    __str__ = __repr__


class CMSPermission():
    #所有权限
    ALL_PERMISSION = 0b11111111
    #1.访问者权限
    VISTOR         = 0b00000001
    #2.管理帖子权限
    POSTER         = 0b00000010
    #3.管理评论权限
    COMMENTER      = 0b00000100
    #4.管理版块权限
    BOARDER        = 0b00001000
    #5.管理前台用户的权限
    FRONTUSER      = 0b00010000
    #6.管理后台用户的权限
    CMSUSER        = 0b00100000
    #7.管理后台管理员的权限
    ADMINER        = 0b01000000


CmsRoleUser = db.Table(
    'cms_role_user',
    db.Column('cms_role_id',db.Integer,db.ForeignKey('cms_role.id'),primary_key=True),
    db.Column('cms_user_id',db.String(50),db.ForeignKey('cms_user.id'),primary_key=True)
)


class CMSRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    permissions = db.Column(db.Integer,default=CMSPermission.VISTOR)
    users = db.relationship('CMSUser',secondary=CmsRoleUser,backref=db.backref('role',uselist=False))
    def __repr__(self):
        return "<CMSURole(name:%s)>" % self.name
