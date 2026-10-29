"""LOAD - copy the raw files into the DuckDB warehouse, unchanged."""
from pathlib import Path

import duckdb

Path("warehouse").mkdir(exist_ok=True)
con = duckdb.connect("warehouse/taxi.duckdb")
con.execute("CREATE SCHEMA IF NOT EXISTS raw")

con.execute("""
    CREATE OR REPLACE TABLE raw.trips AS
    SELECT * FROM read_parquet('data/yellow_tripdata_*.parquet', union_by_name = true)
""")
con.execute("""
    CREATE OR REPLACE TABLE raw.zones AS
    SELECT * FROM read_csv_auto('data/taxi_zone_lookup.csv')
""")

for table in ["raw.trips", "raw.zones"]:
    rows = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"[load] {table}: {rows:,} rows")
con.close()
