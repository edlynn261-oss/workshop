import json
import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)

with open("data/orders.json", encoding="utf-8") as f:
    orders = json.load(f)

# Flatten: one row per item, with the order's details copied onto each row
df = pd.json_normalize(
    orders,
    record_path="items",
    meta=[
        "order_id", "order_date", "status", "payment_method",
        ["customer", "customer_id"], ["customer", "name"], ["customer", "city"],
    ],
)

print("Rows and columns:", df.shape)
print("\nColumn names:")
print(list(df.columns))
print("\nFirst 5 rows:")
print(df[["order_id", "status", "customer.city", "product_name", "quantity", "unit_price"]].head())
