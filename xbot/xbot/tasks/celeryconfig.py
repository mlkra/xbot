# Copyright (C) 2022  Michał Krasoń
from datetime import timedelta

broker_url = "pyamqp://"
beat_schedule = {
    "track_availability": {
        "task": "xbot.tasks.track_availability_task",
        "schedule": timedelta(hours=4),
    },
}
include = ["xbot.tasks"]
result_backend = "rpc://"
