from flask import Flask
from .auth import auth_bp
from .students import students_bp
from .teachers import teachers_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(students_bp, url_prefix='/students')
    app.register_blueprint(teachers_bp, url_prefix='/teachers')
    return app
