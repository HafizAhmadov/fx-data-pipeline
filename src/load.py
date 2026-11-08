import logging
import os

import duckdb

logger = logging.getLogger(__name__)

DB_PATH = "data/fx.duckdb"
TABLE = "raw.cbar_rates"

COLUMNS = [
    "rate_date",
    "currency_type",
    "currency_code",
    "currency_name",
    "nominal",
    "rate",
]

CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE} (
        rate_date     VARCHAR NOT NULL,
        currency_type VARCHAR,
        currency_code VARCHAR NOT NULL,
        currency_name VARCHAR,
        nominal       VARCHAR,
        rate          DOUBLE,
        loaded_at     TIMESTAMP DEFAULT current_timestamp,
        PRIMARY KEY (rate_date, currency_code)
    )
"""

UPSERT_SQL = f"""
    INSERT INTO {TABLE} ({", ".join(COLUMNS)})
    SELECT {", ".join(COLUMNS)} FROM new_rows
    ON CONFLICT (rate_date, currency_code) DO UPDATE SET
        currency_type = EXCLUDED.currency_type,
        currency_name = EXCLUDED.currency_name,
        nominal       = EXCLUDED.nominal,
        rate          = EXCLUDED.rate,
        loaded_at     = now()
"""


def load_raw(df):
    # 1. Check the input before touching the database
    if df.empty:
        raise ValueError("No rows to load. The parsed DataFrame is empty.")

    missing = set(COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"DataFrame is missing columns: {missing}")

    # 2. Load
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    con = duckdb.connect(DB_PATH)
    try:
        con.execute("CREATE SCHEMA IF NOT EXISTS raw")
        con.execute(CREATE_TABLE_SQL)
        con.register("new_rows", df[COLUMNS])
        con.execute(UPSERT_SQL)
        total = con.execute(f"SELECT COUNT(*) FROM {TABLE}").fetchone()[0]
    finally:
        con.close()

    logger.info("Upserted %d rows into %s (table total: %d)", len(df), TABLE, total)
    return total
