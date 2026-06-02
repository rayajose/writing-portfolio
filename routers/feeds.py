from __future__ import annotations

import csv
import io
import re

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)

from db import (
    DB_TYPE,
    get_connection,
    next_feed_id,
    next_submission_job_id,
    next_validation_job_id,
    q,
)
from etl.process_feed import process_feed
from schemas.common import ErrorResponse
from schemas.feeds import FeedCreateResponse, FeedResponse
from security import require_api_key
from services.s3_service import S3_RAW_BUCKET, upload_raw_feed
from utils import utc_now_iso

router = APIRouter(
    prefix="/feeds",
    tags=["Feeds"],
    dependencies=[Depends(require_api_key)],
)

FEED_COLUMNS = [
    "feed_id",
    "partner_id",
    "partner_name",
    "file_name",
    "content_type",
    "status",
    "uploaded_at",
    "validation_job_id",
    "validation_status",
    "validation_message",
    "raw_file_s3_key",
    "raw_file_bucket",
]

REQUIRED_FEED_FIELDS = {
    "sku",
    "product_name",
    "description",
    "brand",
    "category",
    "price",
    "currency",
    "availability",
}

ALLOWED_AVAILABILITY_VALUES = {
    "in_stock",
    "out_of_stock",
}


def clean_value(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value if value else None


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def feed_row_to_dict(row):
    return dict(row)


def update_feed_status(feed_id_value: str, status_value: str) -> None:
    with get_connection() as conn:
        conn.execute(
            q("""
                UPDATE feeds
                SET status = ?
                WHERE feed_id = ?
            """),
            (status_value, feed_id_value),
        )

        if DB_TYPE == "postgres":
            conn.commit()


def run_feed_etl(feed_id_value: str) -> None:
    try:
        process_feed(feed_id_value)
        update_feed_status(feed_id_value, "processed")
    except Exception:
        update_feed_status(feed_id_value, "failed")
        raise


@router.post(
    "/upload",
    response_model=FeedCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a product feed",
    description=(
        "Uploads a CSV product feed for a partner. The file is stored in S3, "
        "feed and job records are created, and ETL processing is started in the background.\n\n"
        "This operation triggers:\n"
        "- A submission job (JSxxxxx)\n"
        "- A validation job (JVxxxxx)\n"
        "- Background ETL processing\n\n"
        "Product ingestion uses idempotent upsert logic to prevent duplicate records."
    ),
    responses={
        400: {"model": ErrorResponse, "description": "Invalid CSV file"},
        401: {"description": "Unauthorized"},
    },
)
async def upload_feed(
    background_tasks: BackgroundTasks,
    partner_id: str = Form(...),
    file: UploadFile = File(...),
):
    allowed_types = {"text/csv", "text/plain", "application/vnd.ms-excel"}

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV uploads are supported at this time.",
        )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )

    try:
        decoded = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CSV file must be UTF-8 encoded.",
        )

    try:
        reader = csv.DictReader(io.StringIO(decoded))

        if reader.fieldnames is None:
            raise ValueError("CSV header row is missing.")

        normalized_headers = {header.strip() for header in reader.fieldnames if header}

        missing_headers = REQUIRED_FEED_FIELDS - normalized_headers

        if missing_headers:
            raise ValueError(
                f"Missing required CSV headers: {', '.join(sorted(missing_headers))}"
            )

        for row_number, row in enumerate(reader, start=2):

            for field in REQUIRED_FEED_FIELDS:
                value = (row.get(field) or "").strip()

                if not value:
                    raise ValueError(
                        f"Missing required value for '{field}' on row {row_number}."
                    )

            try:
                price = float(row["price"])
            except ValueError:
                raise ValueError(
                    f"Invalid price value '{row['price']}' on row {row_number}."
                )

            if price < 0:
                raise ValueError(f"Price cannot be negative on row {row_number}.")

            currency = row["currency"].strip().upper()

            if not re.fullmatch(r"[A-Z]{3}", currency):
                raise ValueError(f"Invalid currency '{currency}' on row {row_number}.")

            availability = (row.get("availability") or "").strip().lower()

            if availability not in ALLOWED_AVAILABILITY_VALUES:
                raise ValueError(
                    f"Invalid availability value '{availability}' "
                    f"on row {row_number}. "
                    "Allowed values: in_stock, out_of_stock."
                )

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid CSV file: {exc}",
        )

    with get_connection() as conn:
        partner = conn.execute(
            q("""
                SELECT partner_id, partner_name, status
                FROM partners
                WHERE partner_id = ?
            """),
            (partner_id,),
        ).fetchone()

        if not partner:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Partner not found.",
            )

        if partner["status"] != "active":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Partner is {partner['status']} and cannot submit feeds.",
            )

        partner_name = partner["partner_name"]

    feed_id = next_feed_id()
    submission_job_id = next_submission_job_id()
    validation_job_id = next_validation_job_id()
    now = utc_now_iso()

    original_filename = file.filename or "uploaded.csv"
    safe_partner_name = slugify(partner_name)

    raw_file_s3_key = (
        f"raw/partners/{safe_partner_name}/feeds/{feed_id}/{original_filename}"
    )

    try:
        upload_raw_feed(
            file_bytes=content,
            object_key=raw_file_s3_key,
            content_type=file.content_type or "text/csv",
        )
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )

    with get_connection() as conn:
        conn.execute(
            q("""
                INSERT INTO feeds (
                    feed_id,
                    partner_id,
                    partner_name,
                    file_name,
                    content_type,
                    status,
                    uploaded_at,
                    validation_job_id,
                    raw_file_s3_key,
                    raw_file_bucket
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """),
            (
                feed_id,
                partner_id,
                partner_name,
                original_filename,
                file.content_type or "text/csv",
                "processing",
                now,
                validation_job_id,
                raw_file_s3_key,
                S3_RAW_BUCKET,
            ),
        )

        conn.execute(
            q("""
                INSERT INTO jobs (
                    job_id,
                    job_type,
                    status,
                    created_at,
                    feed_id,
                    message
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """),
            (
                submission_job_id,
                "submission",
                "completed",
                now,
                feed_id,
                "Feed upload accepted.",
            ),
        )

        conn.execute(
            q("""
                INSERT INTO jobs (
                    job_id,
                    job_type,
                    status,
                    created_at,
                    feed_id,
                    message
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """),
            (
                validation_job_id,
                "validation",
                "queued",
                now,
                feed_id,
                "ETL processing queued.",
            ),
        )

        if DB_TYPE == "postgres":
            conn.commit()

    background_tasks.add_task(run_feed_etl, feed_id)

    return {
        "feed_id": feed_id,
        "job_id": submission_job_id,
        "status": "processing",
    }


@router.get(
    "/{feed_id}",
    response_model=FeedResponse,
    responses={404: {"model": ErrorResponse, "description": "Feed not found"}},
    summary="Retrieve feed details",
    description=(
        "Retrieves metadata for a specific feed, including upload status, "
        "associated validation job details, and raw file storage metadata."
    ),
)
async def read_feed(feed_id: str):
    with get_connection() as conn:
        feed = conn.execute(
            q("""
                SELECT
                    f.feed_id,
                    f.partner_id,
                    f.partner_name,
                    f.file_name,
                    f.content_type,
                    f.status,
                    f.uploaded_at,
                    f.validation_job_id,
                    j.status AS validation_status,
                    j.message AS validation_message,
                    f.raw_file_s3_key,
                    f.raw_file_bucket
                FROM feeds f
                LEFT JOIN jobs j
                    ON f.validation_job_id = j.job_id
                WHERE f.feed_id = ?
            """),
            (feed_id,),
        ).fetchone()

    if not feed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Feed {feed_id} not found.",
        )

    return feed_row_to_dict(feed)
