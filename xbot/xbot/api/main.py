# Copyright (C) 2022  Michał Krasoń
from fastapi import FastAPI, HTTPException, status
from xbot.api.schemas import TrackedProduct, TrackedProductRead
from xbot.api.schemas.responses import APIStatus, HealthCheckResponse
from xbot.repository import get_products_repository
from xbot.xkom_api_client.api_client import XKomAPIClient

app = FastAPI()


@app.get("/api/v1/health", response_model=HealthCheckResponse)
def health_check():
    return {"status": APIStatus.AVAILABLE}


@app.get("/api/v1/tracked_products", response_model=list[TrackedProductRead])
def tracked_products():
    repository = get_products_repository()
    products = repository.list_tracked_products()
    return products


@app.post(
    "/api/v1/tracked_products",
    status_code=status.HTTP_201_CREATED,
    response_model=TrackedProduct,
)
def tracked_product_add(tracked_product: TrackedProduct):
    client = XKomAPIClient()
    with client:
        product = client.get_product(tracked_product.product_id)
    if product:
        repository = get_products_repository()
        repository.add_tracked_product(
            {
                "product_id": product["Id"],
                "availability_status": product["AvailabilityStatus"],
            }
        )
        return tracked_product
    raise HTTPException(status_code=404, detail="Product not found")


@app.delete(
    "/api/v1/tracked_products/{product_id}", status_code=status.HTTP_204_NO_CONTENT
)
def tracked_product_delete(product_id: str):
    repository = get_products_repository()
    repository.delete_tracked_product(product_id)
