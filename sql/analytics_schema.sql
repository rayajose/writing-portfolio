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