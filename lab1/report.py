import pandas as pd

df = pd.read_parquet("output/order_items.parquet")

print("Total revenue: RM", round(df["line_total"].sum(), 2))
print("Number of orders:", df["order_id"].nunique())

print("\nRevenue by city (RM):")
print(df.groupby("city")["line_total"].sum().sort_values(ascending=False).round(2))

print("\nRevenue by month (RM):")
print(df.groupby("order_month")["line_total"].sum().round(2))

print("\nTop 5 products by units sold:")
print(df.groupby("product_name")["quantity"].sum().sort_values(ascending=False).head(5))
