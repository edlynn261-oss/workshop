import json
import pandas as pd

with open("data/orders.json", encoding="utf-8") as f:
    orders = json.load(f)

df = pd.json_normalize(
    orders,
    record_path="items",
    meta=[
        "order_id", "order_date", "status", "payment_method",
        ["customer", "customer_id"], ["customer", "name"], ["customer", "city"],
    ],
)

print("PROBLEM 1 - duplicate rows (the same order sent twice):")
print(df.duplicated(subset=["order_id", "sku"]).sum(), "duplicate item rows")

print("\nPROBLEM 2 - status values are written in different ways:")
print(df["status"].value_counts())

print("\nPROBLEM 3 - missing values in each column:")
print(df.isna().sum()[lambda counts: counts > 0])

print("\nPROBLEM 4 - quantity is sometimes a number, sometimes text:")
print(df["quantity"].map(type).value_counts())

print("\nPROBLEM 5 - order_date is plain text, not a real date:")
print(type(df.loc[0, "order_date"]), df.loc[0, "order_date"])
