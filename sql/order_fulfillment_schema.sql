CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    partner_name TEXT NOT NULL,
    customer_reference TEXT,
    status TEXT NOT NULL DEFAULT 'created',
    total_amount NUMERIC,
    currency TEXT DEFAULT 'USD',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    sku TEXT,
    product_name TEXT,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC,
    line_total NUMERIC,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS fulfillment_jobs (
    job_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'queued',
    message TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE IF NOT EXISTS shipments (
    shipment_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    job_id TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    carrier TEXT,
    tracking_number TEXT,
    shipped_at TEXT,
    delivered_at TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (job_id) REFERENCES fulfillment_jobs(job_id)
);