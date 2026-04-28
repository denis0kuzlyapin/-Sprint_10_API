import allure

from api import User
from models import RegistrationResponse, RegistrationUser


class TestPositiveUserRegistration:

    @allure.title("Успешная регистрация уникального пользователя")
    def test_user_registration_success(self, created_user):
        with allure.step(
            "Выполнить регистрацию уникального пользователя (фикстура 'created_user')"
        ):
            response = created_user["response"]

        with allure.step("Преобразовать ответ в модель RegistrationResponse"):
            response_data = RegistrationResponse(**response.json())

        with allure.step("Проверить, что статус-код 201"):
            assert response.status_code == 201

        with allure.step("Проверить email зарегистрированного пользователя"):
            assert response_data.user.email == created_user["email"]

        with allure.step("Проверить наличие access token"):
            assert response_data.access_token.access_token


class TestNegativeUserRegistration:

    @allure.title("Ошибка при повторной регистрации пользователя")
    def test_repeat_user_registration_error(self, created_user):
        with allure.step(
            "Подготовить данные, используя результат регистрации, который создала фикстура 'created_user'"
        ):
            payload = RegistrationUser(
                email=created_user["email"],
                password=created_user["password"],
                submitPassword=created_user["submitPassword"],
            )

        with allure.step("Отправить повторный запрос на регистрацию с тем же email"):
            response = User.create_user(payload.model_dump())
            error_data = response.json()

        with allure.step("Проверить, что сервер вернул ошибку"):
            assert response.status_code == 400

        with allure.step("Проверить, что в ответе есть текст ошибки"):
            assert error_data["statusCode"] == 400
            assert error_data["message"] == "Почта уже используется"
