# Partner feed onboarding

## Purpose

This page defines the process for onboarding a new partner product feed into the platform.

---

## Scope

This process applies to the following scenarios:

- New partner integrations
- Initial product feed ingestion
- Validation and activation of partner data

It is intended for use by operations teams, integration engineers, and support personnel.

---

## Preconditions

Before starting, confirm the following:

- Partner has provided a valid CSV product feed
- Required fields are present (minimum: `sku`, `product_name`)
- API access is available (API key configured)
- Target environment is identified (test or production)

---

## What happens

- Upload a partner feed  
- Create submission and validation jobs  
- Validate and process data through ETL  
- Store products in the database  
- Make products available via the API  

---

## Procedure

### Step 1: Upload partner feed

Submit the product feed using the upload endpoint.

```bash
curl -X POST "http://api.example.com/feeds/upload" \
  -H "x-api-key: <api-key>" \
  -F "partner_name=<partner_name>" \
  -F "file=@<file_name>.csv"
```

---

### What happens

- A `feed_id` is generated
- A submission job (`JSxxxxx`) is created
- A validation job (`JVxxxxx`) is queued

Example response:

```json
{
  "feed_id": "FD00010",
  "status": "uploaded",
  "validation_job_id": "JV00010"
}
```

---

### Step 2: Verify feed registration

Retrieve the feed to confirm it was successfully registered.

```bash
curl -H "x-api-key: <api-key>" \
  "http://api.example.com/feeds/FD00010"
```

---

### Validation checks

- `status` is `uploaded` or `validating`
- `validation_job_id` is present
- `partner_name` and `file_name` should match input

---

### Step 3: Monitor validation job

Check the status of the validation job.

```bash
curl -H "x-api-key: <api-key>" \
  "http://api.example.com/jobs/JV00010"
```

---

### Expected status flow

- `queued` → `running` → `completed`
- If errors occur: `failed`

---

### Step 4: Review validation results

Once the job is `completed`, review the ETL summary.

Example:

```json
{
  "status": "completed",
  "message": "Products processed: 100. Inserted: 80. Updated: 10. Unchanged: 5. Skipped: 5."
}
```

---

### What the results mean

- **Inserted**: New products added
- **Updated**: Existing products modified (data changes detected)
- **Unchanged**: No changes from existing records
- **Skipped**: Invalid rows (missing required fields or malformed data)

---

### Step 5: Validate product availability

Confirm that products are accessible via the API.

```bash
curl -H "x-api-key: <api-key>" \
  "http://api.example.com/products?partner_name=<partner_name>"
```

---

### Validation checks

- Products are returned for the correct partner
- Key fields (SKU, name, price, availability) are populated
- Record counts align with ETL summary

---

## Decision points

### If validation fails

- Review the error message from the job response
- Check CSV format and required fields
- Correct issues and re-upload feed

---

### If high skip count

- Inspect skipped rows for missing or invalid data
- Confirm required fields (`sku`, `product_name`) are present
- Coordinate with partner to correct source data

---

### If products not returned

- Confirm ETL job completed successfully
- Verify filters in product query
- Check database connectivity or ingestion logs

---

## Results

After successful onboarding:

- Partner products are available via `/products` endpoint
- Feed status is `validated`
- Data is persisted in the system
- Partner can perform subsequent updates via feed re-submission

---

## Additional details

- Re-running validation on the same feed should not create duplicates
- Product uniqueness is enforced by `(partner_name, sku)`
- Updates are only counted when actual data changes occur
- Raw files are stored for traceability and reprocessing

---

## Related documentation

- [API Overview](../api/index.md)
- [Workflows](../api/workflows.md)
- [Products Endpoint](../api/products.md)