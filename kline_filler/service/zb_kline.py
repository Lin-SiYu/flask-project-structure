import pandas

from kline_filler.service.base_kline import BaseKline
from kline_filler.service.kline_get import kline_restful


class ZbKline(BaseKline):
    def __init__(self):
        super().__init__()
        self.period_rule = ['1min', '3min', '5min', '15min', '30min',
                            '1hour', '2hour', '4hour', '6hour', '6hour',
                            '1day', '3day', '1week']
        self.request_address = 'http://api.zb.plus/data/v1/kline'
        self.per_count = 1000
        self.request_type = 'https'

    def get_req_rule(self):
        '''
        note:获取K线数据，最多获取最新的1000条
        :return:
        '''
        coin_pair = self.coin_pair.replace('/', '_').lower()

        request_dic = {
            'market': coin_pair,
            'type': self.period,
            'since': self.from_time * 1000,
            'size': self.per_count,
        }
        return request_dic

    def kline_res_handle(self, kline_acquired):
        if 'data' not in kline_acquired:
            # {"error": "市场错误"}
            # {"code": 3005,"message": "无效的参数"}
            return kline_restful(self.kline_info, 4000, data=kline_acquired)

        kline_data = kline_acquired['data']
        if kline_data[0][0] > (self.kline_info['from_time'] * 1000) \
                and kline_data[-1][0] > (self.kline_info['end_time'] * 1000):
            return kline_restful(self.kline_info, 2001, data=kline_acquired)

        # 存在数据时间重合，即处理数据存库
        parameters_list = ['_id', 'open', 'high', 'low', 'close', 'vol']
        df = pandas.DataFrame(kline_data, columns=parameters_list)

        if self.period == '1min':
            df['ts'] = df['_id'].astype('int64')

        for column in parameters_list[0:6]:
            if column == '_id':
                df[column] = (df[column] / 1000).astype('int32')
                continue
            df[column] = round(df[column].astype('double'), 8)
        kline_list = df.to_dict('records')
        return kline_restful(self.kline_info, 2000, data=kline_list)
