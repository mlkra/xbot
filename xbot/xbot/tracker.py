# Copyright (C) 2022  Michał Krasoń
from email.message import EmailMessage
from typing import Callable

from xbot.enums import AvailabilityStatus
from xbot.repository import ProductsRepository
from xbot.xkom_api_client import XKomAPIClient


def track_availability(
    repository: ProductsRepository,
    api_client: XKomAPIClient,
    send_message: Callable[[EmailMessage], None],
):
    tracked_products = repository.list_tracked_products()
    with api_client:
        for tracked_product in tracked_products:
            product = api_client.get_product(tracked_product["product_id"])
            if not product:
                message = EmailMessage()
                message["Subject"] = "Product was not found"
                message.set_content(
                    f"Product with id {tracked_product['product_id']} was not found."
                )
                send_message(message)
                repository.delete_tracked_product(tracked_product["product_id"])
            elif (
                tracked_product["availability_status"] == AvailabilityStatus.UNAVAILABLE
            ):
                if product["AvailabilityStatus"] == AvailabilityStatus.AVAILABLE:
                    tracked_product[
                        "availability_status"
                    ] = AvailabilityStatus.AVAILABLE
                    repository.update_tracked_product(tracked_product)
                    message = EmailMessage()
                    message["Subject"] = "Product has become available"
                    message.set_content(f"{product['Name']} has become available.")
                    send_message(message)
            else:
                if product["AvailabilityStatus"] == AvailabilityStatus.UNAVAILABLE:
                    tracked_product[
                        "availability_status"
                    ] = AvailabilityStatus.UNAVAILABLE
                    repository.update_tracked_product(tracked_product)
