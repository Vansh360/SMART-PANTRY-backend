from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    password = Column(String, nullable=False)

    inventory = relationship("Inventory", back_populates="owner")

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, nullable=False)
    category = Column(String)
    quantity = Column(Float)
    unit = Column(String)
    purchase_date = Column(Date)
    expiry_date = Column(Date)
    barcode = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="inventory")