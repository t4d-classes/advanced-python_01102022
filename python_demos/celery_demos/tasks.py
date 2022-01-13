from celery import Celery
from time import sleep


app = Celery(
    'tasks',
    broker='pyamqp://guest@localhost//',
    backend="redis://localhost:6379/0")

@app.task
def echo(msg: str):
    sleep(15)
    return msg

@app.task
def get_list(x: int, y: int):
    sleep(15)
    return [x] * y

class Person:

    def __init__(self, fn, ln):
        self.fn = fn
        self.ln = ln

@app.task
def create_person(fn: str, ln: str):
    sleep(15)
    return Person(fn, ln).__dict__      