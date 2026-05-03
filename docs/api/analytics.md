# Analytics Layer

This page explains how the Partner Catalog API supports analytical queries across products, partners, and time.

The analytics layer extends the platform beyond ingestion by enabling aggregated insights through SQL queries and API endpoints.

---

## Overview

The analytics layer enables:

- Product performance analysis
- Partner performance analysis
- Revenue distribution insights
- Time-based trend analysis

Example questions:

- Which partners generate the most revenue?
- Which products drive the highest sales?
- How does revenue vary over time?
- What percentage of revenue does each partner contribute?

---

## Data model

The analytics layer introduces an `orders` table that acts as a fact table.

```text
orders
  product_id → products.product_id
  partner_name
  order_date
  quantity
  unit_price
  total_amount
```

---

## Orders table

```sql
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    product_id TEXT NOT NULL,
    partner_name TEXT NOT NULL,
    order_date DATE NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0),
    total_amount NUMERIC(12, 2) GENERATED ALWAYS AS (quantity * unit_price) STORED,

    CONSTRAINT fk_orders_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);
```

---

## Dimensional model

The analytics layer uses a simplified dimensional model:

| Type      | Table / Field  | Purpose                   |
|-----------|----------------|---------------------------|
| Fact      | `orders`       | Stores sales transactions |
| Dimension | `products`     | Product attributes        |
| Dimension | `partner_name` | Partner grouping          |
| Dimension | `order_date`   | Time-based analysis       |

---

## Dataset characteristics

The sample dataset includes multiple partner types:

- High-volume / low-price — Microbrews Brothers
- High-value electronics — RayTech Corp., Tronics
- Media retail — Cid's Vintage Records
- Luxury goods — Joyeria Reina

This enables comparison across:

- Revenue vs volume
- Product categories
- Partner business models

---

## Example queries

### Sales by partner

```sql
SELECT
    partner_name,
    SUM(quantity) AS units_sold,
    SUM(total_amount) AS total_sales
FROM orders
GROUP BY partner_name
ORDER BY total_sales DESC;
```

---

### Sales over time

```sql
SELECT
    order_date,
    SUM(quantity) AS units_sold,
    SUM(total_amount) AS total_sales
FROM orders
GROUP BY order_date
ORDER BY order_date;
```

---

### Monthly aggregation

```sql
SELECT
    DATE_TRUNC('month', order_date)::date AS sales_month,
    SUM(quantity),
    SUM(total_amount)
FROM orders
GROUP BY sales_month;
```

---

### Top products

```sql
SELECT
    p.product_name,
    SUM(o.quantity) AS units_sold,
    SUM(o.total_amount) AS total_sales
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_sales DESC
LIMIT 5;
```

---

### Revenue share

```sql
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
```

---

## Analytics API

The analytics layer exposes read-only endpoints for aggregated insights.

### GET /analytics/sales-by-partner

Use this endpoint to retrieve total units and revenue by partner.

---

### GET /analytics/sales-over-time

Use this endpoint to retrieve time-based sales metrics.

Supports:

- `daily`
- `monthly`

---

### GET /analytics/top-products

Use this endpoint to retrieve top-performing products ranked by revenue.

---

### GET /analytics/revenue-share

Use this endpoint to retrieve each partner’s percentage contribution to total revenue.

---

## Additional details

- Metrics are computed from processed product and order data  
- Aggregations are optimized for read-heavy workloads  
- Results are exposed through API endpoints for external consumption  