from . import teachers_bp


@teachers_bp.route('/')
def profile():
    return f"TODO: список заданий для учителя"
