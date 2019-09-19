import time

from kline_fill.service.base_kline import BaseKline
from kline_fill.service.kline_get import kline_with_ws, kline_restful
from lib.tools import kline_granularity


class HuobiKline(BaseKline):
    def __init__(self, req_data: dict):
        self.req_data = self.kline_info = req_data.copy()
        self.exchange = 'huobi'
        self.request_type = 'webscoket'
        self.request_address = 'wss://api.huobi.pro/ws'
        self.period_rule = ['1min', '5min', '15min', '30min', '60min', '1day', '1mon', '1week', '1year']
        # 2017-07-28 18:15:00  to  2051-01-01 00:00:00
        self.query_range = [1501236900, 2524579200]

    def get_req_rule(self):
        '''
        注意，from和to参数规则
        - 只有from 则从当前时间往前推 返回300条
        - 只有to 则从to时间往前推 返回300条
        - 有 from + to 时，若 from 和 to 时间间隔相差超过 period/s*300 则报错
        - 二者都空，则查询当前时间往前推，返回300条
        :return: {"req": "market.{coin_pair}.kline.{period}", "id": "id1", "from": 1501236900, "to": 1501254960}
        '''
        coin_pair = self.req_data['coin_pair'].replace('/', '').lower()
        period = self.req_data['period']
        if period not in self.period_rule:
            raise Exception('The period data is against the request rule from HuoBi!')
        req = "market.{coin_pair}.kline.{period}".format(coin_pair=coin_pair, period=period)
        id_num = int(time.time())

        # 数据库确保from和end时间数据存在，处理from开始的300条数据
        query_from = int(self.req_data['from_time'])
        query_end = int(self.req_data['end_time'])
        granularity = kline_granularity(period) * 300
        if query_end - query_from > granularity:
            query_end = int(query_from) + granularity
            self.kline_info['end_time'] = query_end

        request_dic = {
            'req': req,
            'id': str(id_num),
            'from': query_from,
            'to': query_end
        }
        return request_dic

    def get_kline(self):
        kline_dic = kline_with_ws(self.request_address, self.get_req_rule())
        if kline_dic['status'] == 'ok':
            kline_res = kline_dic['data']
            if not kline_res:
                return kline_restful(self.kline_info, 2001, data=kline_res)
            return kline_restful(self.kline_info, 2000, data=kline_res)
        elif kline_dic['status'] == 'error':
            return kline_restful(self.kline_info, 4000, data=kline_dic['err-msg'])
