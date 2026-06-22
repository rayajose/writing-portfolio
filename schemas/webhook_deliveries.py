from datetime import datetime
from typing import Any

from pydantic import BaseModel


class WebhookDeliveryResponse(BaseModel):
    delivery_id: str
    webhook_id: str
    partner_id: str | None = None
    partner_name: str | None = None
    event_type: str
    status: str
    response_code: int | None = None
    request_payload: dict[str, Any] | None = None
    response_body: str | None = None
    created_at: datetime


class WebhookDeliveryListResponse(BaseModel):
    total: int
    items: list[WebhookDeliveryResponse]
