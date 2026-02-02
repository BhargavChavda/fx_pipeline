from extract import extract_rates
from transform import transform
from load import load_to_db
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parent.parent

def run_pipeline():
    RAW_PATH=extract_rates()
    df = transform(RAW_PATH)
    output_PROCESSED = RAW_PATH.name.replace("fx_raw_","fx_rates_").replace(".json",".parquet")
    OUTPUT_PATH = ROOT_PATH/"data"/"processed"/output_PROCESSED
    df.to_parquet(OUTPUT_PATH, index=False)
    load_to_db(df)
    
if __name__ == "__main__":
    run_pipeline()
