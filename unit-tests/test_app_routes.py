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
        assert response.data.strip(
        ), f"{path} вернул только пустые пробельные символы"


def test_invalid_path_returns_404(client):
    response = client.get('/path-not-found-123')
    assert response.status_code == 404
