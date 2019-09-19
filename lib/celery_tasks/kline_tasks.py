from extensions import cel_app
from kline_fill.service.kline_distribute import kline_distribution


@cel_app.task
def kline_handler(obj):
    '''
    调用 kline 填充接口
    :param obj: KlineException sql alchemy object
    :return:处理过后存库的数据内容 dict格式
    e.g. {  'id': 1, 'exchange': 'huobi', 'coin_pair': 'ETH/BTC',
            'period': '1min', 'from_time': '1501470900',
            'end_time': '1568688540', 'status': '0'
            }

    '''
    # 获取data内相关参数调用API
    data = obj.get_dict()
    res = kline_distribution(data)
    # kline_distribution 仅对象存在接入交易所范围内，才有返回信息
    if res:
        if res['status'] in [2000, 2001]:
            # 请求访问成功，不论数据有无返回，都修改sql内from_time字段
            obj.from_time = res['end_time']
        if int(data['end_time']) - res['end_time'] <= 0:
            # 若数据库内 end - from 小于等于0 则表示日期失效，数据处理完成
            obj.status = '1'
        obj.mixin_save()
    return obj.get_dict()
