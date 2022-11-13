import pytest
import logging
from pprint import pformat, pprint
import requests
from utils.helpers import read_json

logger = logging.getLogger(__name__)


@pytest.fixture(scope='session')
def register_initial_user(env_config):
    test_user_data = read_json('./test_data/users_auth_data.json')
    user_data = {
        "name": test_user_data["successful_user_data"]["name"],
        "email": test_user_data["successful_user_data"]["email"],
        "password": test_user_data["successful_user_data"]["password"]
    }

    r = requests.post(f'{env_config.API_URL}/api/users', json=user_data)
    if r.status_code < 200 or r.status_code >= 300:
        pytest.fail(f"request was unsuccessful. status code: {r.status_code}. json: {r.json()}")

    r = requests.post(f'{env_config.API_URL}/api/auth', json=user_data)
    if r.status_code < 200 or r.status_code >= 300:
        pytest.fail(f"request was unsuccessful. status code: {r.status_code}. json: {r.json()}")

    user_data['token'] = r.json()['token']

    payload = {"productCode": test_user_data["successful_user_data"]["productCode"]}
    headers = {'x-auth-token': user_data['token']}

    r = requests.post(f'{env_config.API_URL}/api/users/register-product-code', json=payload, headers=headers)
    if r.status_code < 200 or r.status_code >= 300:
        pytest.fail(f"request was unsuccessful. status code: {r.status_code}. json: {r.json()}")

    user_data['productCode'] = test_user_data["successful_user_data"]["productCode"]

    yield user_data


@pytest.fixture(scope='session')
def autheticate_admin_user(env_config):

    admin_data = {
        'email': env_config.SERVER_ADMIN_EMAIL,
        'password': env_config.SERVER_ADMIN_PASSWORD
    }

    r = requests.post(f'{env_config.API_URL}/api/auth', json=admin_data)
    if r.status_code < 200 or r.status_code >= 300:
        pytest.fail(f"request was unsuccessful. status code: {r.status_code}. json: {r.json()}")

    admin_data['token'] = r.json()['token']

    yield admin_data
