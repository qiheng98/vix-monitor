import json
import urllib.request
from datetime import datetime, timezone

SOURCES = {
    "vix": "https://historyofmarket.com/api/sp500/vix.json",
    "vxn": "https://historyofmarket.com/api/ndx/vxn.json",
}

def get_json(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "VIX-Monitor/1.0"}
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())

def normalize(data):
    if isinstance(data, list):
        series = data
        latest = series[-1] if series else None
        updated = None
    else:
        series = data.get("series", [])
        latest = data.get("latest")
        updated = data.get("updated")

        if not latest and series:
            latest = series[-1]

    return {
        "updated": updated,
        "latest": latest,
        "series": series
    }

for name, url in SOURCES.items():
    data = normalize(get_json(url))

    with open(f"data/{name}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(name.upper(), "latest:", data["latest"])

with open("data/updated-at.txt", "w") as f:
    f.write(datetime.now(timezone.utc).isoformat())

print("Data update completed.")
