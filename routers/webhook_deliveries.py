from fastapi import APIRouter, Depends, HTTPException

from db import get_connection
from schemas.common import ErrorResponse
from schemas.webhook_deliveries import (
    WebhookDeliveryListResponse,
    WebhookDeliveryResponse,
)
from security import require_api_key

router = APIRouter(
    prefix="/webhook-deliveries",
    tags=["Webhook Deliveries"],
    dependencies=[Depends(require_api_key)],
)


def row_to_dict(row):
    return dict(row)


@router.get(
    "",
    response_model=WebhookDeliveryListResponse,
    summary="List webhook deliveries",
    description=(
        "Returns webhook delivery attempts recorded by the platform. "
        "Use this endpoint to review delivery status, response codes, "
        "event types, and delivery timing."
    ),
)
def list_webhook_deliveries():
    with get_connection() as conn:
        rows = conn.execute("""
            select
                partner_id,
                partner_name,
                delivery_id,
                webhook_id,
                event_type,
                status,
                response_code,
                request_payload,
                response_body,
                created_at
            from webhook_deliveries
            order by created_at desc
            """).fetchall()

    return {
        "total": len(rows),
        "items": [row_to_dict(row) for row in rows],
    }


@router.get(
    "/{delivery_id}",
    response_model=WebhookDeliveryResponse,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Webhook delivery not found",
        }
    },
    summary="Get webhook delivery",
    description=("Retrieves a single webhook delivery attempt by delivery ID."),
)
def get_webhook_delivery(delivery_id: str):
    with get_connection() as conn:
        row = conn.execute(
            """
            select
                partner_id,
                partner_name,
                delivery_id,
                webhook_id,
                event_type,
                status,
                response_code,
                request_payload,
                response_body,
                created_at
            from webhook_deliveries
            where delivery_id = %s
            """,
            (delivery_id,),
        ).fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Webhook delivery not found",
        )

    return row_to_dict(row)
