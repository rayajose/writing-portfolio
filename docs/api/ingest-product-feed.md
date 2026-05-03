# Ingest a product feed end-to-End

This guide shows how to upload, process, and verify a partner product feed using the Partner Catalog API.

Use this workflow during partner onboarding or when testing feed ingestion.

---

## Overview

In this guide, you will:

1. Upload a product feed
2. Run validation and ETL processing
3. Review ingestion results
4. Verify products in the catalog

---

## Prerequisites

- Base URL:

  ```text
  http://localhost:8000
  ```

  or

  ```text
  http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com
  ```

- API key:

  ```text
  x-api-key: demo-secret-key
  ```

- A CSV file that includes:

  - `sku`
  - `product_name`

---

## 1. Upload a Product Feed

Upload a CSV file to create a new feed.

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
  "partner_name": "Tronics",
  "file_name": "electronics_catalog.csv",
  "content_type": "text/csv",
  "status": "uploaded",
  "uploaded_at": "2026-04-28T18:22:10Z",
  "validation_job_id": "JV00009",
  "validation_status": "queued",
  "validation_message": "CSV structure validation queued for ETL processing.",
  "raw_file_s3_key": "raw/partners/tronics/feeds/FD00009/electronics_catalog.csv",
  "raw_file_bucket": "partner-catalog-raw-rayj"
}
```

### What happens

- The file is stored in S3 (raw layer)
- A validation job is created
- Feed status is set to `uploaded`
- ETL processing is queued

---

## 2. Run ETL Processing

If processing does not run automatically, trigger the job.

### Request

```bash
curl -X POST "http://localhost:8000/jobs/JV00009/run" \
  -H "x-api-key: demo-secret-key"
```

### Response

```json
{
  "job_id": "JV00009",
  "status": "completed",
  "message": "ETL processing completed."
}
```

### What happens

During processing:

- CSV structure is validated
- Required fields are checked
- Data is transformed into product records
- Records are inserted or updated
- Invalid rows are skipped

---

## 3. Review Processing Results

Retrieve the job to understand the ingestion outcome.

### Request

```bash
curl -X GET "http://localhost:8000/jobs/JV00009" \
  -H "x-api-key: demo-secret-key"
```

### Response

```json
{
  "job_id": "JV00009",
  "status": "completed",
  "result": "Products processed: 13. Inserted: 1. Updated: 5. Unchanged: 7. Skipped: 0."
}
```

### Interpret the result

- **Processed**: Total rows evaluated
- **Inserted**: New products created
- **Updated**: Existing products with changed data (for example, price or availability)
- **Unchanged**: Existing products with no changes
- **Skipped**: Invalid rows or rows missing required fields

---

## 4. Verify Products

Confirm that products are available in the catalog.

### Request

```bash
curl -X GET "http://localhost:8000/products?feed_id=FD00009" \
  -H "x-api-key: demo-secret-key"
```

### Response

```json
{
  "data": [
    {
      "product_id": "PR00001",
      "partner_name": "Tronics",
      "sku": "TV-001",
      "product_name": "4K Smart TV",
      "brand": "VisionTech",
      "category": "Electronics",
      "price": 799.99,
      "availability": "in_stock",
      "feed_id": "FD00009"
    }
  ],
  "next_cursor": null
}
```

### Optional filters

Use query parameters to refine results:

- `partner_name`
- `sku`
- `brand`
- `category`
- `availability`

---

## Troubleshooting
Use this section to identify and resolve common issues encountered during feed ingestion and ETL processing.

### Missing required fields

**Symptom**

- Rows are skipped

**Cause**

- Missing `sku` or `product_name`

**Resolution**

- Ensure all required fields are present

---

### Duplicate products

**Symptom**

- Products are updated instead of inserted

**Cause**

- Deduplication uses:

```
(partner_name, sku)
```

**Resolution**

- Use unique SKUs for new products
- Confirm whether updates are expected

---

### No products returned

**Symptom**

- Query returns no results

**Possible causes**

- Job has not completed
- Incorrect `feed_id`
- Filters exclude results

---

## How the Pipeline Works

The ingestion process includes four stages:

1. **Raw**

   - Stores the original CSV in S3

2. **Validation**

   - Verifies structure and required fields

3. **Transformation**

   - Maps CSV rows to the product schema
   - Normalizes data

4. **Load**

   - Inserts or updates products
   - Applies deduplication

---

## Summary

You:

- Uploaded a product feed
- Ran validation and ETL processing
- Reviewed ingestion results
- Verified products in the catalog

This workflow reflects a typical partner onboarding and feed ingestion process.
