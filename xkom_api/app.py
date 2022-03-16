# Copyright (C) 2022  Michał Krasoń
import random
import string
from typing import Tuple

from flask import Flask, Response, jsonify, request
from user_agents import parse

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

HASH = "".join(random.choices(string.ascii_lowercase + string.digits, k=7))
API_KEY = "".join(random.choices(string.ascii_letters + string.digits, k=16))


class InvalidAPIKey(Exception):
    pass


class InvalidUserAgent(Exception):
    pass


@app.errorhandler(InvalidAPIKey)
def invalid_api_key(_) -> Tuple[Response, int]:
    return (
        jsonify(
            {
                "Errors": [
                    {
                        "Code": "InvalidApiKey",
                        "Message": "Nieprawidłowa wartość API Key.",
                        "Context": "InvalidApiKey",
                    }
                ],
                "Message": "Błąd autoryzacyjny",
            }
        ),
        401,
    )


@app.errorhandler(InvalidUserAgent)
def invalid_user_agent(_) -> Response:
    return Response("error code: 1020", 403)


class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self) -> dict:
        rv = dict(self.payload or ())
        rv["Message"] = self.message
        return rv


class ResourceNotFound(InvalidAPIUsage):
    status_code = 404


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e: InvalidAPIUsage) -> Response:
    return jsonify(e.to_dict()), e.status_code


@app.route("/")
def index() -> str:
    return f"""
        <!doctype html>
        <html lang="pl" >
        <head>
            <meta charset="utf-8">
            <script type="module" src="//{request.host}/public-spa/xkom/chunk-app-{HASH}.esm.min.js"></script>
        </head>
        <body >
            <div id="react-portals"></div>
        </body>
        </html>"""


@app.route(f"/public-spa/xkom/chunk-app-{HASH}.esm.min.js")
def chunk_app() -> Response:
    return Response(
        (
            'var i={protocol:"//",host:"mobileapi.x-kom.pl",port:""},'
            f'c={{xkom:n({{}},i,{{path:"/api/v1/xkom",key:"{API_KEY}"}}),'
            'alto:n({},i,{path:"/api/v1/alto",key:"L2BBIXx5zPfPcFU4"})}'
        ),
        mimetype="text/javascript",
    )


products_ = {
    "1": {
        "Id": "1",
        "Name": "Samsung Galaxy S22 Ultra",
        "AvailabilityStatus": "Available",
    },
    "2": {"Id": "2", "Name": "OnePlus 8T", "AvailabilityStatus": "Available"},
    "3": {"Id": "3", "Name": "Apple iPhone 12", "AvailabilityStatus": "Unavailable"},
    "4": {"Id": "4", "Name": "Xiaomi Mi 10T", "AvailabilityStatus": "Unavailable"},
}


@app.route("/api/v1/xkom/products/<string:product_id>")
def products(product_id: str) -> Response:
    if not _validate_user_agent():
        raise InvalidUserAgent
    if not _validate_api_key():
        raise InvalidAPIKey

    product = products_.get(product_id)
    if product is None:
        raise ResourceNotFound("Nie znaleziono produktu o podanym identyfikatorze.")

    return jsonify(product)


def _validate_user_agent() -> bool:
    user_agent = parse(request.headers.get("User-Agent"))
    return not user_agent.is_bot


def _validate_api_key() -> bool:
    api_key = request.headers.get("X-API-KEY")
    return api_key == API_KEY
