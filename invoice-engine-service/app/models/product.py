import uuid
from sqlalchemy import Column, String, DateTime, Numeric, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key= True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    hsn_code = Column(String, nullable=True)
    unit_price = Column(Numeric(10, 2), nullable=False)
    gst_rate = Column(Numeric(5, 2), nullable=False)
    unit = Column(String, nullable=False, default="piece")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
