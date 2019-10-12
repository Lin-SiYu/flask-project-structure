from flask import request
from flask_restful import Resource

from lib.celery_tasks.celery_example import nums_add
from lib.utils.response_utils import ok


class ExampleHandler(Resource):
    def get(self):
        return ok(data='hello example')

    def post(self):
        print(request.get_json())
        # print(request.args)
        # a = request.args['a']
        # b = request.args['b']
        # res = nums_add.delay(a, b)
        # print(res.id)
        # print(res.status)
        return ok(data='ok')
