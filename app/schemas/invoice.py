import uuid
from decimal import Decimal
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, field_validator
from app.models.invoice import InvoiceStatus

class InvoiceCreate(BaseModel):
    organization_id: uuid.UUID
    customer_id: uuid.UUID
    invoice_number: str
    invoice_date: date
    due_date: date
    notes: Optional[str] = None

    @field_validator("due_date")
    @classmethod
    def due_date_must_be_after_invoice_date(cls, v, info):
        if "invoice_date" in info.data and v < info.data["invoice_date"]:
            raise ValueError("Due date cannot be earlier than invoice date.")
        return v

class InvoiceResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    customer_id: uuid.UUID
    invoice_number: str
    status: InvoiceStatus
    invoice_date: date
    due_date: date
    subtotal: Decimal 
    cgst_amount: Decimal
    sgst_amount: Decimal
    igst_amount: Decimal
    total_amount: Decimal
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True