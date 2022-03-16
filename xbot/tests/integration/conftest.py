# Copyright (C) 2022  Michał Krasoń
# pylint: disable=redefined-outer-name
import sqlite3
from pathlib import Path

import pytest
from xbot.migrations import migrate


@pytest.fixture(scope="session")
def db_path(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return tmp_path_factory.getbasetemp() / "xbot_integration.db"


@pytest.fixture
def connection(db_path: Path) -> sqlite3.Connection:
    con = sqlite3.connect(db_path)

    yield con

    con.rollback()
    con.close()


@pytest.fixture(scope="session", autouse=True)
def setup_database(db_path: Path):
    migrate(db_path)
