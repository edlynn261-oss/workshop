import json

# Open the file and turn the JSON text into Python objects
with open("data/orders.json", encoding="utf-8") as f:
    orders = json.load(f)

print("Python type of the whole file:", type(orders))
print("Number of orders:", len(orders))

first = orders[0]
print("\nKeys in one order:", list(first.keys()))
print("Order ID:", first["order_id"])
print("Customer:", first["customer"]["name"], "from", first["customer"]["city"])
print("Number of items:", len(first["items"]))

print("\nThe first item of the first order:")
print(first["items"][0])
