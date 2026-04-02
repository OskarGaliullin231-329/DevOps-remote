import pytest


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


def test_failing_test_root_returns_404(client):
    """Этот тест заведомо упадёт, потому что корневой путь возвращает 200, а не 404"""
    response = client.get('/')
    assert response.status_code == 404, "Корневой путь должен возвращать 404, но возвращает 200"
