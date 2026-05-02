# Ingesting a Product Feed End-to-End

This guide walks through the complete process of ingesting a partner product feed into the Partner Catalog API—from upload through validation, ETL processing, and final verification.

This represents a typical partner onboarding workflow.

---

## Overview

In this guide, you will:

1. Upload a product feed (CSV)
2. Trigger validation and ETL processing
3. Review processing results
4. Verify products were successfully ingested

---

## Prerequisites

* API base URL:

  ```
  http://localhost:8000
  ```

  or

  ```
  http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com
  ```

* API key:

  ```
  x-api-key: demo-secret-key
  ```

* A valid CSV file with required fields:

  * `sku`
  * `product_name`

---

## Step 1: Upload a Product Feed

Upload a CSV file using the `/feeds/upload` endpoint.

### Example Request

```bash
curl -X POST "http://localhost:8000/feeds/upload" \
  -H "x-api-key: demo-secret-key" \
  -F "file=@electronics_catalog.csv" \
  -F "partner_name=Tronics"
```

### Example Response

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

### What Happens

* The file is stored in S3 (raw layer)
* A validation job is created
* Feed status is set to `uploaded`
* ETL processing is queued

---

## Step 2: Run ETL Processing

If ETL is not automatically triggered, run the validation job manually.

### Example Request

```bash
curl -X POST "http://localhost:8000/jobs/JV00009/run" \
  -H "x-api-key: demo-secret-key"
```

### Example Response

```json
{
  "job_id": "JV00009",
  "status": "completed",
  "message": "ETL processing completed."
}
```

### What Happens

During ETL:

* CSV structure is validated
* Required fields are checked
* Data is transformed into product records
* Records are inserted or updated in the database
* Invalid rows are skipped

---

## Step 3: Review Processing Results

Retrieve job details to understand what happened during ingestion.

### Example Request

```bash
curl -X GET "http://localhost:8000/jobs/JV00009" \
  -H "x-api-key: demo-secret-key"
```

### Example Response

```json
{
  "job_id": "JV00009",
  "status": "completed",
  "result": "Products processed: 13. Inserted: 1. Updated: 5. Unchanged: 7. Skipped: 0."
}
```

### Result Fields Explained

* **Processed**: Total rows evaluated from the CSV
* **Inserted**: New products added
* **Updated**: Existing products where data changed (e.g., price, availability)
* **Unchanged**: Existing products with no data changes
* **Skipped**: Rows missing required fields or invalid

---

## Step 4: Verify Products

Confirm that products were successfully ingested.

### Example Request

```bash
curl -X GET "http://localhost:8000/products?feed_id=FD00009" \
  -H "x-api-key: demo-secret-key"
```

### Example Response

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

### Optional Filters

You can refine results using query parameters:

* `partner_name`
* `sku`
* `brand`
* `category`
* `availability`

---

## Common Issues and Troubleshooting

### Missing Required Fields

**Problem:**
Rows are skipped during processing.

**Cause:**
Missing `sku` or `product_name`.

**Solution:**
Ensure all required fields are present in the CSV.

---

### Duplicate Products

**Problem:**
Products are updated instead of inserted.

**Cause:**
Deduplication is based on:

```
(partner_name, sku)
```

**Solution:**
Ensure SKUs are unique per partner if new products are expected.

---

### No Products Returned

**Problem:**
Query returns empty results.

**Possible Causes:**

* ETL job not completed
* Incorrect `feed_id`
* Filters excluding results

---

## What Happens Behind the Scenes

This workflow follows a simple data pipeline:

1. **Raw Layer**

   * CSV stored in S3
   * Source data preserved

2. **Validation Layer**

   * Structure and required fields checked
   * Invalid rows flagged or skipped

3. **Transformation Layer**

   * CSV rows mapped to product schema
   * Data normalized

4. **Load Layer**

   * Products inserted or updated in database
   * Deduplication applied

---

## Summary

You have successfully:

* Uploaded a partner product feed
* Executed validation and ETL processing
* Interpreted ingestion results
* Verified product data in the system

This workflow represents a typical partner onboarding and data ingestion process for the Partner Catalog API.
