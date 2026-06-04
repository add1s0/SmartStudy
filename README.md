Smart Study

Smart Study е Django уеб приложение, подходящо за начинаещи, което помага за организиране на учебни материали и подготовка за изпити. То създава обобщения и тестове от бележките на ученика чрез прости Python функции. Не използва външна AI услуга.

Функционалности
Регистрация, вход и изход от системата
Лични учебни материали с пълни операции за създаване, четене, редакция и изтриване (CRUD)
Автоматично генерирани обобщения и тестове с въпроси с избираем отговор
Запазване на резултати от тестове с препоръки
Проследяване на изпити, оценка на подготовката и прост учебен план
Страница със статистики и прогрес барове
Таймер Pomodoro (25 минути), работещ в браузъра
Django админ панел
Технологии
Python
Django
SQLite
Bootstrap 5
HTML, CSS и малко JavaScript
pytest за тестове по време на разработка
Инсталация

Отвори терминал в основната директория на проекта и изпълни:

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd src
python manage.py migrate
Стартиране на приложението

От папката src, изпълни:

python manage.py createsuperuser
python manage.py runserver

Отвори http://127.0.0.1:8000/ в браузър.

Стартиране на тестове

Инсталирай зависимостите за разработка от основната директория на проекта, след което стартирай pytest:

pip install -r requirements-dev.txt
pytest
Структура на проекта
SmartStudy/
|-- src/
|   |-- manage.py
|   |-- smart_study/
|   |-- study/
|   |-- static/
|   `-- templates/
|-- tests/
|   |-- test_utils.py
|   `-- test_models.py
|-- requirements.txt
|-- requirements-dev.txt
|-- .gitignore
`-- README.md
Команди за първоначална настройка

Това са пълните стартови команди за проекта. Изпълнявай manage.py командите от папката src.

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd src
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
