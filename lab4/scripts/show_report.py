"""Print the shop owner's report from the warehouse."""
import duckdb

con = duckdb.connect("warehouse/shop.duckdb", read_only=True)

print("Revenue by city and month (first 8 rows):")
con.sql("SELECT * FROM main.revenue_by_city_month LIMIT 8").show()

total, rows = con.execute(
    "SELECT SUM(line_total), COUNT(*) FROM main.fct_order_items"
).fetchone()
print(f"Total revenue: RM {total:,.2f} from {rows} order lines")
con.close()
