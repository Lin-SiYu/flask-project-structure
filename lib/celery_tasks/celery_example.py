from extensions import cel_app


@cel_app.task
def nums_add(a, b):
    return a + b

