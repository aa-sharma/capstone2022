import pytest
import logging
import os
import sys
from pprint import pformat, pprint
from pymongo import MongoClient
from ..config import DevConfig, ProdConfig

logger = logging.getLogger(__name__)

@pytest.fixture(scope='session', autouse=True)
def drop_database(env_config):
    client = MongoClient(env_config.DB_URL)
    db = client[env_config.DATABASE_NAME]

    db.users.delete_many({ 'admin': False })
    db.exercises.delete_many({})
    db.userlevelprogresses.delete_many({})


@pytest.fixture(scope='session')
def env_config():
    if os.getenv('NODE_ENV') == 'development':
        yield DevConfig
    elif os.getenv('NODE_ENV') == 'production':
        yield ProdConfig
    else:
        logger.error('environment variable "NODE_ENV" must be either: "development" OR "production"')
        sys.exit(4)
    