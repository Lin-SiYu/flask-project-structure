from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError, InvalidRequestError

from extensions import db
from lib.sql_models.table_kline_exception import KlineException
from lib.utils.response_utils import ok, error


class StorageRuleHandler(Resource):
    def post(self):
        '''
        e.g.
        [
            {
            "exchange": "binance",
            "coin_pair": "BTC/USDT",
            "period": "1min",
            "from_time": 1569677160,
            "end_time": 1569737210,
            },
            {},{},
        ]
        '''
        data = request.get_json()
        try:
            for exc_info in data:
                if 'status' not in exc_info:
                    exc_info['status'] = 0
                if KlineException.query.filter_by(**exc_info).first():
                    # 存在一模一样的数据，不添加
                    continue
                db.session.add(KlineException(**exc_info))
        except IntegrityError:
            return error(msg='Missing necessary parameters,please check out!')
        except InvalidRequestError:
            return error(msg='Parameters error.')
        else:
            db.session.commit()
            return ok(data='Store successful.')
