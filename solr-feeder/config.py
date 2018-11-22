import os
import dotenv


# Load all the environment variables from a .env file located in some directory above.
dotenv.load_dotenv(dotenv.find_dotenv())

CONFIGURATION = {
    'development': 'config.DevConfig',
    'testing': 'config.TestConfig',
    'production': 'config.Config',
    'default': 'config.Config'
}


class Config(object):
    # The Flask secret key used to encrypt cookies. This must be kept secret, and should be unique per environment. Do
    # not allow a missing value.
    SECRET_KEY = os.getenv('SOLR_FEEDER_FLASK_SECRET_KEY')
    if not SECRET_KEY:
        raise RuntimeError('Environment variable SOLR_FEEDER_FLASK_SECRET_KEY in not defined')

    user = os.getenv('NAMES_DATABASE_USERNAME', '')
    password = os.getenv('NAMES_DATABASE_PASSWORD', '')
    name = os.getenv('NAMES_DATABASE_NAME', '')
    host = os.getenv('NAMES_DATABASE_HOST', '')
    port = os.getenv('NAMES_DATABASE_PORT', '5432')
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{name}'.format(
        user=user,
        password=password,
        host=host,
        port=port,
        name=name,
    )
    SQLALCHEMY_TRACK_MODIFICATIONS="False"

    DEBUG = False
    TESTING = False


class DevConfig(Config):
    DEBUG = True
    TESTING = True


class TestConfig(Config):
    DEBUG = True
    TESTING = True
