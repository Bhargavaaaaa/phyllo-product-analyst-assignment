import json
import os

BASE_PATH = "candidate-pack/responses"
FILES = ["orders_page1.json", "orders_page2.json"]

revenue = 0.0

for file_name in FILES:
    path = os.path.join(BASE_PATH, file_name)

    with open(path, "r") as f:
        response = json.load(f)

    for order in response["data"]:
        if order["status"].lower() not in ["cancelled", "refunded"]:
            revenue += float(order["total"])

print(f"Total Revenue: ${revenue:.2f}")
