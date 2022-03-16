# Copyright (C) 2022  Michał Krasoń
from email.message import EmailMessage

from typing_extensions import Self
from xbot.repository import TrackedProduct
from xbot.xkom_api_client.schemas import Product


class FakeProductsRepository:
    tracked_products: dict[str, TrackedProduct]

    def __init__(self, tracked_products: list[TrackedProduct]):
        self.tracked_products = {
            product["product_id"]: product for product in tracked_products
        }

    def delete_tracked_product(self, product_id: str):
        del self.tracked_products[product_id]

    def list_tracked_products(self) -> list[TrackedProduct]:
        return self.tracked_products.copy().values()

    def update_tracked_product(self, product: TrackedProduct):
        self.tracked_products[product["product_id"]] = product


class FakeAPIClient:
    products: dict[str, Product]

    def __init__(self, products: list[Product]):
        self.products = {product["Id"]: product for product in products}

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_product(self, product_id: str) -> Product | None:
        return self.products.get(product_id)


received_messages: list[EmailMessage] = []


def fake_send_message(message: EmailMessage):
    received_messages.append(message)
