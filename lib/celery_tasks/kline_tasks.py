from extensions import cel_app
from kline_filler.service.kline_distribute import kline_distribution
from lib.sql_models.table_kline_exception import KlineException


@cel_app.task
def kline_handler(data):
    '''
    调用 kline 填充接口
    :param data: KlineException data
    :return:处理过后存库的数据内容 dict格式
    e.g. {  'id': 1, 'exchange': 'huobi', 'coin_pair': 'ETH/BTC',
            'period': '1min', 'from_time': '1501470900',
            'end_time': '1568688540', 'status': '0'
            }

    '''
    # 获取data内相关参数调用API
    res = kline_distribution(data)
    # kline_distribution 仅对象存在接入交易所范围内，才有返回信息
    if res:
        obj = KlineException.query.filter_by(id=data['id']).first()
        if res['status'] in [2000, 2001]:
            # 请求访问成功，不论数据有无返回，都修改sql内from_time字段
            obj.from_time = res['end_time']
        if obj.end_time - obj.from_time <= 0:
            # end-from<=0 ：表示日期失效，数据处理完成
            obj.status = '1'
        obj.mixin_save()
        return obj.get_dict()
    return data
