import pathlib
from flask import Flask

from extensions import db, redis_store, cel_app, mongo, mq
from kline_fill import routers
from kline_fill.logs.logger import log_init
from lib.celery_tasks import celery_config
from lib.mq.mq_consumers import consumer
from lib.mq.mq_register import register
from lib.sql_models.base_model import BaseModel

_default_instance_path = pathlib.Path(__file__).parents[0].joinpath('kline_filler', 'instance')


def create_app():
    app = Flask(__name__, instance_relative_config=True, instance_path=_default_instance_path)
    configure_app(app)
    configure_blueprint(app)
    configure_extensions(app)
    configure_celery(app, cel_app)
    configure_rabbitmq(app)
    return app


def configure_app(app):
    app.config.from_pyfile('dev.py')
    log_init()


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


def configure_rabbitmq(app):
    mq.init_app(app)
    # 初始化队列，并绑定消费函数
    register(app)
    for consumer_info in consumer.subscribers:
        mq.consumer(**consumer_info)
        mq.thread_sub(**consumer_info)