"""LOAD - copy the raw JSON into the warehouse exactly as it is (no cleaning!)."""
from pathlib import Path

import duckdb

Path("warehouse").mkdir(exist_ok=True)
con = duckdb.connect("warehouse/shop.duckdb")

con.execute("CREATE SCHEMA IF NOT EXISTS raw")
con.execute("""
    CREATE OR REPLACE TABLE raw.orders AS
    SELECT * FROM read_json_auto('data/orders.json')
""")

rows = con.execute("SELECT COUNT(*) FROM raw.orders").fetchone()[0]
print(f"[load] {rows} raw orders loaded into raw.orders")
con.close()
