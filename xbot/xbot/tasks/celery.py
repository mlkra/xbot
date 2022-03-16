# Copyright (C) 2022  Michał Krasoń
from celery import Celery

app = Celery("xbot")
app.config_from_object("xbot.tasks.celeryconfig")

if __name__ == "__main__":
    app.start()
