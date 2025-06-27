import allure
import requests

import data
from data import post_login_user, exist_user_payload, get_user_order, get_all_orders


@allure.description('Тестирование получения заказов пользователя')
class TestTakeUserOrder:

    @allure.title('Получение всех заказов (макс. 50)\n'
                  'Ручка: GET /api/orders/all\n'
                  'Ожидаем: 200, поля total и totalToday')
    def test_get_all_orders_true(self):
        response = requests.get(get_all_orders)
        assert response.status_code == 200
        assert response.json()["success"] == True
        assert "total" in response.json() and "totalToday" in response.json()

    @allure.title('Попытка получить заказы без авторизации\n'
                  'Ручка: GET /api/orders\n'
                  'Ожидаем: 401 (неавторизован)')
    def test_unauthorized_get_order_false(self):
        response = requests.get(get_user_order)
        assert response.status_code == 401
        assert response.json() == data.user_error_401_unauthorized_user

    @allure.title('Получение заказов авторизованного пользователя\n'
                  'Ручки: POST /api/auth/login → GET /api/orders\n'
                  'Ожидаем: 200, поля total и totalToday')
    def test_get_orders_authorized_user_true(self):
        # Авторизация
        response = requests.post(post_login_user, data=exist_user_payload)
        assert response.status_code == 200
        assert "accessToken" in response.json()

        # Извлекаем токен (убедимся, что он содержит "Bearer ")
        auth_token = response.json()["accessToken"]
        if not auth_token.startswith("Bearer "):
            auth_token = f"Bearer {auth_token}"

        # Получение заказов
        order_info = requests.get(
            get_user_order,
            headers={
                "Authorization": auth_token,
                "Content-Type": "application/json"
            }
        )

        # Проверяем ответ
        assert order_info.status_code == 200, f"Ожидался статус 200, получен {order_info.status_code}. Ответ: {order_info.text}"
        assert order_info.json()["success"] == True
        assert "total" in order_info.json()
        assert "totalToday" in order_info.json()