# Copyright (C) 2022  Michał Krasoń
from enum import Enum


class AvailabilityStatus(str, Enum):
    AVAILABLE = "Available"
    UNAVAILABLE = "Unavailable"
