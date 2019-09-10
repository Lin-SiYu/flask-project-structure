from extensions import cel_app


@cel_app.task
def subtract(a, b):
    return a - b
