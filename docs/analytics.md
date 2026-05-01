# Analytics Layer

The analytics layer extends the Partner Catalog API project beyond product ingestion and retrieval by adding business intelligence use cases based on product and order data.

This phase demonstrates how catalog data can support reporting, trend analysis, and partner performance insights.

---

## Objective

Enable analytical querying across product, partner, and time dimensions.

The analytics layer supports questions such as:

* Which products generate the most sales?
* Which partners generate the most revenue?
* How do sales trend over time?
* What are daily and monthly sales totals?

---

## Data Model

Phase 4 introduces an `orders` table that functions as a simple fact table.

The `orders` table connects sales activity to existing catalog products.

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

This phase uses a lightweight dimensional model:

| Type      | Table / Field  | Purpose                                         |
| --------- | -------------- | ----------------------------------------------- |
| Fact      | `orders`       | Stores measurable sales events                  |
| Dimension | `products`     | Describes the products being sold               |
| Dimension | `partner_name` | Identifies the partner associated with the sale |
| Dimension | `order_date`   | Enables time-based reporting                    |

---

## Analytics Scenarios

### Sales by Product

This query shows which products generate the most revenue.

```sql
SELECT
    p.product_id,
    p.product_name,
    SUM(o.quantity) AS units_sold,
    SUM(o.total_amount) AS total_sales
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.product_id, p.product_name
ORDER BY total_sales DESC;
```

### Sales by Partner

This query compares revenue by partner.

```sql
SELECT
    partner_name,
    SUM(quantity) AS units_sold,
    SUM(total_amount) AS total_sales
FROM orders
GROUP BY partner_name
ORDER BY total_sales DESC;
```

### Daily Sales

This query aggregates sales by day.

```sql
SELECT
    order_date,
    SUM(quantity) AS units_sold,
    SUM(total_amount) AS total_sales
FROM orders
GROUP BY order_date
ORDER BY order_date;
```

### Monthly Sales

This query aggregates sales by month.

```sql
SELECT
    DATE_TRUNC('month', order_date)::date AS sales_month,
    SUM(quantity) AS units_sold,
    SUM(total_amount) AS total_sales
FROM orders
GROUP BY sales_month
ORDER BY sales_month;
```

### Top Selling Products

This query identifies the products with the highest unit volume.

```sql
SELECT
    p.product_name,
    SUM(o.quantity) AS units_sold
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.product_name
ORDER BY units_sold DESC
LIMIT 5;
```

### Partner Performance

This query compares partner order volume, average order value, and total revenue.

```sql
SELECT
    partner_name,
    COUNT(*) AS total_orders,
    AVG(total_amount) AS avg_order_value,
    SUM(total_amount) AS total_revenue
FROM orders
GROUP BY partner_name
ORDER BY total_revenue DESC;
```

---

## Key Insights

Using the sample dataset, several patterns emerge:

- **RayTech Corp. generates significantly higher revenue** despite lower unit volume, driven by high-value electronics products.
- **Microbrews Brothers drives higher unit sales volume**, but at lower price points, resulting in lower overall revenue.
- Sales activity shows consistent distribution across multiple days, enabling time-based trend analysis.
- Product-level aggregation highlights which SKUs contribute most to total revenue versus unit volume.

These insights demonstrate how the same dataset can support different analytical perspectives, such as revenue optimization, product performance, and partner comparisons.

---

## Concepts Demonstrated

This phase demonstrates:

* Dimensional modeling
* Fact and dimension relationships
* Analytical SQL querying
* Aggregation by product, partner, and time
* Daily and monthly reporting
* Business intelligence use cases based on operational data

---

## Portfolio Value

The analytics layer shows how product catalog data can be extended into reporting and business intelligence workflows.

This demonstrates the ability to document not only API behavior, but also the data relationships and analytical use cases that support business decision-making.
