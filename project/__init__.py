from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache


db = SQLAlchemy()
cache = Cache()


def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    initialize_extensions(app)
    register_blueprints(app)
    return app


def initialize_extensions(app):
    db.init_app(app)
    cache.init_app(app)

    from project.api.v1 import errors

    @app.errorhandler(errors.ApiError)
    def handle_api_error(error):
        return error.get_response()


def register_blueprints(app):
    from project.api.v1 import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
