import pytest
import logging
import os
import sys
from ..config import DevConfig, ProdConfig

logger = logging.getLogger(__name__)

@pytest.fixture(scope='session')
def config():
    if os.getenv('ENV') == 'dev':
        return DevConfig
    elif os.getenv('ENV') == 'prod':
        return ProdConfig
    else:
        logger.error('environment variable "ENV" must be either: "dev" OR "prod"')
        sys.exit(4)
