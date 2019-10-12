from flask_restful import Resource

from extensions import mq
from lib.utils.response_utils import ok


class MqHandle(Resource):
    def get(self):
        mq.publish('{"hello":"world"}', exchange_name='Example')
        return ok(data='Successful.')
