from functools import wraps
from flask import flash, redirect, url_for
from flask_login import login_required, current_user
from . import students_bp
from ..models import User, UserRole


def for_student(func):
    @wraps(func)
    def wrapper():
        if current_user.role != UserRole.STUDENT:
            flash('Войдите как студент, чтобы просматривать эту страницу', 'error')
            return redirect(url_for('auth.login'))
        return func()
    return wrapper


@students_bp.route('/')
@login_required
@for_student
def profile():
    return f"TODO: список заданий для студента {current_user.id}"
