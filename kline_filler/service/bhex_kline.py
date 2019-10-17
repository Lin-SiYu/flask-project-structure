import pandas

from kline_filler.service.base_kline import BaseKline
from kline_filler.service.kline_get import kline_restful
from lib.tools import period_unit_transform


class BhexKline(BaseKline):
    def __init__(self):
        super().__init__()
        self.request_type = 'https'
        self.request_address = 'https://api.bhex.com/openapi/quote/v1/klines'
        self.per_count = 1000
        self.period_rule = ['1min', '3min', '5min', '15min', '30min',
                            '1hour', '2hour', '4hour', '6hour', '8hour', '12hour',
                            '1day', '3day', '1week', '1mon']

    def get_req_rule(self):
        '''
        interval
            m -> minutes; h -> hours; d -> days; w -> weeks; M -> months
        limit
            默认500; 最大1000.
        :return:
        '''
        coin_pair = self.coin_pair.replace('/', '')
        period = period_unit_transform(self.period)

        request_dic = {
            'symbol': coin_pair,
            'interval': period,
            'startTime': self.from_time * 1000,
            'endTime': self.query_end * 1000,
            'limit	': self.per_count,
        }
        return request_dic

    def kline_res_handle(self, kline_acquired):
        if isinstance(kline_acquired, list):
            if not kline_acquired:
                return kline_restful(self.kline_info, 2001, data=kline_acquired)

            parameters_list = ['_id', 'open', 'high', 'low', 'close', 'vol', 'close_time',
                               'quote_asset_volume', 'trades_num', 'taker_buy_base', 'taker_buy_quote']
            df = pandas.DataFrame(kline_acquired, columns=parameters_list).iloc[:, 0:6]

            if self.period == '1min':
                df['ts'] = df['_id']
                df['ts'] = df['ts'].astype('int64')

            for column in parameters_list[0:6]:
                if column == '_id':
                    df[column] = (df[column] / 1000).astype('int32')
                    continue
                data = df[column].astype('double')
                df[column] = round(data, 8)
            kline_list = df.to_dict('records')
            return kline_restful(self.kline_info, 2000, data=kline_list)

        if isinstance(kline_acquired, dict):
            # {"code": -10009,"msg": "Invalid period!"}
            return kline_restful(self.kline_info, 4000, data=kline_acquired)
