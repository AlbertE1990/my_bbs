from sqlalchemy.orm import backref
from exts import db,login_manager
from flask import current_app,url_for,jsonify
import shortuuid
import enum
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin,AnonymousUserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Permission():

    #1.前端登录
    LOGIN                       = 0b1
    #2.查看帖子
    VIEW_POST                   = 0b10
    #3.发表帖子
    PUBLISH_POST                = 0b100
    #4.发表评论
    PUBLISH_COMMENT             = 0b1000
    #5.后台登录
    LOGIN_CMS                   = 0b10000
    # 6.管理帖子
    MANAGE_POST                 = 0b100000
    # 7.管理评论
    MANAGE_COMMENTE             = 0b1000000
    # 8.管理用户账号
    MANAGE_ACCOUNT              = 0b10000000
    # 9.管理用户权限
    MANAGE_PERMISSION           = 0b100000000
    # 10.管理板块
    BOARDER                     = 0b1000000000
    #11.管理轮播图
    BANNER                      = 0b10000000000
    #12.创建账户
    CREATE_ACCOUNT              = 0b100000000000
    #13组管理
    MANAGE_GROUP                = 0b1000000000000
    #14.超级管理员
    SU                          = 0b10000000000000
    # 所有权限
    ALL_PERMISSION              = 0b11111111111111


class PermissionDesc():

    #1.前端登录
    LOGIN                       = '登陆前端'
    #2.查看帖子
    VIEW_POST                   = '查看帖子'
    #3.发表帖子
    PUBLISH_POST                = '发表帖子'
    #4.发表评论
    PUBLISH_COMMENT             = '发表评论'
    #5.后台登录
    LOGIN_CMS                   = '登陆CMS管理系统'
    # 6.管理帖子
    MANAGE_POST                 = '管理帖子'
    # 7.管理评论
    MANAGE_COMMENTE             = '管理评论'
    # 8.管理前台用户账号
    MANAGE_ACCOUNT              = '管理用户账号'
    # 9.管理前台用户权限
    MANAGE_PERMISSION           = '管理用户权限'
    # 10.管理板块
    BOARDER                     = '管理板块'
    #11.管理轮播图
    BANNER                      = '管理轮播图'
    #
    CREATE_ACCOUNT              = '新开账户'
    #13.用户组管理
    MANAGE_GROUP                = '用户组管理'
    #14.超级管理员
    SU                          = '超级管理员'
    # 所有权限
    ALL_PERMISSION              = '所有权限'



class Group(enum.Enum):
    FrontUser     = [Permission.LOGIN, Permission.VIEW_POST, Permission.PUBLISH_POST,
                     Permission.PUBLISH_COMMENT]
    Operator      = FrontUser + [Permission.LOGIN_CMS,Permission.MANAGE_POST,Permission.MANAGE_COMMENTE,
                                      Permission.MANAGE_ACCOUNT,Permission.MANAGE_PERMISSION]
    Administrator = Operator + [Permission.BANNER,Permission.CREATE_ACCOUNT]
    Super = Administrator+[Permission.MANAGE_GROUP,Permission.SU]

class GenderEnum(enum.Enum):
    MALE = 1
    FMALE = 2
    SECRET = 3
    UNKNOW = 4


BookMark = db.Table(
    'bookmark',
    db.Column('user_id',db.String(100),db.ForeignKey('user.id'),primary_key=True),
    db.Column('post_id',db.Integer,db.ForeignKey('post.id'),primary_key=True)
)


class Follow(db.Model):
    __tablename__ = 'follow'
    follower_id = db.Column(db.String(100), db.ForeignKey('user.id'), primary_key=True)
    followed_id = db.Column(db.String(100), db.ForeignKey('user.id'), primary_key=True)
    timestamp = db.Column(db.DateTime,default=datetime.now)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False


login_manager.anonymous_user = AnonymousUser


class User(db.Model, UserMixin):

    __tablename__ = 'user'
    id = db.Column(db.String(100),primary_key=True,default=shortuuid.uuid)
    telephone = db.Column(db.String(11),nullable=False,unique=True)
    username = db.Column(db.String(50),nullable=False)
    _password = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(50),unique=True)
    confirm = db.Column(db.Boolean,default=False)
    realname = db.Column(db.String(100))
    avatar = db.Column(db.String(255))
    signature = db.Column(db.String(100))
    gender  = db.Column(db.Enum(GenderEnum),default=GenderEnum.UNKNOW)
    join_time = db.Column(db.DATETIME,default=datetime.now)
    last_seen = db.Column(db.DATETIME,default=datetime.now)
    birthday = db.Column(db.DATE)
    intro = db.Column(db.Text)
    disabled = db.Column(db.Boolean,default=False)

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
        super(User, self).__init__(*args, **kwargs)

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
        return "<User username:%s,telephone:%s>"%(self.username,self.telephone)

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
        front_user = User().query.get(user_id)
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
        user = User.query.get(user_id)
        if not user:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def init_role(self):
        pass

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.SU)

    def set_permission(self,permission):
        if not self.role:
            self.role = Role()
        self.role.permissions = permission
        db.session.add(self)

    def ping(self):
        self.last_seen = datetime.now()
        db.session.add(self)

    def to_json(self):
        json_user = {
            'url': url_for('cms.profile',uid=self.id),
            'id':self.id,
            'telephone':self.telephone,
            'username': self.username,
            'email': self.email,
            'realname':self.realname,
            'avatar':self.avatar,
            'gender': self.gender.value,
            'join_time': self.join_time,
            'last_seen': self.last_seen,
            'birthday': self.birthday,
            'intro': self.intro,
        }
        return json_user

    def update_profile(self,**data):
        for k in data:
            setattr(self, k, data[k])
        db.session.add(self)
        db.session.commit()

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    u_id = db.Column(db.String(100), db.ForeignKey('user.id'))
    group = db.Column(db.Enum(Group),default=Group.FrontUser,nullable=False)
    permissions = db.Column(db.Integer,nullable=False)
    user = db.relationship('User', backref=db.backref('role', uselist=False))
    default_group = 'FrontUser'

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.group is None:
            self.group = self.default_group
        if self.permissions is None:
            self.permissions = sum(getattr(Group,self.group,0).value)
        else:
            self.permissions = min(sum(getattr(Group,self.group).value),self.permissions)

    def add_permission(self, *perms):
        for perm in perms:
            if not self.has_permission(perm):
                self.permissions += perm

    def remove_permission(self, *perms):
        for perm in perms:
            if self.has_permission(perm):
                self.permissions -= perm

    def reset_permissions(self):
        self.permissions = sum(getattr(Group,self.group).value)

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role:%r>' % self.group


#轮播图
class BannerModel(db.Model):
    __tablename__ = 'banner'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(255),nullable=False)
    image_url = db.Column(db.String(255),nullable=False)
    link_url = db.Column(db.String(255),nullable=False)
    priority = db.Column(db.Integer,default=0)
    create_time = db.Column(db.DateTime,default=datetime.now)

#板块
class BoardModel(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(255),nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)

#帖子
class PostModel(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    board_id = db.Column(db.Integer,db.ForeignKey('board.id'))
    author_id = db.Column(db.String(100),db.ForeignKey('user.id'))

    author = db.relationship('User',backref='posts')
    board = db.relationship('BoardModel',backref='posts')

    __mapper_args__ = {'order_by': create_time.desc()}

#评论
class CommentModel(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    author_id = db.Column(db.String(100), db.ForeignKey('user.id'))
    disabled = db.Column(db.Boolean)

    author = db.relationship('User',backref='comments')
    post = db.relationship('PostModel',backref = 'comments')

    __mapper_args__ ={'order_by':create_time.desc()}


#精华帖
class HighlightPostModel(db.Model):
    __tablename__ = 'highlight_post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)

    post = db.relationship('PostModel',backref=backref('highlight',uselist=False) )


#顶置贴
class TopPostModel(db.Model):
    __tablename__ = 'top_post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)

    post = db.relationship('PostModel',backref=backref('top',uselist=False) )


#加精帖子申请
class ApplyHighlight(db.Model):
    __tablename__ = 'apply_highlight'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)

    post = db.relationship('PostModel', backref=backref('apply_highlight', uselist=False))


#顶置帖子申请
class ApplyTop(db.Model):
    __tablename__ = 'apply_top'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)

    post = db.relationship('PostModel', backref=backref('apply_top', uselist=False))