import requests
import pytest
import allure
from datetime import datetime, timedelta


BASE_URL = "https://staging.danone.oncallcrm.ru/api"

def test_update_visit(get_tokens, visit_id_storage):
    """Обновление визита до COMPLETED"""
    access_token, refresh_token = get_tokens  # Берем токены
    visit_id = visit_id_storage["visit_id"]  # Берем ID визита

    assert visit_id is not None, "Ошибка! Визит не найден!"

    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "x-access-token": access_token,
        "x-refresh-token": refresh_token,
        "x-version": "1001"
    }
    start_date = datetime.utcnow().isoformat() + "Z"
    end_date = (datetime.utcnow() + timedelta(minutes=15)).isoformat() + "Z"

    update_data = {
        "type": "doctor",
        "startDate": start_date,
        "endDate": end_date,
        "report": {
            "channelType": "Индивидуальный визит",
            "visitTarget": "Знакомство",
            "presentedProductsIds": [44, 56, 57]
        },
        "status": "REPORTED",
        "doctorIds": ["7b0f8e1b-54f6-4282-954e-13512bde8a05"],
        "medInstitutionId": 654247
    }

    with allure.step("Отправляем запрос на завершение визита"):
        response = requests.patch(f"{BASE_URL}/visits_next/doctor/{visit_id}", headers=headers, json=update_data)
    with allure.step("Верный код ответа"):
        assert response.status_code == 200, "Ошибка! Визит не завершен!"
    with allure.step("Статус визита - проведен!"):
        response_json = response.json()
        assert response_json["data"]["status"] == "REPORTED", "Ошибка! Статус визита не изменился!"

    print(f"✅ Визит {visit_id} успешно обновлен до REPORTED")