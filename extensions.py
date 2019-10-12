from celery import Celery
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy

# 防止不同环境下的包不同
from lib.mq.mq_base import MqBase

try:
    from flask_redis import FlaskRedis
except ImportError:
    from flask_redis import Redis as FlaskRedis

db = SQLAlchemy()

redis_store = FlaskRedis()

cel_app = Celery('kline-fill')

mongo = PyMongo()

mq = MqBase()