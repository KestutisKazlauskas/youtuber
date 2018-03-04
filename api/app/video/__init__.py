from flask import Blueprint

video_blueprint = Blueprint('video', __name__)

from . import views