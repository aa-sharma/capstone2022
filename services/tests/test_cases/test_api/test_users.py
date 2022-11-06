"""
Test cases for testing creating user and authenticating user
"""

import requests
import pytest
import string
import random
import logging

logger = logging.getLogger(__name__)

def test_register_user(env_config, cache):
    """tests creating a user via api"""

    name = ''.join(random.sample(string.ascii_letters, 8))
    email = ''.join(random.sample(string.ascii_letters, 8)) + '@gmail.com'
    password = ''.join(random.sample(string.ascii_letters, 8))

    cache.set('users/email', email)
    cache.set('users/password', password)

    payload = {
        "name": name,
        "email": email,
        "password": password
        }

    r = requests.post(f'{env_config.API_URL}/api/users', json=payload)
    if r.status_code < 200 or r.status_code >= 300:
        pytest.fail(f"request was unsuccessful. status code: {r.status_code}. json: {r.json()}")

def test_auth(env_config, cache):
    """tests fetching a token for a user via api"""

    email = cache.get('users/email', None)
    password = cache.get('users/password', None)
    
    payload = {"email": email, "password": password}

    r = requests.post(f'{env_config.API_URL}/api/auth', json=payload)
    if r.status_code < 200 or r.status_code >= 300:
        pytest.fail(f"request was unsuccessful. status code: {r.status_code}. json: {r.json()}")

    json = r.json()
    token = json['token']
    assert(token is not None)

    cache.set('users/token', token)

def test_register_product_code(env_config, cache):
    """tests registering a product code"""

    token = cache.get('users/token', None)
    productCode = ''.join(random.sample(string.ascii_letters, 8))

    payload = {"productCode": productCode}
    headers = {'x-auth-token': token}

    r = requests.post(f'{env_config.API_URL}/api/users/register-product-code', json=payload, headers=headers)
    if r.status_code < 200 or r.status_code >= 300:
        pytest.fail(f"request was unsuccessful. status code: {r.status_code}. json: {r.json()}")

    json = r.json()
    productCodeResponse = json['productCode']

    assert(productCodeResponse == productCode)
    
    cache.set('users/productCode', productCode)

def test_auth_device(env_config, cache):
    """tests registering authentication of a device using the product code"""

    productCode = cache.get('users/productCode', None)

    payload = {"productCode": productCode}

    r = requests.post(f'{env_config.API_URL}/api/auth/device', json=payload)
    if r.status_code < 200 or r.status_code >= 300:
        pytest.fail(f"request was unsuccessful. status code: {r.status_code}. json: {r.json()}")

    json = r.json()
    token = json['token']
    
    assert(token is not None)
    
def test_private_function(env_config, cache):
    """tests private function using the users auth token"""

    token = cache.get('users/token', None)
    email = cache.get('users/email', None)

    headers = {'x-auth-token': token}

    r = requests.get(f'{env_config.API_URL}/api/auth', headers=headers)
    if r.status_code < 200 or r.status_code >= 300:
        pytest.fail(f"request was unsuccessful. status code: {r.status_code}. json: {r.json()}")

    json = r.json()
    assert json['email'] == email

def test_private_function_fail(env_config, cache):
    """tests private function using the users auth token"""

    token = cache.get('users/token', None)[:-2] # cut off last digit of token to make it invalid

    headers = {'x-auth-token': token}

    r = requests.get(f'{env_config.API_URL}/api/auth', headers=headers)
    
    assert(r.status_code == 401)
    json = r.json()
    assert json['msg'] == 'Token is not valid'