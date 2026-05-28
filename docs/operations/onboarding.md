# Partner feed onboarding

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

- Upload a partner feed
- Create submission and validation jobs
- Validate and process feed data through ETL workflows
- Store normalized products in PostgreSQL
- Make products available through the API
- Support downstream customer and order workflows


## Procedure


### Step 1. Upload a partner feed

Submit the product feed using the upload endpoint.

```bash
curl -X POST http://api.example.com/feeds/upload \
  -H "x-api-key: YOUR_API_KEY" \
  -F "partner_name=Acme Corp" \
  -F "file=@sample_catalog.csv"
```


### Processing behavior

- A `feed_id` is generated
- A submission job (`JSxxxxx`) is created
- A validation job (`JVxxxxx`) is queued


### Example response

```json
{
  "feed_id": "FD00001",
  "status": "processing",
  "job_id": "JS00001"
}
```


### Step 2. Verify feed registration

Retrieve the feed to confirm successful registration.

```bash
curl -X GET http://api.example.com/feeds/FD00010 \
  -H "x-api-key: YOUR_API_KEY"
```


### Validation checks

Verify that:

- `status` is `uploaded` or `validating`
- `validation_job_id` is present
- `partner_name` and `file_name` match the uploaded feed


### Step 3. Monitor validation job

Retrieve the validation job status.

```bash
curl -X GET http://api.example.com/jobs/JV00010 \
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


### Step 4. Review validation results

After the job reaches `completed`, review the ETL summary.

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


### Step 5. Verify product availability

Confirm that products are accessible through the API.

```bash
curl -X GET \
  "http://api.example.com/products?partner_name=Acme%20Corp" \
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

- Partner products are available through the `/products` endpoint
- Feed status is `validated`
- Product data is persisted in PostgreSQL
- Partners can submit future feed updates
- Products are available for downstream order workflows
- Product data is queryable through analytics endpoints


## Additional details

- Re-running validation on the same feed does not create duplicate products
- Product uniqueness is enforced using `(partner_name, sku)`
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

- [API and integrations](../api/index.md)
- [Integration guide](../api/integration-guide.md)
- [Products](../api/products.md)
- [Customers](../api/customers.md)
- [Orders](../api/orders.md)
- [Security and compliance](../security/index.md)