# Copyright (C) 2022  Michał Krasoń
from typing import Tuple

from tests.fakes import (
    FakeAPIClient,
    FakeProductsRepository,
    fake_send_message,
    received_messages,
)
from xbot.enums import AvailabilityStatus
from xbot.repository import TrackedProduct
from xbot.tracker import track_availability
from xbot.xkom_api_client.schemas import Product


def setup_fake_services(
    tracked_products: list[TrackedProduct], products: list[Product]
) -> Tuple[FakeProductsRepository, FakeAPIClient]:
    return FakeProductsRepository(tracked_products), FakeAPIClient(products)


def create_services_with_product(
    previous_availability_status: AvailabilityStatus,
    new_availability_status: AvailabilityStatus,
) -> Tuple[FakeProductsRepository, FakeAPIClient]:
    product_id = "1"
    return setup_fake_services(
        [
            TrackedProduct(
                product_id=product_id, availability_status=previous_availability_status
            )
        ],
        [
            Product(
                Id=product_id,
                Name="Samsung Galaxy S22 Ultra",
                AvailabilityStatus=new_availability_status,
            )
        ],
    )


def test_tracked_product_has_become_available():
    product_id = "1"
    tracked_product = TrackedProduct(
        product_id=product_id, availability_status=AvailabilityStatus.UNAVAILABLE
    )
    product = Product(
        Id=product_id,
        Name="Samsung Galaxy S22 Ultra",
        AvailabilityStatus=AvailabilityStatus.AVAILABLE,
    )
    repository, api_client = setup_fake_services([tracked_product], [product])

    track_availability(repository, api_client, fake_send_message)

    message = received_messages[-1]
    assert message["Subject"] == "Product has become available"
    assert message.get_content() == f"{product['Name']} has become available.\n"
    assert (
        repository.tracked_products[product_id]["availability_status"]
        == AvailabilityStatus.AVAILABLE
    )


def test_notification_not_sent_if_tracked_product_was_available_before():
    repository, api_client = create_services_with_product(
        previous_availability_status=AvailabilityStatus.AVAILABLE,
        new_availability_status=AvailabilityStatus.AVAILABLE,
    )
    received_messages_len = len(received_messages)

    track_availability(repository, api_client, fake_send_message)

    assert received_messages_len == len(received_messages)


def test_availability_status_updated_when_tracked_product_has_become_unavailable():
    repository, api_client = create_services_with_product(
        previous_availability_status=AvailabilityStatus.AVAILABLE,
        new_availability_status=AvailabilityStatus.UNAVAILABLE,
    )

    track_availability(repository, api_client, fake_send_message)

    assert (
        repository.tracked_products["1"]["availability_status"]
        == AvailabilityStatus.UNAVAILABLE
    )


def test_tracked_product_was_not_found():
    product_id = "1"
    repository, api_client = setup_fake_services(
        [
            TrackedProduct(
                product_id=product_id, availability_status=AvailabilityStatus.AVAILABLE
            )
        ],
        [],
    )

    track_availability(repository, api_client, fake_send_message)

    message = received_messages[-1]
    assert message["Subject"] == "Product was not found"
    assert message.get_content() == f"Product with id {product_id} was not found.\n"
    assert repository.tracked_products.get(product_id) is None
