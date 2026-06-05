import json
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from db import get_connection, next_webhook_id_with_conn, q
from schemas.webhooks import (
    WebhookCreateRequest,
    WebhookCreateResponse,
    WebhookUpdateRequest,
    WebhookResponse,
)
from webhooks.security import generate_webhook_secret
from webhooks.validation import validate_webhook_events

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.post("", response_model=WebhookCreateResponse, status_code=201)
def create_webhook_subscription(request: WebhookCreateRequest):
    validate_webhook_events(request.events)

    now = datetime.now(timezone.utc).isoformat()
    secret = generate_webhook_secret()

    with get_connection() as conn:
        cur = conn.cursor()

        try:
            cur.execute(
                q("SELECT partner_id FROM partners WHERE partner_id = ?"),
                (request.partner_id,),
            )
            partner = cur.fetchone()

            if partner is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Partner not found: {request.partner_id}",
                )

            webhook_id = next_webhook_id_with_conn(conn)

            cur.execute(
                q("""
                    INSERT INTO webhook_subscriptions (
                        webhook_id,
                        partner_id,
                        url,
                        events,
                        secret,
                        status,
                        created_at,
                        updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """),
                (
                    webhook_id,
                    request.partner_id,
                    str(request.url),
                    json.dumps(request.events),
                    secret,
                    "active",
                    now,
                    now,
                ),
            )

            conn.commit()

            return {
                "webhook_id": webhook_id,
                "partner_id": request.partner_id,
                "url": str(request.url),
                "events": request.events,
                "secret": secret,
                "status": "active",
                "created_at": now,
                "updated_at": now,
            }

        finally:
            cur.close()


@router.get("", response_model=list[WebhookResponse])
def list_webhook_subscriptions():
    with get_connection() as conn:
        cur = conn.cursor()

        try:
            cur.execute("""
                SELECT
                    webhook_id,
                    partner_id,
                    url,
                    events,
                    status,
                    created_at,
                    updated_at
                FROM webhook_subscriptions
                ORDER BY created_at DESC
            """)
            rows = cur.fetchall()

            return [
                {
                    **row,
                    "events": (
                        row["events"]
                        if isinstance(row["events"], list)
                        else json.loads(row["events"])
                    ),
                    "created_at": str(row["created_at"]),
                    "updated_at": str(row["updated_at"]),
                }
                for row in rows
            ]

        finally:
            cur.close()


@router.get("/{webhook_id}", response_model=WebhookResponse)
def get_webhook_subscription(webhook_id: str):
    with get_connection() as conn:
        cur = conn.cursor()

        try:
            cur.execute(
                q("""
                    SELECT
                        webhook_id,
                        partner_id,
                        url,
                        events,
                        status,
                        created_at,
                        updated_at
                    FROM webhook_subscriptions
                    WHERE webhook_id = ?
                """),
                (webhook_id,),
            )
            row = cur.fetchone()

            if row is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Webhook subscription not found: {webhook_id}",
                )

            return {
                **row,
                "events": (
                    row["events"]
                    if isinstance(row["events"], list)
                    else json.loads(row["events"])
                ),
                "created_at": str(row["created_at"]),
                "updated_at": str(row["updated_at"]),
            }

        finally:
            cur.close()


@router.patch("/{webhook_id}", response_model=WebhookResponse)
def update_webhook_subscription(
    webhook_id: str,
    request: WebhookUpdateRequest,
):
    with get_connection() as conn:
        cur = conn.cursor()

        try:
            cur.execute(
                q("""
                    SELECT *
                    FROM webhook_subscriptions
                    WHERE webhook_id = ?
                """),
                (webhook_id,),
            )
            existing = cur.fetchone()

            if existing is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Webhook subscription not found: {webhook_id}",
                )

            if request.events is not None:
                validate_webhook_events(request.events)

            updated_url = (
                str(request.url) if request.url is not None else existing["url"]
            )

            updated_events = (
                request.events
                if request.events is not None
                else (
                    existing["events"]
                    if isinstance(existing["events"], list)
                    else json.loads(existing["events"])
                )
            )

            updated_status = (
                request.status if request.status is not None else existing["status"]
            )

            updated_at = datetime.now(timezone.utc).isoformat()

            cur.execute(
                q("""
                    UPDATE webhook_subscriptions
                    SET
                        url = ?,
                        events = ?,
                        status = ?,
                        updated_at = ?
                    WHERE webhook_id = ?
                """),
                (
                    updated_url,
                    json.dumps(updated_events),
                    updated_status,
                    updated_at,
                    webhook_id,
                ),
            )

            conn.commit()

            return {
                "webhook_id": existing["webhook_id"],
                "partner_id": existing["partner_id"],
                "url": updated_url,
                "events": updated_events,
                "status": updated_status,
                "created_at": str(existing["created_at"]),
                "updated_at": updated_at,
            }

        finally:
            cur.close()
