# chanakya_diligent

# Diligent – Exercise

This repo captures three deliverables:

1. Generate realistic synthetic e-commerce data as CSV files.
2. Load the CSVs into a relationally correct SQLite database.
3. Produce an analytics-ready SQL report that joins all tables.

Everything runs locally (or inside Cursor) with plain Python.

## Repository Layout

- `data/` – source CSVs (`users.csv`, `products.csv`, `orders.csv`, `order_items.csv`, `reviews.csv`)
- `generate_data.py` – regenerates the CSVs under `data/`
- `ingest_sqlite.py` – builds `diligent_ecom.db` and loads the CSVs with constraints
- `query.sql` – consolidated analytics query with joins, window aggregate, and order counts
- `run_report.py` – executes `query.sql` and prints a pretty pandas table

## Quick Start

```bash
python generate_data.py      # refresh synthetic CSVs in data/
python ingest_sqlite.py      # rebuild diligent_ecom.db with FK constraints
python run_report.py         # print consolidated report (uses query.sql)
```

`diligent_ecom.db` lives at the repo root so anyone cloning from GitHub can immediately run the report once the CSVs exist in `data/`.

## Prompts Used (for reference)

### Prompt 1 – Generate Synthetic Data
> You are Diligent’s AI Data Engineer working in Cursor IDE. Generate realistic, clean, relational synthetic e-commerce data for a production-like environment. Create exactly **5 CSV files** with schema and sample records that maintain relational integrity… (full instructions omitted for brevity).

### Prompt 2 – Ingest CSVs
> You are now Diligent’s Backend Data Engineer working in Cursor. Write Python code that creates `diligent_ecom.db`, defines the five tables with PK/FK constraints, loads the CSVs with sqlite3 + pandas, and prints row counts… (full constraints preserved above in project history).

### Prompt 3 – Analytics Query
> You are a Senior Data Analyst at Diligent. Generate a single SQL query for SQLite that joins multiple tables (minimum 3 joins) and outputs the consolidated report with totals, order counts, and optional ratings.


 
