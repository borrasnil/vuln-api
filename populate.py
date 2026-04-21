import requests

BASE_URL = "http://localhost:3001/api/item"

sample_items = [
    "Sword",
    "Shield",
    "Potion",
    "Helmet",
    "Boots",
    "Ring",
    "Bow",
    "Arrow"
]

for name in sample_items:
    r = requests.post(
        BASE_URL,
        json={"name": name}
    )

    print(r.status_code, r.json())
