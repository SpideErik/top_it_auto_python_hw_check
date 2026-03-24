# Индивидуальный проект 2
# Автоматический учет и проверка домашних заданий по теме "Основы Python"

## Требования
* python 3.13 или старше
* virtualenv (`py -m pip install virtualenv`)

## Установка
1. Клонирование репозитория <br>
   `git clone https://github.com/SpideErik/top_it_auto_python_hw_check.git`
2. Создание virtualenv, в папке  top_it_auto_python_hw_check<br>
    `py -m virtualenv .venv`
3. Активировать virtualenv <br>
    `.venv\Scripts\activate.bat`
4. Установить зависимости <br>
    `pip install -r requirements.txt`
5. Создать начальную базу данных <br>
    `python init_db.py`
6. Запустить проект <br>
    `python run.py`
7. Открыть браузер http://127.0.0.1:5000

