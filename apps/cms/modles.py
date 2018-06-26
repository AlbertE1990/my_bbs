# -*- coding:utf-8 -*-
from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
import shortuuid
from config import SECRET_KEY

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

if __name__ == '__main__':
    pass
