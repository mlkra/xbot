# Copyright (C) 2022  Michał Krasoń
# pylint: disable=redefined-outer-name
import pytest
from xbot.xkom_api_client import XKomAPIClient


@pytest.fixture
def api_client() -> XKomAPIClient:
    return XKomAPIClient()


def test_getting_existing_product(api_client: XKomAPIClient):
    with api_client:
        product = api_client.get_product("1")

    assert product is not None
    assert product["Id"] == "1"
    assert product["Name"] == "Samsung Galaxy S22 Ultra"
    assert product["AvailabilityStatus"] == "Available"


def test_getting_nonexistent_product_returns_none(api_client: XKomAPIClient):
    with api_client:
        product = api_client.get_product("-1")

    assert product is None
