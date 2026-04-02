import pytest
from flask import abort

from application.app import app
from application.models import db


@pytest.fixture(scope='function')
def client():
    app.config['TESTING'] = True
    # тестовая БД sqlite в памяти, чтобы не зависеть от PostgreSQL окружения
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.init_app(app)  # инициализация ORM на случай, если не была вызвана
        db.create_all()
        test_client = app.test_client()

        yield test_client

        db.session.remove()
        db.drop_all()


def test_valid_paths_return_200_and_non_empty_body(client):
    valid_paths = [
        '/',
        '/hosts',
        '/hosts/add',
        '/horses',
        '/horses/add',
        '/jockeys',
        '/jockeys/add',
        '/races',
        '/races/add',
    ]

    for path in valid_paths:
        response = client.get(path)
        assert response.status_code == 200, f"{path} должен возвращать 200, а вернул {response.status_code}"
        assert response.data, f"{path} вернул пустое тело"
        assert response.data.strip(), f"{path} вернул только пустые пробельные символы"


def test_invalid_path_returns_404(client):
    response = client.get('/path-not-found-123')
    assert response.status_code == 404


# def test_forbidden_path_returns_403(client):
#     endpoint_name = '_test_path_forbidden'

#     # временный маршрут для проверки 403
#     app.add_url_rule('/path-forbidden-123', endpoint=endpoint_name, view_func=lambda: abort(403))

#     try:
#         response = client.get('/path-forbidden-123')
#         assert response.status_code == 403
#     finally:
#         # убираем роут, чтобы не влиять на другие тесты
#         app.url_map._rules = [r for r in app.url_map._rules if r.endpoint != endpoint_name]
#         app.view_functions.pop(endpoint_name, None)
