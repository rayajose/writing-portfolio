# Upload your first product feed

Upload a product feed, process it through the ingestion pipeline, and retrieve product data from the catalog.

In this tutorial, you will:

1. Create a partner
2. Upload a product feed
3. Monitor feed processing
4. Retrieve ingested products
5. Validate ingestion results

## Before you begin

You need the following:

| Requirement      | Description                                                         |
| ---------------- | ------------------------------------------------------------------- |
| Base URL (local) | `http://localhost:8000`                                             |
| Base URL (AWS)   | `http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com` |
| API key          | `x-api-key: YOUR_API_KEY`                                           |
| CSV file         | See [CSV feed file specification](../specs/csv-feed-file-spec.md)   |

## Step 1: Create a partner

Create a partner record before submitting product feeds.

For endpoint details and request parameters, see the [Create partner](../api/partners.md#post-partners) endpoint documentation.

### Example request

```bash
curl -X POST "http://localhost:8000/partners" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "partner_name": "Tronics",
        "contact_email": "integrations@tronics.example"
      }'
```

### Example response

```json
{
  "partner_id": "PT00001",
  "partner_name": "Tronics",
  "status": "active",
  "contact_email": "integrations@tronics.example"
}
```

Save the returned `partner_id`. It is required when uploading feeds.

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
  -F "partner_id=PT00001" \
  -F "file=@electronics_catalog.csv"
```

### Example response

```json
{
  "feed_id": "FD00001",
  "job_id": "JS00001",
  "status": "processing"
}
```

### Validate upload behavior

After uploading the feed:

- The raw CSV file is stored in Amazon S3
- Submission and validation jobs are created
- ETL processing starts automatically in the background
- Feed processing status becomes available through the Jobs API

## Step 3: Monitor feed processing

Retrieve job details to monitor feed processing status.

For endpoint details, see the [Get job](../api/jobs.md#get-jobsjob_id) endpoint documentation.

### Request

```http
GET /jobs/{job_id}
```

### Example request

```bash
curl -X GET "http://localhost:8000/jobs/JS00001" \
  -H "x-api-key: YOUR_API_KEY"
```

### Example response

```json
{
  "job_id": "JS00001",
  "job_type": "submission",
  "status": "completed",
  "feed_id": "FD00001"
}
```

Processing is complete when the associated validation job reaches a `completed` status.

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

### Partner not found

Example response:

```json
{
  "detail": "Partner not found."
}
```

To resolve this issue:

- Verify the partner exists
- Confirm the correct `partner_id` was supplied
- Retrieve available partners using `GET /partners`

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

To resolve this issue:

- Retrieve job details
- Review validation errors
- Correct the source CSV file
- Upload a new feed

## Next steps

- See [Ingest a product feed](../how-to/ingest-product-feed.md) for a workflow-focused guide
- See [Debug a product feed failure](../operations/debug-product-feed.md) for troubleshooting procedures
- Explore the [Products](../api/products.md) API reference for advanced queries
