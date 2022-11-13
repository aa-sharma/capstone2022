"""
Test cases for testing creating user and authenticating user
"""

import requests
import pytest
import logging
from utils.helpers import read_json

logger = logging.getLogger(__name__)


def test_register_user(env_config, cache):
    """tests creating a user via api"""
    users_data = read_json('./test_data/users_auth_data.json')['success']

    # name = ''.join(random.sample(string.ascii_letters, 8))
    # email = ''.join(random.sample(string.ascii_letters, 8)) + '@gmail.com'
    # password = ''.join(random.sample(string.ascii_letters, 8))

    # cache.set('users/email', email)
    # cache.set('users/password', password)

    for user_data in users_data:
        payload = {
            "name": user_data['name'],
            "email": user_data['email'],
            "password": user_data['password']
        }

        r = requests.post(f'{env_config.API_URL}/api/users', json=payload)
        if r.status_code < 200 or r.status_code >= 300:
            pytest.fail(f"request was unsuccessful. status code: {r.status_code}. json: {r.json()}")

        logger.info(f"Successfully registered user email: {user_data['email']}")

    cache.set("users_data/success", users_data)


def test_auth(env_config, cache):
    """tests fetching a token for a user via api"""

    users_data = cache.get("users_data/success", None)

    for user_data in users_data:
        payload = {
            "email": user_data['email'],
            "password": user_data['password'],
        }

        r = requests.post(f'{env_config.API_URL}/api/auth', json=payload)
        if r.status_code < 200 or r.status_code >= 300:
            pytest.fail(f"request was unsuccessful. status code: {r.status_code}. json: {r.json()}")

        token = r.json()['token']
        assert (token is not None)
        logger.info(f"Successfully authenticated email: {user_data['email']}")
        user_data['token'] = token

    cache.set('users_data/success', users_data)


def test_register_product_code(env_config, cache):
    """tests registering a product code"""

    users_data = cache.get("users_data/success", None)

    for user_data in users_data:
        payload = {"productCode": user_data['productCode']}
        headers = {'x-auth-token': user_data['token']}

        r = requests.post(f'{env_config.API_URL}/api/users/register-product-code', json=payload, headers=headers)
        if r.status_code < 200 or r.status_code >= 300:
            pytest.fail(f"request was unsuccessful. status code: {r.status_code}. json: {r.json()}")

        productCodeResponse = r.json()['productCode']

        assert (productCodeResponse == user_data['productCode'])
        logger.info(
            f"Successfully registered product code for email: {user_data['email']}. product_code: {user_data['productCode']}")


def test_auth_device(env_config, cache):
    """tests registering authentication of a device using the product code"""

    users_data = cache.get("users_data/success", None)

    for user_data in users_data:

        payload = {"productCode": user_data['productCode']}

        r = requests.post(f'{env_config.API_URL}/api/auth/device', json=payload)
        if r.status_code < 200 or r.status_code >= 300:
            pytest.fail(f"request was unsuccessful. status code: {r.status_code}. json: {r.json()}")

        token = r.json()['token']

        assert (token is not None)
        logger.info(f"Successfully authenticated using product_code: {user_data['productCode']}")


def test_private_function(env_config, cache):
    """tests private function using the users auth token"""

    users_data = cache.get("users_data/success", None)

    for user_data in users_data:
        headers = {'x-auth-token': user_data['token']}

        r = requests.get(f'{env_config.API_URL}/api/auth', headers=headers)
        if r.status_code < 200 or r.status_code >= 300:
            pytest.fail(f"request was unsuccessful. status code: {r.status_code}. json: {r.json()}")

        assert r.json()['email'] == user_data['email']
        assert r.json()['name'] == user_data['name']
        assert r.json()['productCode'] == user_data['productCode']
        logger.info(f"Successfully logged in user: {user_data['email']}")
