import sqlite3
from pathlib import Path

import pandas as pd


def log(msg: str) -> None:
    print(f"[diligent] {msg}")


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    data_dir = base_dir / "data"
    db_path = base_dir / "diligent_ecom.db"

    csv_files = {
        "users": data_dir / "users.csv",
        "products": data_dir / "products.csv",
        "orders": data_dir / "orders.csv",
        "order_items": data_dir / "order_items.csv",
        "reviews": data_dir / "reviews.csv",
    }

    missing = [name for name, path in csv_files.items() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing CSV files: {', '.join(missing)}")

    conn = sqlite3.connect(db_path)
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        cur = conn.cursor()

        log("Dropping existing tables (if any)")
        cur.executescript(
            """
            DROP TABLE IF EXISTS reviews;
            DROP TABLE IF EXISTS order_items;
            DROP TABLE IF EXISTS orders;
            DROP TABLE IF EXISTS products;
            DROP TABLE IF EXISTS users;
            """
        )

        log("Creating tables with constraints")
        cur.executescript(
            """
            CREATE TABLE users (
                user_id     INTEGER PRIMARY KEY,
                name        TEXT NOT NULL,
                email       TEXT NOT NULL UNIQUE,
                created_at  TEXT NOT NULL,
                country     TEXT NOT NULL
            );

            CREATE TABLE products (
                product_id   INTEGER PRIMARY KEY,
                product_name TEXT NOT NULL,
                category     TEXT NOT NULL,
                price        REAL NOT NULL,
                stock        INTEGER NOT NULL
            );

            CREATE TABLE orders (
                order_id       INTEGER PRIMARY KEY,
                user_id        INTEGER NOT NULL,
                order_date     TEXT NOT NULL,
                total_amount   REAL NOT NULL,
                payment_status TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );

            CREATE TABLE order_items (
                item_id    INTEGER PRIMARY KEY,
                order_id   INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity   INTEGER NOT NULL,
                line_total REAL NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(order_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            );

            CREATE TABLE reviews (
                review_id  INTEGER PRIMARY KEY,
                user_id    INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                rating     INTEGER NOT NULL,
                review_text TEXT NOT NULL,
                created_at  TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            );
            """
        )

        log("Loading CSV files with pandas")
        dataframes = {name: pd.read_csv(path) for name, path in csv_files.items()}

        log("Writing data into SQLite")
        for table, df in dataframes.items():
            df.to_sql(table, conn, if_exists="append", index=False)
            log(f"Inserted {len(df):>4} rows into {table}")

        conn.commit()
        log("Validating row counts")
        for table in csv_files.keys():
            count = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            log(f"{table}: {count} rows")

    except Exception as exc:
        conn.rollback()
        log(f"Error: {exc}")
        raise
    finally:
        conn.close()
        log(f"Database ready at {db_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        log("Script failed")
        raise

