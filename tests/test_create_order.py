import allure
import requests

import data
from data import post_login_user, exist_user_payload, post_create_order
from helpers import password_generator


@allure.description('Класс создания заказа для неавторизованных пользователей')
class TestUnauthorizedCreateOrder:

    @allure.title('Создание заказа без авторизации\n'
                  'С валидными ингредиентами\n'
                  'Ручка: POST /api/orders\n'
                  'Ожидаем: 200')
    def test_unauthorized_create_order_with_ingredients_true(self, return_random_ingredient):
        ingredients = {"ingredients": [return_random_ingredient]}
        create_order = requests.post(post_create_order, json=ingredients)
        assert create_order.json()["success"] == True and create_order.status_code == 200

    @allure.title('Создание заказа без авторизации\n'
                  'Без ингредиентов\n'
                  'Ручка: POST /api/orders\n'
                  'Ожидаем: 400')
    def test_unauthorized_create_order_without_ingredients_false(self):
        ingredients = {"ingredients": []}
        create_order = requests.post(post_create_order, json=ingredients)
        assert create_order.json() == data.no_ingredient_error_400 and create_order.status_code == 400

    @allure.title('Создание заказа без авторизации\n'
                  'С невалидным хешем ингредиента\n'
                  'Ручка: POST /api/orders\n'
                  'Ожидаем: 500')
    def test_unauthorized_create_order_with_invalid_hash_ingredients_false(self):
        ingredients = {"ingredients": [password_generator()]}
        create_order = requests.post(post_create_order, json=ingredients)
        assert create_order.status_code == 500


@allure.description('Класс создания заказа для авторизованных пользователей')
class TestLoginUserCreateOrder:

    @allure.title('Создание заказа с авторизацией\n'
                  'С валидными ингредиентами\n'
                  'Ручки: POST /api/auth/login → POST /api/orders\n'
                  'Ожидаем: 200')
    def test_login_user_create_order_with_ingredients_true(self, return_random_ingredient):
        ingredients = {"ingredients": [return_random_ingredient]}
        response = requests.post(post_login_user, data=exist_user_payload)
        auth_token = response.json()["accessToken"]
        assert "accessToken" in response.json() and response.status_code == 200

        create_order = requests.post(post_create_order,
                                   headers={"Authorization": f"{auth_token}"},
                                   json=ingredients)
        assert create_order.json()["success"] == True and create_order.status_code == 200

    @allure.title('Создание заказа с авторизацией\n'
                  'Без ингредиентов\n'
                  'Ручки: POST /api/auth/login → POST /api/orders\n'
                  'Ожидаем: 400')
    def test_login_user_create_order_without_ingredients_false(self):
        ingredients = {"ingredients": []}
        response = requests.post(post_login_user, data=exist_user_payload)
        auth_token = response.json()["accessToken"]
        assert "accessToken" in response.json() and response.status_code == 200

        create_order = requests.post(post_create_order,
                                   headers={"Authorization": f"{auth_token}"},
                                   json=ingredients)
        assert create_order.json() == data.no_ingredient_error_400 and create_order.status_code == 400

    @allure.title('Создание заказа с авторизацией\n'
                  'С невалидным хешем ингредиента\n'
                  'Ручки: POST /api/auth/login → POST /api/orders\n'
                  'Ожидаем: 500')
    def test_login_user_create_order_with_invalid_hash_ingredients_false(self):
        ingredients = {"ingredients": [password_generator()]}
        response = requests.post(post_login_user, data=exist_user_payload)
        auth_token = response.json()["accessToken"]
        assert "accessToken" in response.json() and response.status_code == 200

        create_order = requests.post(post_create_order,
                                   headers={"Authorization": f"{auth_token}"},
                                   json=ingredients)
        assert create_order.status_code == 500