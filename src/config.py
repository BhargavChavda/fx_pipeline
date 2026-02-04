from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parent.parent
rawd_dir = ROOT_PATH/"data"/"raw"

DB_Name = 'etl_db'
DB_User = 'bha'
DB_Host = 'localhost'
DB_Port = 5432
