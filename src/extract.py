import json
from datetime import datetime
from pathlib import Path

import requests


def extract_rates():
    base_url = "https://api.currencyfreaks.com/v2.0/rates/latest?apikey=REMOVED_API_KEY "
    rawd_dir = Path("data/raw")

    rawd_dir.mkdir(parents=True, exist_ok=True)

    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        fetch_time = datetime.utcnow().isoformat()
        data["fetch_time"] = fetch_time
        filename = f"fx_raw_{fetch_time.replace(':', '-')}.json"
        file_path = rawd_dir / filename
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        return file_path
