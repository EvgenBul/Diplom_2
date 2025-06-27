import json
import random

import pytest
import requests

from data import get_ingredients


@pytest.fixture(scope='session')
def return_random_ingredient():
    get_info = requests.get(get_ingredients)
    data_text = json.loads(get_info.text)
    ingredients = [element['_id'] for element in data_text['data']]
    return random.choice(ingredients)