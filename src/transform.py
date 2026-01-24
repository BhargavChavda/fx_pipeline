import json
from pathlib import Path
import pandas as pd
import pyarrow
import fastparquet

RAW_PATH = Path("/Users/lydia/Dev/Data Engineering/fx_pipeline/data/raw/fx_raw_2026-01-24T15-38-54.218882.json")
OUTPUT_PATH = Path("/Users/lydia/Dev/Data Engineering/fx_pipeline/data/processed/fx_rates.parquet")

REQUIRED_SCHEMA = {
    "date": "datetime64[us, UTC]",
    "base": "string",
    "target": "string",
    "rates": "float64",
    "fetch_time": "datetime64[us]",
}

def load_raw(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_json(path)


def normalize(df: pd.DataFrame) -> pd.DataFrame:
    # bring index (currency codes) into a column
    df = df.reset_index(drop=False)
    df = df.rename(columns={"index": "target"})

    # reorder columns intentionally
    col = "target"
    cols = list(df.columns)
    cols.remove(col)
    cols.insert(2, col)
    return df[cols]

def normalize_timestamps(df):
    for col in ["date", "fetch_time"]:
        df[col] = pd.to_datetime(df[col], utc=True)
        df[col] = df[col].dt.tz_localize(None)
    return df

def enforce_schema(df: pd.DataFrame) -> pd.DataFrame:
    expected_cols = list(REQUIRED_SCHEMA.keys())

    if list(df.columns) != expected_cols:
        raise ValueError(
            f"schema mismatch.\n"
            f"expected: {expected_cols}\n"
            f"got: {list(df.columns)}"
        )
    return df


def validate(df: pd.DataFrame) -> None:
    if df.isnull().any().any():
        raise ValueError("Null detected")

    if (df["rates"] <= 0).any():
        raise ValueError("Rates must be positive")

    if (df["date"] > df["fetch_time"]).any():
        raise ValueError("date cannot be greater than fetch_time")


def transform(path: Path) -> pd.DataFrame:
    df = load_raw(path)
    df = normalize(df)
    df = normalize_timestamps(df)
    df = enforce_schema(df)
    validate(df)
    return df


def load(df: pd.DataFrame, out_path: Path) -> None:
    df.to_parquet(out_path, index=False)


if __name__ == "__main__":
    df = transform(RAW_PATH)
    load(df, OUTPUT_PATH)