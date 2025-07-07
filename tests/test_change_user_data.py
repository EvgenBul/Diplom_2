import allure
import requests

import data
from data import patch_change_user_data
from helpers import mail_generator, name_generator, password_generator


@allure.description('Класс изменения данных пользователя')
class TestChangeUserData:

    @allure.title('Изменение данных пользователя с неверным токеном. Ожидаем 403. Ручка: PATCH /api/auth/user')
    def test_broken_token_user_change_data(self):
        auth_token = "Bearer eyJhbGciOiJIU"
        patch_email = {"email": mail_generator()}
        response = requests.patch(
            patch_change_user_data,
            headers={"Authorization": auth_token},
            data=patch_email
        )
        assert response.json() == data.user_error_403_token_bad_change_data
        assert response.status_code == 403

    @allure.title('Пробуем изменить данные не авторизованным пользователем. Токен не передан.\n'
                  ' Ожидаем ошибку 401. Ручка: PATCH /api/auth/user')
    def test_unauthorized_user_change_data(self):
        patch_email = {"email": mail_generator()}
        response = requests.patch(
            patch_change_user_data,
            headers={"Authorization": ""},
            data=patch_email
        )
        assert response.json() == data.user_error_401_unauthorized_user
        assert response.status_code == 401

    @allure.title('Создаем, авторизуемся, изменяем имя пользователя\n'
                  'Ожидаем успех 200 и 202\n'
                  'Ручки: POST /api/auth/register → PATCH /api/auth/user')
    def test_change_profile_name_true(self, registered_user):
        patch_name = {"name": name_generator()}
        response = requests.patch(
            patch_change_user_data,
            headers={"Authorization": registered_user},
            data=patch_name
        )
        assert response.json()["success"] == True
        assert response.status_code == 200

    @allure.title('Создаем, авторизуемся, изменяем email\n'
                  'Ожидаем успех 200 и 202\n'
                  'Ручки: POST /api/auth/register → PATCH /api/auth/user')
    def test_change_profile_email_true(self, registered_user):
        patch_email = {"email": mail_generator()}
        response = requests.patch(
            patch_change_user_data,
            headers={"Authorization": registered_user},
            data=patch_email
        )
        assert response.json()["success"] == True
        assert response.status_code == 200

    @allure.title('Создаем, авторизуемся, изменяем пароль\n'
                  'Ожидаем успех 200 и 202\n'
                  'Ручки: POST /api/auth/register → PATCH /api/auth/user')
    def test_change_profile_password_true(self, registered_user):
        patch_password = {"password": password_generator()}
        response = requests.patch(
            patch_change_user_data,
            headers={"Authorization": registered_user},
            data=patch_password
        )
        assert response.json()["success"] == True
        assert response.status_code == 200

    @allure.title('Создаем, авторизуемся, изменяем email пользователя на существующий\n'
                  'Ожидаем ошибку 403 и успех 202 при удалении\n'
                  'Ручки: POST /api/auth/register → PATCH /api/auth/user')
    def test_change_profile_mail_false(self, registered_user):
        patch_email = {"email": data.exist_user_email}
        response = requests.patch(
            patch_change_user_data,
            headers={"Authorization": registered_user},
            data=patch_email
        )
        assert response.json()["success"] == False
        assert response.status_code == 403