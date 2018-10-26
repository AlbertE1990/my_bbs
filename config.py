# -*- coding:utf-8 -*-
import os
from datetime import timedelta
DEBUG = True
SECRET_KEY = os.urandom(24)

#db
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST     = 'localhost'
DB_PORT     = '3306'
DB_NAME     = 'mybbs'
DB_URI      = "mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8"%\
         (DB_USERNAME,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False


#设置cookies过期时间,2小时
# PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
# REMEMBER_COOKIE_DURATION = timedelta(days=7)
# REMEMBER_COOKIE_PATH = '127.0.0.1:8000'

#mail
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = '587'
MAIL_USE_TLS = True
#MAIL_USE_SSL = True
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

FLASKY_MAIL_SUBJECT_PREFIX = '[CMS]'
FLASKY_MAIL_SENDER = 'CMS Admin <CMS@qq.com>'
FLASKY_ADMIN = 'CMS后台管理系统_ADMIN'

#前端
PER_PAGE = 10

# BOOTSTRAP_SERVE_LOCAL = True

#CMS
CMS_PER_PAGE = 10

#
SERVER_NAME = "bat.com:5000"