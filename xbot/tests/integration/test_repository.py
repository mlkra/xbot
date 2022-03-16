# Copyright (C) 2022  Michał Krasoń
# pylint: disable=redefined-outer-name
import sqlite3

import pytest
from xbot.enums import AvailabilityStatus
from xbot.repository import ProductsRepository, TrackedProduct


@pytest.fixture
def repository(connection: sqlite3.Connection) -> ProductsRepository:
    return ProductsRepository(connection)


def test_adding_tracked_product(repository: ProductsRepository):
    product_id = "5"
    availability_status = AvailabilityStatus.AVAILABLE
    product = TrackedProduct(
        product_id=product_id, availability_status=availability_status
    )

    repository.add_tracked_product(product)

    product = repository.list_tracked_products()[-1]

    assert product["product_id"] == product_id
    assert product["availability_status"] == availability_status


def test_deleting_tracked_product(repository: ProductsRepository):
    product_id = "4"
    product = TrackedProduct(
        product_id=product_id, availability_status=AvailabilityStatus.AVAILABLE
    )
    repository.add_tracked_product(product)

    repository.delete_tracked_product(product_id)

    products = repository.list_tracked_products()
    assert product not in products


def test_listing_tracked_products(repository: ProductsRepository):
    products = [
        TrackedProduct(
            product_id="1", availability_status=AvailabilityStatus.AVAILABLE
        ),
        TrackedProduct(
            product_id="2", availability_status=AvailabilityStatus.UNAVAILABLE
        ),
    ]
    repository.add_tracked_product(products[0])
    repository.add_tracked_product(products[1])

    listed_products = repository.list_tracked_products()[-2:]

    assert products == listed_products


def test_updating_tracked_product(repository: ProductsRepository):
    product_id = "3"
    product = TrackedProduct(
        product_id=product_id, availability_status=AvailabilityStatus.AVAILABLE
    )
    repository.add_tracked_product(product)

    updated_product = TrackedProduct(
        product_id=product_id, availability_status=AvailabilityStatus.UNAVAILABLE
    )
    repository.update_tracked_product(updated_product)

    product = repository.list_tracked_products()[-1]
    assert product["availability_status"] == AvailabilityStatus.UNAVAILABLE
