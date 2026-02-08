from pathlib import Path
from dotenv import load_dotenv
import os

# Paths
# ROOT_PATH = Path(__file__).resolve().parent.parent
rawd_dir = Path("/data/raw")
processed_dir = Path("/data/processed")

# API base url
load_dotenv()
API_KEY = os.getenv("CURRENCYFREAKS_API_KEY")
if not API_KEY:
    raise RuntimeError("CURRENCYFREAKS_API_KEY environment variable not set")

base_url = f"https://api.currencyfreaks.com/v2.0/rates/latest?apikey={API_KEY}"

# DB Creds
DB_Name = 'etl_db'
DB_User = 'bha'
DB_Host = 'host.docker.internal'
DB_Port = 5432
