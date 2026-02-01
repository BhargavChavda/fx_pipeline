# What is it?
fx_pipeline is a personal data engineering project which implements a daily FX (foreign exchange) snapshot pipeline built from first principles with a focus on core principles like correctness, idempotency, etc.

## What does it do?
On each run:
- Fetches latest FX rates from CurrencyFreaksAPI
- Writes the raw data into disk
- Transforms nested JSON to a well defined schema
- Inserts the transformed schema into PostgreSQL
- Saves the transformed data as a parquet file in ./data/processed
- Supports safe reruns with no risk of duplicating and corrupting data.

This pipeline was designed with reliability in mind meaning you could run this with your eyes closed and it would run or fail loudly if something's wrong.

## Data Model:
### Dataset grain:
One row of the table rates represents FX rate for (base currency, target currency) on a specific date. Base currency here being USD.

*This is a daily snapshot dataset, not intraday (yet)*

### Table Schema:
```sql
CREATE TABLE rates (
    date        TIMESTAMPTZ NOT NULL,
    base        TEXT        NOT NULL,
    target      TEXT        NOT NULL,
    rates       DOUBLE PRECISION NOT NULL,
    fetch_time  TIMESTAMP   NOT NULL,
    PRIMARY KEY (date, base, target)
);
```
## Rerun and Idempotency:
This pipeline was designed to be append only. Here the primary key is (date, base, target) where inserts use `ON CONFLICT (date,base,target) DO NOTHING` this make sure reruns on the same day doesn't overwrite the date and duplicates are never created.

## Project Structure:
```
fx_pipeline
├── data
│   ├── raw
│   └── processed
├── setup
│   └── setup_db.py
├── src
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── main.py
├── .env
├── requirements.txt
└── README.md
```

## Where it fails:
- Missing API Key = extract.py fail
- Invalid/Null data = transform.py fail
- DB Unavailable = load.py fails (unless setup.py is run)
- Duplicate inserts = ignored by load.py

## Secrets:
- API keys are read from environment variable in the .env file
- No secrets are hardcoded
- local .env is ignored by git

 ## How to run? (Locally)
1) One-Time Setup
```bash
python setup/setup.py
```
2) Set env variables
```bash
export CURRENCYFREAKS_API_KEY=your_api_key
```
Or use .env
3) Run the pipeline in this order:
- src/extract.py
- src/transform.py
- src/load.py

## Next Steps:
TBD