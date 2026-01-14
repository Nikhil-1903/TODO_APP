from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()                                                         # create database object globally

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'to_do_or_not_to_do'                       # create a key for sessions
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'           # database configuration
    app.config['SQLALCHEMY_MODIFICATIONS'] = False                        # currently false to avoid warnings

    db.__init__(app)

    from app.routes.auth import auth_bp                                   # import blue_prints
    from app.routes.auth import tasks_bp                                  
    app.register_blueprint(auth_bp)                                       # register blue_prints         
    app.register_blueprint(tasks_bp)
    
    return app
