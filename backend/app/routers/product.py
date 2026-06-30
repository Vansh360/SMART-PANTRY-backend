from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Product
from app.schemas import ProductCreate, ProductResponse

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("/", response_model=ProductResponse)
def add_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(Product).filter(
        Product.barcode == product.barcode
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Barcode already exists"
        )

    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.get("/{barcode}", response_model=ProductResponse)
def get_product(
    barcode: str,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.barcode == barcode
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )

    return product
