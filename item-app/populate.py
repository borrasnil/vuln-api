import requests


BASE_URL = "http://localhost:3001/api/item"
API_KEY = "$uP3r_$tR0nG_p4$$w0rd_M0nl4u2026"

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

header = {
    'Authorization': f'Bearer {API_KEY}'
}

for name in sample_items:
    r = requests.post(
        BASE_URL,
        json={"name": name},
        headers=header,
    )

    print(r.status_code, r.json())


