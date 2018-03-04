import os


class MainConfig:
    """Main Class for config"""
    DEBUG = False
    SECRET = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevelopmentConfig(MainConfig):
    """Configurations for DEVELOPMENT"""
    DEBUG = True
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')


class TestingConfig(MainConfig):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysqldb://test_db:change_this@localhost/test_db'
    DEBUG = True


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}
