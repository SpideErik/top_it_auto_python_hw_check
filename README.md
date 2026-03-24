# Индивидуальный проект 2
# Автоматический учет и проверка домашних заданий по теме "Основы Python"

## Требования
* python 3.13 или старше
* virtualenv 
  * windows: ```py -m pip install virtualenv```
  * linux ```pip3 install virtualenv```

## Установка
1. Клонирование репозитория <br>
   ```git clone https://github.com/SpideErik/top_it_auto_python_hw_check.git```
2. Создание virtualenv, в папке  top_it_auto_python_hw_check<br>
    * windows: ```py -m virtualenv .venv```
    * linux: ```python3 -m virtualenv .venv```
3. Активировать virtualenv <br>
    * windows: ```.venv\Scripts\activate.bat```
    * linux: ```source .venv/Scripts//activate```
4. Установить зависимости <br>
    ```pip3 install -r requirements.txt```
5. Создать начальную базу данных <br>
    ```python3 init_db.py```
6. Запустить проект <br>
    ```python3 run.py```
7. Открыть браузер http://127.0.0.1:5000

