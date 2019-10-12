import pandas
from pymongo.errors import OperationFailure

from extensions import mongo, db
from kline_filler.logs.logger import log
from kline_filler.service.kline_get import kline_with_ws, kline_with_api
from lib.sql_models.table_kline_exception import KlineException
from lib.tools import kline_granularity


class BaseKline:
    def __init__(self):
        # 规则单位非交易所规则单位，请务必使用 min/hour/day/week/mon
        self.period_rule = []
        self.request_address = ''
        # 单次请求返回数据
        self.per_count = 0
        # https or websocket
        self.request_type = 'https'

    def __call__(self, req_data, *args, **kwargs):
        self.kline_info = req_data.copy()
        self.exchange = req_data['exchange']
        self.coin_pair = req_data['coin_pair']
        self.period = req_data['period']
        self.from_time = req_data['from_time']
        self.end_time = req_data['end_time']
        if self.period not in self.period_rule:
            raise Exception(
                'The period data is against the request rule from {exchange}!'.format(exchange=self.exchange))
        self.query_end, self.granularity = self.end_time_handle()

    def get_kline(self):
        request_dic = self.get_req_rule()
        if self.request_type == 'websocket':
            kline_acquired = kline_with_ws(self.request_address, request_dic)
        elif self.request_type == 'https':
            kline_acquired = kline_with_api(self.request_address, request_dic)
        else:
            raise Exception('Wrong request type!')
        res = self.kline_res_handle(kline_acquired)
        return res

    def get_req_rule(self):
        # 根据交易所业务获取请求参数
        raise NotImplemented

    def kline_res_handle(self, kline_acquired):
        '''
        根据交易所返回内容，自定义处理规则，处理错误请求等。
        返回 kline_restful 格式数据
        :return: kline_restful
            kline_info 后处理数据，非原库数据，end-time 经过处理
            data 必须手动处理成下列相同 key-value 格式进行存储
        e.g.
            {
                'kline_info':{'id': 1, 'exchange': 'huobi', 'coin_pair': 'BTC/USDT', 'period': '1min',
                                'from_time': 1569357600, 'end_time': 1569369600, 'status': 2000},
                'msg':'ok',
                'data':[{
                        '_id': 1569677160, 'open': 0.00808471, 'high': 0.00808471,
                        'low': 0.0080742, 'close': 0.00808087, 'vol': 9884.7},
                        {},{},……,
                       ]
            }

        '''
        raise NotImplemented

    def end_time_handle(self):
        '''
        根据 self.per_count 和 self.period 计算单次请求的 end-time
            self.per_count:该交易所，单次请求最大返回数量
            self.period:该次请求的kline周期
        :return: (int,int)
            query-end:该次请求的 end-time
            granularity:周期数转换以秒为单位的粒子
        '''
        # 假设 per-count = 300
        # 数据库确保from和end时间数据存在，处理from开始的300条数据
        query_end = self.end_time
        granularity = kline_granularity(self.period)
        # 计算300条对应等时间戳粒子数
        granularity_count = granularity * self.per_count
        if query_end - self.from_time > granularity:
            query_end = self.from_time + granularity_count
            self.kline_info['end_time'] = query_end
        return query_end, granularity

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
        kline_data = kline_res['data']
        kline_info = kline_res['kline_info']

        if kline_info['status'] == 2000:
            # mongo 存储规则匹配，规则统一后再进行存储
            self._mongo_storage(kline_info, kline_data)

        # 查询异常，则将该条数据入库，等待下次执行推送处理
        # 不对参数不正确的查询错误（4000）进行入库，防止错误增生。
        if kline_info['status'] in [5000]:
            insert_dic = kline_info.copy()

            # 移动原数据时间的from-time，防止下一次数据重复请求。
            o_id = insert_dic.pop('id')
            obj_old = KlineException.query.filter_by(id=o_id).first()
            obj_old.from_time = insert_dic['end_time']
            db.session.add(obj_old)

            insert_dic['status'] = 0
            obj = KlineException.query.filter_by(**insert_dic).first()
            if not obj:
                db.session.add(KlineException(**insert_dic))
            db.session.commit()

        res = dict(
            end_time=kline_info['end_time'],
            status=kline_info['status'],
        )
        return res

    def _mongo_storage(self, kline_info, kline_data):
        '''
        处理mongodb存储规则,不匹配则抛错
            - _id ：int32 为10位时间戳，若存在则不进行修改
            - open/high/low/close/vol :Double
        :return:
        '''
        exchange = kline_info['exchange']
        coll_name = 'k_%s_%s' % (kline_info['coin_pair'].replace('/', ''), kline_info['period'])
        doc = mongo.cx[exchange][coll_name]
        try:
            # 相同数据的异常处理
            df = pandas.DataFrame.from_dict(kline_data)
            id_list = df._id.to_list()
            mongo_objs = doc.find({"_id": {"$in": id_list}})
            obj_ids = [obj['_id'] for obj in mongo_objs]
            df = df[~ df._id.isin(obj_ids)]
            insert_data = df.to_dict('records')
            if insert_data:
                doc.insert_many(insert_data)
        except OperationFailure as e:
            log.error('ERROR:%s - Kline data does not comply with storage rules！'
                      'Duplicate data queries may fail because the data is not refreshed.' % e)
