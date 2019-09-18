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
