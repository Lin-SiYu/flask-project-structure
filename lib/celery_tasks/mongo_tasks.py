from extensions import cel_app, mongo


@cel_app.task
def mongo_example():
    # 查
    # data = mongo.db.testtable.find_one({'name': 'name'})
    # data = mongo.db['huobi'].find_one({'name': 'huobi'})
    # 增
    # obj = mongo.db['huobi'].insert_one({'name':'hello'})
    data = mongo.cx['huobi']['test'].insert_one({'name': 'hello'})
    return '------------------ %s -------------------' % data
