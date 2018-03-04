import os
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

from app.configs import app_config

db = SQLAlchemy()


def create_app(config_name):
    """Function for creating flask app with needed configs"""

    app = FlaskAPI(
        __name__,
        instance_relative_config=True,
        instance_path=os.path.dirname(__file__)
    )
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('configs.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # register blueprints of the app
    # TODO make url config
    from app.video import video_blueprint
    from app.tags import tag_blueprint
    app.register_blueprint(video_blueprint)
    app.register_blueprint(tag_blueprint)

    return app
