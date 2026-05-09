from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from db import (
    get_connection,
    next_order_id,
    next_order_item_id_with_conn,
    q,
)
from schemas.orders import (
    OrderCreateRequest,
    OrderListResponse,
    OrderResponse,
)
from security import require_api_key

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    dependencies=[Depends(require_api_key)],
)


def _get_order_with_items(conn, order_id: str) -> dict | None:
    cur = conn.cursor()

    try:
        order = cur.execute(
            q("""
                SELECT
                    order_id,
                    partner_name,
                    customer_reference,
                    status,
                    total_amount,
                    currency,
                    created_at,
                    updated_at
                FROM orders
                WHERE order_id = ?
            """),
            (order_id,),
        ).fetchone()

        if order is None:
            return None

        items = cur.execute(
            q("""
                SELECT
                    order_item_id,
                    product_id,
                    sku,
                    product_name,
                    quantity,
                    unit_price,
                    line_total
                FROM order_items
                WHERE order_id = ?
                ORDER BY order_item_id ASC
            """),
            (order_id,),
        ).fetchall()

        return {
            "order_id": order["order_id"],
            "partner_name": order["partner_name"],
            "customer_reference": order["customer_reference"],
            "status": order["status"],
            "total_amount": order["total_amount"],
            "currency": order["currency"],
            "items": [
                {
                    "order_item_id": item["order_item_id"],
                    "product_id": item["product_id"],
                    "sku": item["sku"],
                    "product_name": item["product_name"],
                    "quantity": item["quantity"],
                    "unit_price": item["unit_price"],
                    "line_total": item["line_total"],
                }
                for item in items
            ],
        }

    finally:
        cur.close()


@router.post("", response_model=OrderResponse, status_code=201)
def create_order(request: OrderCreateRequest):
    if not request.items:
        raise HTTPException(
            status_code=400,
            detail="Order must contain at least one item.",
        )

    conn = get_connection()
    cur = conn.cursor()

    try:
        order_id = next_order_id()
        currency = "USD"
        order_items = []

        # Create the parent order first so order_items can reference it.
        cur.execute(
            q("""
                INSERT INTO orders (
                    order_id,
                    partner_name,
                    customer_reference,
                    status,
                    currency
                )
                VALUES (?, ?, ?, ?, ?)
            """),
            (
                order_id,
                request.partner_name,
                request.customer_reference,
                "created",
                currency,
            ),
        )

        total_amount = 0.0

        for request_item in request.items:
            product = cur.execute(
                q("""
                    SELECT
                        product_id,
                        sku,
                        product_name,
                        price,
                        currency,
                        availability
                    FROM products
                    WHERE product_id = ?
                """),
                (request_item.product_id,),
            ).fetchone()

            if product is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Product not found: {request_item.product_id}",
                )

            if product["availability"] != "in_stock":
                raise HTTPException(
                    status_code=409,
                    detail=f"Product is not available: {request_item.product_id}",
                )

            unit_price = float(product["price"] or 0)
            line_total = unit_price * request_item.quantity
            total_amount += line_total

            order_item_id = next_order_item_id_with_conn(conn)

            cur.execute(
                q("""
                    INSERT INTO order_items (
                        order_item_id,
                        order_id,
                        product_id,
                        sku,
                        product_name,
                        quantity,
                        unit_price,
                        line_total
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """),
                (
                    order_item_id,
                    order_id,
                    product["product_id"],
                    product["sku"],
                    product["product_name"],
                    request_item.quantity,
                    unit_price,
                    line_total,
                ),
            )

            order_items.append({
                "order_item_id": order_item_id,
                "product_id": product["product_id"],
                "sku": product["sku"],
                "product_name": product["product_name"],
                "quantity": request_item.quantity,
                "unit_price": unit_price,
                "line_total": line_total,
            })

        cur.execute(
            q("""
                UPDATE orders
                SET total_amount = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE order_id = ?
            """),
            (
                total_amount,
                order_id,
            ),
        )

        conn.commit()

        return _get_order_with_items(conn, order_id) or {
            "order_id": order_id,
            "partner_name": request.partner_name,
            "customer_reference": request.customer_reference,
            "status": "created",
            "total_amount": total_amount,
            "currency": currency,
            "items": order_items,
        }

    except HTTPException:
        conn.rollback()
        raise

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()


@router.get("", response_model=OrderListResponse)
def list_orders():
    conn = get_connection()
    cur = conn.cursor()

    try:
        rows = cur.execute(
            q("""
                SELECT order_id
                FROM orders
                ORDER BY created_at DESC, order_id DESC
            """)
        ).fetchall()

        orders = []

        for row in rows:
            order = _get_order_with_items(conn, row["order_id"])
            if order is not None:
                orders.append(order)

        return {
            "count": len(orders),
            "items": orders,
        }

    finally:
        cur.close()
        conn.close()


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: str):
    conn = get_connection()

    try:
        order = _get_order_with_items(conn, order_id)

        if order is None:
            raise HTTPException(
                status_code=404,
                detail=f"Order not found: {order_id}",
            )

        return order

    finally:
        conn.close()