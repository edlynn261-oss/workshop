"""EXTRACT - download today's raw orders from the shop's system."""
import urllib.request
from pathlib import Path

SOURCE_URL = "https://dataengineeringfc.lovable.app/workshop-data/orders.json"
TARGET = Path("data/orders.json")

TARGET.parent.mkdir(parents=True, exist_ok=True)
# Some web servers refuse Python's default "user agent", so we say who we are
request = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "workshop-lab/1.0"})
with urllib.request.urlopen(request) as response:
    TARGET.write_bytes(response.read())
size_kb = TARGET.stat().st_size / 1024
print(f"[extract] downloaded {size_kb:.0f} KB to {TARGET}")
