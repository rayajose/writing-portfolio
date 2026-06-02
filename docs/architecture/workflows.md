# Workflows

Use this guide to upload a partner feed, run ETL processing, retrieve product data, and create customer orders.

## Processing behavior

- Upload a feed
- Create submission and validation jobs
- Run ETL processing
- Store products in the database
- Retrieve products through the API
- Create fictional customer and shipping address records
- Create transactional orders
- Retrieve analytics and reporting data

## Upload and process a feed

This workflow shows the full ingestion pipeline from raw upload to queryable product data.

### Step 1: Upload a feed

```bash
curl -X POST "http://api.example.com/feeds/upload" \
  -H "x-api-key: YOUR_API_KEY" \
  -F "partner_name=Acme Corp" \
  -F "file=@sample_catalog.csv"
```

### Example response

```json
{
  "feed_id": "FD00001",
  "status": "uploaded",
  "job_id": "JS00001"
}
```

### Processing behavior

- CSV structure is validated
- Raw file is stored in Amazon S3
- A submission job (`JSxxxxx`) is created
- A validation job (`JVxxxxx`) is created
- Feed metadata is persisted

> Product data is not ingested at this stage.

### Step 2: Check submission job

```bash
curl -H "x-api-key: YOUR_API_KEY" \
  "http://api.example.com/jobs/JS00001"
```

### Step 3: Check validation job

```bash
curl -H "x-api-key: YOUR_API_KEY" \
  "http://api.example.com/jobs/JV00001"
```

### Example response

```json
{
  "job_id": "JV00001",
  "job_type": "validation",
  "status": "queued",
  "feed_id": "FD00001",
  "message": "CSV structure validation queued for ETL processing."
}
```

### Step 4: Run ETL processing

```bash
curl -X POST "http://api.example.com/jobs/JV00001/run" \
  -H "x-api-key: YOUR_API_KEY"
```

### Processing behavior

- Raw CSV is read from S3
- Data is cleaned and normalized
- Products are compared against existing records
- Only changed products are updated
- New products are inserted
- Unchanged products are skipped
- Job status and message are updated with ETL results

### Step 5: Verify feed processing

```bash
curl -H "x-api-key: YOUR_API_KEY" \
  "http://api.example.com/feeds/FD00001"
```

### Example response

```json
{
  "feed_id": "FD00001",
  "partner_id": "PT00001"
  "partner_name": "Acme Corp",
  "file_name": "acme-product-catalog.csv",
  "content_type": "text/csv",
  "status": "uploaded",
  "uploaded_at": "YYYY-MM-DDTHH:MM:SSZ",
  "validation_job_id": "JV00001",
  "validation_status": "completed",
  "validation_message": "ETL processing completed. Products processed: 13. Inserted: 1. Updated: 0. Unchanged: 12. Skipped: 0.",
  "raw_file_s3_key": "raw/partners/acme-corp/feeds/FD00001/acme-product-catalog.csv",
  "raw_file_bucket": "commerce-integration-raw"
}
```

### Step 6: Query products

```bash
curl -H "x-api-key: YOUR_API_KEY" \
  "http://api.example.com/products?limit=5"
```

### Example response

```json
{
  "count": 5,
  "items": [
    {
      "product_id": "PR00001",
      "feed_id": "FD00001",
      "partner_name": "Acme Corp",
      "sku": "AC-1001",
      "product_name": "Acme widget 3000",
      "price": 49.99,
      "currency": "USD",
      "availability": "in_stock",
      "created_at": "YYYY-MM-DDTHH:MM:SSZ"
    }
  ],
  "next_cursor": "PR00005"
}
```

## Create customer and shipping records

This workflow shows how to create fictional customer and shipping address records before creating an order.

### Step 1: Create a customer

```bash
curl -X POST "http://api.example.com/customers" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Alex",
    "last_name": "Morgan",
    "email": "alex.morgan@example.com",
    "phone": "555-0101"
  }'
```

### Example response

```json
{
  "customer_id": "CU00001",
  "first_name": "Alex",
  "last_name": "Morgan",
  "email_masked": "al***@example.com",
  "phone_masked": "***-***-0101"
}
```

### Processing behavior

- Sensitive customer fields are encrypted before storage
- API responses return masked customer values
- Customer records are persisted in PostgreSQL

### Step 2: Create a shipping address

```bash
curl -X POST "http://api.example.com/customers/CU00001/addresses" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "address_line1": "123 Example Street",
    "city": "Seattle",
    "state": "WA",
    "postal_code": "98101"
  }'
```

### Example response

```json
{
  "address_id": "AD00001",
  "customer_id": "CU00001",
  "address_line1_masked": "123 ***",
  "postal_code_masked": "***01"
}
```

### Processing behavior

- Address fields are encrypted before storage
- API responses return masked address values
- Shipping address records are linked to customers

## Create an order

This workflow shows how to create an order using products previously loaded into the catalog.

### Step 1: Retrieve products

```bash
curl -H "x-api-key: YOUR_API_KEY" \
  "http://api.example.com/products?limit=5"
```

### Example response

```json
{
  "count": 1,
  "items": [
    {
      "product_id": "PR00001",
      "product_name": "Acme widget 3000",
      "price": 49.99,
      "availability": "in_stock"
    }
  ]
}
```

### Step 2: Create an order

```bash
curl -X POST "http://api.example.com/orders" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "partner_name": "Acme Corp",
    "customer_reference": "CR00001",
    "customer_id": "CU00001",
    "shipping_address_id": "AD00001",
    "items": [
      {
        "product_id": "PR00001",
        "quantity": 2
      }
    ]
  }'
```

### Example response

```json
{
  "order_id": "OR00001",
  "partner_name": "Acme Corp",
  "customer_reference": "CR00001",
  "customer_id": "CU00001",
  "shipping_address_id": "AD00001",
  "status": "created",
  "total_amount": 99.98,
  "currency": "USD",
  "items": [
    {
      "order_item_id": "OI00001",
      "product_id": "PR00001",
      "sku": "AC-1001",
      "product_name": "Acme widget 3000",
      "quantity": 2,
      "unit_price": 49.99,
      "line_total": 99.98
    }
  ]
}
```

### Processing behavior

- The system validates that the requested product exists
- Product availability is checked before order creation
- Customer and shipping records can be associated with the order
- Product pricing is copied into each order item
- Line totals are calculated for each item
- The order total is calculated from all order items
- The order and associated order items are stored transactionally

### Step 3: Retrieve the order

```bash
curl -H "x-api-key: YOUR_API_KEY" \
  "http://api.example.com/orders/OR00001"
```

### Related APIs

- [Products API](../api/products.md)
- [Orders API](../api/orders.md)

## Reprocessing example (idempotency)

Re-running ETL on the same feed demonstrates how the system avoids duplicate updates.

### First run

```text
Products processed: 13. Inserted: 13. Updated: 0. Unchanged: 0. Skipped: 0.
```

### Second run (same data)

```text
Products processed: 13. Inserted: 0. Updated: 0. Unchanged: 13. Skipped: 0.
```

### After modifying one product (for example, price)

```text
Products processed: 13. Inserted: 0. Updated: 1. Unchanged: 12. Skipped: 0.
```

> This behavior ensures efficient processing and avoids unnecessary database writes.

## Workflow summary

```text
Upload Feed
  → Store raw file in S3
  → Create submission job (JSxxxxx)
  → Create validation job (JVxxxxx)

Run ETL
  → POST /jobs/{job_id}/run
  → Read CSV from S3
  → Transform + compare data
  → Insert / update only when needed

Query
  → Products become available via /products

Customer Workflows
  → Create customer records via /customers
  → Encrypt sensitive customer data
  → Create shipping addresses

Order Processing
  → Create orders via /orders
  → Link customers and shipping addresses
  → Store transactional order and order item data

Analytics
  → Aggregate sales and revenue reporting
```

## Key points

- Upload and ingestion are separate steps
- Raw data is stored in S3 for reprocessing and auditability
- ETL is triggered explicitly via API
- Jobs provide full pipeline visibility
- Product updates are change-detected (no blind updates)
- Reprocessing is idempotent
- Product data is only available after ETL completes
- Customer-sensitive fields are encrypted before storage
- API responses return masked customer and address values
- Orders use transactional relational modeling
- Product pricing is preserved at order creation time
- IDs follow structured formats:

| Prefix    | Resource         |
| --------- | ---------------- |
| `FDxxxxx` | Feed             |
| `JSxxxxx` | Submission Job   |
| `JVxxxxx` | Validation Job   |
| `PRxxxxx` | Product          |
| `CUxxxxx` | Customer         |
| `ADxxxxx` | Customer Address |
| `ORxxxxx` | Order            |
| `OIxxxxx` | Order Item       |

## Additional details

- ETL processing is currently synchronous
- Designed to support asynchronous execution in the future
- Validation includes both structure and transformation readiness
- Customer-sensitive fields use field-level encryption
- Orders can optionally reference customer and shipping address records
- Orders and order items are persisted in PostgreSQL using foreign key relationships

## Related documentation

- [Feeds API](../api/feeds.md)
- [Jobs API](../api/jobs.md)
- [Products API](../api/products.md)
- [Customers API](../api/customers.md)
- [Orders API](../api/orders.md)
- [Analytics API](../api/analytics.md)
- [Errors](../api/errors.md)