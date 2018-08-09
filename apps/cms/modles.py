# -*- coding:utf-8 -*-
from exts import db,login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
import shortuuid
from config import SECRET_KEY
from flask import url_for
from flask_login import UserMixin
from faker import Faker
from random import randint,choice
import json


class CMSPermission():
    #所有权限
    ALL_PERMISSION = 0b11111111
    #1.访问者权限
    VISTOR         = 0b00000001
    #2.管理帖子权限
    POSTER         = 0b00000010
    #3.管理评论权限
    COMMENTER      = 0b00000100
    #4.管理版块权限,管理轮播图
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


class CMSUser(UserMixin,db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.String(50),primary_key=True)
    username = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(50),nullable=False,unique=True)
    phone = db.Column(db.String(20), nullable=True)
    _password = db.Column(db.String(150),nullable=False)
    name = db.Column(db.String(50), nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    #0女 1男
    gender = db.Column(db.Integer, nullable=True)
    intro = db.Column(db.Text, nullable=True)
    avatar = db.Column(db.String(255), nullable=True)
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

    def has_permission(self,permission):
        if self.role.permissions & permission == permission:
            return True
        else:
            return False

    def get_avatar(self):
        if not self.avatar:
            if self.gender == 0:
                avatar_img = url_for('static', filename='cms/images/d0.png')
            else:avatar_img = url_for('static', filename='cms/images/d1.png')
            return avatar_img
        return self.avatar

    def __repr__(self):
        return '<CMSUser username:%s>'%self.username

    @classmethod
    def gen_fake_user(cls,count):
        fake = Faker(locale='zh_CN')
        roles = CMSRole.query.all()
        for i in range(count):
            u = cls(username = fake.user_name(),email = fake.ascii_free_email(),password = 'password')
            u.phone = fake.phone_number()
            u.birthday = fake.date_of_birth(minimum_age=20, maximum_age=55)
            # 0女 1男 2 secrete
            gender = randint(0,2)
            u.gender = gender
            if gender == 0:
                name = fake.name_female()
            elif gender == 1:
                name = fake.name_male()
            else:
                name =fake.name()
            u.name = name
            u.intro = fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
            with open('mxavatar.json','r') as f:
                avatar_list = json.load(f)
            u.avatar = choice(avatar_list)
            u.join_time = fake.date_this_year(before_today=True, after_today=False)
            u.role = choice(roles)
            db.session.add(u)
        db.session.commit()
        print('CMS用户添加成功，共同添加%d个'%count)



    __str__ = __repr__









