import requests

url = "https://world.openfoodfacts.org/api/v0/product/8901030895482.json"

headers = {
    "User-Agent": "SmartPantry/1.0 (vansh@example.com)"
}

response = requests.get(
    url,
    headers=headers,
    timeout=10
)

print(response.status_code)
print(response.text[:500])