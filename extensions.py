from celery import Celery
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy

from lib.celery_tasks import celery_config

db = SQLAlchemy()

redis = FlaskRedis()


cel_app = Celery('kline-fill')
cel_app.config_from_object(celery_config)
