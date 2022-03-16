# Copyright (C) 2022  Michał Krasoń
import sqlite3

from xbot.email import send_message
from xbot.repository import ProductsRepository
from xbot.settings import settings
from xbot.tasks.celery import app
from xbot.tracker import track_availability
from xbot.xkom_api_client import XKomAPIClient


@app.task
def track_availability_task():
    connection = sqlite3.connect(settings.db_path)
    repository = ProductsRepository(connection)
    api_client = XKomAPIClient()

    track_availability(repository, api_client, send_message)
