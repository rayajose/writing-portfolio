# Debug failed feed runbook

Use this guide to investigate and fix a failed product feed during validation or ETL processing.
Use this workflow during partner onboarding or when troubleshooting production ingestion issues.

<div class="doc-meta">
  <span>Troubleshooting</span>
  <span>Operations</span>
  <span>ETL processing</span>
  <span>Support workflow</span>
</div>

## Overview

In this guide, you will:

1. Identify the failed feed or job
2. Retrieve validation and ETL processing details
3. Interpret error messages
4. Fix data issues
5. Re-run processing and verify results

!!! note "Operational troubleshooting"

    Feed validation and ETL processing failures are commonly caused by schema inconsistencies, missing required fields, or invalid source data.

## Prerequisites

| Requirement         | Description                                                         |
| ------------------- | ------------------------------------------------------------------- |
| Base URL (local)    | `http://localhost:8000`                                             |
| Base URL (AWS)      | `http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com` |
| API key             | `x-api-key: demo-secret-key`                                        |
| Completed operation | Uploaded feed (`feed_id`) or job (`job_id`)                         |

!!! tip "Preserve failed files"

    Retaining the original uploaded CSV file can help compare corrected data against the initial failed ingestion attempt.

## 1. Identify the failed feed

Retrieve the feed to confirm its status.

### Request

```bash
curl -X GET "http://localhost:8000/feeds/FD00009" \
  -H "x-api-key: demo-secret-key"
```

### Response

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

### What to look for

- `status: failed`
- `validation_status: failed`
- `validation_message` describing the issue


## 2. Retrieve job details

Get ETL processing results for the associated job.

### Request

```bash
curl -X GET "http://localhost:8000/jobs/JV00009" \
  -H "x-api-key: demo-secret-key"
```

### Response

```json
{
  "job_id": "JV00009",
  "status": "failed",
  "result": "Products processed: 10. Inserted: 0. Updated: 0. Unchanged: 0. Skipped: 10."
}
```

### Interpret the result

- All rows were skipped
- No records were inserted or updated
- The issue likely affects the entire file (schema or required fields)

!!! warning "High skipped counts"

    Large skipped-record counts typically indicate schema-level or required-field issues affecting multiple rows within the uploaded feed.

## 3. Diagnose the failure

Use the patterns below to identify common issues.

### Missing required fields

**Symptoms**

- High `Skipped` count
- Validation message references missing fields

**Example**

```
Missing required field: sku
```

**Fix**

Ensure every row includes:

- `sku`
- `product_name`


### Invalid data format

**Symptoms**

- Rows skipped or partially processed
- Unexpected values in results

**Examples**

- Non-numeric `price`
- Invalid `availability` values

**Fix**

Validate data types and normalize values before upload.


### Duplicate records

**Symptoms**

- No new inserts
- High `Updated` or `Unchanged` counts

**Cause**

Deduplication uses:

```text
(partner_name, sku)
```

**Fix**

- Use unique SKUs for new products
- Confirm whether updates are expected

!!! note "Idempotent processing"

    Existing product records are updated only when incoming feed data changes, reducing unnecessary database updates during recurring feed ingestion.

### Partial success

**Symptoms**

- Mix of `Inserted`, `Updated`, and `Skipped`

**Interpretation**

- Some rows are valid
- Some rows failed validation

**Fix**

- Review skipped rows
- Correct only invalid records


## 4. Fix the source file

Update the CSV file based on the identified issue.

### Invalid example

```csv
sku,product_name,price
,4K Smart TV,799.99
TV-002,,599.99
```

### Corrected example

```csv
sku,product_name,price
TV-001,4K Smart TV,799.99
TV-002,LED TV,599.99
```


## 5. Re-run ETL processing

After fixing the data, reprocess the feed.

!!! tip "Safe reprocessing"

    ETL processing can be safely re-run after correcting source data without creating duplicate product records.

### Re-run the existing job

```bash
curl -X POST "http://localhost:8000/jobs/JV00009/run" \
  -H "x-api-key: demo-secret-key"
```

### Upload a new feed

```bash
curl -X POST "http://localhost:8000/feeds/upload" \
  -H "x-api-key: demo-secret-key" \
  -F "file=@corrected_catalog.csv" \
  -F "partner_name=Tronics"
```


## 6. Verify success

Retrieve the job again to confirm successful ETL processing.

```bash
curl -X GET "http://localhost:8000/jobs/JV00009" \
  -H "x-api-key: demo-secret-key"
```

### Successful response

```json
{
  "job_id": "JV00009",
  "status": "completed",
  "result": "Products processed: 10. Inserted: 10. Updated: 0. Unchanged: 0. Skipped: 0."
}
```


## Debugging checklist

Use this checklist when troubleshooting:

- Confirm required fields (`sku`, `product_name`)
- Validate data types (`price`, `availability`)
- Check for duplicate SKUs
- Review `validation_message`
- Compare processed vs skipped counts
- Re-run the job after fixes


## How the system processes a feed

When a feed is processed:

1. **Validation**

   - Checks CSV structure and required fields
   - Generates validation errors

2. **ETL processing**

   - Transforms valid rows
   - Skips invalid rows

3. **Result aggregation**

   - Counts inserted, updated, unchanged, and skipped records

4. **Status update**

   - Sets job and feed status to `failed` or `completed`

!!! note "Processing visibility"

    Job status values and ETL summaries provide operational visibility into validation failures, skipped rows, and successful product updates.

## Summary

In this workflow, you:

- Identified the failed feed
- Retrieved validation and job details
- Diagnosed the issue
- Fixed the data
- Reprocessed and verified the results

This workflow reflects a typical troubleshooting process for feed ingestion failures.
