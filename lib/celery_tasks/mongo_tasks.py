from extensions import cel_app, mongo


@cel_app.task
def mongo_example():
    # 查
    data = mongo.db.testtable.find_one({'name': 'name'})
    return '------------------ %s -------------------' % data
