from __future__ import annotations

import csv
import io

import boto3

from db import DB_TYPE, get_connection, next_product_id_with_conn, q
from services.s3_service import S3_RAW_BUCKET
from utils import utc_now_iso


def clean_value(value: str | None) -> str | None:
    if value is None:
        return None

    value = str(value).strip()
    return value if value else None


def parse_price(value: str | None) -> float | None:
    cleaned = clean_value(value)

    if cleaned is None:
        return None

    cleaned = cleaned.replace("$", "").replace(",", "")

    try:
        return float(cleaned)
    except ValueError:
        return None


def values_match(existing_value, incoming_value) -> bool:
    if existing_value is None and incoming_value is None:
        return True

    if isinstance(existing_value, float) or isinstance(incoming_value, float):
        try:
            return float(existing_value) == float(incoming_value)
        except (TypeError, ValueError):
            return False

    return clean_value(existing_value) == clean_value(incoming_value)


def update_validation_job(feed_id_value: str, status: str, message: str) -> None:
    with get_connection() as conn:
        conn.execute(
            q("""
                UPDATE jobs
                SET status = ?, message = ?
                WHERE feed_id = ?
                  AND job_type = 'validation'
            """),
            (status, message, feed_id_value),
        )

        if DB_TYPE == "postgres":
            conn.commit()


def get_feed(feed_id_value: str) -> dict:
    with get_connection() as conn:
        feed = conn.execute(
            q("""
                SELECT
                    feed_id,
                    partner_name,
                    raw_file_s3_key,
                    raw_file_bucket
                FROM feeds
                WHERE feed_id = ?
            """),
            (feed_id_value,),
        ).fetchone()

    if not feed:
        raise ValueError(f"Feed {feed_id_value} not found.")

    if DB_TYPE == "sqlite":
        feed = dict(feed)
    else:
        feed = {
            "feed_id": feed[0],
            "partner_name": feed[1],
            "raw_file_s3_key": feed[2],
            "raw_file_bucket": feed[3],
        }

    if not feed["raw_file_s3_key"]:
        raise ValueError(f"Feed {feed_id_value} does not have an S3 raw file key.")

    return feed


def read_csv_from_s3(bucket: str, object_key: str) -> list[dict]:
    s3_client = boto3.client("s3")

    response = s3_client.get_object(
        Bucket=bucket,
        Key=object_key,
    )

    content = response["Body"].read().decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(content))

    return list(reader)


def row_has_changed(existing_product: dict | tuple, incoming_product: dict) -> bool:
    if DB_TYPE == "sqlite":
        existing_values = {
            "product_name": existing_product["product_name"],
            "description": existing_product["description"],
            "brand": existing_product["brand"],
            "category": existing_product["category"],
            "price": existing_product["price"],
            "currency": existing_product["currency"],
            "availability": existing_product["availability"],
        }
    else:
        existing_values = {
            "product_name": existing_product[1],
            "description": existing_product[2],
            "brand": existing_product[3],
            "category": existing_product[4],
            "price": existing_product[5],
            "currency": existing_product[6],
            "availability": existing_product[7],
        }

    for field_name, incoming_value in incoming_product.items():
        if not values_match(existing_values[field_name], incoming_value):
            return True

    return False


def load_products(feed: dict, rows: list[dict]) -> dict:
    now = utc_now_iso()

    summary = {
        "inserted": 0,
        "updated": 0,
        "unchanged": 0,
        "skipped": 0,
    }

    with get_connection() as conn:
        for row in rows:
            sku = clean_value(row.get("sku"))
            product_name = clean_value(row.get("product_name"))

            if not sku or not product_name:
                summary["skipped"] += 1
                continue

            incoming_product = {
                "product_name": product_name,
                "description": clean_value(row.get("description")),
                "brand": clean_value(row.get("brand")),
                "category": clean_value(row.get("category")),
                "price": parse_price(row.get("price")),
                "currency": clean_value(row.get("currency")),
                "availability": clean_value(row.get("availability")),
            }

            existing_product = conn.execute(
                q("""
                    SELECT
                        product_id,
                        product_name,
                        description,
                        brand,
                        category,
                        price,
                        currency,
                        availability
                    FROM products
                    WHERE partner_name = ?
                      AND sku = ?
                """),
                (
                    feed["partner_name"],
                    sku,
                ),
            ).fetchone()

            if existing_product:
                product_id = (
                    existing_product["product_id"]
                    if DB_TYPE == "sqlite"
                    else existing_product[0]
                )

                if not row_has_changed(existing_product, incoming_product):
                    summary["unchanged"] += 1
                    continue

                conn.execute(
                    q("""
                        UPDATE products
                        SET
                            feed_id = ?,
                            product_name = ?,
                            description = ?,
                            brand = ?,
                            category = ?,
                            price = ?,
                            currency = ?,
                            availability = ?
                        WHERE product_id = ?
                    """),
                    (
                        feed["feed_id"],
                        incoming_product["product_name"],
                        incoming_product["description"],
                        incoming_product["brand"],
                        incoming_product["category"],
                        incoming_product["price"],
                        incoming_product["currency"],
                        incoming_product["availability"],
                        product_id,
                    ),
                )

                summary["updated"] += 1

            else:
                product_id = next_product_id_with_conn(conn)

                conn.execute(
                    q("""
                        INSERT INTO products (
                            product_id,
                            feed_id,
                            partner_name,
                            sku,
                            product_name,
                            description,
                            brand,
                            category,
                            price,
                            currency,
                            availability,
                            created_at
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """),
                    (
                        product_id,
                        feed["feed_id"],
                        feed["partner_name"],
                        sku,
                        incoming_product["product_name"],
                        incoming_product["description"],
                        incoming_product["brand"],
                        incoming_product["category"],
                        incoming_product["price"],
                        incoming_product["currency"],
                        incoming_product["availability"],
                        now,
                    ),
                )

                summary["inserted"] += 1

        if DB_TYPE == "postgres":
            conn.commit()

    return summary


def process_feed(feed_id_value: str) -> None:
    try:
        update_validation_job(
            feed_id_value=feed_id_value,
            status="running",
            message="ETL processing started.",
        )

        feed = get_feed(feed_id_value)
        bucket = feed["raw_file_bucket"] or S3_RAW_BUCKET

        rows = read_csv_from_s3(
            bucket=bucket,
            object_key=feed["raw_file_s3_key"],
        )

        summary = load_products(feed, rows)

        products_processed = (
            summary["inserted"]
            + summary["updated"]
            + summary["unchanged"]
        )

        message = (
            "ETL processing completed. "
            f"Products processed: {products_processed}. "
            f"Inserted: {summary['inserted']}. "
            f"Updated: {summary['updated']}. "
            f"Unchanged: {summary['unchanged']}. "
            f"Skipped: {summary['skipped']}."
        )

        update_validation_job(
            feed_id_value=feed_id_value,
            status="completed",
            message=message,
        )

        print(f"Processed feed {feed_id_value}")
        print(f"Products processed: {products_processed}")
        print(f"Products inserted: {summary['inserted']}")
        print(f"Products updated: {summary['updated']}")
        print(f"Products unchanged: {summary['unchanged']}")
        print(f"Products skipped: {summary['skipped']}")

    except Exception as exc:
        update_validation_job(
            feed_id_value=feed_id_value,
            status="failed",
            message=f"ETL processing failed: {exc}",
        )
        raise


if __name__ == "__main__":
    requested_feed_id = input("Enter feed ID to process: ").strip()
    process_feed(requested_feed_id)