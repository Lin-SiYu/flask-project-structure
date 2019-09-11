import pathlib
from datetime import timedelta

CELERY_TASKS_DIR = pathlib.Path(__file__).parents[0]
CELERY_INCLUDE = ['lib.celery_tasks.%s' % task_file.name.split('.')[0] for task_file in
                  CELERY_TASKS_DIR.glob('*.py')]

BROKER_URL = 'redis://127.0.0.1:6379/13'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/14'
CELERYBEAT_SCHEDULE = {
    'rate-every-60-seconds': {
        'task': 'lib.celery_tasks.kline_exceptions.get_kline_exceptions',
        # 每隔60秒执行一次
        'schedule': timedelta(seconds=60),
        # 'args': ('test',)
    },
}
