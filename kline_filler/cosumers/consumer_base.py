from kline_filler.logs.logger import log


class ConsumerBase:
    def __init__(self, app):
        self.app = app

    def consumer_callback(self, channel, deliver, properties, body, *args, **kwargs):
        # 用于 channel 调用的 callback func
        try:
            self.app.app_context().push()
            self.consumer_handle(body)
        except Exception as e:
            log.error(e)
            channel.basic_nack(deliver.delivery_tag, requeue=False)
        else:
            channel.basic_ack(deliver.delivery_tag)

    def consumer_handle(self, body):
        # 用于写入业务代码，子类覆盖
        raise NotImplemented
