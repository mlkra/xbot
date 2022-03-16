# Copyright (C) 2022  Michał Krasoń
import argparse
import sqlite3
from pathlib import Path


def migrate(db_path: str | Path):
    con = sqlite3.connect(db_path)

    con.execute(
        (
            "CREATE TABLE IF NOT EXISTS tracked_products("
            "product_id TEXT UNIQUE,"
            "availability_status TEXT"
            ")"
        )
    )

    con.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Migrate database.")
    parser.add_argument(
        "--db-path", type=str, default="xbot.db", help="a path of the database file"
    )
    args = parser.parse_args()
    migrate(args.db_path)
