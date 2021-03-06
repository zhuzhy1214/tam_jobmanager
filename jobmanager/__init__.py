from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from jobmanager.config import Config
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
jwt = JWTManager()

def creat_app(config_class=Config):
    """

    :param config_class:
    :return:
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)
    # api = Api(app)

    from jobmanager.users.routes import users
    from jobmanager.posts.routes import post_bp
    from jobmanager.main.routes import main
    from jobmanager.jobs.routes import jobs
    from jobmanager.apis.routes import rest_api
    from jobmanager.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(post_bp)
    app.register_blueprint(main)
    app.register_blueprint(jobs)
    app.register_blueprint(rest_api)
    app.register_blueprint(errors)


    #
    # from jobmanager.apis.postmile import PostMile,TaskManager
    # from jobmanager.apis.todo_list import Todo, TodoList
    # api.add_resource(PostMile,
    #                  '/postmile/<int:task_id>')
    # api.add_resource(TaskManager,
    #                  '/tm_add/<string:func_name>', '/tm_ck/<int:task_id>')
    #
    # api.add_resource(TodoList, '/todos')
    # api.add_resource(Todo, '/todos/<string:todo_id>')

    return app

