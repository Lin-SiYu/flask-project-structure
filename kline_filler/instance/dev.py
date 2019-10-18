REDIS_URL = "redis://127.0.0.1:6379/0"

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://test:test123@localhost/mytest'
SQLALCHEMY_TRACK_MODIFICATIONS = False

MONGO_URI = 'mongodb://127.0.0.1:27017/test'

FLASK_PIKA_PARAMS = {
    'host': 'localhost',  # amqp.server.com
    'username': 'test',  # convenience param for username
    'password': '123',  # convenience param for password
    'port': 5672,  # amqp server port
    # 'virtual_host': 'kline'  # amqp vhost
}

# optional pooling params
# FLASK_PIKA_POOL_PARAMS = {
#     'pool_size': 8,
#     'pool_recycle': 600
# }

MQ_EXCHANGES = {
    'fanout': ['KlineException'],
    'topic': [],
    'direct': []
}
