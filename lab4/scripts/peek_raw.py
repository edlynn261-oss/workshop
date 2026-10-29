"""Look inside the warehouse: the raw table is still messy (that's OK in ELT)."""
import duckdb

con = duckdb.connect("warehouse/shop.duckdb", read_only=True)
con.sql("""
    SELECT status, COUNT(*) AS orders
    FROM raw.orders
    GROUP BY status
    ORDER BY orders DESC
""").show()
con.close()
