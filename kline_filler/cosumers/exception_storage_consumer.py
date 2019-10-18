import json
from extensions import db
from kline_filler.cosumers.consumer_base import ConsumerBase
from kline_filler.logs.logger import log
from lib.sql_models.table_kline_exception import KlineException


class ExceptionStorage(ConsumerBase):

    def consumer_handle(self, body):
        data = json.loads(body)
        for exc_info in data:
            if 'status' not in exc_info:
                exc_info['status'] = 0
            if KlineException.query.filter_by(**exc_info).first():
                # 存在一模一样的数据，不添加
                continue
            db.session.add(KlineException(**exc_info))
        db.session.commit()
        log.info('kline_exception_storage - Store successful.')
