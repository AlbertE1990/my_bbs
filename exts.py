# -*- coding:utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_moment import Moment
from flask_bootstrap import Bootstrap


login_manager = LoginManager()
login_manager.session_protection='strong'
login_manager.login_view='cms.login'


moment = Moment()
db = SQLAlchemy()
mail = Mail()
bootstrap = Bootstrap()