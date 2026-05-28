# Upload your first product feed

Upload a product feed, process it through the ingestion pipeline, and retrieve product data from the catalog.

In this tutorial, you will:

1. Upload a product feed
2. Run ETL processing
3. Retrieve ingested products
4. Validate ingestion results


## Before you begin

You need the following:

| Requirement      | Description                                                         |
| ---------------- | ------------------------------------------------------------------- |
| Base URL (local) | `http://localhost:8000`                                             |
| Base URL (AWS)   | `http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com` |
| API key          | `x-api-key: YOUR_API_KEY`                                           |
| CSV file         | See [CSV feed file specification](../specs/csv-feed-file-spec.md)   |


## Step 1: Understand product feeds

A product feed is a CSV file containing product data provided by a partner.

Each row represents a product record. At minimum, the system requires:

- `sku`
- `product_name`

When a feed is uploaded, the system stores the raw file and creates validation jobs before product data becomes available in the catalog.


## Step 2: Upload the feed

Upload a CSV file to create a new feed.

For endpoint details and request parameters, see the [Upload feed](../api/feeds.md#post-feedsupload) endpoint documentation.

### Request

```http
POST /feeds/upload
```

### Example request

```bash
curl -X POST "http://localhost:8000/feeds/upload" \
  -H "x-api-key: YOUR_API_KEY" \
  -F "file=@electronics_catalog.csv" \
  -F "partner_name=Tronics"
```

### Example response

```json
{
  "feed_id": "FD00001",
  "status": "uploaded",
  "validation_job_id": "JV00001",
  "validation_status": "queued"
}
```

### Validate upload behavior

After uploading the feed:

- The raw CSV file is stored in Amazon S3
- A validation job is created
- Feed processing is queued
- Products are not yet available in the catalog


## Step 3: Run ETL processing

Run the validation job to process the uploaded feed.

For endpoint details, see the [Run job](../api/jobs.md#post-jobsjob_idrun) endpoint documentation.

### Request

```http
POST /jobs/{job_id}/run
```

### Example request

```bash
curl -X POST "http://localhost:8000/jobs/JV00009/run" \
  -H "x-api-key: YOUR_API_KEY"
```

### Example response

```json
{
  "job_id": "JV00001",
  "status": "completed"
}
```

### Validate processing behavior

During processing, the system:

- Validates CSV structure
- Checks required fields
- Transforms rows into product records
- Inserts or updates products in PostgreSQL

Products become available for querying only after processing completes successfully.


## Step 4: Retrieve products

Retrieve products from the catalog to confirm ingestion completed successfully.

For filters, sorting options, and pagination behavior, see the [Get products](../api/products.md#get-products) endpoint documentation.

### Request

```http
GET /products?partner_name=Tronics&limit=5
```

### Example request

```bash
curl -X GET "http://localhost:8000/products?partner_name=Tronics&limit=5" \
  -H "x-api-key: YOUR_API_KEY"
```

### Example response

```json
{
  "count": 1,
  "items": [
    {
      "product_id": "PR00001",
      "partner_name": "Tronics",
      "sku": "TV-001",
      "product_name": "4K Smart TV",
      "category": "Electronics",
      "price": 799.99,
      "availability": "in_stock"
    }
  ]
}
```

### Validate ingestion results

After retrieving products:

- Product data is available in the catalog
- Feed ingestion completed successfully
- Product records were loaded into PostgreSQL


## Understand the ingestion pipeline

The ingestion workflow consists of four stages:

| Stage          | Description                                       |
| -------------- | ------------------------------------------------- |
| Raw            | Stores the original CSV file                      |
| Validation     | Validates structure and required fields           |
| Transformation | Converts CSV rows into normalized product records |
| Load           | Inserts or updates products in PostgreSQL         |


## Troubleshoot common issues

### Invalid CSV structure

Example response:

```json
{
  "detail": "Invalid CSV format"
}
```

To resolve this issue:

- Verify the file uses CSV format
- Confirm column headers are present
- Validate delimiter formatting


### Missing required fields

Example response:

```json
{
  "detail": "Missing required field: sku"
}
```

To resolve this issue:

- Ensure all required fields are included
- Verify each product row contains valid values


### Feed processing failed

Example response:

```json
{
  "job_id": "JV00001",
  "status": "failed"
}
```

To resolve this issue:

- Retrieve job details
- Review validation errors
- Correct the source CSV file
- Re-upload the feed


## Next steps

- See [Ingest a product feed](../how-to/ingest-product-feed.md) for a workflow-focused guide
- See [Debug a product feed failure](../operations/debug-product-feed.md) for troubleshooting procedures
- Explore the [Products](../api/products.md) API reference for advanced queries