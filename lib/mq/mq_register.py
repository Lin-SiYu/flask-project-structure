from kline_filler.cosumers.exception_storage_consumer import ExceptionStorage
from lib.mq.mq_consumers import consumer


def register(app):
    '''
    根据业务逻辑，注册需要初始化队列的对象信息
    ！注意！：需保证exchange存在
    '''
    # 提供 Asynchronous callback，自定义queue_name,已存在的exchange_name
    consumer.register(ExceptionStorage(app).consumer_callback, 'kline_exception', 'KlineException', no_ack=False)
