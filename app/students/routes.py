from flask import flash, redirect, url_for
from flask_login import login_required, current_user
from . import students_bp
from ..models import User, UserRole


@students_bp.route('/')
@login_required
def profile():
    if current_user.role != UserRole.STUDENT:
        flash('Войдите как студент, чтобы просматривать эту страницу', 'error')
        return redirect(url_for('auth.login'))
    return f"TODO: список заданий для студента {current_user.id}"
