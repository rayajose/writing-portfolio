from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()

# SQLite config
DB_PATH = Path(__file__).resolve().parent / "partner_catalog.db"

# PostgreSQL config
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "partner_catalog")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")


def q(sql: str) -> str:
    """
    Convert generic ? placeholders to database-specific placeholders.

    SQLite uses ? placeholders.
    PostgreSQL uses %s placeholders.
    """
    if DB_TYPE == "postgres":
        return sql.replace("?", "%s")

    return sql


def get_connection():
    """
    Return a database connection for the configured database type.
    """
    if DB_TYPE == "sqlite":
        import sqlite3

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    if DB_TYPE == "postgres":
        import psycopg
        from psycopg.rows import dict_row

        return psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            row_factory=dict_row,
        )

    raise ValueError(f"Unsupported DB_TYPE: {DB_TYPE}")


def init_db() -> None:
    """
    Create database tables and indexes if they do not already exist.
    """
    with get_connection() as conn:
        cur = conn.cursor()

        try:
            cur.execute(q("""
                CREATE TABLE IF NOT EXISTS id_counters (
                    prefix TEXT PRIMARY KEY,
                    last_value INTEGER NOT NULL
                )
            """))

            cur.execute(q("""
                CREATE TABLE IF NOT EXISTS feeds (
                    feed_id TEXT PRIMARY KEY,
                    partner_name TEXT NOT NULL,
                    file_name TEXT NOT NULL,
                    content_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    uploaded_at TEXT NOT NULL,
                    validation_job_id TEXT
                )
            """))

            cur.execute(q("""
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    job_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    feed_id TEXT NOT NULL,
                    message TEXT,
                    FOREIGN KEY (feed_id) REFERENCES feeds(feed_id)
                )
            """))

            product_price_type = "DOUBLE PRECISION" if DB_TYPE == "postgres" else "REAL"

            cur.execute(q(f"""
                CREATE TABLE IF NOT EXISTS products (
                    product_id TEXT PRIMARY KEY,
                    feed_id TEXT NOT NULL,
                    partner_name TEXT NOT NULL,
                    sku TEXT,
                    product_name TEXT NOT NULL,
                    description TEXT,
                    brand TEXT,
                    category TEXT,
                    price {product_price_type},
                    currency TEXT,
                    availability TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (feed_id) REFERENCES feeds(feed_id)
                )
            """))

            cur.execute(q("""
                CREATE UNIQUE INDEX IF NOT EXISTS idx_products_partner_sku
                ON products (partner_name, sku)
            """))

            amount_type = "DOUBLE PRECISION" if DB_TYPE == "postgres" else "REAL"

            cur.execute(q(f"""
                CREATE TABLE IF NOT EXISTS orders (
                    order_id TEXT PRIMARY KEY,
                    partner_name TEXT NOT NULL,
                    customer_reference TEXT,
                    customer_id TEXT,
                    shipping_address_id TEXT,
                    status TEXT NOT NULL DEFAULT 'created',
                    total_amount {amount_type},
                    currency TEXT DEFAULT 'USD',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                    FOREIGN KEY (shipping_address_id) REFERENCES customer_addresses(address_id)
            )
            """))

            cur.execute(q("""
                CREATE TABLE IF NOT EXISTS customers (
                    customer_id TEXT PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email_encrypted TEXT NOT NULL,
                    phone_encrypted TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """))

            cur.execute(q("""
                CREATE TABLE IF NOT EXISTS customer_addresses (
                    address_id TEXT PRIMARY KEY,
                    customer_id TEXT NOT NULL,
                    address_line1_encrypted TEXT NOT NULL,
                    address_line2_encrypted TEXT,
                    city TEXT NOT NULL,
                    state TEXT NOT NULL,
                    postal_code_encrypted TEXT NOT NULL,
                    country TEXT NOT NULL DEFAULT 'US',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (customer_id)
                        REFERENCES customers(customer_id)
                )
            """))

            cur.execute(q(f"""
                CREATE TABLE IF NOT EXISTS order_items (
                    order_item_id TEXT PRIMARY KEY,
                    order_id TEXT NOT NULL,
                    product_id TEXT NOT NULL,
                    sku TEXT,
                    product_name TEXT,
                    quantity INTEGER NOT NULL,
                    unit_price {amount_type},
                    line_total {amount_type},
                    FOREIGN KEY (order_id) REFERENCES orders(order_id),
                    FOREIGN KEY (product_id) REFERENCES products(product_id)
                )
            """))

            cur.execute(q("""
                CREATE TABLE IF NOT EXISTS fulfillment_jobs (
                    job_id TEXT PRIMARY KEY,
                    order_id TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'queued',
                    message TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (order_id) REFERENCES orders(order_id)
                )
            """))

            cur.execute(q("""
                CREATE TABLE IF NOT EXISTS shipments (
                    shipment_id TEXT PRIMARY KEY,
                    order_id TEXT NOT NULL,
                    job_id TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending',
                    carrier TEXT,
                    tracking_number TEXT,
                    shipped_at TEXT,
                    delivered_at TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (order_id) REFERENCES orders(order_id),
                    FOREIGN KEY (job_id) REFERENCES fulfillment_jobs(job_id)
                )
            """))

            conn.commit()

        finally:
            cur.close()


def _next_id_with_conn(conn, prefix: str) -> str:
    """
    Generate the next ID for a prefix using the shared id_counters table.

    Examples:
        FD00001
        JS00001
        JV00001
        PR00001
        OR00001
        OI00001
        JF00001
        SH00001
    """
    cur = conn.cursor()

    try:
        cur.execute(
            q("SELECT last_value FROM id_counters WHERE prefix = ?"),
            (prefix,),
        )
        row = cur.fetchone()

        if row is None:
            next_value = 1
            cur.execute(
                q("INSERT INTO id_counters (prefix, last_value) VALUES (?, ?)"),
                (prefix, next_value),
            )
        else:
            last_value = row["last_value"]
            next_value = last_value + 1
            cur.execute(
                q("UPDATE id_counters SET last_value = ? WHERE prefix = ?"),
                (next_value, prefix),
            )

        return f"{prefix}{next_value:05d}"

    finally:
        cur.close()


def _next_id(prefix: str) -> str:
    """
    Generate and commit the next ID using a standalone connection.
    """
    with get_connection() as conn:
        next_id = _next_id_with_conn(conn, prefix)
        conn.commit()
        return next_id


def next_feed_id() -> str:
    return _next_id("FD")


def next_submission_job_id() -> str:
    return _next_id("JS")


def next_validation_job_id() -> str:
    return _next_id("JV")


def next_product_id() -> str:
    return _next_id("PR")


def next_product_id_with_conn(conn) -> str:
    return _next_id_with_conn(conn, "PR")


def next_order_id() -> str:
    return _next_id("OR")


def next_customer_id() -> str:
    return _next_id("CU")


def next_address_id_with_conn(conn) -> str:
    return _next_id_with_conn(conn, "AD")


def next_order_item_id_with_conn(conn) -> str:
    return _next_id_with_conn(conn, "OI")


def next_fulfillment_job_id_with_conn(conn) -> str:
    return _next_id_with_conn(conn, "JF")


def next_shipment_id_with_conn(conn) -> str:
    return _next_id_with_conn(conn, "SH")
