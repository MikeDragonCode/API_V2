import pytest
import os
import allure


@pytest.fixture(scope="session")
def get_tokens():
    """Читаем access_token и refresh_token из файла"""
    with open("stage/danone/visits/tokens.txt", "r") as file:
        lines = file.readlines()
        access_token = lines[0].strip()
        refresh_token = lines[1].strip()

    return access_token, refresh_token  # Возвращаем токены


@pytest.fixture(scope="session")
def visit_id_storage():
    """Хранит ID визита"""
    return {"visit_id": None}  # Используем словарь для хранения visit_id