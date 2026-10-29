"""Lab 1 - a small ETL pipeline.

Extract   : read raw orders from data/orders.json
Transform : flatten, clean and enrich them with Pandas
Load      : save one tidy table to output/order_items.parquet
"""
import json
from pathlib import Path

import pandas as pd

RAW_FILE = Path("data/orders.json")
OUTPUT_FILE = Path("output/order_items.parquet")


def extract(path):
    """E - read the raw JSON file into a list of Python dictionaries."""
    with open(path, encoding="utf-8") as f:
        orders = json.load(f)
    print(f"[extract]   read {len(orders)} orders from {path}")
    return orders


def transform(orders):
    """T - turn nested orders into one clean row per item."""
    df = pd.json_normalize(
        orders,
        record_path="items",
        meta=[
            "order_id", "order_date", "status", "payment_method",
            ["customer", "customer_id"], ["customer", "name"], ["customer", "city"],
        ],
    )
    df = df.rename(columns={
        "customer.customer_id": "customer_id",
        "customer.name": "customer_name",
        "customer.city": "city",
    })
    raw_rows = len(df)

    # 1. Remove duplicates: the same order was sent twice
    df = df.drop_duplicates(subset=["order_id", "sku"])

    # 2. Make status consistent: " Paid " -> "paid"
    df["status"] = df["status"].str.strip().str.lower()

    # 3. Fill in missing cities
    df["city"] = df["city"].fillna("Unknown")

    # 4. Fix data types
    df["quantity"] = pd.to_numeric(df["quantity"]).astype(int)
    df["unit_price"] = df["unit_price"].astype(float)
    df["order_date"] = pd.to_datetime(df["order_date"])

    # 5. Keep only real sales (cancelled orders earn no money)
    df = df[df["status"] != "cancelled"]

    # 6. Add useful new columns
    df["line_total"] = (df["quantity"] * df["unit_price"]).round(2)
    df["order_month"] = df["order_date"].dt.strftime("%Y-%m")

    columns = [
        "order_id", "order_date", "order_month", "status", "payment_method",
        "customer_id", "customer_name", "city",
        "sku", "product_name", "category", "quantity", "unit_price", "line_total",
    ]
    df = df[columns].sort_values(["order_date", "order_id", "sku"]).reset_index(drop=True)
    print(f"[transform] {raw_rows} raw item rows -> {len(df)} clean rows")
    return df


def load(df, path):
    """L - save the clean table as a Parquet file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
    print(f"[load]      wrote {len(df)} rows to {path}")


def main():
    orders = extract(RAW_FILE)
    clean = transform(orders)
    load(clean, OUTPUT_FILE)
    print("Pipeline finished successfully!")


if __name__ == "__main__":
    main()
