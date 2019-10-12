import time
import pandas
from kline_filler.service.kline_get import kline_restful
from lib.tools import timestamp2iso
from kline_filler.service.base_kline import BaseKline


class OkexKline(BaseKline):
    def __init__(self):
        super().__init__()
        self.period_rule = ['1min', '3min', '5min', '15min', '30min',
                            '1hour', '2hour', '4hour', '6hour', '12hour', '1day', '1week']
        self.request_address = 'https://www.okex.com/api/spot/v3/instruments/{query_pair}/candles'
        self.per_count = 200
        self.request_type = 'https'

    def get_req_rule(self):
        '''
        :return:{'start': '2019-09-24T04:40:00.000000Z', 'end': '2019-09-24T08:00:00.000000Z', 'granularity': 60}
        '''
        coin_pair = self.coin_pair.replace('/', '-')
        self.request_address = self.request_address.format(query_pair=coin_pair)

        query_from = timestamp2iso(self.from_time, tt='iso_8601')
        query_end = timestamp2iso(self.query_end, tt='iso_8601')
        request_dic = {
            'start': query_from,
            'end': query_end,
            'granularity': self.granularity
        }
        return request_dic

    def kline_res_handle(self, kline_acquired):
        if isinstance(kline_acquired, list):
            if kline_acquired:
                # okex 返回值的存储规则处理
                parameters_list = ['_id', 'open', 'high', 'low', 'close', 'vol']
                df = pandas.DataFrame(kline_acquired, columns=parameters_list)
                for column in parameters_list:
                    if column == '_id':
                        df['_id'] = df['_id'].apply(lambda x: time.mktime(time.strptime(x, "%Y-%m-%dT%H:%M:%S.000Z")))
                        df['_id'] = df['_id'].astype('int32')
                        continue
                    data = df[column].astype('double')
                    df[column] = round(data, 8)
                final_kline = df.to_dict('records')
                return kline_restful(self.kline_info, 2000, data=final_kline)
            return kline_restful(self.kline_info, 2001, data=kline_acquired)
        if isinstance(kline_acquired, dict):
            # {'code': 30032, 'message': 'The currency pair does not exist'}
            return kline_restful(self.kline_info, 4000, data=kline_acquired)
