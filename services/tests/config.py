import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    API_URL = os.getenv('API_URL')


class DevConfig(Config):
    ENV = 'development'

    API_URL = 'http://127.0.0.1:5000'

    DB_URL = 'mongodb://127.0.0.1:27017'
    JWT_SECRET = 'this-is-a-secret'


class ProdConfig(Config):
    ENV = 'production'
