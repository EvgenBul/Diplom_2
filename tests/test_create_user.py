import allure
import requests

import data
from helpers import mail_generator, password_generator, name_generator, payload_new_user
from data import post_register_user, del_user_data, exist_user_email


@allure.description('Класс тестирования регистрации пользователя')
class TestCreateUser:

    @allure.title('Успешная регистрация и удаление пользователя\n'
                  'Ручки: POST /api/auth/register → DELETE /api/auth/user\n'
                  'Ожидаем: 200 (регистрация), 202 (удаление)')
    def test_create_user_true(self):
        response = requests.post(post_register_user, data=payload_new_user())
        auth_token = response.json()["accessToken"]
        assert "accessToken" in response.json() and response.status_code == 200

        del_user = requests.delete(del_user_data, headers={"Authorization": f"{auth_token}"})
        assert del_user.json() == data.user_delete_202 and del_user.status_code == 202

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
        assert response.json() == data.user_error_403_exists and response.status_code == 403

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
        assert response.json() == data.user_error_403_no_required_fields and response.status_code == 403

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
        assert response.json() == data.user_error_403_no_required_fields and response.status_code == 403

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
        assert response.json() == data.user_error_403_no_required_fields and response.status_code == 403

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
        assert response.json() == data.user_error_403_no_required_fields and response.status_code == 403