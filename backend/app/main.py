from fastapi import FastAPI

from app.database import Base, engine
import app.models

from app.routers.user import router as user_router
from app.routers.inventory import router as inventory_router
from app.routers.barcode import router as barcode_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Pantry API"
)

app.include_router(user_router)
app.include_router(inventory_router)
app.include_router(barcode_router)

@app.get("/")
def home():
    return {
        "message": "Smart Pantry API Running"
    }


app.include_router(barcode_router)