import re
import time

import pandas

from kline_filler.service.base_kline import BaseKline
from kline_filler.service.kline_get import kline_restful


class HitbtcKline(BaseKline):
    def __init__(self):
        super().__init__()
        self.period_rule = ['1min', '5min', '15min', '30min', '60min',
                            '4hour', '1day', '1week', '1mon']
        self.request_address = 'https://api.hitbtc.com/api/2/public/candles/{symbol}'
        self.per_count = 1000
        self.request_type = 'https'

    def get_req_rule(self):
        '''
        period
            Accepted values: M1 (one minute), M3, M5, M15, M30, H1 (one hour), H4, D1 (one day), D7, 1M (one month)
            Default value: M30 (30 minutes)
        sort
            Accepted values: ASC, DESC
            Default value: ASC
        from
            If sorting by timestamp is used, then Datetime, otherwise Number of index value.
        till
            If sorting by timestamp is used, then Datetime, otherwise Number of index value.
        limit
            Default value: 100
            Max value: 1000
        offset
            Default value: 0
            Max value: 100000

        note:该交易所存在数据缺失，但无填补方式，暂略填补。
        :return:
        '''
        coin_pair = self.coin_pair.replace('/', '')
        self.request_address = self.request_address.format(symbol=coin_pair)

        period_units = {'min': 'M{num}', 'hour': 'H{num}', 'day': 'D{num}', 'mon': '{num}M'}
        period_unit = re.findall(r'\D+', self.period)[0]
        period_num = int(re.findall(r'\d+', self.period)[0])
        period = period_units[period_unit].format(num=period_num)

        request_dic = {
            'limit': self.per_count,
            'period': period,
            'from': self.from_time,
            'till': self.query_end,
        }
        return request_dic

    def kline_res_handle(self, kline_acquired):
        if isinstance(kline_acquired, list):
            if not kline_acquired:
                return kline_restful(self.kline_info, 2001, data=kline_acquired)

            df = pandas.DataFrame(kline_acquired)
            df = df.drop(columns=['volumeQuote'])
            rename_map = {
                'volume': 'vol',
                'timestamp': '_id',
                'min': 'low',
                'max': 'high'
            }
            df = df.rename(columns=rename_map)
            df['_id'] = df['_id'].apply(lambda x: time.mktime(time.strptime(x, "%Y-%m-%dT%H:%M:%S.000Z")))

            if self.period == '1min':
                df['ts'] = df['_id'] * 1000
                df['ts'] = df['ts'].astype('int64')

            columns = [column for column in df]
            for column in columns:
                if column not in ['_id', 'ts']:
                    df[column] = round(df[column].astype('double'), 8)
            df['_id'] = df['_id'].astype('int32')

            kline_list = df.to_dict('records')
            return kline_restful(self.kline_info, 2000, data=kline_list)

        if isinstance(kline_acquired, dict):
            '''
            {
                "error": {
                    "code": 10001,
                    "message": "Validation error",
                    "description": "Parameter period with value 1mon unsupported"
                }
            }
            '''
            return kline_restful(self.kline_info, 4000, data=kline_acquired)