# Copyright (C) 2022  Michał Krasoń
from typing import TypedDict

import requests

MAILHOG_URL = "http://localhost:8025"


class Headers(TypedDict):
    Subject: list[str]


class Content(TypedDict):
    Body: str
    Headers: Headers


class Message(TypedDict):
    Content: Content


def count_messages() -> int:
    response = requests.get(f"{MAILHOG_URL}/api/v2/messages", params={"limit": 1})
    return response.json()["total"]


def get_message() -> Message:
    response = requests.get(f"{MAILHOG_URL}/api/v2/messages", params={"limit": 1})
    return response.json()["items"][0]


def get_message_content(message: Message) -> str:
    return message["Content"]["Body"]


def get_message_subject(message: Message) -> str:
    return message["Content"]["Headers"]["Subject"][0]
