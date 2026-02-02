import pandas as pd
from sqlalchemy import create_engine,text

def load_to_db(dataframe: pd.DataFrame):
    
    # df = pd.read_parquet(latest_processed_path)
    
    DB_Name = 'etl_db'
    DB_User = 'bha'
    DB_Host = 'localhost'
    DB_Port = 5432
    
    engine = create_engine(f"postgresql://{DB_User}@{DB_Host}:{DB_Port}/{DB_Name}", echo=True)
    
    with engine.begin() as conn:
        records = dataframe.to_dict(orient="records")
        conn.execute(text("""INSERT INTO rates (date, base, target, rates, fetch_time)
                VALUES (:date, :base, :target, :rates, :fetch_time)
                ON CONFLICT (date, base, target) DO NOTHING"""), records)
