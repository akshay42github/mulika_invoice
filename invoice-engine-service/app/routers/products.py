import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    organization_id = current_user.get("organization_id")
    product = Product(
    organization_id=organization_id,  # from token
    **payload.model_dump()
)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.get("/", response_model=list[ProductResponse])
def list_products(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    organization_id = current_user.get("organization_id")
    return db.query(Product).filter(
        Product.organization_id == organization_id
    ).all()

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    organization_id = current_user.get("organization_id")
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.organization_id == organization_id
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product