from flask_restful import Resource

from lib.utils.response_utils import ok


class ExampleHandler(Resource):
    def get(self):
        return ok(data='hello example')
