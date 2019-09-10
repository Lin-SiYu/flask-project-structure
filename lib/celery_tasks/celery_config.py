import pathlib

CELERY_TASKS_DIR = pathlib.Path(__file__).parents[0]
CELERY_INCLUDE = ['lib.celery_tasks.%s' % task_file.name.split('.')[0] for task_file in
                  CELERY_TASKS_DIR.glob('*.py')]

BROKER_URL = 'redis://localhost:6379/13'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/14'
