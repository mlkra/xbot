# Copyright (C) 2022  Michał Krasoń
from fastapi import status
from fastapi.testclient import TestClient
from xbot.api import app
from xbot.api.schemas.responses import APIStatus
from xbot.enums import AvailabilityStatus

client = TestClient(app)


def test_health_check():
    response = client.get("/api/v1/health")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": APIStatus.AVAILABLE}


def test_adding_tracked_product():
    response = client.post("/api/v1/tracked_products", json={"product_id": "2"})

    assert response.status_code == status.HTTP_201_CREATED
    response = client.get("/api/v1/tracked_products")
    assert response.status_code == status.HTTP_200_OK
    product = response.json()[-1]
    assert product["product_id"] == "2"
    assert product["availability_status"] == AvailabilityStatus.AVAILABLE


def test_adding_nonexistent_tracked_product_returns_404():
    response = client.get("/api/v1/tracked_products")
    tracked_products_len = len(response.json())

    response = client.post("/api/v1/tracked_products", json={"product_id": "-1"})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    response = client.get("/api/v1/tracked_products")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == tracked_products_len


def test_deleting_added_tracked_product():
    response = client.get("/api/v1/tracked_products")
    tracked_products_len = len(response.json())

    client.post("/api/v1/tracked_products", {"product_id": "3"})

    response = client.delete("/api/v1/tracked_products/3")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = client.get("/api/v1/tracked_products")
    assert tracked_products_len == len(response.json())
