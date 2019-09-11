# 建议直接使用IP，若使用localhost会降低速度
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'

REDIS_URL = "redis://127.0.0.1:6379/6"

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://test:test123@localhost/mysqlalchey'
SQLALCHEMY_TRACK_MODIFICATIONS = False