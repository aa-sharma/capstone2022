"""
Test cases for testing creating, getting, and deleting, exercises for when they should be successful
"""

import requests
import pytest
import logging
from utils.helpers import read_json

logger = logging.getLogger(__name__)


def test_create_exercise(env_config, cache, autheticate_admin_user):
    exercises_data = read_json('./test_data/exercise_data.json')['success']

    headers = {'x-auth-token': autheticate_admin_user['token']}

    for exercise_data in exercises_data:
        r = requests.post(f'{env_config.API_URL}/api/exercise', json=exercise_data, headers=headers)
        if r.status_code < 200 or r.status_code >= 300:
            pytest.fail(f"request was unsuccessful. status code: {r.status_code}. json: {r.json()}")

        result = r.json()
        result.pop("_id")
        assert result == exercise_data

        exercise_data['_id'] = r.json()['_id']

    logger.info("verified creating exercises from ./test_data/exercise_data.json")
    cache.set("exercises_data/success", exercises_data)


def test_get_exercise_by_id(env_config, cache, register_initial_user):
    exercises_data = cache.get("exercises_data/success", None)

    headers = {'x-auth-token': register_initial_user['token']}

    for exercise_data in exercises_data:

        r = requests.get(f'{env_config.API_URL}/api/exercise/{exercise_data["_id"]}', headers=headers)
        if r.status_code < 200 or r.status_code >= 300:
            pytest.fail(f"request was unsuccessful. status code: {r.status_code}. json: {r.json()}")

        assert r.json() == exercise_data

    logger.info("verified getting exercises from ./test_data/exercise_data.json")


def test_get_all_exercises(env_config, cache, register_initial_user):
    exercises_data = cache.get("exercises_data/success", None)

    headers = {'x-auth-token': register_initial_user['token']}

    r = requests.get(f'{env_config.API_URL}/api/exercise', headers=headers)
    if r.status_code < 200 or r.status_code >= 300:
        pytest.fail(f"request was unsuccessful. status code: {r.status_code}. json: {r.json()}")

    assert r.json()['items'] == exercises_data

    logger.info("verified getting all exercises from ./test_data/exercise_data.json")


def test_get_exercises_by_level(env_config, cache, register_initial_user):
    exercises_data = cache.get("exercises_data/success", None)

    headers = {'x-auth-token': register_initial_user['token']}

    for exercise_data in exercises_data:

        r = requests.get(f'{env_config.API_URL}/api/exercise/level/{exercise_data["level"]}', headers=headers)
        if r.status_code < 200 or r.status_code >= 300:
            pytest.fail(f"request was unsuccessful. status code: {r.status_code}. json: {r.json()}")

        for result in r.json()['items']:
            assert result['level'] == exercise_data['level']

    logger.info("verified getting exercises by level")
