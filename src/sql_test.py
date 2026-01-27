from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql://bha@localhost:5432/etl_db",
    echo=True
)

with engine.begin() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS rates (
            date DATE,
            value NUMERIC
        )
    """))

rows = [
    {"date": "2026-01-01", "value": 1.23},
    {"date": "2026-01-02", "value": 1.25},
]

with engine.begin() as conn:
    conn.execute(
        text("INSERT INTO rates (date, value) VALUES (:date, :value)"),
        rows
    )