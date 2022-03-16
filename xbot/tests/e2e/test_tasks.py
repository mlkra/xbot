# Copyright (C) 2022  Michał Krasoń
# pylint: disable=redefined-outer-name
import sqlite3

import pytest
from tests.mailhog_client import (
    count_messages,
    get_message,
    get_message_content,
    get_message_subject,
)
from xbot.enums import AvailabilityStatus
from xbot.repository import ProductsRepository, TrackedProduct
from xbot.tasks import track_availability_task


@pytest.fixture
def products_repository(connection: sqlite3.Connection) -> ProductsRepository:
    repository = ProductsRepository(connection)

    yield repository

    for product in repository.list_tracked_products():
        repository.delete_tracked_product(product["product_id"])


@pytest.mark.usefixtures("celery_session_worker")
def test_tracked_product_has_become_available(products_repository: ProductsRepository):
    products_repository.add_tracked_product(
        TrackedProduct(
            product_id="1", availability_status=AvailabilityStatus.UNAVAILABLE
        )
    )

    track_availability_task.delay().get()

    message = get_message()
    assert get_message_subject(message) == "Product has become available"
    assert (
        get_message_content(message) == "Samsung Galaxy S22 Ultra has become available."
    )


@pytest.mark.usefixtures("celery_session_worker")
def test_tracked_product_has_become_unavailable(
    products_repository: ProductsRepository,
):
    products_repository.add_tracked_product(
        TrackedProduct(product_id="3", availability_status=AvailabilityStatus.AVAILABLE)
    )
    received_messages_count = count_messages()

    track_availability_task.delay().get()

    tracked_product = products_repository.list_tracked_products()[0]
    assert tracked_product["availability_status"] == AvailabilityStatus.UNAVAILABLE
    assert received_messages_count == count_messages()


@pytest.mark.usefixtures("celery_session_worker")
def test_tracked_product_does_not_exist(products_repository: ProductsRepository):
    product_id = "-1"
    products_repository.add_tracked_product(
        TrackedProduct(
            product_id=product_id, availability_status=AvailabilityStatus.AVAILABLE
        )
    )

    track_availability_task.delay().get()

    message = get_message()
    assert get_message_subject(message) == "Product was not found"
    assert (
        get_message_content(message) == f"Product with id {product_id} was not found."
    )
    assert len(products_repository.list_tracked_products()) == 0
