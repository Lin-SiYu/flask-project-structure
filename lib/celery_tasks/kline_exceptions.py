from extensions import cel_app
from lib.celery_tasks.task0 import say_hello
from lib.sql_models.table_kline_exception import KlineException


@cel_app.task(bind=True)
def get_kline_exceptions(self):
    query_data = KlineException.query.filter_by(status='0').all()
    if query_data:
        # 补齐k线业务
        for obj in query_data:
            data_dic = obj.get_dict()
            say_hello.delay(data_dic)
        return 'Pushed success.'