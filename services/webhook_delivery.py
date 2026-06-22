from __future__ import annotations

import json
from datetime import date, datetime
from decimal import Decimal
from typing import Any

import requests

from db import get_connection, q


def make_json_safe(value):
    if isinstance(value, Decimal):
        return float(value)

    if isinstance(value, (datetime, date)):
        return value.isoformat()

    if isinstance(value, dict):
        return {key: make_json_safe(item) for key, item in value.items()}

    if isinstance(value, list):
        return [make_json_safe(item) for item in value]

    return value


def next_delivery_id(conn) -> str:
    row = conn.execute(
        q("""
            UPDATE id_counters
            SET last_value = last_value + 1
            WHERE prefix = ?
            RETURNING last_value
        """),
        ("WD",),
    ).fetchone()

    if row is None:
        conn.execute(
            q("""
                INSERT INTO id_counters (prefix, last_value)
                VALUES (?, ?)
            """),
            ("WD", 1),
        )
        return "WD00001"

    return f"WD{row['last_value']:05d}"


def record_webhook_delivery(
    *,
    webhook_id: str,
    partner_id: str | None,
    partner_name: str | None,
    event_type: str,
    status: str,
    response_code: int | None,
    request_payload: dict[str, Any],
    response_body: str | None,
) -> None:
    safe_payload = make_json_safe(request_payload)

    with get_connection() as conn:
        delivery_id = next_delivery_id(conn)

        conn.execute(
            q("""
                INSERT INTO webhook_deliveries (
                    delivery_id,
                    webhook_id,
                    partner_id,
                    partner_name,
                    event_type,
                    status,
                    response_code,
                    request_payload,
                    response_body
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """),
            (
                delivery_id,
                webhook_id,
                partner_id,
                partner_name,
                event_type,
                status,
                response_code,
                json.dumps(safe_payload),
                response_body,
            ),
        )


def deliver_webhook(
    *,
    webhook: dict[str, Any],
    event_type: str,
    payload: dict[str, Any],
) -> None:
    webhook_id = webhook["webhook_id"]
    partner_id = webhook.get("partner_id")
    partner_name = webhook.get("partner_name")
    url = webhook["url"]

    safe_payload = make_json_safe(payload)

    try:
        response = requests.post(
            url,
            json=safe_payload,
            timeout=10,
        )

        status = "succeeded" if 200 <= response.status_code < 300 else "failed"

        record_webhook_delivery(
            webhook_id=webhook_id,
            partner_id=partner_id,
            partner_name=partner_name,
            event_type=event_type,
            status=status,
            response_code=response.status_code,
            request_payload=safe_payload,
            response_body=response.text[:2000],
        )

    except requests.RequestException as exc:
        record_webhook_delivery(
            webhook_id=webhook_id,
            partner_id=partner_id,
            partner_name=partner_name,
            event_type=event_type,
            status="failed",
            response_code=None,
            request_payload=safe_payload,
            response_body=str(exc),
        )
