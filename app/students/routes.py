from functools import wraps
from flask import flash, redirect, url_for, render_template, request, abort
from flask_login import login_required, current_user
from . import students_bp
from ..models import User, UserRole, Task, Assignment, AssignmentState


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
    new = Assignment.query.filter_by(user_id=current_user.id, state=AssignmentState.ISSUED)
    return render_template('students/assignments.html', new=new)


@students_bp.route('/solve', methods=['GET', 'POST'])
@login_required
@for_student
def solve():
    if request.method == 'POST':
        return 'TODO'
    assignment_id = request.args.get('assignment_id')
    if not assignment_id:
        abort(404, description = 'Задание не выбрано или не существует')
    assignment = Assignment.query.get_or_404(assignment_id, 'Задание не выбрано или не существует')
    return render_template('students/solve.html', assignment=assignment)
