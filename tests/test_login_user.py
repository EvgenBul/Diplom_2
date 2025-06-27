import allure
import requests

import data
from data import post_login_user, exist_user_payload
from helpers import mail_generator, password_generator


@allure.description('Класс вариантов входа в систему и возможные ошибки.')
class TestLoginUser:

    @allure.title('Логинемся под существующим пользователем. Есть в ответе accessToken - значит авторизован. Статус ответа 200.')
    def test_post_login_user_true(self):
        response = requests.post(post_login_user, data=exist_user_payload)
        assert "accessToken" in response.json() and response.status_code == 200

    @allure.title('Не авторизованный пользователь. Генерируем логин и пароль. Статус ответа 401.')
    def test_unauthorized_user(self):
        payload = {
            "email": mail_generator(),
            "password": password_generator()
        }
        response = requests.post(post_login_user, data=payload)
        assert response.json() == data.user_error_403_unauthorized and response.status_code == 401

    @allure.title('Не авторизованный пользователь. Не передали логин, генерируем пароль. Статус ответа 401.')
    def test_unauthorized_user_no_login(self):
        payload = {
            "email": "",
            "password": password_generator()
        }
        response = requests.post(post_login_user, data=payload)
        assert response.json() == data.user_error_403_unauthorized and response.status_code == 401

    @allure.title('Не авторизованный пользователь. Не передали пароль, генерируем логин. Статус ответа 401.')
    def test_unauthorized_user_no_password(self):
        payload = {
            "email": mail_generator(),
            "password": ""
        }
        response = requests.post(post_login_user, data=payload)
        assert response.json() == data.user_error_403_unauthorized and response.status_code == 401