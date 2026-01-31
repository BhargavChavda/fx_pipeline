import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine,text

ROOT_PATH = Path(__file__).resolve().parent.parent
processed_path = ROOT_PATH/"data"/"processed"
latest_processed_path = sorted(processed_path.glob("fx_rates_*.parquet"))[-1]


def load_to_db():
    
    df = pd.read_parquet(latest_processed_path)
    
    DB_Name = 'etl_db'
    DB_User = 'bha'
    DB_Host = 'localhost'
    DB_Port = 5432
    
    engine = create_engine(f"postgresql://{DB_User}@{DB_Host}:{DB_Port}/{DB_Name}", echo=True)
    
    with engine.begin() as conn:
        df.to_sql(name="rates",con = conn, if_exists="append", method = "multi",index=False,chunksize=1000)
    
    conn.close()
    
load_to_db()
