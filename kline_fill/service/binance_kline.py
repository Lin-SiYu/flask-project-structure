import re
import pandas
from kline_fill.service.base_kline import BaseKline
from kline_fill.service.kline_get import kline_restful


class BinanceKline(BaseKline):
    def __init__(self):
        super().__init__()
        self.request_type = 'https'
        self.request_address = 'https://api.binance.com/api/v1/klines'
        self.per_count = 500
        self.period_rule = ['1min', '3min', '5min', '15min', '30min',
                            '1hour', '2hour', '4hour', '6hour', '8hour', '12hour',
                            '1day', '3day', '1week', '1mon']

    def get_req_rule(self):
        '''
        规则注意点
        - 周期单位转换
            m -> minutes; h -> hours; d -> days; w -> weeks; M -> months
        - 请求时间戳，必须为13位
            e.g. 1569677160000
        - 单次请求返回数据：默认 500，最大 1000
            注意：若给请求数值，返回error，所以当前程序默认使用默认500条
            {'code': -1104, 'msg': "Not all sent parameters were read; read '4' parameter(s) but was sent '5'."}
        :return:
        '''
        coin_pair = self.coin_pair.replace('/', '')

        period_units = {'min': 'm', 'hour': 'h', 'day': 'd', 'week': 'w', 'mon': 'M'}
        period_unit = re.findall(r'\D+', self.period)[0]
        period = self.period.replace(period_unit, period_units[period_unit])

        request_dic = {
            'symbol': coin_pair,
            'interval': period,
            'startTime': self.from_time * 1000,
            'endTime': self.query_end * 1000,
            # 'limit	': self.per_count,
        }
        return request_dic

    def kline_res_handle(self, kline_acquired):
        if isinstance(kline_acquired, list):
            if kline_acquired:
                parameters_list = ['_id', 'open', 'high', 'low', 'close', 'vol', 'close_time',
                                   'quote_asset_volume', 'trades_num', 'taker_buy_base', 'taker_buy_quote', 'ignore']
                df = pandas.DataFrame(kline_acquired, columns=parameters_list).iloc[:, 0:6]
                for column in parameters_list[0:6]:
                    if column == '_id':
                        df[column] = (df[column] / 1000).astype('int32')
                        continue
                    data = df[column].astype('double')
                    df[column] = round(data, 8)
                kline_list = df.to_dict('records')
                return kline_restful(self.kline_info, 2000, data=kline_list)
            return kline_restful(self.kline_info, 2001, data=kline_acquired)
        if isinstance(kline_acquired, dict):
            # {'code': -1104, 'msg': "Not all sent parameters were read; read '4' parameter(s) but was sent '5'."}
            return kline_restful(self.kline_info, 4000, data=kline_acquired)
