# Ingest a product feed end-to-End

This guide shows how to upload, process, and verify a partner product feed using the Commerce Integration API.

Use this workflow during partner onboarding or when testing feed ingestion.


## Overview

In this guide, you will:

1. Upload a product feed
2. Review ingestion results
3. Verify products in the catalog


## Prerequisites

| Requirement       | Description                                                         |
| ----------------- | ------------------------------------------------------------------- |
| Base URL (local)  | `http://localhost:8000`                                             |
| Base URL (AWS)    | `http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com` |
| API key           | `x-api-key: demo-secret-key`                                        |
| Valid .`csv` file | see  [CSV feed file specification](../specs/csv-feed-file-spec.md)  |

### Feed file specification

For complete CSV formatting rules, supported fields, validation requirements, and file constraints, see the [CSV Feed File Specification](../specs/csv-feed-file-spec.md).

## 1. Upload a product feed

To upload a product feed, do the following:

- Run the POST /feeds/upload endpoint to submit the product `.csv` file.
- Note the `feed_id` value in the response for use in the next step. In the example the `feed_id` is FD00021.

**Example request**

```bash
curl -X POST "http://api.example.com/feeds/upload" \
  -H "x-api-key: demo-secret-key" \
  -F "file=@electronics_catalog.csv" \
  -F "partner_name=Tronics"
```

**Example response**

```json
{
  "feed_id": "FD00021",
  "job_id": "JS00021",
  "status": "processing"
}
```

## 2. Review processing results
Run the GET /feeds/{feed_id} endpoint using the `feed_id` captured in previous step, FD00021.

### Example request

```bash
curl --request GET \
  --url http://api.example.com/feeds/FD00021 \
  --header 'x-api-key: demo-secret-key'
```

### Example response

```json
{
  "feed_id": "FD00021",
  "partner_name": "Joyeria Reina",
  "file_name": "test-only-sku-product_name.csv",
  "content_type": "text/csv",
  "status": "processed",
  "uploaded_at": "2026-05-05T16:18:58.792011Z",
  "validation_job_id": "JV00021",
  "validation_status": "completed",
  "validation_message": "ETL processing completed. Products processed: 10. Inserted: 10. Updated: 0. Unchanged: 0. Skipped: 0.",
  "raw_file_s3_key": "raw/partners/joyeria-reina/feeds/FD00021/test-only-sku-product_name.csv",
  "raw_file_bucket": "partner-catalog-raw-rayj"
}
```

### Interpret the results
Review the following values from the `validation_message` field in the response.

- **Processed**: Total rows evaluated
- **Inserted**: New products created
- **Updated**: Existing products with changed data (for example, price or availability)
- **Unchanged**: Existing products with no changes
- **Skipped**: Invalid rows or rows missing required fields


## 3. Verify Products
Run the GET /products endpoint using the `feed_id` from step 1 (FD00021) as a query parameter.

**Example request**

```bash
curl -X GET "http://api.example.com/products?feed_id=FD00021" \
  -H "x-api-key: demo-secret-key"
```

**Example response**

```json
{
  "count": 2,
  "items": [
    {
      "product_id": "PR00145",
      "feed_id": "FD00019",
      "partner_name": "Test",
      "sku": "RS1001",
      "product_name": "Nike Air Zoom Pegasus 40",
      "description": "Versatile daily trainer with responsive Zoom Air units and breathable mesh upper",
      "brand": "Nike",
      "category": "Running Shoes",
      "price": 129.99,
      "currency": "USD",
      "availability": "In Stock",
      "created_at": "2026-05-04T16:48:42.611576+00:00"
    },
    {
      "product_id": "PR00146",
      "feed_id": "FD00019",
      "partner_name": "Test",
      "sku": "RS1002",
      "product_name": "Adidas Ultraboost 22",
      "description": "High-cushion running shoe with Boost midsole for energy return and Primeknit upper",
      "brand": "Adidas",
      "category": "Running Shoes",
      "price": 189.99,
      "currency": "USD",
      "availability": "In Stock",
      "created_at": "2026-05-04T16:48:42.611576+00:00"
    }
  ]
}
```

### Optional filters

Use query parameters to refine results:

- `partner_name`
- `sku`
- `brand`
- `category`
- `availability`


## Related documentation

- [Debug a product feed](../operations/debug-product-feed.md)


