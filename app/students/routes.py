from . import students_bp


@students_bp.route('/<int:sid>')
def profile(sid):
    return f"TODO: список заданий для студента №{sid}"
