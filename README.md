# Smart Study

Smart Study is a beginner-friendly Django web application for organizing study
materials and preparing for exams. It creates summaries and quizzes
from a student's notes using simple Python functions. It does not use an external
AI service.

## Features

- Register, login, and logout
- Private study materials with full create, read, update, and delete actions
- Automatically generated summaries and multiple-choice quizzes
- Saved quiz results with recommendations
- Exam tracking, preparedness score, and a simple study plan
- Statistics page with progress bars
- Browser-based 25-minute Pomodoro timer
- Django admin site

## Technologies

- Python
- Django
- SQLite
- Bootstrap 5
- HTML, CSS, and a small amount of JavaScript
- pytest for development tests

## Installation

Open a terminal in the project root and run:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd src
python manage.py migrate
```

## Running The Application

From the `src` folder, run:

```powershell
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in a browser.

## Running Tests

Install the development requirements from the project root, then run pytest:

```powershell
pip install -r requirements-dev.txt
pytest
```

## Project Structure

```text
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
```

## First-Time Setup Commands

These are the complete startup commands requested for the project. Run the
`manage.py` commands from inside the `src` folder.

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd src
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
