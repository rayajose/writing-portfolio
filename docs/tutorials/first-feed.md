# Your first feed ingestion

In this tutorial, you will upload a product feed, process it through the system, and retrieve product data.

This tutorial is designed for first-time users. It introduces the core workflow and explains what happens at each step.


## What you’ll learn

By the end of this tutorial, you will understand:

- What a product feed is
- How the ingestion pipeline works
- How product data becomes available in the API


## Before you begin

You need:

| Requirement       | Description                                                         |
| ----------------- | ------------------------------------------------------------------- |
| Base URL (local)  | `http://localhost:8000`                                             |
| Base URL (AWS)    | `http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com` |
| API key           | `x-api-key: demo-secret-key`                                        |
| Valid .`csv` file | see  [CSV feed file specification](../sop/csv-feed-file-spec.md)    |


## Step 1: Understand what a feed is

A **product feed** is a CSV file that contains product data from a partner.

Each row represents a product. At minimum, the system requires:

- `sku` (unique identifier per partner)
- `product_name`

When you upload a feed, the system does not immediately make products available. Instead, it stores the raw file and prepares it for processing.


## Step 2: Upload the feed

Upload your CSV file to create a new feed.

### Request

```bash
curl -X POST "http://localhost:8000/feeds/upload" \
  -H "x-api-key: demo-secret-key" \
  -F "file=@electronics_catalog.csv" \
  -F "partner_name=Tronics"
```

### Response

```json
{
  "feed_id": "FD00009",
  "status": "uploaded",
  "validation_job_id": "JV00009",
  "validation_status": "queued"
}
```

### What happens

- The file is stored in the raw data layer (S3)
- A validation job is created
- The system queues the feed for processing

At this point, the data is not yet available for querying.


## Step 3: Run ETL processing

Process the feed to validate and transform the data.

### Request

```bash
curl -X POST "http://localhost:8000/jobs/JV00009/run" \
  -H "x-api-key: demo-secret-key"
```

### Response

```json
{
  "job_id": "JV00009",
  "status": "completed"
}
```

### What happens

During this step, the system:

- Validates the CSV structure
- Checks required fields
- Transforms rows into product records
- Inserts or updates products in the database

Only after this step completes can you query product data.


## Step 4: Retrieve products

Query the API to confirm that products were ingested.

### Request

```bash
curl -X GET "http://localhost:8000/products?limit=5" \
  -H "x-api-key: demo-secret-key"
```

### Response

```json
{
  "count": 1,
  "items": [
    {
      "product_id": "PR00001",
      "sku": "TV-001",
      "product_name": "4K Smart TV"
    }
  ]
}
```

### What this means

- Products are now available in the catalog
- The ingestion pipeline completed successfully


## How the system processes your data

The ingestion workflow follows four stages:

1. **Raw**

   - Stores the original CSV file

2. **Validation**

   - Checks structure and required fields

3. **Transformation**

   - Converts CSV rows into product records

4. **Load**

   - Inserts or updates products in the database


## What to try next

Now that you’ve completed your first ingestion:

- Use filters to query specific products
- Upload a larger or more complex feed
- Introduce invalid data to see how validation behaves


## Next steps

- See [Ingest a Product Feed End-to-End](../api/ingest-product-feed.md) for a task-focused workflow
- See [Debug a Failed Feed](../api/debug-product-feed.md) to troubleshoot issues
- Explore [Products API](../api/products.md) for advanced queries
