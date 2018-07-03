# -*- coding:utf-8 -*-
import os
from datetime import timedelta
DEBUG = True
SECRET_KEY = os.urandom(24)

#db
DB_USERNAME = 'root'
DB_PASSWORD = 'root'
DB_HOST     = 'localhost'
DB_PORT     = '3306'
DB_NAME     = 'mybbs'
DB_URI      = "mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8"%\
         (DB_USERNAME,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

CMS_USER_ID = "you can not guess it"

#设置cookies过期时间,2小时
PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

#mail
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = '587'
MAIL_USE_TLS = True
#MAIL_USE_SSL = True
MAIL_USERNAME = "112288349@qq.com"
MAIL_PASSWORD = "kgqembbxywxfcbbb"
MAIL_DEFAULT_SENDER = "112288349@qq.com"

