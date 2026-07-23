from sqlalchemy import Column, String, Numeric, DateTime, Integer, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class InvoiceLineItem(Base):
    __tablename__ = "invoice_line_items"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    invoice_id = Column(UUID(as_uuid=True), nullable=False)
    product_id = Column(UUID(as_uuid=True), nullable=True)

    #copied from product table at the time of invoice creation or sale
    product_name = Column(String, nullable=False)
    hsn_code = Column(String, nullable=True)
    unit = Column(String, nullable=False)

    #quantity and price
    quantity = Column(Numeric(10, 2), nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)

    #GST fields
    gst_rate = Column(Numeric(5, 2), nullable=False)
    cgst_rate = Column(Numeric(5, 2), nullable=False, default=0)
    sgst_rate = Column(Numeric(5, 2), nullable=False, default=0)
    igst_rate = Column(Numeric(5, 2), nullable=False, default=0)

    # Calculated amt
    taxable_amount = Column(Numeric(12, 2), nullable=False)
    cgst_amount = Column(Numeric(12, 2), nullable=False, default=0)
    sgst_amount = Column(Numeric(12, 2), nullable=False, default=0)
    igst_amount = Column(Numeric(12, 2), nullable=False, default=0)
    total_amount = Column(Numeric(12, 2), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
