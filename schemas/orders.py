from pydantic import BaseModel, Field
from typing import List, Optional


class OrderItemCreate(BaseModel):
    product_id: str
    quantity: int = Field(gt=0)


class OrderCreateRequest(BaseModel):
    partner_name: str
    customer_reference: Optional[str] = None
    customer_id: Optional[str] = None
    shipping_address_id: Optional[str] = None
    items: List[OrderItemCreate]


class OrderItemResponse(BaseModel):
    order_item_id: str
    product_id: str
    sku: Optional[str] = None
    product_name: Optional[str] = None
    quantity: int
    unit_price: Optional[float] = None
    line_total: Optional[float] = None
    customer_id: Optional[str] = None
    shipping_address_id: Optional[str] = None


class OrderResponse(BaseModel):
    order_id: str
    partner_name: str
    customer_reference: Optional[str] = None
    status: str
    total_amount: Optional[float] = None
    currency: str = "USD"
    items: List[OrderItemResponse]


class OrderListResponse(BaseModel):
    count: int
    items: List[OrderResponse]


class FulfillmentJobResponse(BaseModel):
    job_id: str
    order_id: str
    status: str
    message: Optional[str] = None


class ShipmentResponse(BaseModel):
    shipment_id: str
    order_id: str
    job_id: str
    status: str
    carrier: Optional[str] = None
    tracking_number: Optional[str] = None
