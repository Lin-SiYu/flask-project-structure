# flask-project-structure
A flask project with components

- 项目根目录下执行;-n 后随意跟别名，用于防止worker同名
**celery worker 启动方式**：celery worker -A celery_worker.cel_app  -l info -P eventlet -n worker0
**celery beat 启动方式**：celery beat -A celery_worker.cel_app  -l info -s ./lib/celery_tasks/celery_log/beat