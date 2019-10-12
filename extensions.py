from celery import Celery
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from lib.mq.mq_base import MqBase

db = SQLAlchemy()

redis_store = FlaskRedis()

cel_app = Celery('kline-fill')

mongo = PyMongo()

mq = MqBase()