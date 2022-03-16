from pydantic import BaseModel
from xbot.enums import AvailabilityStatus


class TrackedProduct(BaseModel):
    product_id: str


class TrackedProductRead(TrackedProduct):
    availability_status: AvailabilityStatus
