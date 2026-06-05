from typing import Literal

from pydantic import BaseModel, HttpUrl


class WebhookCreateRequest(BaseModel):
    partner_id: str
    url: HttpUrl
    events: list[str]


class WebhookUpdateRequest(BaseModel):
    url: HttpUrl | None = None
    events: list[str] | None = None
    status: Literal["active", "disabled"] | None = None


class WebhookCreateResponse(BaseModel):
    webhook_id: str
    partner_id: str
    url: str
    events: list[str]
    secret: str
    status: str
    created_at: str
    updated_at: str


class WebhookResponse(BaseModel):
    webhook_id: str
    partner_id: str
    url: str
    events: list[str]
    status: str
    created_at: str
    updated_at: str
