from flask import Flask
import config
from apps.cms import bp as cms_bp
from apps.front import bp as front_bp
from flask_wtf import CSRFProtect
from exts import db,mail,login_manager,moment,bootstrap


def create_app():
    app = Flask(__name__)
    app.register_blueprint(cms_bp,prefix='cms')
    app.register_blueprint(front_bp,prefix='front')
    login_manager.init_app(app)
    app.config.from_object(config)
    # app.url_map.default_subdomain = 'www'
    db.init_app(app)
    mail.init_app(app)
    CSRFProtect(app)
    moment.init_app(app)
    bootstrap.init_app(app)
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)
