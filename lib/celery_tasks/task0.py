from extensions import cel_app


@cel_app.task
def say_hello(data):
    return 'hello world'
