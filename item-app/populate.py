import requests
import time


BASE_URL = "http://flask:3001/"
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

while True:
    try:
        r = requests.get(BASE_URL+"health")
        break
    except Exception as e:
        print("api not up yet!")

for name in sample_items:
    r = requests.post(
        BASE_URL+"api/item",
        json={"name": name},
        headers=header,
    )

    print(r.status_code, r.json())

while True:
    time.sleep(5)
    r = requests.get(
        BASE_URL+"api/items",
        headers=header,
    )
