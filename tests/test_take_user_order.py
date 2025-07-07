import allure
import requests

import data
from data import get_user_order, get_all_orders


@allure.description('Тестирование получения заказов пользователя')
class TestTakeUserOrder:

    @allure.title('Получение всех заказов (макс. 50)\n'
                  'Ручка: GET /api/orders/all\n'
                  'Ожидаем: 200, поля total и totalToday')
    def test_get_all_orders_true(self):
        response = requests.get(get_all_orders)
        assert response.status_code == 200
        assert response.json()["success"] == True
        assert "total" in response.json()
        assert "totalToday" in response.json()

    @allure.title('Получение всех заказов без авторизации\n'
                  'Ручка: GET /api/orders\n'
                  'Ожидаем: 401 (не авторизован)')
    def test_unauthorized_get_order_false(self):
        response = requests.get(get_user_order)
        assert response.status_code == 401
        assert response.json() == data.user_error_401_unauthorized_user

    @allure.title('Получение заказов авторизованного пользователя\n'
                  'Ручки: POST /api/auth/login → GET /api/orders\n'
                  'Ожидаем: 200, поля total и totalToday')
    def test_get_orders_authorized_user_true(self, authenticated_user):
        response = requests.get(
            get_user_order,
            headers={
                "Authorization": authenticated_user,
                "Content-Type": "application/json"
            }
        )
        assert response.status_code == 200
        assert response.json()["success"] == True
        assert "total" in response.json()
        assert "totalToday" in response.json()