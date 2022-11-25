"""
Test cases for testing creating, getting, and deleting, exercises for when there should be an error
"""

import requests
import logging
from utils.helpers import read_json

logger = logging.getLogger(__name__)


def test_create_exercise_fail(env_config, autheticate_admin_user):
    """tests creating exercises for failure conditions"""

    exercises_data = read_json('./test_data/exercise_data.json')['error']['create']
    headers = {'x-auth-token': autheticate_admin_user['token']}

    for exercise_data in exercises_data:
        payload = {
            "level": exercise_data['data']['level'],
            "description": exercise_data['data']['description'],
            "position": exercise_data['data']['position']
        }
        if not exercise_data['data']['level']:
            payload.pop("level")
        if not exercise_data['data']['description']:
            payload.pop("description")

        r = requests.post(f'{env_config.API_URL}/api/exercise', json=payload, headers=headers)

        assert r.status_code == exercise_data['status_code']
        assert r.json()['errors'][0]['msg'] == exercise_data['msg']
        logger.info(f"Successfully confirmed exercise error with error msg: {exercise_data['msg']}")


def test_get_exercise_by_id_fail(env_config, register_initial_user):
    """tests getting exercises by id for failure conditions"""

    exercises_data = read_json('./test_data/exercise_data.json')['error']['get']
    headers = {'x-auth-token': register_initial_user['token']}

    for exercise_data in exercises_data:
        r = requests.get(f'{env_config.API_URL}/api/exercise/{exercise_data["data"]["_id"]}', headers=headers)

        assert r.status_code == exercise_data['status_code']
        assert r.json()['errors'][0]['msg'] == exercise_data['msg']
        logger.info(f"Successfully confirmed exercise error with error msg: {exercise_data['msg']}")


def test_get_exercise_by_level_fail(env_config, register_initial_user):
    """tests getting exercises by id for failure conditions"""

    exercises_data = read_json('./test_data/exercise_data.json')['error']['get_by_level']
    headers = {'x-auth-token': register_initial_user['token']}

    for exercise_data in exercises_data:
        r = requests.get(f'{env_config.API_URL}/api/exercise/level/{exercise_data["data"]["level"]}', headers=headers)

        assert r.status_code == exercise_data['status_code']
        assert r.json()['errors'][0]['msg'] == exercise_data['msg']
        logger.info(f"Successfully confirmed exercise error with error msg: {exercise_data['msg']}")
