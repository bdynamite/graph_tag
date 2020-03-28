from flask import Blueprint

bp = Blueprint('api/v1', __name__)

from . import endpoints
