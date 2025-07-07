import json
import random
import pytest
import requests

from data import get_ingredients, post_register_user, del_user_data, post_login_user, exist_user_payload
from helpers import payload_new_user

# Фикстура для получения случайного ингредиента
@pytest.fixture(scope='session')
def return_random_ingredient():

    get_info = requests.get(get_ingredients)
    data_text = json.loads(get_info.text)
    ingredients = [element['_id'] for element in data_text['data']]
    return random.choice(ingredients)

# Фикстура для регистрации и удаления тестового пользователя
@pytest.fixture
def registered_user():
    # Регистрация нового пользователя
    response = requests.post(post_register_user, data=payload_new_user())
    assert response.status_code == 200, "Не удалось зарегистрировать пользователя"
    auth_token = response.json()["accessToken"]

    yield auth_token  # Возвращаем токен для использования в тестах

    # Финализатор - удаление пользователя после завершения теста
    requests.delete(del_user_data, headers={"Authorization": auth_token})

# Фикстура для авторизации существующего пользователя
@pytest.fixture
def authenticated_user():
    response = requests.post(post_login_user, data=exist_user_payload)
    assert response.status_code == 200, "Не удалось авторизовать пользователя"
    auth_token = response.json()["accessToken"]
    yield auth_token