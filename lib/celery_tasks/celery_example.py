# 注意 celery-app 必须使用相对路径导入
from .celery import cel_app


@cel_app.task
def add(a, b):
    return a + b
