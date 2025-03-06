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

    update_data = {
        "materialIds": [537],
        "status": "COMPLETE",
        "report": {
            "presentedProductsIds": [44, 56, 57]
        }
    }

    with allure.step("Отправляем запрос на проведение визита"):
        response = requests.patch(f"{BASE_URL}/visits_next/doctor/{visit_id}", headers=headers, json=update_data)
    with allure.step("Верный код ответа"):
        assert response.status_code == 200, "Ошибка! Визит не обновлен!"
    with allure.step("Статус визита - проведен!"):
        response_json = response.json()
        assert response_json["data"]["status"] == "COMPLETE", "Ошибка! Статус визита не изменился!"

    print(f"✅ Визит {visit_id} успешно обновлен до COMPLETED")