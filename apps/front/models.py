from exts import db
from flask import current_app,url_for
import shortuuid
import enum
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from faker import Faker
from random import choice,randint
import json


class Permission():
    #所有权限
    ALL_PERMISSION   = 0b111111111111
    #1.前端登录
    LOGIN            = 0b000000000001
    #2.查看帖子
    VIEW_POST        = 0b000000000010
    #3.发表帖子
    PUBLISH_POST     = 0b000000000100
    #4.发表评论
    PUBLISH_COMMENT  = 0b000000001000

    #5.后台登录
    LOGIN_CMS        = 0b000000010000
    # 6.管理帖子
    MANAGE_POST      = 0b000000100000
    # 7.管理评论
    MANAGE_COMMENTER = 0b000001000000
    # 8.管理板块
    BOARDER          = 0b000010000000
    #9.管理轮播图
    BANNER           = 0b000100000000
    #10.管理前台用户的权限
    FRONTUSER        = 0b001000000000
    #11.管理后台用户的权限
    CMSUSER          = 0b010000000000
    #12.超级管理员
    ADMINER          = 0b100000000000


class GenderEnum(enum.Enum):
    MALE = 1
    FMALE = 2
    SECRET = 3
    UNKNOW = 4


BookMark = db.Table(
    'bookmark',
    db.Column('user_id',db.String(100),db.ForeignKey('front_user.id'),primary_key=True),
    db.Column('post_id',db.Integer,db.ForeignKey('post.id'),primary_key=True)
)


class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.String(100), db.ForeignKey('front_user.id'), primary_key=True)
    followed_id = db.Column(db.String(100), db.ForeignKey('front_user.id'), primary_key=True)
    timestamp = db.Column(db.DateTime,default=datetime.now)


class FrontUser(db.Model):

    __tablename__ = 'front_user'
    id = db.Column(db.String(100),primary_key=True,default=shortuuid.uuid)
    telephone = db.Column(db.String(11),nullable=False,unique=True)
    username = db.Column(db.String(50),nullable=False)
    _password = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(50),unique=True)
    confirm = db.Column(db.Boolean,default=False)
    realname = db.Column(db.String(100))
    avatar = db.Column(db.String(100))
    signature = db.Column(db.String(100))
    gender  = db.Column(db.Enum(GenderEnum),default=GenderEnum.UNKNOW)
    join_time = db.Column(db.DATETIME,default=datetime.now)
    last_seen = db.Column(db.DATETIME,default=datetime.now)

    bookmark = db.relationship('PostModel', secondary=BookMark, backref=db.backref('mark_users'))

    followed = db.relationship('Follow',
                              foreign_keys=[Follow.follower_id],
                              backref=db.backref('follower',lazy='joined'),
                              lazy='dynamic',
                              cascade='all,delete-orphan')
    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all,delete-orphan')

    def __init__(self, *args, **kwargs):
        if 'password' in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop('password')
        super(FrontUser, self).__init__(*args, **kwargs)

    def follow(self,user):
        if not self.is_following(user):
            f = Follow(follower=self,followed=user)
            db.session.add(f)

    def is_following(self,user):
        return self.followed.filter_by(followed_id=user.id).first() is not None

    def unfollow(self,user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_followd_by(self,user):
        return self.followers.filter_by(follower_id=user.id).first() is not None



    def __repr__(self):
        return "<FrontUser username:%s,telephone:%s>"%(self.username,self.telephone)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,newpassword):
        self._password = generate_password_hash(newpassword)

    def get_avatar(self):
        defautl_avatar = url_for('static',filename='common/images/avatar.jpg')
        return self.avatar or defautl_avatar

    def check_password(self,rawpassword):
        return check_password_hash(self._password,rawpassword)

    def generate_reset_token(self,expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    def generate_comfirmation_token(self,expiration=3600*24):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'comfirm': self.id}).decode('utf-8')

    def confirm_token(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user_id = data.get('comfirm')
        front_user = FrontUser().query.get(user_id)
        if front_user:
            front_user.confirm = True
            db.session.add(front_user)
            return True
        return False


    @staticmethod
    def reset_password(token,new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user_id = data.get('reset')
        user = FrontUser.query.get(user_id)
        if not user:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    @classmethod
    def gen_fake_user(cls, count):
        fake = Faker(locale='zh_CN')
        n=0
        for i in range(count):
            u = cls()
            u.telephone = fake.phone_number()
            u.username = fake.user_name()
            u.email = fake.ascii_free_email()
            u.password = 'password'
            u.confirm = choice([True,False])
            u.realname = fake.name()
            with open('mxavatar.json','r') as f:
                avatar_list = json.load(f)
            u.avatar = choice(avatar_list)
            u.signature = fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
            u.gender = GenderEnum(randint(1,4))
            u.join_time = fake.date_this_year(before_today=True, after_today=False)
            db.session.add(u)
        try:
            db.session.commit()
            n += 1
        except Exception:
            db.session.rollback()
        db.session.commit()
        print('Front用户添加成功，共同添加%d个' % n)

    def init_role(self):
        pass

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMINER)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    u_id = db.Column(db.String(100), db.ForeignKey('front_user.id'))
    name = db.Column(db.Enum('FrontUser', 'CmsUser','Operator','Administrator'),nullable=False)
    permissions = db.Column(db.Integer,nullable=False)
    user = db.relationship('FrontUser', backref=db.backref('role',uselist=False))

    roles = {
        'FrontUser': [Permission.LOGIN, Permission.VIEW_POST, Permission.PUBLISH_POST,
                      Permission.PUBLISH_COMMENT],
        'CmsUser': [Permission.LOGIN, Permission.VIEW_POST, Permission.PUBLISH_POST,
                    Permission.PUBLISH_COMMENT, Permission.LOGIN_CMS],
        'Operator': [Permission.LOGIN, Permission.VIEW_POST, Permission.PUBLISH_POST,
                     Permission.PUBLISH_COMMENT, Permission.LOGIN_CMS, Permission.MANAGE_POST,
                     Permission.MANAGE_COMMENTER, Permission.BOARDER, Permission.BANNER,
                     Permission.FRONTUSER],
        'Administrator': [Permission.ALL_PERMISSION]
    }
    default_role = 'FrontUser'

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.name is None:
            self.name = self.default_role
        if self.permissions is None:
            self.permissions = sum(self.roles[self.name])

    def add_permission(self, *perms):
        for perm in perms:
            if not self.has_permission(perm):
                self.permissions += perm

    def remove_permission(self, *perms):
        for perm in perms:
            if self.has_permission(perm):
                self.permissions -= perm

    def reset_permissions(self):
        self.permissions = sum(self.roles[self.default_role])

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name