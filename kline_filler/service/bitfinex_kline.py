import re
import pandas
from kline_filler.service.base_kline import BaseKline
from kline_filler.service.kline_get import kline_restful, kline_with_api


class BitfinexKline(BaseKline):
    def __init__(self):
        super().__init__()
        self.period_rule = ['1min', '5min', '15min', '30min',
                            '1hour', '3hour', '6hour', '12hour',
                            '1day', '7day', '14day', '1mon']
        self.request_address = 'https://api-pub.bitfinex.com/v2/candles/trade:{period}:{coin_pair}/hist'
        self.per_count = 5000
        self.request_type = 'https'

    def get_req_rule(self):
        '''
        规则注意点
        - 周期单位转换
            m -> minutes; h -> hours; D -> days;  M -> months
        - 时间戳单位 ： ms（13位）
        - 单次请求返回数据：默认120，最大5000
            每次返回数量大概率达不到请求数量，存在时间偏移误差
        - sort：排序，默认 -1，if = 1 it sorts results returned with old > new
        :return:
        '''
        coin_pair = 't%s' % self.coin_pair.replace('/', '')

        period_units = {'min': 'm', 'hour': 'h', 'day': 'D', 'mon': 'M'}
        period_unit = re.findall(r'\D+', self.period)[0]
        period = self.period.replace(period_unit, period_units[period_unit])

        self.request_address = self.request_address.format(period=period, coin_pair=coin_pair)

        request_dic = {
            'limit': self.per_count,
            'start': self.from_time * 1000,
            'end': self.query_end * 1000,
            # 'sort':-1
        }
        return request_dic

    def kline_res_handle(self, kline_acquired):
        if isinstance(kline_acquired, list):
            if not kline_acquired:
                return kline_restful(self.kline_info, 2001, data=kline_acquired)

            if 'error' in kline_acquired:
                # ['error', 10020, 'time_interval: invalid']
                return kline_restful(self.kline_info, 4000, data=kline_acquired[2])

            df = self.df_handle(kline_acquired)
            if len(kline_acquired) < self.per_count:
                # 返回数据存在丢失，使用pandas获取丢失时间戳，并进行补全操作。
                miss_info = self.missing_data_handle(df)
                miss_data = self.get_miss_data(miss_info)
                miss_df = self.df_handle(miss_data)
                df = df.append(miss_df, ignore_index=True)

            kline_list = df.to_dict('records')
            return kline_restful(self.kline_info, 2000, data=kline_list)

    def missing_data_handle(self, df_hist):
        '''
        :param df: 入库标准的 DataFrame class
        :return: [
             {
            'limit': 1,
            'start': time - self.period(s),
            'end': time ,
            },
            {},{},
        ]
        '''
        df = df_hist.copy()

        df.index = pandas.to_datetime(df['_id'], unit='s')
        df = df.resample('%sS' % self.granularity).asfreq()

        null_ts = df[pandas.isna(df['_id'])].index.to_pydatetime()
        ts_list = [int(pandas.Timestamp.timestamp(pandas.Timestamp(i))) for i in null_ts]

        miss_info = [dict(limit=1, start=(ts - self.granularity) * 1000, end=ts * 1000) for ts in ts_list]
        return miss_info

    def get_miss_data(self, miss_info):
        '''
        :param miss_info: [{},{}]
        :return:[[],[]]
        '''
        miss_data = [kline_with_api(self.request_address, info)[0] for info in miss_info]
        return miss_data

    def df_handle(self, kline_acquired):
        parameters_list = ['_id', 'open', 'close', 'high', 'low', 'vol']
        df = pandas.DataFrame(kline_acquired, columns=parameters_list)
        df['_id'] = (df['_id'] / 1000).astype('int32')
        for column in parameters_list:
            if column == '_id':
                continue
            df[column] = round(df[column].astype('double'), 8)
        return df
