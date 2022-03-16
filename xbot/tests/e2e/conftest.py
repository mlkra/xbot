# Copyright (C) 2022  Michał Krasoń
# pylint: disable=redefined-outer-name
import sqlite3
from pathlib import Path

import pytest
from xbot.migrations import migrate
from xbot.settings import settings


@pytest.fixture(scope="session")
def celery_config():
    return {"broker_url": "amqp://", "result_backend": "rpc://"}


@pytest.fixture(scope="session", autouse=True)
def db_path(tmp_path_factory: pytest.TempPathFactory) -> Path:
    path = tmp_path_factory.getbasetemp() / "xbot_e2e.db"
    settings.db_path = path.as_posix()
    return path


@pytest.fixture(scope="session")
def connection(db_path: Path) -> sqlite3.Connection:
    con = sqlite3.connect(db_path)

    yield con

    con.close()


@pytest.fixture(scope="session", autouse=True)
def setup_database(db_path: Path):
    migrate(db_path)
