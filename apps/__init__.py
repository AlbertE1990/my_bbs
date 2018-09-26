# -*- coding:utf-8 -*-
from flask import Flask
import config
from flask_wtf import CSRFProtect
from exts import db,mail,login_manager,moment,bootstrap
from .cms import bp as cms_bp
from .front import bp as front_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(cms_bp)
    app.register_blueprint(front_bp)
    login_manager.init_app(app)
    app.config.from_object(config)
    db.init_app(app)
    mail.init_app(app)
    CSRFProtect(app)
    moment.init_app(app)
    bootstrap.init_app(app)
    return app