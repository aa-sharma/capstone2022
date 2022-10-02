import requests
from urllib.parse import urlencode
import logging


logger = logging.getLogger(__name__)


class ApiRequest:
    """
    API class for fetching data from Apollo HTTP API
    """

