"""
Test cases for testing creating user and authenticating user
"""

import requests
import pytest
import string
import random
import logging

logger = logging.getLogger(__name__)

def test_post_users(env_config, cache):
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

def test_post_token(env_config, cache):
    """tests fetching a token for a user via api"""

    email = cache.get('users/email', None)
    password = cache.get('users/password', None)
    
    payload = {"email": email, "password": password}

    r = requests.post(f'{env_config.API_URL}/api/auth', json=payload)
    if r.status_code < 200 or r.status_code >= 300:
        pytest.fail(f"request was unsuccessful. status code: {r.status_code}. json: {r.json()}")

    json = r.json()
    token = json['token']
    cache.set('users/token', token)

def test_get_user(env_config, cache):
    """tests private function to get a user using the users auth token"""

    token = cache.get('users/token', None)
    email = cache.get('users/email', None)

    headers = {'x-auth-token': token}

    r = requests.get(f'{env_config.API_URL}/api/auth', headers=headers)
    if r.status_code < 200 or r.status_code >= 300:
        pytest.fail(f"request was unsuccessful. status code: {r.status_code}. json: {r.json()}")

    json = r.json()
    assert json['email'] == email