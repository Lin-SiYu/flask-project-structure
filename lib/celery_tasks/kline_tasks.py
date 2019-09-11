from extensions import cel_app


@cel_app.task
def kline_handler(data):
    '''
    调用 kline 填充接口
    :param data: 数据库数据，dict
    :return:
    '''
    return 'hello world'
