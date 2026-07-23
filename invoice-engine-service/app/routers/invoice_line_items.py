import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.invoice_line_item import InvoiceLineItem
from app.models.invoice import Invoice
from app.models.product import Product
from app.schemas.invoice_line_item import LineItemCreate, LineItemResponse
from app.services.gst_engine import calculate_line_item
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/line-items", tags=["invoice-line-items"])

@router.post("/", response_model=LineItemResponse, status_code=201)
def add_line_item(
    payload: LineItemCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    organization_id = current_user.get("organization_id")

    # Verify invoice belongs to this organization
    invoice = db.query(Invoice).filter(
        Invoice.id == payload.invoice_id,
        Invoice.organization_id == organization_id
    ).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    # If product_id provided, verify it belongs to this organization
    if payload.product_id:
        product = db.query(Product).filter(
            Product.id == payload.product_id,
            Product.organization_id == organization_id
        ).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

    calculated = calculate_line_item(
        unit_price=payload.unit_price,
        quantity=payload.quantity,
        gst_rate=payload.gst_rate,
        is_interstate=payload.is_interstate
    )

    line_item = InvoiceLineItem(
        invoice_id=payload.invoice_id,
        product_id=payload.product_id,
        product_name=payload.product_name,
        hsn_code=payload.hsn_code,
        unit=payload.unit,
        unit_price=payload.unit_price,
        quantity=payload.quantity,
        gst_rate=payload.gst_rate,
        **calculated
    )

    db.add(line_item)

    invoice.subtotal = invoice.subtotal + calculated["taxable_amount"]
    invoice.cgst_amount = invoice.cgst_amount + calculated["cgst_amount"]
    invoice.sgst_amount = invoice.sgst_amount + calculated["sgst_amount"]
    invoice.igst_amount = invoice.igst_amount + calculated["igst_amount"]
    invoice.total_amount = invoice.total_amount + calculated["total_amount"]

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not add line item")

    db.refresh(line_item)
    return line_item

@router.get("/invoice/{invoice_id}", response_model=list[LineItemResponse])
def get_line_items(
    invoice_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    organization_id = current_user.get("organization_id")

    # Verify invoice belongs to this organization first
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id,
        Invoice.organization_id == organization_id
    ).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    return db.query(InvoiceLineItem).filter(
        InvoiceLineItem.invoice_id == invoice_id
    ).all()