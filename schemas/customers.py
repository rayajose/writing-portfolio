from __future__ import annotations

from pydantic import BaseModel, Field


class CustomerCreate(BaseModel):
    first_name: str = Field(..., examples=["Alex"])
    last_name: str = Field(..., examples=["Morgan"])
    email: str = Field(..., examples=["alex.morgan@example.com"])
    phone: str | None = Field(None, examples=["555-0101"])


class CustomerResponse(BaseModel):
    customer_id: str
    first_name: str
    last_name: str
    email_masked: str | None = None
    phone_masked: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class CustomerAddressCreate(BaseModel):
    address_line1: str = Field(..., examples=["123 Example Street"])
    address_line2: str | None = Field(None, examples=["Apt 4B"])
    city: str = Field(..., examples=["Seattle"])
    state: str = Field(..., examples=["WA"])
    postal_code: str = Field(..., examples=["98101"])
    country: str = Field("US", examples=["US"])


class CustomerAddressResponse(BaseModel):
    address_id: str
    customer_id: str
    address_line1_masked: str | None = None
    address_line2_encrypted: str | None = None
    city: str
    state: str
    postal_code_masked: str | None = None
    country: str
    created_at: str | None = None


class CustomerDeleteRequest(BaseModel):
    customer_ids: list[str]


class CustomerDeleteResult(BaseModel):
    customer_id: str
    status: str
    message: str


class CustomerDeleteResponse(BaseModel):
    deleted_count: int
    failed_count: int
    results: list[CustomerDeleteResult]
