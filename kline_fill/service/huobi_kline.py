import time

import pandas

from kline_fill.service.base_kline import BaseKline
from kline_fill.service.kline_get import kline_restful


class HuobiKline(BaseKline):
    def __init__(self):
        super().__init__()
        self.request_address = 'wss://api.huobi.pro/ws'
        self.period_rule = ['1min', '5min', '15min', '30min', '60min', '1day', '1mon', '1week', '1year']
        # 2017-07-28 18:15:00  to  2051-01-01 00:00:00
        # self.query_range = [1501236900, 2524579200]
        self.per_count = 300
        self.request_type = 'websocket'

    def get_req_rule(self):
        '''
        注意，from和to参数规则
        - 只有from 则从当前时间往前推 返回300条
        - 只有to 则从to时间往前推 返回300条
        - 有 from + to 时，若 from 和 to 时间间隔相差超过 period/s*300 则报错
        - 二者都空，则查询当前时间往前推，返回300条
        :return: {"req": "market.{coin_pair}.kline.{period}", "id": "id1", "from": 1501236900, "to": 1501254960}
        '''
        coin_pair = self.coin_pair.replace('/', '').lower()
        req = "market.{coin_pair}.kline.{period}".format(coin_pair=coin_pair, period=self.period)
        id_num = int(time.time())
        request_dic = {
            'req': req,
            'id': str(id_num),
            'from': self.from_time,
            'to': self.query_end
        }
        return request_dic

    def kline_res_handle(self, kline_dic):
        try:
            if kline_dic['status'] == 'ok':
                kline_res = kline_dic['data']
                if not kline_res:
                    return kline_restful(self.kline_info, 2001, data=kline_res)
                # huobi 返回值的存储规则处理
                df = pandas.DataFrame.from_dict(kline_res)
                df = df.rename(columns={'id': '_id'})
                # amount 和 vol 对换
                df['vol'], df['amount'] = round(df['amount'], 8), round(df['vol'], 8)
                final_kline = df.to_dict('records')
                return kline_restful(self.kline_info, 2000, data=final_kline)
            elif kline_dic['status'] == 'error':
                return kline_restful(self.kline_info, 4000, data=kline_dic['err-msg'])
        except KeyError as e:
            return kline_restful(self.kline_info, 5000, data=e)
