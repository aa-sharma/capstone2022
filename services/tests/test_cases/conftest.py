import pytest
import logging
import os
import sys

from ..config import DevConfig, ProdConfig

logger = logging.getLogger(__name__)

@pytest.fixture(scope='session')
def env_config():
    if os.getenv('NODE_ENV') == 'development':
        yield DevConfig
    elif os.getenv('NODE_ENV') == 'production':
        yield ProdConfig
    else:
        logger.error('environment variable "NODE_ENV" must be either: "development" OR "production"')
        sys.exit(4)
    