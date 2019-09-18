from lib.celery_tasks.mongo_tasks import mongo_example

if __name__ == '__main__':
    mongo_example.delay()
