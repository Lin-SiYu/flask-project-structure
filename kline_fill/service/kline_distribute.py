import importlib

from kline_fill.instance.kline_conf import KLINE_EXCHANGE_DISPATCH as kline_dispatch


def kline_distribution(data_dic):
    '''
    对接交易所，获取相关KLINE数据，并存库操作
    :param data_dic: 交易所所需请求参数
    :return: 返回表明是否获取并入库成功
    {
    'id': 1, 'exchange': 'huobi', 'coin_pair': 'ETH/BTC', 'period': '1min',
    'from_time': '1501236900', 'end_time': 1501254900, 'status': 2000
    }
    '''
    exchange = data_dic['exchange']
    if exchange in kline_dispatch:
        mpath, mclass = kline_dispatch[exchange].rsplit('.', maxsplit=1)
        mod = importlib.import_module(mpath)
        cla_obj = getattr(mod, mclass)
        # kline 数据 mongodb 存储
        return cla_obj(data_dic).data_storage()
