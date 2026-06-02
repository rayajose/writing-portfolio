# Ingest a product feed

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
| API key           | `x-api-key: YOUR_API_KEY`                                           |
| Valid `.csv` file | See [CSV feed file specification](../specs/csv-feed-file-spec.md)   |


### Feed file specification

For complete CSV formatting rules, supported fields, validation requirements, and file constraints, see the [CSV feed file specification](../specs/csv-feed-file-spec.md).


## 1. Upload a product feed

Run the `POST /feeds/upload` endpoint to submit the product `.csv` file.

Record the `feed_id` value from the response for use in the next step. In this example, the `feed_id` is `FD00021`.

### Example request

```bash
curl -X POST http://api.example.com/feeds/upload \
  -H "x-api-key: YOUR_API_KEY" \
  -F "file=@electronics_catalog.csv" \
  -F "partner_id=PT00001"
```


### Example response

```json
{
  "feed_id": "FD00001",
  "job_id": "JS00001",
  "status": "processing"
}
```


## 2. Review processing results

Run the `GET /feeds/{feed_id}` endpoint using the `feed_id` from the upload response.

### Example request

```bash
curl -X GET http://api.example.com/feeds/FD00001 \
  -H "x-api-key: YOUR_API_KEY"
```


### Example response

```json
{
  "feed_id": "FD00001",
  "partner_id": "PT00001",
  "partner_name": "GoFasters'",
  "file_name": "acme-product-catalog.csv",
  "content_type": "text/csv",
  "status": "processed",
  "uploaded_at": "YYYY-MM-DDTHH:MM:SSZ",
  "validation_job_id": "JV00001",
  "validation_status": "completed",
  "validation_message": "ETL processing completed. Products processed: 10. Inserted: 10. Updated: 0. Deleted: 1.Unchanged: 0. Skipped: 0.",
  "raw_file_s3_key": "raw/partners/acme-corp/feeds/FD00001/acme-product-catalog.csv",
  "raw_file_bucket": "commerce-integration-raw"
}
```


### Interpret the results

Review the following values from the `validation_message` field:

- **Products processed**: Total rows evaluated
- **Inserted**: New products created
- **Updated**: Existing products with changed data, such as price or availability
- **Deleted**: Existing products no longer in stock
- **Unchanged**: Existing products with no changes
- **Skipped**: Invalid rows or rows missing required fields


## 3. Verify products

Run the `GET /products` endpoint using the `feed_id` from step 1 (`FD00001`) as a query parameter.

### Example request

```bash
curl -X GET "http://api.example.com/products?feed_id=FD00001" \
  -H "x-api-key: YOUR_API_KEY"
```


### Example response

```json
{
  "count": 2,
  "items": [
    {
      "product_id": "PR00145",
      "partner_id": "PT00001",
      "feed_id": "FD00001",
      "partner_name": "GoFasters'",
      "sku": "RS1001",
      "product_name": "Nike Air Zoom Pegasus 40",
      "description": "Versatile daily trainer with responsive Zoom Air units and breathable mesh upper",
      "brand": "Nike",
      "category": "Running Shoes",
      "price": 129.99,
      "currency": "USD",
      "availability": "In Stock",
      "created_at": "YYYY-MM-DDTHH:MM:SSZ"
    },
    {
      "product_id": "PR00146",
      "partner_id": "PT00001",
      "feed_id": "FD00001",
      "partner_name": "GoFasters'",
      "sku": "RS1002",
      "product_name": "Adidas Ultraboost 22",
      "description": "High-cushion running shoe with Boost midsole for energy return and Primeknit upper",
      "brand": "Adidas",
      "category": "Running Shoes",
      "price": 189.99,
      "currency": "USD",
      "availability": "In Stock",
      "created_at": "YYYY-MM-DDTHH:MM:SSZ"
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

- [Feeds](../api/feeds.md)
- [Jobs](../api/jobs.md)
- [Products](../api/products.md)
- [CSV feed file specification](../specs/csv-feed-file-spec.md)
- [Debug a product feed failure](../operations/debug-product-feed.md)