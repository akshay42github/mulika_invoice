import uuid
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, field_validator

VALID_GST_RATES = [Decimal("0"), Decimal("5"), Decimal("12"), 
                   Decimal("18"), Decimal("28")]

class LineItemCreate(BaseModel):
    invoice_id: uuid.UUID
    quantity: Decimal
    is_interstate: bool = False

    # Optional — if provided, prefills name/hsn/gst from catalog
    product_id: Optional[uuid.UUID] = None

    # Always required on the form — editable regardless of product_id
    product_name: str
    hsn_code: Optional[str] = None
    unit: str = "piece"
    unit_price: Decimal        # negotiated price — never auto-locked
    gst_rate: Decimal          # editable — even if from catalog

    @field_validator("unit_price")
    @classmethod
    def validate_unit_price(cls, v):
        if v <= 0:
            raise ValueError("Unit price must be greater than zero")
        return v

    @field_validator("gst_rate")
    @classmethod
    def validate_gst_rate(cls, v):
        if v not in VALID_GST_RATES:
            raise ValueError("GST rate must be 0, 5, 12, 18, or 28 percent")
        return v

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be greater than zero")
        return v
    
class LineItemResponse(BaseModel):
    id: uuid.UUID
    invoice_id: uuid.UUID
    product_id: Optional[uuid.UUID] = None
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
