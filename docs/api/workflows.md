# Workflows

Use this guide to upload a partner feed, run ETL processing, and retrieve product data.

## What happens

- Upload a feed  
- Create submission and validation jobs  
- Run ETL processing  
- Store products in the database  
- Retrieve products through the API  


## Upload and process a feed

This workflow shows the full ingestion pipeline from raw upload to queryable product data.


### Step 1: Upload a feed

```bash
curl -X POST "http://api.example.com/feeds/upload" \
  -H "x-api-key: demo-secret-key" \
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


### What happens

- CSV structure is validated
- Raw file is stored in Amazon S3
- A **submission job (JSxxxxx)** is created
- A **validation job (JVxxxxx)** is created
- Feed metadata is persisted

> Product data is **not ingested at this stage**


### Step 2: Check submission job

```bash
curl -H "x-api-key: demo-secret-key" \
  "http://api.example.com/jobs/JS00001"
```


### Step 3: Check validation job (queued)

```bash
curl -H "x-api-key: demo-secret-key" \
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
  -H "x-api-key: demo-secret-key"
```


### What happens

- Raw CSV is read from S3
- Data is cleaned and normalized
- Products are compared against existing records
- Only changed products are updated
- New products are inserted
- Unchanged products are skipped
- Job status and message are updated with ETL results


### Step 5: Verify feed processing

```bash
curl -H "x-api-key: demo-secret-key" \
  "http://api.example.com/feeds/FD00001"
```

### Example response

```json
{
  "feed_id": "FD00001",
  "partner_name": "Acme Corp",
  "file_name": "sample_catalog.csv",
  "content_type": "text/csv",
  "status": "uploaded",
  "uploaded_at": "2026-04-06T14:17:27+00:00",
  "validation_job_id": "JV00001",
  "validation_status": "completed",
  "validation_message": "ETL processing completed. Products processed: 13. Inserted: 1. Updated: 0. Unchanged: 12. Skipped: 0.",
  "raw_file_s3_key": "raw/partners/acme/feeds/FD00001/sample_catalog.csv",
  "raw_file_bucket": "partner-catalog-raw-rayj"
}
```


### Step 6: Query products

```bash
curl -H "x-api-key: demo-secret-key" \
  "http://api.example.com/products?limit=5"
```


### Response

```json
{
  "count": 5,
  "items": [
    {
      "product_id": "PR00001",
      "feed_id": "FD00001",
      "partner_name": "Acme Corp",
      "sku": "AC-1001",
      "product_name": "Sample Product",
      "price": 49.99,
      "currency": "USD",
      "availability": "in_stock",
      "created_at": "2026-04-08T12:00:00Z"
    }
  ],
  "next_cursor": "PR00005"
}
```


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

### After modifying one product (e.g., price)

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
```

## Key points

- Upload and ingestion are **separate steps**
- Raw data is stored in S3 for reprocessing and auditability
- ETL is triggered explicitly via API
- Jobs provide full pipeline visibility
- Product updates are **change-detected (no blind updates)**
- Reprocessing is **idempotent**
- Product data is only available after ETL completes
- IDs follow structured formats:

  - `FDxxxxx` → Feed
  - `JSxxxxx` → Submission Job
  - `JVxxxxx` → Validation Job
  - `PRxxxxx` → Product

## Additional details

- ETL processing is currently synchronous
- Designed to support asynchronous execution in the future
- Validation includes both structure and transformation readiness


## Related documentation

- [Feeds API](feeds.md)
- [Jobs API](jobs.md)
- [Products API](products.md)
- [Errors](errors.md)
