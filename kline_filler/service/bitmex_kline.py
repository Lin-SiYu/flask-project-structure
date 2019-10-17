import time

import pandas

from kline_filler.service.base_kline import BaseKline
from kline_filler.service.kline_get import kline_restful
from lib.tools import timestamp2iso, period_unit_transform


class BitmexKline(BaseKline):
    def __init__(self):
        super().__init__()
        self.period_rule = ['1min', '5min', '1hour', '1day']
        self.request_address = 'https://www.bitmex.com/api/v1/trade/bucketed'
        self.per_count = 100
        self.request_type = 'https'

    def get_req_rule(self):
        '''
        bitmex 目前仅支持 ETH/XBT
        :return:
        '''
        coin_pair = self.coin_pair.replace('/', '')
        period = period_unit_transform(self.period)

        query_from = timestamp2iso(self.from_time, tt='iso_8601')
        query_end = timestamp2iso(self.query_end, tt='iso_8601')
        request_dic = {
            'startTime': query_from,
            'endTime': query_end,
            'binSize': period,
            'symbol': coin_pair,
        }
        return request_dic

    def kline_res_handle(self, kline_acquired):
        if isinstance(kline_acquired, list):
            if not kline_acquired:
                return kline_restful(self.kline_info, 2001, data=kline_acquired)
            df = pandas.DataFrame(kline_acquired)
            drop_column = ['foreignNotional', 'homeNotional', 'lastSize', 'symbol', 'trades', 'turnover', 'vwap']
            df = df.drop(columns=drop_column)
            df = df.rename(columns={'volume': 'vol', 'timestamp': '_id'})
            df['_id'] = df['_id'].apply(lambda x: time.mktime(time.strptime(x, "%Y-%m-%dT%H:%M:%S.000Z")))
            if self.period == '1min':
                df['ts'] = df['_id'] * 1000
                df['ts'] = df['ts'].astype('int64')
            df['_id'] = df['_id'].astype('int32')
            kline_list = df.to_dict('records')
            return kline_restful(self.kline_info, 2000, data=kline_list)
        if isinstance(kline_acquired, dict):
            # {'error': {'message': 'binSize is invalid.', 'name': 'HTTPError'}}
            return kline_restful(self.kline_info, 4000, data=kline_acquired)
