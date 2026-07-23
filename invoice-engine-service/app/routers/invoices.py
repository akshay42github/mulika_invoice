import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.invoice import Invoice
from app.models.customer import Customer
from app.schemas.invoice import InvoiceCreate, InvoiceResponse
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/invoices", tags=["invoices"])

@router.post("/", response_model=InvoiceResponse, status_code=201)
def create_invoice(
    payload: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    customer_data = payload.customer
    customer_id = customer_data.customer_id
    organization_id = current_user.get("organization_id")

    if customer_id:
        customer = db.query(Customer).filter(
            Customer.id == customer_id,
            Customer.organization_id == organization_id
        ).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
    else:
        customer = Customer(
            organization_id=organization_id,
            name=customer_data.customer_name,
            email=customer_data.customer_email,
            phone=customer_data.customer_phone,
            gst_number=customer_data.customer_gstin,
        )
        db.add(customer)
        db.flush()
        customer_id = customer.id

    invoice = Invoice(
        organization_id=organization_id,
        customer_id=customer_id,
        invoice_number=payload.invoice_number,
        invoice_date=payload.invoice_date,
        due_date=payload.due_date,
        notes=payload.notes,
        customer_name=customer_data.customer_name,
        customer_gstin=customer_data.customer_gstin,
        customer_email=customer_data.customer_email,
        customer_phone=customer_data.customer_phone,
        customer_address=customer_data.customer_address,
        customer_city=customer_data.customer_city,
        customer_state=customer_data.customer_state,
    )

    db.add(invoice)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=f"Invoice number '{payload.invoice_number}' already exists"
        )

    db.refresh(invoice)
    return invoice

@router.get("/", response_model=list[InvoiceResponse])
def list_invoices(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    organization_id = current_user.get("organization_id")
    return db.query(Invoice).filter(
        Invoice.organization_id == organization_id
    ).all()

@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(
    invoice_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    organization_id = current_user.get("organization_id")
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id,
        Invoice.organization_id == organization_id
    ).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice