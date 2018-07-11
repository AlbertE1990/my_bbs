# -*- coding:utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.session_protection='strong'


db = SQLAlchemy()
mail = Mail()