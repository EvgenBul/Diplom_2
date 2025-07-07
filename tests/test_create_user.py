import allure
import requests

import data
from data import post_register_user, exist_user_email
from helpers import mail_generator, password_generator, name_generator


@allure.description('Класс тестирования регистрации пользователя')
class TestCreateUser:

    @allure.title('Регистрация без password\n'
                  'Ручка: POST /api/auth/register\n'
                  'Ожидаем: 403')
    def test_create_user_true(self, registered_user):
        assert True  # Фикстура уже проверила успешность регистрации

    @allure.title('Попытка регистрации с существующим email\n'
                  'Ручка: POST /api/auth/register\n'
                  'Ожидаем: 403')
    def test_cant_create_two_same_user_false(self):
        payload = {
            "email": exist_user_email,
            "password": password_generator(),
            "name": name_generator()
        }
        response = requests.post(post_register_user, data=payload)
        assert response.json() == data.user_error_403_exists
        assert response.status_code == 403

    @allure.title('Регистрация без email\n'
                  'Ручка: POST /api/auth/register\n'
                  'Ожидаем: 403')
    def test_missing_email_data_false(self):
        payload = {
            "email": "",
            "password": password_generator(),
            "name": name_generator()
        }
        response = requests.post(post_register_user, data=payload)
        assert response.json() == data.user_error_403_no_required_fields
        assert response.status_code == 403

    @allure.title('Регистрация без password\n'
                  'Ручка: POST /api/auth/register\n'
                  'Ожидаем: 403')
    def test_missing_password_data_false(self):
        payload = {
            "email": mail_generator(),
            "password": "",
            "name": name_generator()
        }
        response = requests.post(post_register_user, data=payload)
        assert response.json() == data.user_error_403_no_required_fields
        assert response.status_code == 403

    @allure.title('Регистрация без name\n'
                  'Ручка: POST /api/auth/register\n'
                  'Ожидаем: 403')
    def test_missing_name_data_true(self):
        payload = {
            "email": mail_generator(),
            "password": password_generator(),
            "name": ""
        }
        response = requests.post(post_register_user, data=payload)
        assert response.json() == data.user_error_403_no_required_fields
        assert response.status_code == 403

    @allure.title('Регистрация без всех обязательных полей\n'
                  'Ручка: POST /api/auth/register\n'
                  'Ожидаем: 403')
    def test_cant_create_without_fields_false(self):
        payload = {
            "email": "",
            "password": "",
            "name": ""
        }
        response = requests.post(post_register_user, data=payload)
        assert response.json() == data.user_error_403_no_required_fields
        assert response.status_code == 403