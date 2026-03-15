from . import students_bp


@students_bp.route('/')
def profile():
    return f"TODO: список заданий для студента"
