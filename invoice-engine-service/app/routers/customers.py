import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/customers", tags=["customers"])

@router.post("/", response_model=CustomerResponse, status_code=201)
def create_customer(payload: CustomerCreate, db: Session = Depends(get_db),
                    current_user: dict = Depends(get_current_user)):

    organization_id = current_user.get("organization_id")
    customer = Customer(
    organization_id=organization_id,  # from token
    name=payload.name,
    email=payload.email,
    phone=payload.phone,
    gst_number=payload.gst_number,
)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

@router.get("/", response_model=list[CustomerResponse])
def list_customers(db: Session = Depends(get_db),
                   current_user: dict = Depends(get_current_user)):
    
    organization_id = current_user.get("organization_id")
    return db.query(Customer).filter(
        Customer.organization_id == organization_id).all()

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: uuid.UUID, db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)):
    
    organization_id = current_user.get("organization_id")
    customer = db.query(Customer).filter(Customer.id == customer_id,
        Customer.organization_id == organization_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer