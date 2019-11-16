from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

from .agora import AuthClient
agora_auth = AuthClient()


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    agora_auth.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .dashboard import dashboard as dashboard_blueprint
    app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    with app.app_context():
        db.create_all()

    return app

