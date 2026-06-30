from pydantic import BaseModel, EmailStr
from datetime import date

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class ProductCreate(BaseModel):
    barcode: str
    product_name: str
    brand: str
    category: str
    image_url: str | None = None

class ProductResponse(ProductCreate):
    id: int

    class Config:
        from_attributes = True

class InventoryCreate(BaseModel):
    item_name: str
    category: str
    quantity: float
    unit: str
    purchase_date: date
    expiry_date: date
    barcode: str | None = None
    image_url: str | None = None

class InventoryResponse(BaseModel):
    id: int
    item_name: str
    category: str
    quantity: float
    unit: str
    purchase_date: date
    expiry_date: date
    barcode: str | None
    image_url: str | None

    class Config:
        from_attributes = True