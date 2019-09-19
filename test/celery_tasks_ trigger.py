from app import create_app
from extensions import cel_app
from lib.celery_tasks.celery_example import nums_add
from lib.celery_tasks.mongo_tasks import mongo_example
from test.task_status import get_status

app = create_app()

if __name__ == '__main__':
    data = mongo_example.delay()
    print(data.status)
    # data = nums_add.delay(1, 2)
    # print(get_status(data))
    # print(cel_app.AsyncResult('ceb7633d-6250-4abf-9be4-9dfc231d2140').info)

from app import create_app
from lib.celery_tasks.kline_exceptions import get_kline_exceptions
from lib.celery_tasks.kline_tasks import kline_handler

app = create_app()

# huobi - 成功例子
# data = {'id': 1, 'exchange': 'huobi', 'coin_pair': 'ETH/BTC', 'period': '1min', 'from_time': '1501236900',
#         'end_time': '1568688540',
#         'status': 0}

# huobi - 请求成功但数据获取失败例子
# data = {'id':1,'exchange': 'huobi', 'coin_pair': 'BTC/USDT', 'period': '1min', 'from_time': '1501236900',
#         'end_time': '1568688540',
#         'status': 0}

# {'id': 1, 'exchange': 'huobi', 'coin_pair': 'ETH/BTC', 'period': '1min', 'from_time': '1501236900',
#  'end_time': '1568688540', 'status': '0'}


if __name__ == '__main__':
    data = {'id': 1, 'exchange': 'huobi', 'coin_pair': 'ETH/BTC', 'period': '1min', 'from_time': '1501236900',
            'end_time': '1568688540', 'status': '0'}

    # todo 同步可执行，推入celery报错
    # res = get_kline_exceptions.delay()
    # print(res.status)
    get_kline_exceptions()
    # res = kline_handler.delay(data)
    # kline_handler(data)
    # ws_test.delay('ws://127.0.0.1:8765')
    # res = ws_test('wss://api.huobi.pro/ws')
    # print(res)
    # ws_test.delay('wss://api.huobi.pro/ws')

