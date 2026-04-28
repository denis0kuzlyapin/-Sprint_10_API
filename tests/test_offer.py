import allure

from api import Offer, User
from helpers import GenDataForUser
from models import (
    CreateOfferRequest,
    CreateOfferResponse,
    RegistrationUser,
    RegistrationResponse,
    UpdateOfferRequest,
)
from storage import TestStorage


class TestPositiveCreateOffer:

    @allure.title("Успешное создание объявления")
    def test_create_offer_success(self, auth_token):
        with allure.step("Подготовить данные для создания объявления"):
            payload = CreateOfferRequest(
                name="Тестовое объявление",
                category="Книги",
                condition="Новый",
                city="Москва",
                description="Тестовое описание",
                price=99999,
            )

        with allure.step("Отправить запрос на создание объявления"):
            response = Offer.create_offer(auth_token, payload.model_dump())

        with allure.step("Преобразовать ответ в модель CreateOfferResponse"):
            response_data = CreateOfferResponse(**response.json())

        with allure.step("Сохранить id созданного объявления для очистки после теста"):
            TestStorage.add_offer(auth_token, response_data.id)

        with allure.step("Проверить статус-код ответа"):
            assert response.status_code == 201

        with allure.step("Проверить данные созданного объявления"):
            assert response_data.name == payload.name
            assert response_data.category == payload.category
            assert response_data.condition == payload.condition
            assert response_data.city == payload.city
            assert response_data.description == payload.description
            assert response_data.price == payload.price

        with allure.step("Проверить наличие id объявления"):
            assert response_data.id is not None

    @allure.title("Успешное удаление объявления")
    def test_delete_offer_success(self, auth_token):
        with allure.step("Подготовить данные для создания объявления"):
            create_payload = CreateOfferRequest(
                name="Объявление под снос",
                category="Хобби",
                condition="Новый",
                city="Москва",
                description="Описание тест",
                price=749,
            )

        with allure.step("Создать объявление"):
            create_response = Offer.create_offer(
                auth_token, create_payload.model_dump()
            )

        with allure.step("Преобразовать ответ создания объявления в модель"):
            created_offer = CreateOfferResponse(**create_response.json())

        with allure.step(
            "Сохранить объявление в TestStorage для очистки (на случай падения теста)"
        ):
            TestStorage.add_offer(auth_token, created_offer.id)

        with allure.step("Отправить запрос на удаление объявления"):
            delete_response = Offer.delete_offer(auth_token, created_offer.id)

        with allure.step("Проверить результаты"):
            assert create_response.status_code == 201
            assert delete_response.status_code == 200


class TestNegativeEditOffer:

    @allure.title("Ошибка при редактировании чужого объявления")
    def test_edit_other_user_offer_error(self, auth_token):
        with allure.step(
            "Подготовить данные для создания объявления первым пользователем"
        ):
            create_payload = CreateOfferRequest(
                name="Объявление_1",
                category="Хобби",
                condition="Новый",
                city="Москва",
                description="Описание",
                price=178,
            )

        with allure.step("Создать объявление первым пользователем"):
            create_response = Offer.create_offer(
                auth_token, create_payload.model_dump()
            )

        with allure.step("Преобразовать ответ создания объявления в модель"):
            created_offer = CreateOfferResponse(**create_response.json())

        with allure.step("Сохранить id созданного объявления для очистки после теста"):
            TestStorage.add_offer(auth_token, created_offer.id)

        with allure.step("Подготовить и зарегистрировать второго пользователя"):
            second_user_data = GenDataForUser.gen_user()
            second_user_payload = RegistrationUser(**second_user_data)
            second_user_response = User.create_user(second_user_payload.model_dump())
            second_user = RegistrationResponse(**second_user_response.json())
            second_user_token = second_user.access_token.access_token

        with allure.step(
            "Подготовить данные для попытки редактирования объявления вторым пользователем"
        ):
            update_payload = UpdateOfferRequest(
                description="Попытка изменить чужое объявление"
            )

        with allure.step(
            "Отправить запрос на редактирование чужого объявления вторым пользователем"
        ):
            update_response = Offer.change_data_offer(
                second_user_token, update_payload.model_dump(), created_offer.id
            )

        with allure.step("Получить тело ответа с ошибкой"):
            error_data = update_response.json()

        with allure.step("Проверить результаты"):
            assert create_response.status_code == 201
            assert second_user_response.status_code == 201
            assert update_response.status_code == 401
            assert (
                error_data["message"]
                == "Оффер не найден или у вас нет прав на его редактирование"
            )
            assert error_data["error"] == "Unauthorized"
            assert error_data["statusCode"] == 401
