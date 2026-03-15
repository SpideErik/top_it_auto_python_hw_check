from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
    app.config['SECRET_KEY'] = 'dev-key'
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = '/'

    from .auth import auth_bp
    from .students import students_bp
    from .teachers import teachers_bp
    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(students_bp, url_prefix='/students')
    app.register_blueprint(teachers_bp, url_prefix='/teachers')

    # Настройка загрузки пользователя для Flask-Login
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
