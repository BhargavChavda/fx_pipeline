import json
from datetime import datetime,timezone
import requests
from config import rawd_dir, base_url

def extract_rates():
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
