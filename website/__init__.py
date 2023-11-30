import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
db = SQLAlchemy()
admin = Admin()

DB_NAME = "website\\instance\\database.db"
BASE_DIR = os.path.abspath(os.path.dirname(__name__))

DB_FULL_PATH = os.path.join(BASE_DIR, DB_NAME)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'YOLO PASSWORD KEY  xxx'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_FULL_PATH}'
    app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(app)
    admin.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Item

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
