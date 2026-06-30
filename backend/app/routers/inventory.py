from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app.database import get_db
from app.models import Inventory
from app.schemas import InventoryCreate, InventoryResponse
from app.auth import get_current_user
from sqlalchemy import or_

from datetime import date, timedelta


router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

@router.get("/", response_model=list[InventoryResponse])
def get_inventory(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_id = get_current_user(token)
    return (
        db.query(Inventory)
        .filter(Inventory.user_id == user_id)
        .all()
    )


@router.post("/", response_model=InventoryResponse)
def add_inventory(
    item: InventoryCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_id = get_current_user(token)
    inventory = Inventory(
        item_name=item.item_name,
        category=item.category,
        quantity=item.quantity,
        unit=item.unit,
        purchase_date=item.purchase_date,
        expiry_date=item.expiry_date,
        barcode=item.barcode,
        image_url=item.image_url,
        user_id=user_id
    )
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory


@router.put("/{item_id}", response_model=InventoryResponse)
def update_inventory(
    item_id: int,
    updated_item: InventoryCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    user_id = get_current_user(token)

    item = db.query(Inventory).filter(
        Inventory.id == item_id,
        Inventory.user_id == user_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.item_name = updated_item.item_name
    item.category = updated_item.category
    item.quantity = updated_item.quantity
    item.unit = updated_item.unit
    item.purchase_date = updated_item.purchase_date
    item.expiry_date = updated_item.expiry_date
    item.barcode = updated_item.barcode
    item.image_url = updated_item.image_url

    db.commit()
    db.refresh(item)

    return item


@router.delete("/{item_id}")
def delete_inventory(
    item_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    user_id = get_current_user(token)

    item = db.query(Inventory).filter(
        Inventory.id == item_id,
        Inventory.user_id == user_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()

    return {"message": "Item Deleted Successfully"}


@router.get("/search/{keyword}")
def search_inventory(
    keyword: str,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    user_id = get_current_user(token)

    items = db.query(Inventory).filter(
        Inventory.user_id == user_id,
        or_(
            Inventory.item_name.ilike(f"%{keyword}%"),
            Inventory.category.ilike(f"%{keyword}%")
        )
    ).all()

    return items

@router.get("/expiring")
def expiring_items(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    user_id = get_current_user(token)

    today = date.today()
    next_week = today + timedelta(days=7)

    items = db.query(Inventory).filter(
        Inventory.user_id == user_id,
        Inventory.expiry_date >= today,
        Inventory.expiry_date <= next_week
    ).all()

    return items


@router.get("/low-stock")
def low_stock(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    user_id = get_current_user(token)

    items = db.query(Inventory).filter(
        Inventory.user_id == user_id,
        Inventory.quantity <= 2
    ).all()

    return items

