from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PartnerCreate(BaseModel):
    partner_name: str
    contact_email: Optional[str] = None
    feed_type: str = "product_catalog"
    default_file_format: str = "csv"


class PartnerUpdate(BaseModel):
    partner_name: Optional[str] = None
    status: Optional[str] = None
    contact_email: Optional[str] = None
    feed_type: Optional[str] = None
    default_file_format: Optional[str] = None


class PartnerResponse(BaseModel):
    partner_id: str
    partner_name: str
    status: str
    contact_email: Optional[str] = None
    feed_type: str
    default_file_format: str
    created_at: datetime
    updated_at: datetime
