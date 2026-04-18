import ast
from functools import wraps
from datetime import date
from flask import render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from sqlalchemy import select
from . import teachers_bp
from .. import db
from ..models import User, UserRole, Task, Assignment, AssignmentState


def for_teacher(func):
    @wraps(func)
    def wrapper():
        if current_user.role != UserRole.TEACHER:
            flash('Войдите как учитель, чтобы просматривать эту страницу', 'error')
            return redirect(url_for('auth.login'))
        return func()
    return wrapper


@teachers_bp.route('/')
@login_required
@for_teacher
def profile():
    return render_template('teachers/assignments.html')


@teachers_bp.route('/task_list')
@login_required
@for_teacher
def task_list():
    tasks = Task.query.order_by(Task.id.desc()).all()
    return render_template('teachers/task_list.html', tasks=tasks)


@teachers_bp.route('/new_task', methods=['GET', 'POST'])
@login_required
@for_teacher
def new_task():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        test_file = request.files.get('test_file')

        if not all([title, description, test_file]) or test_file.filename == '':
            flash('Заполните все поля и выберите файл.', 'error')
            return render_template('teachers/new_task.html')

        # Читаем содержимое файла
        try:
            test_content = test_file.read().decode('utf-8')
        except UnicodeDecodeError:
            flash('Файл должен быть сохранён в кодировке UTF-8.', 'error')
            return render_template('teachers/new_task.html')

        # Проверка синтаксиса Python (защита от битых файлов)
        try:
            ast.parse(test_content)
        except SyntaxError as e:
            flash(f'Ошибка синтаксиса в тесте: {e.msg} (строка {e.lineno})', 'error')
            return render_template('teachers/new_task.html')

        # Сохраняем в БД
        task = Task(
            title=title,
            description=description,
            test_code=test_content
        )
        db.session.add(task)
        db.session.commit()

        flash('Задание успешно создано!', 'success')
        return redirect(url_for('teachers.task_list'))

    return render_template('teachers/new_task.html')


@teachers_bp.route('/new_assignment', methods=['GET', 'POST'])
@login_required
@for_teacher
def new_assignment():
    if request.method == 'POST':
        task_id = int(request.form.get('task_id'))
        try:
            deadline = date.fromisoformat(request.form.get('deadline'))
        except ValueError:
            flash('Ошибка в дате', 'error')
            task = Task.query.get_or_404(task_id, 'Задача не выбрана или не существует')
            return render_template('teachers/new_assignment.html', task=task)

        stmt = (
            select(User.id)
            .outerjoin(Assignment, (User.id == Assignment.user_id) & (Assignment.task_id == task_id))
            .where(
                User.role == UserRole.STUDENT,
                Assignment.id  == None  # Выбираем только тех, у кого нет связи
            )
        )
        user_ids = db.session.execute(stmt).scalars().all()
        if not user_ids:
            flash('Эта задача уже назначена всем студентам', 'info')
            return redirect(url_for('teachers.task_list'))

        assignments_to_add = [
            Assignment(
                task_id=task_id,
                user_id=user_id,
                deadline=deadline,
            )
            for user_id in user_ids
        ]
        db.session.add_all(assignments_to_add)
        db.session.commit()

        flash('Назначение успешно создано!', 'success')
        return redirect(url_for('teachers.profile'))

    task_id = request.args.get('task_id')
    if not task_id:
        abort(404, description = 'Задача не выбрана или не существует')
    task = Task.query.get_or_404(task_id, 'Задача не выбрана или не существует')
    return render_template('teachers/new_assignment.html', task=task)
