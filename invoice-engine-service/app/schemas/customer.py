import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class CustomerCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None 
    gst_number: Optional[str] = None

class CustomerResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None 
    gst_number: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True