from flask import Flask, login_manager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()                                                         # create database object globally

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'to_do_or_not_to_do'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    return app
