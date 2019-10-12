# from celery.bin import worker


'''
worker 开启方式： celery worker -A celery_worker.cel_app -l info -P eventlet
'''
from app import create_app
from extensions import cel_app

# 让当前进程初始化flask组件
app = create_app()

if __name__ == '__main__':
    '''以下方法测试中，未开启节点，无法处理消息'''

    # worker = worker.worker(cel_app)
    # options = {
    #     'loglevel': 'INFO',
    #     'pool_cls': 'eventlet'
    # }
    # worker.run(**options)

    # celery worker -A extensions -l info -P eventlet
    # argv = ['-A=extensions', '-l=info', '-P=eventlet', '-n=worker_0']
    # cel_app.worker_main(argv=argv)

    # celery beat -A extensions -l info
    # argv = ['celery', 'worker', '-A=extensions', '-l=info']
    # # cel_app.start(argv=argv)
    with app.app_context():
        # cel_app.start(argv=argv)
        argv = ['-A=extensions', '-l=info', '-P=eventlet', '-n=worker_0']
        cel_app.worker_main(argv=argv)
