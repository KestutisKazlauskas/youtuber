import os


class MainConfig:
    """Main Class for config"""
    DEBUG = False
    SECRET = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@database/%s?use_unicode=1&charset=utf8" % (
        os.getenv('MYSQL_USER'), os.getenv('MYSQL_PASSWORD'), os.getenv('MYSQL_DATABASE')
    )


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
