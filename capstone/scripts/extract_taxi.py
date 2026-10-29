"""EXTRACT - download NYC yellow-taxi trips and the taxi-zone lookup table."""
import urllib.request
from pathlib import Path

MONTHS = ["2024-01", "2024-02", "2024-03"]  # add more months for bonus points!
BASE = "https://d37ci6vzurychx.cloudfront.net"

data = Path("data")
data.mkdir(exist_ok=True)

files = {f"yellow_tripdata_{m}.parquet": f"{BASE}/trip-data/yellow_tripdata_{m}.parquet" for m in MONTHS}
files["taxi_zone_lookup.csv"] = f"{BASE}/misc/taxi_zone_lookup.csv"

for name, url in files.items():
    target = data / name
    if target.exists():
        print(f"[extract] {name} already downloaded - skipping")
        continue
    urllib.request.urlretrieve(url, target)
    print(f"[extract] downloaded {name} ({target.stat().st_size / 1e6:.1f} MB)")
