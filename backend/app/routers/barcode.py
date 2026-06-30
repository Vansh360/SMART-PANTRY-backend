from fastapi import APIRouter, HTTPException
import requests

router = APIRouter(
    prefix="/barcode",
    tags=["Barcode Scanner"]
)

@router.get("/{barcode}")
def scan_barcode(barcode: str):

    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"

    headers = {
        "User-Agent": "SmartPantry/1.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=10
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )

    data = response.json()

    if data["status"] == 0:
        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )

    product = data["product"]

    return {
        "barcode": barcode,
        "name": product.get("product_name"),
        "brand": product.get("brands"),
        "category": product.get("categories"),
        "image": product.get("image_url")
    }