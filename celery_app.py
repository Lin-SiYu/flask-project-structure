from celery.bin import worker

from extensions import cel_app

if __name__ == '__main__':
    # worker = worker.worker(cel_app)
    # options = {
    #     'loglevel': 'INFO',
    #     'pool_cls': 'eventlet'
    # }
    # worker.run(**options)

    # celery worker -A extensions -l info -P eventlet
    argv = ['worker', '-A=extensions', '-l=info', '-P=eventlet','-n=worker_0@%h' ]
    cel_app.worker_main(argv=argv)
