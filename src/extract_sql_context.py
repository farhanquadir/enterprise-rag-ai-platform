from __future__ import annotations
from typing import Any
import duckdb
import pandas as pd

from src.config import WAREHOUSE_DB, EXPORTS_DIR
from src.utils import ensure_dir, save_pickle


def _safe_fetch(con: duckdb.DuckDBPyConnection, table: str) -> pd.DataFrame:
    try:
        return con.execute(f"select * from {table}").fetchdf()
    except Exception:
        return pd.DataFrame()


def extract_sql_context() -> list[dict[str, Any]]:
    con = duckdb.connect(str(WAREHOUSE_DB), read_only=True)
    try:
        tables = [t[0] for t in con.execute("show tables").fetchall()]
        print("Available tables:", tables)

        records: list[dict[str, Any]] = []

        # mart_monthly_revenue
        df = _safe_fetch(con, "mart_monthly_revenue")
        for _, row in df.iterrows():
            records.append(
                {
                    "id": f"mart_monthly_revenue::{row.get('year_month', 'unknown')}",
                    "text": (
                        f"In {row.get('year_month', 'unknown')}, revenue was "
                        f"{float(row.get('revenue', 0.0)):.2f} from "
                        f"{int(row.get('invoices', 0) or 0)} invoices and "
                        f"{int(row.get('order_lines', 0) or 0)} order lines."
                    ),
                    "source_type": "sql",
                    "table": "mart_monthly_revenue",
                    "entity_id": str(row.get("year_month", "unknown")),
                }
            )

        # mart_country_sales
        df = _safe_fetch(con, "mart_country_sales")
        for _, row in df.iterrows():
            records.append(
                {
                    "id": f"mart_country_sales::{row.get('country', 'Unknown')}",
                    "text": (
                        f"Country {row.get('country', 'Unknown')} generated "
                        f"{float(row.get('total_revenue', 0.0)):.2f} in revenue across "
                        f"{int(row.get('invoice_count', 0) or 0)} invoices and "
                        f"{int(row.get('customer_count', 0) or 0)} customers."
                    ),
                    "source_type": "sql",
                    "table": "mart_country_sales",
                    "entity_id": str(row.get("country", "Unknown")),
                }
            )

        # mart_top_customers
        df = _safe_fetch(con, "mart_top_customers")
        for _, row in df.iterrows():
            customer_key = str(row.get("customer_key", "UNKNOWN"))
            records.append(
                {
                    "id": f"mart_top_customers::{customer_key}",
                    "text": (
                        f"Top customer {customer_key} from {row.get('country', 'Unknown')} generated "
                        f"{float(row.get('total_revenue', 0.0)):.2f} in revenue across "
                        f"{int(row.get('invoice_count', 0) or 0)} invoices. "
                        f"The last order timestamp was {row.get('last_order_ts', 'unknown')}."
                    ),
                    "source_type": "sql",
                    "table": "mart_top_customers",
                    "entity_id": customer_key,
                }
            )

        # ai_customer_context
        df = _safe_fetch(con, "ai_customer_context")
        for _, row in df.iterrows():
            customer_key = str(row.get("customer_key", "UNKNOWN"))
            lifetime_value = float(row.get("lifetime_value", 0.0))
            if lifetime_value >= 50000:
                value_segment = "high_value"
            elif lifetime_value >= 10000:
                value_segment = "mid_value"
            else:
                value_segment = "low_value"

            records.append(
                {
                    "id": f"ai_customer_context::{customer_key}",
                    "text": (
                        f"Customer {customer_key} is a {value_segment} customer from "
                        f"{row.get('country', 'Unknown')}. Lifetime value is "
                        f"{lifetime_value:.2f} across {int(row.get('invoice_count', 0) or 0)} invoices. "
                        f"The last order timestamp was {row.get('last_order_ts', 'unknown')}. "
                        f"They purchased {int(row.get('distinct_products_purchased', 0) or 0)} distinct products."
                    ),
                    "source_type": "sql",
                    "table": "ai_customer_context",
                    "entity_id": customer_key,
                }
            )

        return records

    finally:
        con.close()


def main() -> None:
    records = extract_sql_context()
    ensure_dir(EXPORTS_DIR)
    out = EXPORTS_DIR / "sql_context.pkl"
    save_pickle(records, out)
    print(f"Extracted {len(records)} SQL records to {out}")


if __name__ == "__main__":
    main()