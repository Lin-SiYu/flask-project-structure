import pathlib
from flask import Flask

from extensions import db, redis_store, cel_app, mongo
from kline_fill import routers
from lib.celery_tasks import celery_config
from lib.sql_models.base_model import BaseModel

_default_instance_path = pathlib.Path(__file__).parents[0].joinpath('kline_fill', 'instance')


def create_app():
    app = Flask(__name__, instance_relative_config=True, instance_path=_default_instance_path)
    configure_app(app)
    configure_blueprint(app)
    configure_extensions(app)
    configure_celery(app, cel_app)
    return app


def configure_app(app):
    app.config.from_pyfile('dev.py')


def configure_blueprint(app):
    routers.register_blueprint(app)


def configure_extensions(app):
    # db
    db.init_app(app)
    db.BaseModel = BaseModel

    # redis
    redis_store.init_app(app)

    # mongo
    mongo.init_app(app)


def configure_celery(app, celery):
    celery.config_from_object(celery_config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
