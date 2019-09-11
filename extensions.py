from celery import Celery
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

redis_store = FlaskRedis()

cel_app = Celery('kline-fill')
