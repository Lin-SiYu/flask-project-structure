from app import create_app
from extensions import mongo
from kline_filler.logs.logger import log
from kline_filler.service.binance_kline import BinanceKline

from lib.celery_tasks.kline_exceptions import get_kline_exceptions

app = create_app()
if __name__ == '__main__':
    # res = get_kline_exceptions.delay()
    # print(res.status)
    # get_kline_exceptions()

    # 单交易所类下的测试方式
    # date = {'id': 1, 'exchange': 'binance', 'coin_pair': 'BTC/USDT', 'period': '1min', 'from_time': 1569677160,
    #         'end_time': 1569737210,
    #         'status': 0}
    # obj = BinanceKline()
    # obj(date)
    # res = obj.kline_res
    # print(res)

    # db = mongo.cx['binance']
    # data = db.getCollection('k_BTCUSDT_1min').find_one({'_id': 1569348000000})
    # data = mongo.cx['binance']['k_BTCUSDT_1min'].find_one({'_id': 1569348000000})
    # db = mongo.cx['binance']['k_BTCUSDT_1min']
    # # # data = db.find_one({'_id': 1569348000000})
    # # data = db.insert_one({'_id': float(156934)})
    # # print(data)
    # l = [1569378000, 1569677220, 1569677280, 1569677340, 1569677400, 1569677460, 1569677520, 1569677580, ]
    # a = db.find({"_id": {"$in":l}})
    # print(a)
    # print([i for i in a])
    '''
    {"exchange": "binance",
    "coin_pair": "BTC/USDT",
    "period": "1min",
    "from_time": 1569677160,
    "end_time": 1569737210,
    "status": 0
    }
    '''
