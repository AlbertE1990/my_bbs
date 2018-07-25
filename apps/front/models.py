from exts import db
from flask import current_app
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

class FrontUser(db.Model):
    __tablename__ = 'front_user'
    id = db.Column(db.String(100),primary_key=True,default=shortuuid.uuid)
    telephone = db.Column(db.String(11),nullable=False,unique=True)
    username = db.Column(db.String(50),nullable=False)
    _password = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(50),unique=True)
    realname = db.Column(db.String(100))
    avatar = db.Column(db.String(100))
    signature = db.Column(db.String(100))
    gender  = db.Column(db.Enum(GenderEnum),default=GenderEnum.UNKNOW)
    join_time = db.Column(db.DATETIME,default=datetime.now)

    def __init__(self,*args,**kwargs):
        if 'password' in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop('password')
        super(FrontUser,self).__init__(*args,**kwargs)

    def __repr__(self):
        return "<FrontUser username:%s,telephone:%s>"%(self.username,self.telephone)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,newpassword):
        self._password = generate_password_hash(newpassword)

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
        user = FrontUser.query.get(data.get('reset'))
        if not user:
            return False
        user.password = new_password
        db.session.add(user)
        return True


