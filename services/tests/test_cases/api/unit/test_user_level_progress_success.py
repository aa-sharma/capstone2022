"""
Test cases for testing creating, getting, and deleting, exercises for when they should be successful
"""

import requests
import pytest
import logging
from utils.helpers import read_json

logger = logging.getLogger(__name__)


def test_create_user_level_progress(env_config, cache, register_initial_user):
    user_level_progresses_data = read_json('./test_data/user_level_progress_data.json')['success']

    headers = {'x-auth-token': register_initial_user['token']}

    for user_level_progress_data in user_level_progresses_data:
        r = requests.post(f'{env_config.API_URL}/api/user-level-progress',
                          json=user_level_progress_data, headers=headers)
        if r.status_code < 200 or r.status_code >= 300:
            pytest.fail(f"request was unsuccessful. status code: {r.status_code}. json: {r.json()}")

        result = r.json()
        result.pop("_id")
        result.pop("date")
        assert result == user_level_progress_data

        user_level_progress_data['_id'] = r.json()['_id']
        user_level_progress_data['date'] = r.json()['date']

    logger.info("verified creating user level progress report from ./test_data/user_level_progress_data.json")
    cache.set("user_level_progresses_data/success", user_level_progresses_data)


def test_get_user_level_progress_by_id(env_config, cache, register_initial_user):
    user_level_progresses_data = cache.get("user_level_progresses_data/success", None)

    headers = {'x-auth-token': register_initial_user['token']}

    for user_level_progress_data in user_level_progresses_data:
        r = requests.get(
            f'{env_config.API_URL}/api/user-level-progress/{user_level_progress_data["_id"]}', headers=headers)
        if r.status_code < 200 or r.status_code >= 300:
            pytest.fail(f"request was unsuccessful. status code: {r.status_code}. json: {r.json()}")

        assert r.json() == user_level_progress_data

    logger.info("verified getting user level progress reports by id from ./test_data/user_level_progress_data.json")


def test_get_all_user_level_progress(env_config, cache, register_initial_user):
    user_level_progresses_data = cache.get("user_level_progresses_data/success", None)

    headers = {'x-auth-token': register_initial_user['token']}

    r = requests.get(f'{env_config.API_URL}/api/user-level-progress', headers=headers)
    if r.status_code < 200 or r.status_code >= 300:
        pytest.fail(f"request was unsuccessful. status code: {r.status_code}. json: {r.json()}")

    assert __sort_by_date(r.json()['items']) == __sort_by_date(user_level_progresses_data)

    logger.info("verified getting all user level progress reports from ./test_data/user_level_progress_data.json")


def test_get_user_level_progress_by_level(env_config, cache, register_initial_user):
    user_level_progresses_data = cache.get("user_level_progresses_data/success", None)

    headers = {'x-auth-token': register_initial_user['token']}

    for user_level_progress_data in user_level_progresses_data:

        r = requests.get(
            f'{env_config.API_URL}/api/user-level-progress/level/{user_level_progress_data["exercise"]["level"]}', headers=headers)
        if r.status_code < 200 or r.status_code >= 300:
            pytest.fail(f"request was unsuccessful. status code: {r.status_code}. json: {r.json()}")

        for result in r.json()['items']:
            assert result['exercise']['level'] == user_level_progress_data['exercise']['level']

    logger.info("verified getting user level progress report by level")


def __sort_by_date(list):
    return sorted(list, key=lambda i: i['date'])
