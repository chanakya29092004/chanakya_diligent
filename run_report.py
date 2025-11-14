import sqlite3
from pathlib import Path

import pandas as pd

QUERY_PATH = Path(__file__).with_name("query.sql")

def main():
    if not QUERY_PATH.exists():
        raise FileNotFoundError(f"Missing SQL file: {QUERY_PATH}")
    query = QUERY_PATH.read_text(encoding="utf-8")

    conn = sqlite3.connect("diligent_ecom.db")
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(query).fetchall()
        df = pd.DataFrame([dict(row) for row in rows])
        if df.empty:
            print("No results found.")
        else:
            pd.set_option("display.max_rows", None)
            pd.set_option("display.width", 0)
            print(df.to_string(index=False))
    finally:
        conn.close()

if __name__ == "__main__":
    main()