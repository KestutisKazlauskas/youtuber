from flask import Blueprint

tag_blueprint= Blueprint('tag', __name__)

from . import views