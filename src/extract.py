import json
from datetime import datetime,timezone
from pathlib import Path
import requests
import os

API_KEY = os.getenv("CURRENCYFREAKS_API_KEY")
if not API_KEY:
    raise RuntimeError("CURRENCYFREAKS_API_KEY environment variable not set")

def extract_rates():
    base_url = f"https://api.currencyfreaks.com/v2.0/rates/latest?apikey={API_KEY}"
    ROOT_PATH = Path(__file__).resolve().parent.parent
    rawd_dir = ROOT_PATH/"data"/"raw"

    rawd_dir.mkdir(parents=True, exist_ok=True)

    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        fetch_time = datetime.now(timezone.utc).isoformat()
        data["fetch_time"] = fetch_time
        filename = f"fx_raw_{fetch_time.replace(':', '-')}.json"
        file_path = rawd_dir / filename
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        return file_path

extract_rates()
