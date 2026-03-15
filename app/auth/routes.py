from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user
from ..models import User
from . import auth_bp


@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Ищем пользователя в БД
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:  # Для простоты без хеша
            login_user(user)
            # Перенаправление по роли
            if user.role == 'teacher':
                return redirect(url_for('teachers.profile'))
            elif user.role == 'student':
                return redirect(url_for('students.profile'))

        flash('Неверное имя или пароль')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('/'))
