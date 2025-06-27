import allure
import requests

import data
from data import patch_change_user_data, del_user_data, post_register_user, exist_user_email
from helpers import mail_generator, name_generator, payload_new_user, password_generator


@allure.description('Класс изменение данных пользователя')
class TestChangeUserData:

    @allure.title('Изменение данных пользователя с неверным токеном. Ожидаем 403. Ручка: PATCH /api/auth/user')
    def test_broken_token_user_change_data(self):
        auth_token = "Bearer eyJhbGciOiJIU"
        patch_email = {"email": mail_generator()}
        change_profile_data = requests.patch(patch_change_user_data, headers={"authorization": auth_token}, data=patch_email)
        assert change_profile_data.json() == data.user_error_403_token_bad_change_data and change_profile_data.status_code == 403

    @allure.title('Пробуем изменить данные не авторизованным пользователем. Токен не передан.\n'
                  ' Ожидаем ошибку 401. Ручка: PATCH /api/auth/user')
    def test_unauthorized_user_change_data(self):
        patch_email = {"email": mail_generator()}
        change_profile_data = requests.patch(patch_change_user_data, headers={"authorization": ""}, data=patch_email)
        assert change_profile_data.json() == data.user_error_401_unauthorized_user and change_profile_data.status_code == 401

    @allure.title('Создаем, авторизуемся, изменяем имя пользователя\n'
              'Ожидаем успех 200 и 202\n'
              'Ручки: POST /api/auth/register → PATCH /api/auth/user → DELETE /api/auth/user')
    def test_change_profile_name_true(self):
        patch_name = {"name": name_generator()}
        new_user = requests.post(post_register_user, data=payload_new_user())
        auth_token = new_user.json()["accessToken"]
        change_profile_data = requests.patch(patch_change_user_data, headers={"authorization": f"{auth_token}"}, data=patch_name)
        assert change_profile_data.json()["success"] == True and change_profile_data.status_code == 200

        del_user = requests.delete(del_user_data, headers={"authorization": f"{auth_token}"})
        assert del_user.json() == data.user_delete_202 and del_user.status_code == 202

    @allure.title('Создаем, авторизуемся, изменяем email\n'
              'Ожидаем успех 200 и 202\n'
              'Ручки: POST /api/auth/register → PATCH /api/auth/user → DELETE /api/auth/user')
    def test_change_profile_email_true(self):
        patch_email = {"email": mail_generator()}
        new_user = requests.post(post_register_user, data=payload_new_user())
        auth_token = new_user.json()["accessToken"]
        change_profile_data = requests.patch(patch_change_user_data, headers={"authorization": f"{auth_token}"}, data=patch_email)
        assert change_profile_data.json()["success"] == True and change_profile_data.status_code == 200

        del_user = requests.delete(del_user_data, headers={"authorization": f"{auth_token}"})
        assert del_user.json() == data.user_delete_202 and del_user.status_code == 202

    @allure.title('Создаем, авторизуемся, изменяем пароль\n'
              'Ожидаем успех 200 и 202\n'
              'Ручки: POST /api/auth/register → PATCH /api/auth/user → DELETE /api/auth/user')
    def test_change_profile_password_true(self):
        patch_password = {"email": password_generator()}
        new_user = requests.post(post_register_user, data=payload_new_user())
        auth_token = new_user.json()["accessToken"]
        change_profile_data = requests.patch(patch_change_user_data, headers={"authorization": f"{auth_token}"}, data=patch_password)
        assert change_profile_data.json()["success"] == True and change_profile_data.status_code == 200

        del_user = requests.delete(del_user_data, headers={"authorization": f"{auth_token}"})
        assert del_user.json() == data.user_delete_202 and del_user.status_code == 202

    @allure.title('Создаем, авторизуемся, изменяем email пользователя на существующий\n'
              'Ожидаем ошибку 403 и успех 202 при удалении\n'
              'Ручки: POST /api/auth/register → PATCH /api/auth/user → DELETE /api/auth/user')
    def test_change_profile_mail_false(self):
        patch_email = {"email": exist_user_email}
        new_user = requests.post(post_register_user, data=payload_new_user())
        auth_token = new_user.json()["accessToken"]
        change_profile_data = requests.patch(patch_change_user_data, headers={"authorization": f"{auth_token}"}, data=patch_email)
        assert change_profile_data.json()["success"] == False and change_profile_data.status_code == 403

        del_user = requests.delete(del_user_data, headers={"authorization": f"{auth_token}"})
        assert del_user.json() == data.user_delete_202 and del_user.status_code == 202