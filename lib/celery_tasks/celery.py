import pathlib

from celery import Celery

CELERY_TASKS_DIR = pathlib.Path(__file__).parents[0]
# 获取当前目录下的文件信息，在include自动录入有效任务
task_files = ['celery_tasks.%s' % task_file.name.split('.')[0] for task_file in
              CELERY_TASKS_DIR.glob('*.py')]

# 在lib目录下
# 命令行执行 celery worker -A celery_tasks  -l info ；注意，windows下加参数：-P eventlet
# 注意，当前 celery 文件名不可更改
cel_app = Celery('example', broker='redis://localhost:6379/0', include=task_files)
