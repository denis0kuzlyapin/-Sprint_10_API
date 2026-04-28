import pytest
from data import Data
from api import User, Offer
from helpers import GenDataForUser
from storage import TestStorage
from models import UserAuth, AuthResponse, RegistrationUser, RegistrationResponse


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
    login_payload = UserAuth(email=Data.EMAIL, password=Data.PASSWORD)

    login_response = User.login(login_payload.model_dump())

    if login_response.status_code != 201:
        raise AssertionError(
            f"Не удалось получить токен. Статус: {login_response.status_code}, тело: {login_response.text}"
        )

    auth_data = AuthResponse(**login_response.json())
    return auth_data.token.access_token


@pytest.fixture(scope="function")
def created_user():
    # Создает нового пользователя и возвращает его данные
    user_data = GenDataForUser.gen_user()
    payload = RegistrationUser(**user_data)

    response = User.create_user(payload.model_dump())

    registration_data = RegistrationResponse(**response.json())
    token = registration_data.access_token.access_token

    return {
        "token": token,
        "email": payload.email,
        "password": payload.password,
        "submitPassword": payload.submitPassword,
        "name": registration_data.user.name,
        "response": response,
    }
