import json
from threading import Thread

from kline_filler.logs.logger import log
from lib.mq.flask_pika import Pika


class MqBase:
    def __init__(self, app=None):
        self.fpika = Pika()

        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.pika_params = app.config['FLASK_PIKA_PARAMS']
        self.fpika.init_app(app)
        self._channel = self.fpika.channel()
        self._has_consuming = False

        self._init_exchanges()

    def _init_exchanges(self):
        exchanges = self.app.config['MQ_EXCHANGES']
        try:
            for e_type, e_names in exchanges.items():
                if e_type not in ['fanout', 'topic', 'direct']:
                    raise Exception("GET THE WRONG EXCHANGE TYPE! PLEASE CHECK OUT!")
                for e_name in e_names:
                    self.producer(exchange_name=e_name, exchange_type=e_type, durable=True)
        except Exception as e:
            log.error('%s - Exchange init error : %s' % (self, e))

    def producer(self, exchange_name='', exchange_type='', *args, **kwargs):
        # 生产者初始化exchange
        self._channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type, auto_delete=True,
                                       *args, **kwargs)
        log.info('%s - Create exchange success! name:%s,type:%s' % (self, exchange_name, exchange_type))

    def publish(self, msg, exchange_name='', routing_key='', *args, **kwargs):
        '''
        广播至指定的exchange
        :param msg: 接受dict，处理成json格式
        :return:
        '''
        json_msg = json.dumps(msg)
        self._channel.basic_publish(body=json_msg, exchange=exchange_name, routing_key=routing_key, *args,
                                    **kwargs)
        log.info('%s - Publish messages success! name:%s' % (self, exchange_name))

    def consumer(self, queue_name='', exchange_name='', routing_key='', prefetch_count=1, *args, **kwargs):
        # e消费者初始化queue，绑定指定exchang
        self._channel.queue_declare(queue=queue_name, auto_delete=True)

        self._channel.queue_bind(queue=queue_name, exchange=exchange_name, routing_key=routing_key)
        self._channel.basic_qos(prefetch_count=prefetch_count)
        log.info(
            '%s - Consumer initialize success! exchange_name=%s,queue_name:%s' % (self, exchange_name, queue_name))

    def thread_sub(self, consumer_callback=None, queue_name='', *args, **kwargs):
        Thread(target=self._subscribe, args=(consumer_callback, queue_name, *args), kwargs=kwargs, daemon=True).start()

    def _subscribe(self, consumer_callback=None, queue_name='', no_ack=True, *args, **kwargs):
        # 订阅指定队列
        self._channel = self.fpika.channel()
        self._channel.basic_consume(consumer_callback=consumer_callback, queue=queue_name, no_ack=no_ack)

        if not self._has_consuming:
            self._channel.start_consuming()
            self._has_consuming = True
        log.info('%s - Subscribe success! queue_name:%s' % (self, queue_name))
