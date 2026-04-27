import pytest
from data import Data
from api import User, Offer
from helpers import GenDataForUser
from storage import TestStorage


@pytest.fixture(autouse=True, scope="function")
def cleanup_after_test():
    # Очистка после каждого теста
    yield

    for token, offer_id in TestStorage.get_offers():
        try:
            Offer.delete_offer(token, offer_id)
        except Exception as e:
            print(f"Не удалось удалить объявление {offer_id}: {e}")
    TestStorage.clear_offers()


@pytest.fixture
def auth_token():
    # Возвращает токен пользователя
    login_payload = {"email": Data.EMAIL, "password": Data.PASSWORD}
    login_response = User.login(login_payload)
    token = login_response.json()["access_token"]

    if login_response.status_code != 200:
        raise AssertionError(
            f"Не удалось получить токен. Статус: {login_response.status_code}, тело: {login_response.text}"
        )
    else:
        return token


@pytest.fixture(scope="function")
def created_user():
    # Создает нового пользователя и возвращает его данные
    payload = GenDataForUser.gen_user()
    response = User.create_user(payload)
    token = response.json()["access_token"]

    return {
        "token": token,
        "email": payload["email"],
        "name": payload["name"],
        "password": payload["password"],
        "response": response,
    }
