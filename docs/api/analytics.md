# Analytics Layer

The analytics layer extends the Partner Catalog API beyond data ingestion by enabling business intelligence use cases across products, partners, and time.

This phase demonstrates how operational data can be transformed into meaningful insights through aggregation, dimensional modeling, and API-driven analytics.

---

## Objective

Enable analytical querying across:

* Product performance
* Partner performance
* Revenue distribution
* Time-based trends

The system answers questions such as:

* Which partners generate the most revenue?
* Which products drive the highest sales?
* How does revenue vary over time?
* What percentage of revenue does each partner contribute?

---

## Data Model

Phase 4 introduces an `orders` table that acts as a **fact table**.

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

## Orders Table

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

## Dimensional Model

This phase uses a simplified dimensional model:

| Type      | Table / Field  | Purpose                   |
|-----------|----------------|---------------------------|
| Fact      | `orders`       | Stores sales transactions |
| Dimension | `products`     | Product attributes        |
| Dimension | `partner_name` | Partner grouping          |
| Dimension | `order_date`   | Time-based analysis       |

---

## Dataset Characteristics

The sample dataset includes multiple partner types:

* **High-volume / low-price** — Microbrews Brothers
* **High-value electronics** — RayTech Corp., Tronics
* **Media retail** — Cid's Vintage Records
* **Luxury goods** — Joyeria Reina

This enables realistic comparisons across:

* Revenue vs volume
* Product categories
* Partner business models

---

## Analytics Scenarios

### Sales by Partner

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

### Sales Over Time

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

### Monthly Aggregation

```sql
SELECT
    DATE_TRUNC('month', order_date)::date AS sales_month,
    SUM(quantity),
    SUM(total_amount)
FROM orders
GROUP BY sales_month;
```

---

### Top Products

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

### Revenue Share (Window Function)

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

## Analytics API Endpoints

The analytics layer exposes read-only endpoints for aggregated insights.

---

### GET /analytics/sales-by-partner

Returns total units and revenue by partner.

---

### GET /analytics/sales-over-time

Returns time-based sales metrics.

Supports:

* `daily`
* `monthly`

---

### GET /analytics/top-products

Returns top-performing products ranked by revenue.

---

### GET /analytics/revenue-share

Returns each partner’s percentage contribution to total revenue.

Demonstrates use of SQL window functions.

---

## Key Insights

Using the dataset, several patterns emerge:

* **Joyeria Reina and RayTech Corp. generate high revenue** with lower unit volume (high-value items)
* **Microbrews Brothers drives high unit volume** but lower total revenue
* **Tronics introduces competitive overlap** in electronics
* Revenue distribution is **heavily concentrated among high-ticket partners**
* Time-series data enables trend analysis and future forecasting

---

## Concepts Demonstrated

This phase demonstrates:

* Dimensional modeling (fact + dimensions)
* Analytical SQL querying
* Aggregations (SUM, GROUP BY)
* Time-based analysis (daily, monthly)
* Window functions (revenue share)
* API-driven analytics delivery
* Schema validation with Pydantic

---

## Portfolio Value

The analytics layer shows how an operational API system can evolve into a data platform that supports:

* Business intelligence
* Partner performance analysis
* Revenue reporting
* Data-driven decision-making

This demonstrates the ability to design, implement, and document both application logic and analytical systems.
