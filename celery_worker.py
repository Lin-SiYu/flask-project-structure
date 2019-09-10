# from celery.bin import worker

from extensions import cel_app

'''
worker 开启方式： celery worker -A celery_worker -l info -P eventlet
'''

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
    # argv = ['celery','beat', '-A=extensions', '-l=info']
    # cel_app.start(argv=argv)
