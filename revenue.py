import json
import os

BASE_PATH = "candidate-pack/responses"
FILES = ["orders_page1.json", "orders_page2.json"]

revenue = 0.0
included_orders = []
excluded_orders = []

for file_name in FILES:
    path = os.path.join(BASE_PATH, file_name)

    with open(path, "r") as f:
        response = json.load(f)

    for order in response["data"]:
        status = order["status"].lower()
        total = order["total"]

        # Exclude refunded/cancelled orders
        if status in ["cancelled", "refunded"]:
            excluded_orders.append((order["id"], status, total))
            continue

        # Normalize money format
        if isinstance(total, int):
            total = total / 100

        revenue += total
        included_orders.append((order["id"], status, total))

print("Included Orders:")
for order in included_orders:
    print(order)

print("\nExcluded Orders:")
for order in excluded_orders:
    print(order)

print(f"\nTotal Revenue: ${revenue:.2f}")