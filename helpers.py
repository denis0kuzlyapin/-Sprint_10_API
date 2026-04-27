import random
import string
from faker import Faker


class GenDataForUser:

    fake = Faker()

    @staticmethod
    def email_fake():
        email = GenDataForUser.fake.email()
        return email

    @staticmethod
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = "".join(random.choice(letters) for i in range(length))
        return random_string

    @staticmethod
    def gen_user():

        # генерируем логин, пароль и имя пользователя
        email = f"test_{GenDataForUser.email_fake()}"
        password = f"test_{GenDataForUser.generate_random_string(10)}"
        name = f"test{GenDataForUser.generate_random_string(10)}"

        # собираем тело запроса
        return {"email": email, "password": password, "name": name}
