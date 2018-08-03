from exts import db
from flask import current_app,url_for
import shortuuid
import enum
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


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







