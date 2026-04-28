import allure

from api import User
from data import Data
from models import UserAuth, AuthResponse


class TestPositiveUserAuthorization:

    @allure.title("Успешная авторизация ранее зарегистрированного пользователя")
    def test_user_authorization_success(self):
        with allure.step("Подготовить данные существующего пользователя из data.py"):
            payload = UserAuth(email=Data.EMAIL, password=Data.PASSWORD)

        with allure.step("Отправить запрос на авторизацию"):
            response = User.login(payload.model_dump())

        with allure.step("Преобразовать ответ в модель AuthResponse"):
            auth_data = AuthResponse(**response.json())

        with allure.step("Проверить статус-код ответа"):
            assert response.status_code == 200

        with allure.step("Проверить email авторизованного пользователя"):
            assert auth_data.user.email == Data.EMAIL

        with allure.step("Проверить, что access token не пустой"):
            assert auth_data.token.access_token
