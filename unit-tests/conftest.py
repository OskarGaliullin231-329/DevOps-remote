import sys
import os
import pytest

# Добавляем корневую папку проекта в sys.path для корректного импорта модулей
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'app'))

# Устанавливаем переменные окружения для тестирования до импорта app
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['FLASK_ENV'] = 'testing'

# Импортируем приложение и модели до создания фикстур
from app import app
from models import db


@pytest.fixture(scope='session')
def flask_app():
    """Создаёт приложение Flask с конфигурацией для тестирования."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    return app


@pytest.fixture
def client(flask_app):
    """Создаёт тестовый клиент приложения с подготовленной БД."""
    with flask_app.app_context():
        # Создаём таблицы в памяти для каждого теста
        # (db уже инициализирована в app.py)
        db.create_all()
        
        yield flask_app.test_client()
        
        # Очищаем данные после теста
        db.session.remove()
        db.drop_all()
