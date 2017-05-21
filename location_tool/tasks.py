from celery import Celery

app = Celery('tasks')
app.config_from_object('location_tool.celeryconfig')

@app.task
def add(x, y):
    return x + y

