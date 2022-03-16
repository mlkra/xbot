# Copyright (C) 2022  Michał Krasoń
import sqlite3
from typing import TypedDict

from xbot.enums import AvailabilityStatus
from xbot.settings import settings


class TrackedProduct(TypedDict):
    product_id: str
    availability_status: AvailabilityStatus


class ProductsRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def add_tracked_product(self, product: TrackedProduct):
        self.connection.execute(
            "INSERT INTO tracked_products(product_id, availability_status) VALUES (?, ?)",
            (product["product_id"], product["availability_status"]),
        )
        self.connection.commit()

    def delete_tracked_product(self, product_id: str):
        print(product_id)
        self.connection.execute(
            "DELETE FROM tracked_products WHERE product_id = ?", [product_id]
        )
        self.connection.commit()

    def list_tracked_products(self) -> list[TrackedProduct]:
        cursor = self.connection.execute(
            "SELECT product_id, availability_status FROM tracked_products"
        )
        return [
            TrackedProduct(product_id=row[0], availability_status=row[1])
            for row in cursor.fetchall()
        ]

    def update_tracked_product(self, product: TrackedProduct):
        self.connection.execute(
            "UPDATE tracked_products SET availability_status = ? WHERE product_id = ?",
            (product["availability_status"], product["product_id"]),
        )
        self.connection.commit()


def get_products_repository() -> ProductsRepository:
    connection = sqlite3.connect(settings.db_path)
    return ProductsRepository(connection)
