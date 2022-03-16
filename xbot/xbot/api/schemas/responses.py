# Copyright (C) 2022  Michał Krasoń
from enum import Enum

from pydantic import BaseModel


class APIStatus(str, Enum):
    AVAILABLE = "available"


class HealthCheckResponse(BaseModel):
    status: APIStatus
