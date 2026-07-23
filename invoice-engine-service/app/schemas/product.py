import uuid
from decimal import Decimal
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    hsn_code: Optional[str] = None
    unit_price: Decimal
    gst_rate: Decimal
    unit: Optional[str] = "piece"

    @field_validator("gst_rate")
    @classmethod
    def validate_gst_rate(cls, v):
        allowed = [Decimal("0"), Decimal("5"), Decimal("12"), Decimal("18"), Decimal("28")]
        if v not in allowed:
            raise ValueError(f"GST rate must be 0, 5, 12, 18, or 28 percent")
        return v
    
    @field_validator("unit_price")
    @classmethod
    def validate_unit_price(cls, v):
        if v <= 0:
            raise ValueError("Unit price must be greater than zero")
        return v
    
class ProductResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    name: str
    description: Optional[str] = None
    hsn_code: Optional[str] = None
    unit_price: Decimal
    gst_rate: Decimal
    unit: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True



