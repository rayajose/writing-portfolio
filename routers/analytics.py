from fastapi import APIRouter, Depends, HTTPException, Query

from db import get_connection, q
from schemas.analytics import (
    RevenueShareResponse,
    SalesByPartnerResponse,
    SalesOverTimeResponse,
    TimeGrain,
)
from security import require_api_key

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
    dependencies=[Depends(require_api_key)],
)


@router.get(
    "/sales-by-partner",
    response_model=SalesByPartnerResponse,
    summary="Get sales by partner",
)
def get_sales_by_partner():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            q("""
                SELECT
                    partner_name,
                    COUNT(order_id)::int AS units_sold,
                    SUM(total_amount) AS total_sales
                FROM orders
                GROUP BY partner_name
                ORDER BY total_sales DESC
            """)
        )

        rows = cursor.fetchall()

        results = [
            {
                "partner_name": row["partner_name"],
                "units_sold": row["units_sold"],
                "total_sales": row["total_sales"],
            }
            for row in rows
        ]

        return {
            "analytics_type": "sales_by_partner",
            "results": results,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()


@router.get(
    "/sales-over-time",
    response_model=SalesOverTimeResponse,
    summary="Get sales over time",
)
def get_sales_over_time(
    grain: TimeGrain = Query(
        default=TimeGrain.daily,
        description="Aggregation level (daily or monthly)",
    )
):
    if grain == TimeGrain.monthly:
        date_expression = "DATE_TRUNC('month', created_at)::date"
    else:
        date_expression = "DATE(created_at)"

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            f"""
            SELECT
                {date_expression} AS sales_period,
                COUNT(order_id)::int AS units_sold,
                SUM(total_amount) AS total_sales
            FROM orders
            GROUP BY sales_period
            ORDER BY sales_period
            """
        )

        rows = cursor.fetchall()

        results = [
            {
                "sales_period": row["sales_period"],
                "units_sold": row["units_sold"],
                "total_sales": row["total_sales"],
            }
            for row in rows
        ]

        return {
            "analytics_type": "sales_over_time",
            "grain": grain.value,
            "results": results,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()


@router.get(
    "/revenue-share",
    response_model=RevenueShareResponse,
    summary="Get revenue share by partner",
)
def get_revenue_share():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            q("""
                SELECT
                    partner_name,
                    SUM(total_amount) AS total_revenue,
                    ROUND(
                        100.0 * SUM(total_amount)
                        / SUM(SUM(total_amount)) OVER (),
                        2
                    ) AS revenue_pct
                FROM orders
                GROUP BY partner_name
                ORDER BY total_revenue DESC
            """)
        )

        rows = cursor.fetchall()

        results = [
            {
                "partner_name": row["partner_name"],
                "total_revenue": row["total_revenue"],
                "revenue_pct": row["revenue_pct"],
            }
            for row in rows
        ]

        return {
            "analytics_type": "revenue_share",
            "results": results,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()