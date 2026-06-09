from pathlib import Path
from app import create_app, db
import app.models as mod

def new_user(login:str, name:str, role:str):
    # Проверяем, нет ли уже такого пользователя
    if not mod.User.query.filter_by(username=login).first():
        pw = '123'
        user = mod.User(username=login, password=pw, role=role, name=name)
        db.session.add(user)
        db.session.commit()
        print(f"Пользователь {user.username} создан!")
    else:
        print("Пользователь уже существует.")


def new_task(title, descr, tests):
    if not mod.Task.query.filter_by(title=title).first():
        task = mod.Task(title=title, description=descr, test_code=tests)
        db.session.add(task)
        db.session.commit()
        print(f"Задача {title} создана!")
    else:
        print("Задача уже существует.")

users = [
    ['s1', 'Смирнов Андрей Викторович', mod.UserRole.STUDENT],
    ['s2', 'Кузнецова Мария Александровна', mod.UserRole.STUDENT],
    ['s3', 'Михайлов Дмитрий Сергеевич', mod.UserRole.STUDENT],
    ['s4', 'Васильева Анна Игоревна', mod.UserRole.STUDENT],
    ['t1', 'Попов Алексей Николаевич', mod.UserRole.TEACHER],
]

app = create_app()
# Входим в контекст приложения, чтобы SQLAlchemy знал настройки БД
with app.app_context():
    # На всякий случай создаем таблицы, если их нет
    db.create_all()
    for u in users:
        new_user(*u)
    for fn in (Path(__file__).parent / 'example_tasks').glob('*.descr'):
        txt = fn.read_text('UTF8').splitlines(keepends=True)
        title = txt[0].strip()
        decr = ''.join(txt[1:])
        tests = fn.with_suffix('.txt').read_text('UTF8')
        new_task(title, decr, tests)
