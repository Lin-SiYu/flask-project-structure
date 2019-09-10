import pathlib
from flask import Flask

from kline_fill import routers

_default_instance_path = pathlib.Path(__file__).parents[0].joinpath('kline_fill', 'instance')


def create_app():
    app = Flask(__name__, instance_relative_config=True, instance_path=_default_instance_path)
    configure_app(app)
    configure_blueprint(app)
    configure_extensions(app)
    return app


def configure_app(app):
    app.config.from_pyfile('dev.py')


def configure_blueprint(app):
    routers.register_blueprint(app)


def configure_extensions(app):
    pass
