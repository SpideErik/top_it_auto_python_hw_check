from . import teachers_bp


@teachers_bp.route('/<int:sid>')
def profile(sid):
    return f"TODO: список заданий для учителя №{sid}"
