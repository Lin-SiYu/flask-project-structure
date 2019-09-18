from extensions import cel_app, mongo


@cel_app.tasks
def mongo_example():
    # 查
    data = mongo.db.testtable.find({'name': 'name'})
    return '------------------ %s -------------------' % data
