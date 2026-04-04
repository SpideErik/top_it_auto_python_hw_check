from app import create_app, db
import app.models as mod

def new_user(name:str):
    # Проверяем, нет ли уже такого пользователя
    if not mod.User.query.filter_by(username=name).first():
        pw = '123'
        role = mod.UserRole.TEACHER if name.startswith('t') else mod.UserRole.STUDENT
        user = mod.User(username=name, password=pw, role=role)
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
