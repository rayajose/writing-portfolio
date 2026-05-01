from fastapi import APIRouter, HTTPException, Query, Depends
from security import require_api_key
from db import get_connection
from schemas.analytics import SalesByPartnerResponse, SalesOverTimeResponse, TimeGrain, RevenueShareResponse


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
    dependencies=[Depends(require_api_key)]
)


def rows_to_dicts(cursor, rows):
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in rows]


@router.get(
    "/sales-by-partner",
    response_model=SalesByPartnerResponse,
    summary="Get sales by partner",
    response_description="Aggregated sales metrics grouped by partner",
    description=(
        "Returns aggregated sales metrics grouped by partner. "
        "Use this endpoint to compare partner-level revenue and unit volume."
    ),
    responses={
        200: {
            "description": "Sales totals grouped by partner were returned successfully."
        },
        500: {
            "description": "An internal server error occurred while retrieving analytics data."
        },
    },
)
def get_sales_by_partner():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                partner_name,
                SUM(quantity)::int AS units_sold,
                SUM(total_amount) AS total_sales
            FROM orders
            GROUP BY partner_name
            ORDER BY total_sales DESC;
            """
        )

        rows = cursor.fetchall()
        results = rows_to_dicts(cursor, rows)

        cursor.close()
        conn.close()

        return {
            "analytics_type": "sales_by_partner",
            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/sales-over-time",
    response_model=SalesOverTimeResponse,
    summary="Get sales over time",
    description=(
        "Returns aggregated sales metrics over time. "
        "Use the grain query parameter to group results by day or month."
    ),
    responses={
        200: {
            "description": "Sales totals over time were returned successfully."
        },
        400: {
            "description": "Invalid grain value. Supported values are daily and monthly."
        },
        500: {
            "description": "An internal server error occurred while retrieving analytics data."
        },
    },
)
def get_sales_over_time(
    grain: TimeGrain = Query(
        default=TimeGrain.daily,
        description="Aggregation level (daily or monthly)",
    )
):
    if grain == TimeGrain.monthly:
        date_expression = "DATE_TRUNC('month', order_date)::date"
    else:
        date_expression = "order_date"

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            f"""
            SELECT
                {date_expression} AS sales_period,
                SUM(quantity)::int AS units_sold,
                SUM(total_amount) AS total_sales
            FROM orders
            GROUP BY sales_period
            ORDER BY sales_period;
            """
        )

        rows = cursor.fetchall()
        results = rows_to_dicts(cursor, rows)

        cursor.close()
        conn.close()

        return {
            "analytics_type": "sales_over_time",
            "grain": grain.value,
            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/revenue-share",
    response_model=RevenueShareResponse,
    summary="Get revenue share by partner",
    response_description="Percentage of total revenue contributed by each partner",
    description=(
        "Returns each partner's contribution to total revenue as a percentage. "
        "This endpoint demonstrates use of SQL window functions for analytics."
    ),
    responses={
        200: {
            "description": "Revenue share calculated successfully."
        },
        500: {
            "description": "An internal server error occurred while retrieving analytics data."
        },
    },
)
def get_revenue_share():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                partner_name,
                SUM(total_amount) AS total_revenue,
                ROUND(
                    100.0 * SUM(total_amount) / SUM(SUM(total_amount)) OVER (),
                    2
                ) AS revenue_pct
            FROM orders
            GROUP BY partner_name
            ORDER BY total_revenue DESC;
            """
        )

        rows = cursor.fetchall()
        results = rows_to_dicts(cursor, rows)

        cursor.close()
        conn.close()

        return {
            "analytics_type": "revenue_share",
            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))