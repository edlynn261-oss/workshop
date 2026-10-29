from pathlib import Path
import pandas as pd

df = pd.read_parquet("output/order_items.parquet")

# Save the same table in two more formats so we can compare
df.to_csv("output/order_items.csv", index=False)
df.to_json("output/order_items.json", orient="records", indent=2, date_format="iso")

print("File sizes for the SAME data:")
for name in ["order_items.json", "order_items.csv", "order_items.parquet"]:
    size_kb = Path("output", name).stat().st_size / 1024
    print(f"  {name:22} {size_kb:7.1f} KB")

print("\nData types after reading the CSV back:")
print(pd.read_csv("output/order_items.csv").dtypes[["order_date", "quantity", "line_total"]])

print("\nData types after reading the Parquet back:")
print(pd.read_parquet("output/order_items.parquet").dtypes[["order_date", "quantity", "line_total"]])
