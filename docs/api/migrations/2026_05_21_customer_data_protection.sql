-- Commerce Integration API
-- Customer and data protection migration
-- Version: v0.6.0
-- Date: 2026-05-21

BEGIN;

-- =========================================================
-- Customer table
-- =========================================================

CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),

    -- Protected customer data
    email VARCHAR(255),
    phone VARCHAR(50),
    street_address VARCHAR(255),
    city VARCHAR(100),
    state_region VARCHAR(100),
    postal_code VARCHAR(30),
    country VARCHAR(100),

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_customers_email
ON customers(email);


-- =========================================================
-- Orders table customer linkage
-- =========================================================

ALTER TABLE orders
ADD COLUMN IF NOT EXISTS customer_id VARCHAR(20);

ALTER TABLE orders
ADD CONSTRAINT fk_orders_customer
FOREIGN KEY (customer_id)
REFERENCES customers(customer_id);


-- =========================================================
-- Customer data audit events
-- =========================================================

CREATE TABLE IF NOT EXISTS customer_data_events (
    event_id BIGSERIAL PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    actor VARCHAR(100),
    event_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    details TEXT,

    CONSTRAINT fk_customer_data_events_customer
    FOREIGN KEY (customer_id)
    REFERENCES customers(customer_id)
);

CREATE INDEX IF NOT EXISTS idx_customer_data_events_customer_id
ON customer_data_events(customer_id);

CREATE INDEX IF NOT EXISTS idx_customer_data_events_timestamp
ON customer_data_events(event_timestamp);


-- =========================================================
-- Data retention support
-- =========================================================

ALTER TABLE orders
ADD COLUMN IF NOT EXISTS retention_expiration_date DATE;

ALTER TABLE feeds
ADD COLUMN IF NOT EXISTS retention_expiration_date DATE;


-- =========================================================
-- Updated-at trigger support
-- =========================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_customers_updated_at ON customers;

CREATE TRIGGER trg_customers_updated_at
BEFORE UPDATE ON customers
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();


-- =========================================================
-- Sample ID counter initialization
-- =========================================================

INSERT INTO id_counters (entity_name, current_value)
SELECT 'customer', 0
WHERE NOT EXISTS (
    SELECT 1
    FROM id_counters
    WHERE entity_name = 'customer'
);

COMMIT;
