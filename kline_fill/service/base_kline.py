from extensions import mongo


class BaseKline:
    def get_kline(self):
        raise NotImplemented

    def get_req_rule(self):
        raise NotImplemented

    @property
    def kline_res(self):
        return self.get_kline()

    @property
    def req_dic(self):
        return self.get_req_rule()

    def data_storage(self):
        '''
        mongodb 存储规则
            e.g.
            collection name ：huobi
            doc name : k_ETHBTC_1min
        :return:
            {
             'end_time': 1501254900, 'status': 2000
            }

        '''
        kline_res = self.kline_res
        kline_info = kline_res['kline_info']
        coll_name = 'k_%s_%s' % (kline_info['coin_pair'].replace('/', ''), kline_info['period'])
        if kline_info['status'] == 2000:
            mongo.cx[kline_info['exchange']][coll_name].insert_many(kline_res['data'])

        res = dict(
            end_time=kline_res['kline_info']['end_time'],
            status=kline_res['kline_info']['status'],
        )
        return res
