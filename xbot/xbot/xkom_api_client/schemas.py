# Copyright (C) 2022  Michał Krasoń
from typing import TypedDict

from xbot.enums import AvailabilityStatus


class Product(TypedDict):
    Id: str
    Name: str
    AvailabilityStatus: AvailabilityStatus
