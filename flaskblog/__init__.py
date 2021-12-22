from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
mail = Mail()


def creat_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)


    from flaskblog.users.routes import users
    from flaskblog.posts.routes import post_bp
    from flaskblog.main.routes import main
    from flaskblog.apis.routes import rest_api

    app.register_blueprint(users)
    app.register_blueprint(post_bp)
    app.register_blueprint(main)
    app.register_blueprint(rest_api)

    return app

