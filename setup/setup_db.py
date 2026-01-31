from sqlalchemy import create_engine,text
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DB_Name = 'etl_db'
DB_User = 'bha'
DB_Host = 'localhost'
DB_Port = 5432

def create_db_if_not_exists():
    conn = psycopg2.connect(
        dbname = 'postgres',
        user = DB_User,
        host = DB_Host,
        port = DB_Port,
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("""
            SELECT 1 FROM pg_database where datname = %s
        """, (DB_Name,),)
    exists = cur.fetchone()
    if not exists:
        cur.execute(f"CREATE DATABASE {DB_Name}")
    cur.close()
    conn.close()

def create_table():
    
    engine = create_engine(f"postgresql://{DB_User}@{DB_Host}:{DB_Port}/{DB_Name}", echo=True)
    
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS rates(
                date TIMESTAMPTZ NOT NULL,
                base TEXT NOT NULL,
                target TEXT NOT NULL,
                rates DOUBLE PRECISION NOT NULL,
                fetch_time TIMESTAMP NOT NULL,
                PRIMARY KEY (date,base,target)
            )
            """))

if __name__ == "__main__":
    create_db_if_not_exists()
    create_table()
