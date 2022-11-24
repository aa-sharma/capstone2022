import pytest
import logging
import requests
import os
import sys
import time
from pprint import pformat, pprint
from pymongo import MongoClient
from ..config import DevConfig, ProdConfig
from ..utils.helpers import create_folder_file_now

logger = logging.getLogger(__name__)


@pytest.fixture(scope='session', autouse=True)
def wait_server_ready(env_config):
    while True:
        try:
            r = requests.get(f'{env_config.API_URL}/')
            if r.json()['msg'] == "Welcome to the Apollo API...":
                break
        except Exception as e:
            logger.warning("Server not ready yet, sleeping 2 seconds...")
        time.sleep(2)


@pytest.fixture(scope='session', autouse=True)
def drop_database(env_config):
    client = MongoClient(env_config.DB_URL)
    db = client[env_config.DATABASE_NAME]

    db.users.delete_many({'admin': False})
    db.exercises.delete_many({})
    db.userlevelprogresses.delete_many({})


def pytest_configure(config):
    """***config.option.htmlpath needs to be fixed and relooked at***"""

    if not config.option.htmlpath:
        file = create_folder_file_now(directory='reports', file_name='reports', file_type='html')
        config.option.htmlpath = file


@pytest.fixture(scope='session')
def env_config():
    if os.getenv('NODE_ENV') == 'development':
        yield DevConfig
    elif os.getenv('NODE_ENV') == 'production':
        yield ProdConfig
    else:
        logger.error('environment variable "NODE_ENV" must be either: "development" OR "production"')
        sys.exit(4)
