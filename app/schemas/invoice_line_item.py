import uuid
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, field_validator

class LineItemCreate(BaseModel):
    invoice_id: uuid.UUID
    product_id: uuid.UUID
    quantity: Decimal
    is_interstate: bool = False  # True if selling across states, False if selling within the same state

    @field_validator("quantity")
    @classmethod
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be greater than zero.")
        return v
    
class LineItemResponse(BaseModel):
    id: uuid.UUID
    invoice_id: uuid.UUID
    product_id: uuid.UUID
    product_name: str
    hsn_code: Optional[str]
    unit: str
    quantity: Decimal
    unit_price: Decimal
    gst_rate: Decimal
    taxable_amount: Decimal
    cgst_rate: Decimal
    sgst_rate: Decimal
    igst_rate: Decimal
    cgst_amount: Decimal
    sgst_amount: Decimal
    igst_amount: Decimal
    total_amount: Decimal

    class Config:
        from_attributes = True
        