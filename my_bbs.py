from flask import Flask
import config
from apps.cms import bp as cms_bp
from apps.front import bp as front_bp
from flask_wtf import CSRFProtect
from exts import db,mail





def create_app():
    app = Flask(__name__)
    app.register_blueprint(cms_bp)
    app.register_blueprint(front_bp)
    app.config.from_object(config)
    db.init_app(app)
    mail.init_app(app)
    CSRFProtect(app)
    return app

app = create_app()
if __name__ == '__main__':
    app.run(port=8000)
