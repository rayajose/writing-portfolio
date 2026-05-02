# How to Debug a Failed Feed

This guide walks through how to investigate and resolve issues when a product feed fails during validation or ETL processing.

This reflects a real-world troubleshooting scenario during partner onboarding or production ingestion.

---

## Overview

In this guide, you will:

1. Identify a failed feed or job
2. Retrieve validation and processing details
3. Interpret error messages and results
4. Fix common issues
5. Re-run processing and verify success

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

* A previously uploaded feed with a known `feed_id` or `job_id`

---

## Step 1: Identify the Failed Feed

Start by retrieving the feed details.

### Example Request

```bash
curl -X GET "http://localhost:8000/feeds/FD00009" \
  -H "x-api-key: demo-secret-key"
```

### Example Response

```json
{
  "feed_id": "FD00009",
  "partner_name": "Tronics",
  "file_name": "electronics_catalog.csv",
  "status": "failed",
  "validation_job_id": "JV00009",
  "validation_status": "failed",
  "validation_message": "Missing required field: sku"
}
```

### What to Look For

* `status = failed`
* `validation_status = failed`
* `validation_message` contains the root cause

---

## Step 2: Retrieve Job Details

Get more detailed processing results from the associated job.

### Example Request

```bash
curl -X GET "http://localhost:8000/jobs/JV00009" \
  -H "x-api-key: demo-secret-key"
```

### Example Response

```json
{
  "job_id": "JV00009",
  "status": "failed",
  "result": "Products processed: 10. Inserted: 0. Updated: 0. Unchanged: 0. Skipped: 10."
}
```

### What This Tells You

* All rows were skipped
* No valid records were processed
* The issue likely affects the entire file (schema or required fields)

---

## Step 3: Interpret Common Failure Scenarios

### Missing Required Fields

**Symptoms:**

* High `Skipped` count
* Validation message references missing fields

**Example:**

```
Missing required field: sku
```

**Fix:**
Ensure all rows include:

* `sku`
* `product_name`

---

### Invalid Data Format

**Symptoms:**

* Rows skipped or partially processed
* Unexpected values in output

**Examples:**

* Non-numeric price values
* Invalid availability values

**Fix:**
Validate data types and normalize values before upload.

---

### Duplicate Records

**Symptoms:**

* No new inserts
* High `Updated` or `Unchanged` counts

**Cause:**
Deduplication is based on:

```
(partner_name, sku)
```

**Fix:**

* Use unique SKUs for new products
* Confirm whether updates are expected

---

### Partial Success

**Symptoms:**

* Mix of `Inserted`, `Updated`, and `Skipped`

**Interpretation:**

* Some rows are valid
* Some rows failed validation

**Fix:**

* Review skipped rows
* Correct only the invalid records

---

## Step 4: Fix the Source File

Update the CSV file based on findings.

### Example Before (Invalid)

```csv
sku,product_name,price
,4K Smart TV,799.99
TV-002,,599.99
```

### Example After (Corrected)

```csv
sku,product_name,price
TV-001,4K Smart TV,799.99
TV-002,LED TV,599.99
```

---

## Step 5: Re-run Processing

After fixing the data, reprocess the feed.

### Option A: Re-run Existing Job

```bash
curl -X POST "http://localhost:8000/jobs/JV00009/run" \
  -H "x-api-key: demo-secret-key"
```

### Option B: Upload a New Feed

```bash
curl -X POST "http://localhost:8000/feeds/upload" \
  -H "x-api-key: demo-secret-key" \
  -F "file=@corrected_catalog.csv" \
  -F "partner_name=Tronics"
```

---

## Step 6: Verify Success

Check job results again.

```bash
curl -X GET "http://localhost:8000/jobs/JV00009" \
  -H "x-api-key: demo-secret-key"
```

### Example Successful Result

```json
{
  "job_id": "JV00009",
  "status": "completed",
  "result": "Products processed: 10. Inserted: 10. Updated: 0. Unchanged: 0. Skipped: 0."
}
```

---

## Debugging Checklist

Use this quick checklist when troubleshooting:

* Confirm required fields (`sku`, `product_name`)
* Validate data types (price, availability)
* Check for duplicate SKUs
* Review `validation_message`
* Compare processed vs skipped counts
* Re-run job after fixes

---

## What Happens Behind the Scenes

When a feed fails:

1. **Validation Layer**

   * Checks CSV structure and required fields
   * Generates validation errors

2. **ETL Processing**

   * Attempts to transform valid rows
   * Skips invalid rows

3. **Result Aggregation**

   * Summarizes inserted, updated, unchanged, skipped

4. **Status Update**

   * Marks job and feed as `failed` or `completed`

---

## Summary

You have successfully:

* Identified a failed feed
* Retrieved validation and job details
* Diagnosed the root cause
* Fixed data issues
* Reprocessed and verified results

This workflow represents a typical troubleshooting process for feed ingestion failures in the Partner Catalog API.
