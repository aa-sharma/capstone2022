import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    JWT_SECRET = os.getenv("JWT_SECRET")


class DevConfig(Config):
    ENV = 'development'

    API_URL = f'http://{os.getenv("SERVER_HOST")}:{os.getenv("SERVER_PORT")}'
    DB_URL = f'mongodb://{os.getenv("MONGO_INITDB_ROOT_USERNAME")}:{os.getenv("MONGO_INITDB_ROOT_PASSWORD")}@' \
        f'{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("MONGO_INITDB_DATABASE")}'


class ProdConfig(Config):
    ENV = 'production'
