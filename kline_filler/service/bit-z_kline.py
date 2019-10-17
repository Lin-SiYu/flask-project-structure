import pandas

from kline_filler.service.base_kline import BaseKline
from kline_filler.service.kline_get import kline_restful


class BitzKline(BaseKline):
    def __init__(self):
        super(BitzKline, self).__init__()
        self.period_rule = ['1min', '5min', '15min', '30min', '60min',
                            '4hour', '1day', '1week', '1mon']
        self.request_address = 'https://apiv2.bitz.com/Market/kline'
        self.per_count = 300
        self.request_type = 'https'

    def get_req_rule(self):
        coin_pair = self.coin_pair.replace('/', '_').lower()

        request_dic = {
            'size': self.per_count,
            'to': self.query_end * 1000,
            'symbol': coin_pair,
            'resolution': self.period
        }
        return request_dic

    def kline_res_handle(self, kline_acquired):
        if kline_acquired['status'] == 200:
            kline_data = kline_acquired['data']
            if not kline_data:
                # {"status":200,"msg":"","data":{},"time":1571123247,"microtime":"0.46184200 1571123247","source":"api"}
                return kline_restful(self.kline_info, 2001, data=kline_acquired)
            kline_bars = kline_data['bars']
            df = pandas.DataFrame(kline_bars)
            df = df.rename(columns={'volume': 'vol', 'time': '_id'})
            df = df.drop(columns=['datetime'])

            if self.period == '1min':
                df['ts'] = df['_id']
                df['ts'] = df['ts'].astype('int64')

            columns = [column for column in df]
            for column in columns:
                if column not in ['_id', 'ts']:
                    df[column] = round(df[column].astype('double'), 8)

            df['_id'] = (df['_id'].astype('double') / 1000).astype('int32')
            kline_list = df.to_dict('records')
            return kline_restful(self.kline_info, 2000, data=kline_list)

        else:
            # {"status":-102,"msg":"","data":"","time":1571123137,"microtime":"0.69178400 1571123137","source":"api"}
            return kline_restful(self.kline_info, 4000, data=kline_acquired)
