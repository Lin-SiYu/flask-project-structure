from kline_filler.logs.logger import log
from lib.mq.mq_consumers import consumer


def register(app):
    '''
    根据业务逻辑，注册需要初始化队列的对象信息
    ！注意！：需保证exchange存在
    '''
    # 提供 Asynchronous callback，自定义queue_name,已存在的exchange_name
    consumer.register(example_callback, 'example', 'Example')
    consumer.register(example_callback, 'example2', 'Example2')


def example_callback(channel, body, envelope, properties, *args, **kwargs):
    print(body)
    log.info('example_callback')
