# flask-project-structure
A flask project with components

# 注意事项

- 项目根目录下执行;
- -n 参数用于跟别名，用于防止 worker 同名

**celery worker 启动方式(win)**

celery worker -A celery_worker.cel_app  -l info -P eventlet -n worker0

**celery beat 启动方式**

celery beat -A celery_worker.cel_app  -l info -s ./lib/celery_tasks/celery_log/beat

**一起启动 worker 和 beat,不适用于win**

celery -B -A celery_worker.cel_app worker -l info  -s ./lib/celery_tasks/celery_log/beat -P eventlet -n worker0
