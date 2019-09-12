from extensions import cel_app, db
from kline_fill.service.kline_get import get_kline
from lib.sql_models.table_kline_exception import KlineException


@cel_app.task
def kline_handler(data):
    '''
    调用 kline 填充接口
    :param data: 数据库数据，dict
    :return:
    '''
    # 获取data内相关参数调用API
    res = get_kline(data)
    if res:
        # 历史kline数据填充成功，修改exception表内信息
        obj = KlineException.query.filter_by(id=data['id']).update({'status': '1'})
        if obj:
            # 仅正确查询到对象才能返回1，提交执行。
            db.session.commit()
            return 'kline fill success'
