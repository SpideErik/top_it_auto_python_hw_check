from app import create_app, db
from app.models import User


def new_user(name:str):
    # Проверяем, нет ли уже такого пользователя
    if not User.query.filter_by(username=name).first():
        pw = '123'
        role = 'teacher' if name.startswith('t') else 'student'
        user = User(username=name, password=pw, role=role)
        db.session.add(user)
        db.session.commit()
        print(f"Пользователь {user.username} создан!")
    else:
        print("Пользователь уже существует.")


app = create_app()
# Входим в контекст приложения, чтобы SQLAlchemy знал настройки БД
with app.app_context():
    # На всякий случай создаем таблицы, если их нет
    db.create_all()
    for n in ('t1', 's1', 's2', 's3'):
        new_user(n)
