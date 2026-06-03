# Partner onboarding

## Purpose

This page defines the process for onboarding a new partner product feed into the platform.

## Scope

This process applies to:

- New partner integrations
- Initial product feed ingestion
- Validation and activation of partner data

This process is intended for operations teams, integration engineers, and support personnel.

## Preconditions

Before starting, confirm the following:

- The partner has provided a valid CSV product feed
- Required fields are present (`sku` and `product_name` minimum)
- API access is available
- The target environment is identified (`test` or `production`)

## Workflow overview

The onboarding workflow performs the following operations:

- Create a partner record
- Assign a unique partner identifier
- Upload a partner feed
- Create submission and validation jobs
- Validate and process feed data through ETL workflows
- Store normalized products in PostgreSQL
- Make products available through the API
- Support downstream customer and order workflows

## Procedure

### Step 1. Create a partner

Create a partner record before uploading product feeds.

For endpoint details, request parameters, response fields, and error handling information, see [POST /partners](../api/partners.md#post-partners).

```bash
curl -X POST http://<base-url>/partners \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "partner_name": "Acme Corp",
    "contact_email": "integrations@acme.example"
  }'
```

### Processing behavior

- A partner record is created
- A unique partner identifier (`PTxxxxx`) is assigned
- The partner becomes available for feed submissions

### Example response

```json
{
  "partner_id": "PT00001",
  "partner_name": "Acme Corp",
  "status": "active"
}
```

### Step 2. Upload a partner feed

Submit the product feed using the upload endpoint.

For endpoint details, request parameters, response fields, and error handling information, see [POST /feeds/upload](../api/feeds.md#post-feedsupload).

```bash
curl -X POST http://<base-url>/feeds/upload \
  -H "x-api-key: YOUR_API_KEY" \
  -F "partner_id=PT00001" \
  -F "file=@sample_catalog.csv"
```

### Processing behavior

- A `feed_id` is generated
- A submission job (`JSxxxxx`) is created
- A validation job (`JVxxxxx`) is queued
- ETL processing begins asynchronously

### Example response

```json
{
  "feed_id": "FD00001",
  "status": "processing",
  "job_id": "JS00001"
}
```

### Step 3. Verify feed registration

Retrieve the feed to confirm successful registration.

For endpoint details, request parameters, response fields, and error handling information, see [GET /feeds/{feed_id}](../api/feeds.md#get-feedsfeed_id).

```bash
curl -X GET http://<base-url>/feeds/FD00010 \
  -H "x-api-key: YOUR_API_KEY"
```

### Validation checks

Verify that:

- `status` is `uploaded` or `processing`
- `validation_job_id` is present
- The feed is associated with the expected partner
- `file_name` matches the uploaded feed

### Step 4. Monitor validation job

Retrieve the validation job status.

For endpoint details, request parameters, response fields, and error handling information, see [GET /jobs/{job_id}](../api/jobs.md#get-jobsjob_id).

```bash
curl -X GET http://<base-url>/jobs/JV00010 \
  -H "x-api-key: YOUR_API_KEY"
```

### Expected status flow

```text
queued → running → completed
```

If processing fails, the job status becomes:

```text
failed
```

### Step 5. Review validation results

After the job reaches `completed`, review the ETL summary.

For response field descriptions, see [GET /feeds/{feed_id}, Response fields](../api/feeds.md#response-fields_1).

### Example response

```json
{
  "status": "completed",
  "message": "Products processed: 100. Inserted: 80. Updated: 10. Unchanged: 5. Skipped: 5."
}
```

### Result definitions

| Result    | Description                                    |
| --------- | ---------------------------------------------- |
| Inserted  | New products added                             |
| Updated   | Existing products updated because data changed |
| Unchanged | Existing products matched incoming data        |
| Skipped   | Invalid rows or rows missing required fields   |

### Step 6. Verify product availability

Confirm that products are accessible through the API and associated with the expected partner.

For endpoint details, request parameters, response fields, and error handling information, see [GET /products](../api/products.md#get-products).

```bash
curl -X GET \
  "http://<base-url>/products?partner_name=Acme%20Corp" \
  -H "x-api-key: YOUR_API_KEY"
```

### Validation checks

Verify that:

- Products are returned for the correct partner
- Key fields are populated
- Record counts align with the ETL summary
- Products are available for downstream order workflows

## Decision points

### Validation failed

If validation fails:

1. Review the job response error message
2. Verify CSV formatting and required fields
3. Correct feed issues
4. Re-upload the feed

### High skipped-row count

If the skipped count is unexpectedly high:

1. Inspect skipped rows for invalid or missing values
2. Verify required fields such as `sku` and `product_name`
3. Coordinate with the partner to correct source data

### Products not returned

If products are not returned through the API:

1. Confirm that ETL processing completed successfully
2. Verify product query filters
3. Review ingestion logs and database connectivity

## Results

After successful onboarding:

- A partner record exists and is available for future feed submissions
- Partner products are available through the `/products` endpoint
- Feed status is `validated`
- Product data is persisted in PostgreSQL
- Partners can submit future feed updates
- Products are available for downstream order workflows
- Product data is queryable through analytics endpoints

## Additional details

- Re-running validation on the same feed does not create duplicate products
- Product uniqueness is enforced using the partner and SKU combination
- Products are updated only when data changes are detected
- Raw uploaded files are retained for replay and troubleshooting workflows
- Feed ingestion supports downstream transactional order workflows
- Product records may later be associated with customer-linked orders

## Security considerations

- API access requires authenticated requests using `x-api-key`
- Raw uploaded files should remain restricted to authorized workflows
- Customer-sensitive workflows are separated from ingestion workflows
- Operational logs should avoid storing credentials or secrets

## Related documentation

- [Integration guide](../architecture/integration-guide.md)
- [Partners](../api/partners.md)
- [Products](../api/products.md)
- [Customers](../api/customers.md)
- [Orders](../api/orders.md)
- [Security and compliance](../security/index.md)
