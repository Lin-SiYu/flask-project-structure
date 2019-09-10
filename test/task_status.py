from celery.result import AsyncResult
from extensions import cel_app


# 指定查询对象，id为task_id 93d0890f-488a-4ed5-bafc-b86df81d23a2,app指定对象，需要导入

def get_status(task_id):
    async = AsyncResult(id=task_id, app=cel_app)
    print(async.status)
    if async.successful():
        result = async.get()
        print(result)
        # result.forget() # 将结果删除
    elif async.failed():
        print('执行失败')
    elif async.status == 'PENDING':
        print('任务等待中被执行')
    elif async.status == 'RETRY':
        print('任务异常后正在重试')
    elif async.status == 'STARTED':
        print('任务已经开始被执行')


if __name__ == '__main__':
    get_status('2a382d22-3760-4dc9-9069-affb95ba6dc1')
