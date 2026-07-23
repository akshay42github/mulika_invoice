import uuid
from decimal import Decimal
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, field_validator, EmailStr
from app.models.invoice import InvoiceStatus

class InvoiceCustomer(BaseModel):
    """
    Customer details on the invoice form.
    Either customer_id (existing) or customer_name (new) must be provided.
    """
    customer_id: Optional[uuid.UUID] = None     # existing customer
    customer_name: str                           # always required — shown on invoice
    customer_gstin: Optional[str] = None
    customer_email: Optional[EmailStr] = None
    customer_phone: Optional[str] = None
    customer_address: Optional[str] = None
    customer_city: Optional[str] = None
    customer_state: Optional[str] = None

class InvoiceCreate(BaseModel):
    organization_id: uuid.UUID
    invoice_number: str
    invoice_date: date
    due_date: date
    notes: Optional[str] = None

    # Customer details inline — no pre-created customer needed
    customer: InvoiceCustomer

    @field_validator("due_date")
    @classmethod
    def due_date_must_be_after_invoice_date(cls, v, info):
        if "invoice_date" in info.data and v < info.data["invoice_date"]:
            raise ValueError("Due date cannot be before invoice date")
        return v

class InvoiceResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    invoice_number: str
    status: InvoiceStatus
    invoice_date: date
    due_date: date

    # Customer details stored on invoice
    customer_id: Optional[uuid.UUID]
    customer_name: str
    customer_gstin: Optional[str]
    customer_email: Optional[str]
    customer_phone: Optional[str]
    customer_address: Optional[str]
    customer_city: Optional[str]
    customer_state: Optional[str]

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