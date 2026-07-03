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

router = APIRouter(prefix="/line-items", tags=["invoice-line-items"])

@router.post("/", response_model=LineItemResponse, status_code=201)
def add_line_item(payload: LineItemCreate, db: Session = Depends(get_db)):

    # verify if invoice exists

    invoice = db.query(Invoice).filter(Invoice.id == payload.invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found.")
    
    # verify if product exists

    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    
    # run gst calculation

    calculated = calculate_line_item(
        unit_price=product.unit_price,
        quantity=payload.quantity,
        gst_rate=product.gst_rate,
        is_interstate=payload.is_interstate
    )

    # create line item with copied product data + calculated amounts

    line_item = InvoiceLineItem(
        invoice_id=payload.invoice_id,
        product_id=payload.product_id,
        product_name=product.name,
        hsn_code=product.hsn_code,
        unit=product.unit,
        unit_price=product.unit_price,
        quantity=payload.quantity,
        gst_rate=product.gst_rate,
        **calculated
    )

    db.add(line_item)

    # update invoice total 

    invoice.subtotal = (invoice.subtotal or 0) + calculated["taxable_amount"]
    invoice.cgst_amount = (invoice.cgst_amount or 0) + calculated["cgst_amount"]
    invoice.sgst_amount = (invoice.sgst_amount or 0) + calculated["sgst_amount"]
    invoice.igst_amount = (invoice.igst_amount or 0) + calculated["igst_amount"]
    invoice.total_amount = (invoice.total_amount or 0) + calculated["total_amount"]

    try: 
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not add line item")
    

    db.refresh(line_item)
    return line_item

@router.get("/invoice/{invoice_id}", response_model=list[LineItemResponse])
def get_line_items(invoice_id: uuid.UUID, db: Session = Depends(get_db)):
    return db.query(InvoiceLineItem).filter(
        InvoiceLineItem.invoice_id == invoice_id
    ).all()

