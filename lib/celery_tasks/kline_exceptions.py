from extensions import cel_app, db
from lib.sql_models.table_kline_exception import KlineException
from lib.celery_tasks.kline_tasks import kline_handler


@cel_app.task
def get_kline_exceptions():
    '''
    定时执行，轮询数据库内数据是否存在未处理数据
     - 存在数据：推送 task 给 celery
    :return:
    '''
    query_data = KlineException.query.filter_by(status='0').all()
    if query_data:
        # 补齐k线业务
        for obj in query_data:
            db.session.add(obj)
            data = obj.get_dict()
            kline_handler.delay(data)
