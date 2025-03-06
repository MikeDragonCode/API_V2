import requests
import pytest
import allure

BASE_URL = "https://staging.danone.oncallcrm.ru/api"


def test_login():
    """Логин и сохранение токенов"""
    response = requests.post(
        f"{BASE_URL}/auth/login",
        headers={"content-type": "application/json"},
        json={"email": "test@test.ru", "password": "danonepro101"}
    )

    assert response.status_code == 201, "Ошибка логина!"

    tokens = response.json()
    access_token = tokens["accessToken"]
    refresh_token = tokens["refreshToken"]

    # Записываем токены в conftest.py
    with open("stage/danone/visits/tokens.txt", "w") as file:
        file.write(f"{access_token}\n{refresh_token}")

    print("✅ Успешный логин. Токены сохранены.")