from fastapi import APIRouter, Depends, HTTPException, Query

from db import get_connection, q
from schemas.products import ProductListResponse, ProductResponse
from security import require_api_key

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    dependencies=[Depends(require_api_key)],
)

PRODUCT_COLUMNS = """
    product_id,
    feed_id,
    partner_id,
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
"""


def product_row_to_dict(row) -> dict:
    return {
        "product_id": row["product_id"],
        "feed_id": row["feed_id"],
        "partner_id": row["partner_id"],
        "partner_name": row["partner_name"],
        "sku": row["sku"],
        "product_name": row["product_name"],
        "description": row["description"],
        "brand": row["brand"],
        "category": row["category"],
        "price": row["price"],
        "currency": row["currency"],
        "availability": row["availability"],
        "created_at": row["created_at"],
    }


def product_rows_to_dicts(rows) -> list[dict]:
    return [product_row_to_dict(row) for row in rows]


@router.get(
    "",
    response_model=ProductListResponse,
    response_model_exclude_none=True,
    summary="List products",
    description=(
        "Retrieves products from the catalog with support for filtering, "
        "sorting, and pagination.\n\n"
        "Filtering options include:\n"
        "- partner_id\n"
        "- partner_name\n"
        "- feed_id\n"
        "- sku\n"
        "- brand\n"
        "- category\n"
        "- availability\n\n"
        "Pagination uses a cursor-based approach for efficient large dataset traversal.\n\n"
        "Results are returned by product ID in ascending order by default."
    ),
)
def list_products(
    partner_id: str | None = Query(default=None, description="Filter by partner ID"),
    partner_name: str | None = Query(
        default=None, description="Filter by partner name"
    ),
    feed_id: str | None = Query(default=None, description="Filter by feed ID"),
    sku: str | None = Query(default=None, description="Filter by SKU"),
    brand: str | None = Query(default=None, description="Filter by brand"),
    category: str | None = Query(default=None, description="Filter by category"),
    availability: str | None = Query(
        default=None, description="Filter by availability"
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Number of results to return (default: 10, max: 100)",
    ),
    sort_by: str = Query(
        default="product_id",
        description="Field to sort by: product_id, created_at, price, product_name, brand, or category",
    ),
    order: str = Query(default="asc", description="Sort direction: asc or desc"),
    cursor: str | None = Query(
        default=None,
        description="Cursor for pagination. Use the `next_cursor` value from the previous response.",
    ),
):
    allowed_sort_fields = {
        "product_id": "product_id",
        "price": "price",
        "product_name": "product_name",
        "brand": "brand",
        "category": "category",
        "created_at": "created_at",
    }

    allowed_order = {
        "asc": "ASC",
        "desc": "DESC",
    }

    if sort_by not in allowed_sort_fields:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort_by value. Allowed values: product_id, price, product_name, brand, category, created_at.",
        )

    if order not in allowed_order:
        raise HTTPException(
            status_code=400,
            detail="Invalid order value. Allowed values: asc, desc.",
        )

    if cursor and sort_by != "product_id":
        raise HTTPException(
            status_code=400,
            detail="Cursor pagination is currently supported only with sort_by=product_id.",
        )

    sort_column = allowed_sort_fields[sort_by]
    sort_direction = allowed_order[order]
    secondary_order = sort_direction if sort_by == "product_id" else "ASC"

    base_query = """
        FROM products
        WHERE 1=1
    """
    params = []

    if partner_id:
        base_query += " AND partner_id = ?"
        params.append(partner_id)

    if partner_name:
        base_query += " AND partner_name = ?"
        params.append(partner_name)

    if feed_id:
        base_query += " AND feed_id = ?"
        params.append(feed_id)

    if sku:
        base_query += " AND sku = ?"
        params.append(sku)

    if brand:
        base_query += " AND brand = ?"
        params.append(brand)

    if category:
        base_query += " AND category = ?"
        params.append(category)

    if availability:
        base_query += " AND availability = ?"
        params.append(availability)

    if cursor:
        cursor_operator = ">" if order == "asc" else "<"
        base_query += f" AND product_id {cursor_operator} ?"
        params.append(cursor)

    conn = get_connection()
    db_cursor = conn.cursor()

    try:
        count_query = q("SELECT COUNT(*) AS count " + base_query)

        count_row = db_cursor.execute(
            count_query,
            params,
        ).fetchone()

        total_count = count_row["count"] if count_row else 0

        data_query = q(f"""
            SELECT {PRODUCT_COLUMNS}
            {base_query}
            ORDER BY {sort_column} {sort_direction}, product_id {secondary_order}
            LIMIT ?
        """)

        rows = db_cursor.execute(
            data_query,
            params + [limit + 1],
        ).fetchall()

        has_more = len(rows) > limit
        rows = rows[:limit]

        items = product_rows_to_dicts(rows)

        response = {
            "count": total_count,
            "items": items,
        }

        if has_more and items:
            response["next_cursor"] = items[-1]["product_id"]

        return response

    finally:
        db_cursor.close()
        conn.close()


@router.get(
    "/by-feed/{feed_id}",
    response_model=ProductListResponse,
    response_model_exclude_none=True,
    summary="List products for a feed",
)
def list_products_by_feed(feed_id: str):
    conn = get_connection()
    db_cursor = conn.cursor()

    try:
        rows = db_cursor.execute(
            q(f"""
                SELECT {PRODUCT_COLUMNS}
                FROM products
                WHERE feed_id = ?
                ORDER BY product_id ASC
            """),
            (feed_id,),
        ).fetchall()

        items = product_rows_to_dicts(rows)

        return {
            "count": len(items),
            "items": items,
        }

    finally:
        db_cursor.close()
        conn.close()


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    response_model_exclude_none=True,
    summary="Get product by ID",
)
def get_product(product_id: str):
    conn = get_connection()
    db_cursor = conn.cursor()

    try:
        row = db_cursor.execute(
            q(f"""
                SELECT {PRODUCT_COLUMNS}
                FROM products
                WHERE product_id = ?
            """),
            (product_id,),
        ).fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found.",
            )

        return product_row_to_dict(row)

    finally:
        db_cursor.close()
        conn.close()
