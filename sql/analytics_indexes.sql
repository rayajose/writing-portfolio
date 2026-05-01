CREATE INDEX IF NOT EXISTS idx_orders_product_id ON orders(product_id);
CREATE INDEX IF NOT EXISTS idx_orders_partner_name ON orders(partner_name);
CREATE INDEX IF NOT EXISTS idx_orders_order_date ON orders(order_date);