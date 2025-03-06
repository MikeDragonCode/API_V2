import requests
import pytest
from datetime import datetime, timedelta
import allure

BASE_URL = "https://staging.danone.oncallcrm.ru/api"


def test_create_visit(get_tokens, visit_id_storage):
    """Создание визита и сохранение visit_id"""
    access_token, refresh_token = get_tokens  # Получаем токены

    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "x-access-token": access_token,
        "x-refresh-token": refresh_token,
        "x-version": "1001"
    }
    start_date = datetime.utcnow().isoformat() + "Z"
    end_date = (datetime.utcnow() + timedelta(minutes=15)).isoformat() + "Z"

    data = {
        "type": "doctor",
        "status": "PLANNED",
        "startDate": start_date,
        "endDate": end_date,
        "medInstitutionId": 654247,
        "doctorIds": ["7b0f8e1b-54f6-4282-954e-13512bde8a05"]
    }
    with allure.step("Визит создан!"):
        response = requests.post(f"{BASE_URL}/visits_next", headers=headers, json=data)
        assert response.status_code == 201, "Ошибка! Визит не создан!"

    response_json = response.json()
    visit_id = response_json["data"]["id"]

    # Сохраняем visit_id в словарь
    visit_id_storage["visit_id"] = visit_id

    print(f"✅ Визит создан с ID: {visit_id}")