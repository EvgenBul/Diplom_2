import allure
import requests

import data
from data import  post_create_order
from helpers import password_generator


@allure.description('Класс создания заказа для неавторизованных пользователей')
class TestUnauthorizedCreateOrder:

    @allure.title('Создание заказа без авторизации\n'
                  'С валидными ингредиентами\n'
                  'Ручка: POST /api/orders\n'
                  'Ожидаем: 200')
    def test_unauthorized_create_order_with_ingredients_true(self, return_random_ingredient):
        ingredients = {"ingredients": [return_random_ingredient]}
        response = requests.post(post_create_order, json=ingredients)
        assert response.json()["success"] == True
        assert response.status_code == 200

    @allure.title('Создание заказа без авторизации\n'
                  'Без ингредиентов\n'
                  'Ручка: POST /api/orders\n'
                  'Ожидаем: 400')
    def test_unauthorized_create_order_without_ingredients_false(self):
        ingredients = {"ingredients": []}
        response = requests.post(post_create_order, json=ingredients)
        assert response.json() == data.no_ingredient_error_400
        assert response.status_code == 400

    @allure.title('Создание заказа без авторизации\n'
                  'С невалидным хешем ингредиента\n'
                  'Ручка: POST /api/orders\n'
                  'Ожидаем: 500')
    def test_unauthorized_create_order_with_invalid_hash_ingredients_false(self):
        ingredients = {"ingredients": [password_generator()]}
        response = requests.post(post_create_order, json=ingredients)
        assert response.status_code == 500


@allure.description('Класс создания заказа для авторизованных пользователей')
class TestLoginUserCreateOrder:

    @allure.title('Создание заказа с авторизацией\n'
                  'С валидными ингредиентами\n'
                  'Ручки: POST /api/auth/login → POST /api/orders\n'
                  'Ожидаем: 200')
    def test_login_user_create_order_with_ingredients_true(self, authenticated_user, return_random_ingredient):
        ingredients = {"ingredients": [return_random_ingredient]}
        response = requests.post(
            post_create_order,
            headers={"Authorization": authenticated_user},
            json=ingredients
        )
        assert response.json()["success"] == True
        assert response.status_code == 200

    @allure.title('Создание заказа с авторизацией\n'
                  'Без ингредиентов\n'
                  'Ручки: POST /api/auth/login → POST /api/orders\n'
                  'Ожидаем: 400')
    def test_login_user_create_order_without_ingredients_false(self, authenticated_user):
        ingredients = {"ingredients": []}
        response = requests.post(
            post_create_order,
            headers={"Authorization": authenticated_user},
            json=ingredients
        )
        assert response.json() == data.no_ingredient_error_400
        assert response.status_code == 400

    @allure.title('Создание заказа с авторизацией\n'
                  'С невалидным хешем ингредиента\n'
                  'Ручки: POST /api/auth/login → POST /api/orders\n'
                  'Ожидаем: 500')
    def test_login_user_create_order_with_invalid_hash_ingredients_false(self, authenticated_user):
        ingredients = {"ingredients": [password_generator()]}
        response = requests.post(
            post_create_order,
            headers={"Authorization": authenticated_user},
            json=ingredients
        )
        assert response.status_code == 500