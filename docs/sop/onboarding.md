# Partner Feed Onboarding SOP

## Purpose

This document defines the standard process for onboarding a new partner product feed into the platform. It ensures consistent ingestion, validation, and availability of partner data while minimizing errors and operational risk.

---

## Scope

This procedure applies to:

* New partner integrations
* Initial product feed ingestion
* Validation and activation of partner data

It is intended for use by operations teams, integration engineers, and support personnel.

---

## Preconditions

Before starting, confirm the following:

* Partner has provided a valid CSV product feed
* Required fields are present (minimum: `sku`, `product_name`)
* API access is available (API key configured)
* Target environment is identified (test or production)

---

## Procedure

### Step 1 — Upload Partner Feed

Submit the product feed using the upload endpoint.

```bash
curl -X POST "http://<host>/feeds/upload" \
  -H "x-api-key: <api-key>" \
  -F "partner_name=<partner_name>" \
  -F "file=@<file_name>.csv"
```

---

### Expected Result

* A `feed_id` is generated
* A submission job (`JSxxxxx`) is created
* A validation job (`JVxxxxx`) is queued

Example response:

```json
{
  "feed_id": "FD00010",
  "status": "uploaded",
  "validation_job_id": "JV00010"
}
```

---

### Step 2 — Verify Feed Registration

Retrieve the feed to confirm it was successfully registered.

```bash
curl -H "x-api-key: <api-key>" \
  "http://<host>/feeds/FD00010"
```

---

### Validation Checks

* `status` should be `uploaded` or `validating`
* `validation_job_id` should be present
* `partner_name` and `file_name` should match input

---

### Step 3 — Monitor Validation Job

Check the status of the validation job.

```bash
curl -H "x-api-key: <api-key>" \
  "http://<host>/jobs/JV00010"
```

---

### Expected Status Flow

* `queued` → `in_progress` → `completed`
* If errors occur: `failed`

---

### Step 4 — Review Validation Results

Once the job is `completed`, review the ETL summary.

Example:

```json
{
  "status": "completed",
  "message": "Products processed: 100. Inserted: 80. Updated: 10. Unchanged: 5. Skipped: 5."
}
```

---

### Interpretation

* **Inserted** — New products added
* **Updated** — Existing products modified (data changes detected)
* **Unchanged** — No changes from existing records
* **Skipped** — Invalid rows (missing required fields or malformed data)

---

### Step 5 — Validate Product Availability

Confirm that products are accessible via the API.

```bash
curl -H "x-api-key: <api-key>" \
  "http://<host>/products?partner_name=<partner_name>"
```

---

### Validation Checks

* Products are returned for the correct partner
* Key fields (SKU, name, price, availability) are populated
* Record counts align with ETL summary

---

## Decision Points

### If Validation Fails

* Review error message from job response
* Check CSV format and required fields
* Correct issues and re-upload feed

---

### If High Skip Count

* Inspect skipped rows for missing or invalid data
* Confirm required fields (`sku`, `product_name`) are present
* Coordinate with partner to correct source data

---

### If Products Not Returned

* Confirm ETL job completed successfully
* Verify filters in product query
* Check database connectivity or ingestion logs

---

## Post-Conditions

After successful onboarding:

* Partner products are available via `/products` endpoint
* Feed status is `validated`
* Data is persisted in the system
* Partner can perform subsequent updates via feed re-submission

---

## Operational Notes

* Re-running validation on the same feed should not create duplicates
* Product uniqueness is enforced by `(partner_name, sku)`
* Updates are only counted when actual data changes occur
* Raw files are stored for traceability and reprocessing

---

## Related Documentation

* API Overview: `/api/index.md`
* Workflows: `/workflows.md`
* Products Endpoint: `/products.md`

---

## What This Demonstrates

This SOP reflects:

* Ability to document repeatable operational processes
* Understanding of ETL workflows and data validation
* Clear handling of success and failure scenarios
* Alignment between API behavior and operational procedures

It is designed to reduce onboarding friction, standardize execution, and support scalable partner integrations.
