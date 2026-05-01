-- ============================================
-- SALES BY PRODUCT
-- ============================================
SELECT
    p.product_id,
    p.product_name,
    SUM(o.quantity) AS units_sold,
    SUM(o.total_amount) AS total_sales
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.product_id, p.product_name
ORDER BY total_sales DESC;


-- ============================================
-- SALES BY PARTNER
-- ============================================
SELECT
    partner_name,
    SUM(quantity) AS units_sold,
    SUM(total_amount) AS total_sales
FROM orders
GROUP BY partner_name
ORDER BY total_sales DESC;


-- ============================================
-- DAILY SALES
-- ============================================
SELECT
    order_date,
    SUM(quantity) AS units_sold,
    SUM(total_amount) AS total_sales
FROM orders
GROUP BY order_date
ORDER BY order_date;


-- ============================================
-- MONTHLY SALES
-- ============================================
SELECT
    DATE_TRUNC('month', order_date)::date AS sales_month,
    SUM(quantity) AS units_sold,
    SUM(total_amount) AS total_sales
FROM orders
GROUP BY sales_month
ORDER BY sales_month;


-- ============================================
-- TOP SELLING PRODUCTS
-- ============================================
SELECT
    p.product_name,
    SUM(o.quantity) AS units_sold
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.product_name
ORDER BY units_sold DESC
LIMIT 5;


-- ============================================
-- PARTNER PERFORMANCE (AVG ORDER VALUE)
-- ============================================
SELECT
    partner_name,
    COUNT(*) AS total_orders,
    AVG(total_amount) AS avg_order_value,
    SUM(total_amount) AS total_revenue
FROM orders
GROUP BY partner_name
ORDER BY total_revenue DESC;

-- ============================================
-- REVENUE SHARE BY PARTNER (% OF TOTAL)
-- ============================================
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