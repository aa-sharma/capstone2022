"""
Test cases for testing creating, getting, and deleting, exercises for when there should be an error
"""

import requests
import logging
from utils.helpers import read_json

logger = logging.getLogger(__name__)


def test_create_user_level_progress_fail(env_config, autheticate_admin_user):
    """tests creating exercises for failure conditions"""

    user_level_progresses_data = read_json('./test_data/user_level_progress_data.json')['error']['create']
    headers = {'x-auth-token': autheticate_admin_user['token']}

    for user_level_progress_data in user_level_progresses_data:
        r = requests.post(f'{env_config.API_URL}/api/user-level-progress',
                          json=user_level_progress_data['data'], headers=headers)

        assert r.status_code == user_level_progress_data['status_code']
        assert r.json()['errors'][0]['msg'] == user_level_progress_data['msg']
        logger.info(f"Successfully confirmed exercise error with error msg: {user_level_progress_data['msg']}")


def test_get_user_level_progress_by_id_fail(env_config, register_initial_user):
    """tests getting exercises by id for failure conditions"""

    user_level_progresses_data = read_json('./test_data/user_level_progress_data.json')['error']['get']
    headers = {'x-auth-token': register_initial_user['token']}

    for user_level_progress_data in user_level_progresses_data:
        r = requests.get(
            f'{env_config.API_URL}/api/user-level-progress/{user_level_progress_data["data"]["_id"]}', headers=headers)

        assert r.status_code == user_level_progress_data['status_code']
        assert r.json()['errors'][0]['msg'] == user_level_progress_data['msg']
        logger.info(f"Successfully confirmed exercise error with error msg: {user_level_progress_data['msg']}")


def test_get_user_level_progress_by_level_fail(env_config, register_initial_user):
    """tests getting exercises by id for failure conditions"""

    user_level_progresses_data = read_json('./test_data/user_level_progress_data.json')['error']['get_by_level']
    headers = {'x-auth-token': register_initial_user['token']}

    for user_level_progress_data in user_level_progresses_data:
        r = requests.get(
            f'{env_config.API_URL}/api/user-level-progress/level/{user_level_progress_data["data"]["level"]}', headers=headers)

        assert r.status_code == user_level_progress_data['status_code']
        assert r.json()['errors'][0]['msg'] == user_level_progress_data['msg']
        logger.info(f"Successfully confirmed exercise error with error msg: {user_level_progress_data['msg']}")
