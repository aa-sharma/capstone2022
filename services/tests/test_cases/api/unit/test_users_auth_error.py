"""
Test cases for testing creating user and authenticating user
"""

import requests
import logging
from utils.helpers import read_json

logger = logging.getLogger(__name__)


def test_register_user_fail(env_config, register_initial_user):
    """tests registering a user for failure conditions"""

    users_data = read_json('./test_data/users_auth_data.json')['error']['register']

    for user_data in users_data:
        payload = {
            "name": user_data['data']['name'],
            "email": user_data['data']['email'],
            "password": user_data['data']['password']
        }
        if not user_data['data']['name']:
            payload.pop("name")

        r = requests.post(f'{env_config.API_URL}/api/users', json=payload)

        assert r.status_code == user_data['status_code']
        assert r.json()['errors'][0]['msg'] == user_data['msg']
        logger.info(f"Successfully confirmed error with error msg: {user_data['msg']}")


def test_update_user_fail(env_config, register_initial_user):
    """tests registering a user for failure conditions"""

    update_users_data = read_json('./test_data/users_auth_data.json')['error']['update_user']

    for update_user_data in update_users_data:
        headers = {'x-auth-token': register_initial_user['token']}
        r = requests.put(f'{env_config.API_URL}/api/users',
                         json=update_user_data['data'], headers=headers)
        assert r.status_code == update_user_data['status_code']
        assert r.json()['errors'][0]['msg'] == update_user_data['msg']
        logger.info(f"Successfully confirmed error with error msg: {update_user_data['msg']}")


def test_auth_fail(env_config, register_initial_user):
    """tests fetching a token for a user via api"""

    auths_data = read_json('./test_data/users_auth_data.json')['error']['auth']
    for auth_data in auths_data:
        payload = {
            "email": auth_data['data']['email'],
            "password": auth_data['data']['password'],
        }
        if not auth_data['data']['password']:
            payload.pop("password")

        r = requests.post(f'{env_config.API_URL}/api/auth', json=payload)
        assert r.status_code == auth_data['status_code']
        assert r.json()['errors'][0]['msg'] == auth_data['msg']
        logger.info(f"Successfully confirmed error with error msg: {auth_data['msg']}")


def test_auth_device_fail(env_config, register_initial_user):
    """tests fetching a token for a user via api"""

    auth_devices_data = read_json('./test_data/users_auth_data.json')['error']['auth_device']

    for auth_device_data in auth_devices_data:
        payload = {"productCode": auth_device_data['data']['productCode']}

        r = requests.post(f'{env_config.API_URL}/api/auth/device', json=payload)

        assert r.status_code == auth_device_data['status_code']
        assert r.json()['errors'][0]['msg'] == auth_device_data['msg']
        logger.info(f"Successfully confirmed error with error msg: {auth_device_data['msg']}")


def test_private_function_fail(env_config, cache, register_initial_user):
    """tests private function using the users auth token"""

    # cut off last digit of token to make it invalid
    headers = {'x-auth-token': register_initial_user['token'][:-2]}

    r = requests.get(f'{env_config.API_URL}/api/auth', headers=headers)

    expected_error_msg = 'Token is not valid'
    assert r.status_code == 401
    assert r.json()['errors'][0]['msg'] == expected_error_msg
    logger.info(f"Successfully confirmed error with error msg: {expected_error_msg}")

    headers = {'x-auth-token': None}

    r = requests.get(f'{env_config.API_URL}/api/auth', headers=headers)

    expected_error_msg = 'No token, authorization denied'
    assert r.status_code == 401
    assert r.json()['errors'][0]['msg'] == expected_error_msg
    logger.info(f"Successfully confirmed error with error msg: {expected_error_msg}")
