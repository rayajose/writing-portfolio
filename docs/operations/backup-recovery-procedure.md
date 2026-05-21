# Backup and recovery runbook

This procedure defines backup, recovery, replay, and operational restoration workflows for the Commerce Integration API platform.

The procedure supports operational continuity by preserving raw feed data, processed application data, and workflow metadata required for troubleshooting and recovery.

<div class="doc-meta">
  <span>Business continuity</span>
  <span>Disaster recovery</span>
  <span>Backup operations</span>
  <span>Recovery procedures</span>
</div>

## Purpose

The purpose of this procedure is to:

- Support recovery from processing failures
- Preserve raw feed data for replay workflows
- Protect processed product and order data
- Protect customer and shipping address records
- Support operational troubleshooting
- Reduce data loss risk
- Maintain traceability across recovery activities


## Scope

This procedure applies to:

- Uploaded feed files
- Feed and job metadata
- Product, customer, address, and order records
- ETL processing summaries
- PostgreSQL database resources
- Amazon S3 raw feed storage
- Operational recovery workflows


## Backup architecture

The platform separates recoverable data across raw and processed storage layers.

| Data type                | Storage location | Recovery purpose                     |
| ------------------------ | ---------------- | ------------------------------------ |
| Raw feed files           | Amazon S3        | Feed replay and reprocessing         |
| Product records          | PostgreSQL       | Product catalog restoration          |
| Customer records         | PostgreSQL       | Customer workflow restoration        |
| Customer address records | PostgreSQL       | Shipping workflow restoration        |
| Order records            | PostgreSQL       | Order history restoration            |
| Feed metadata            | PostgreSQL       | Ingestion traceability               |
| Job metadata             | PostgreSQL       | Processing recovery and auditability |
| ETL summaries            | PostgreSQL       | Troubleshooting and verification     |


## Raw feed recovery

Raw uploaded feed files are retained in Amazon S3.

Example object structure:

```text
raw/partners/{partner_name}/feeds/{feed_id}/{filename}.csv
```

Raw feed retention supports:

- Reprocessing failed ingestion workflows
- Recovering from ETL processing failures
- Troubleshooting validation issues
- Preserving feed-level traceability


## Database backup considerations

PostgreSQL stores processed application data and operational metadata.

Database recovery planning should account for:

- Product records
- Customer records
- Customer address records
- Order records
- Feed records
- Job records
- ETL summaries
- Identifier counters

Database backups should be captured before major schema changes or production-style deployments.


## Recovery scenarios

### Failed ETL processing

Use this workflow when a validation or ETL job fails.

1. Review the failed job status.
2. Review the ETL summary or validation message.
3. Confirm the raw feed file is available in Amazon S3.
4. Correct the source data or processing issue.
5. Re-run the job using the Jobs API.
6. Verify job status changes to `completed`.
7. Validate product records and ETL summary results.


### Database connectivity failure

Use this workflow when the application cannot connect to PostgreSQL.

1. Confirm RDS instance status.
2. Verify security group rules.
3. Confirm ECS task networking configuration.
4. Verify database environment variables.
5. Restart or redeploy the ECS task if required.
6. Confirm the `/health` endpoint returns successfully.


### Deployment-related failure

Use this workflow when a deployment introduces application instability.

1. Review ECS task status.
2. Review ALB target health.
3. Validate container startup behavior.
4. Confirm database connectivity.
5. Redeploy a known-good image or task definition if required.
6. Verify API and ETL workflows after recovery.


### Data processing inconsistency

Use this workflow when processed records do not match expected feed results.

1. Identify the affected feed.
2. Review associated job records.
3. Confirm ETL summary counts.
4. Verify the raw feed file in Amazon S3.
5. Reprocess the feed if needed.
6. Validate product query results after reprocessing.

### Customer workflow recovery

Use this workflow when customer or shipping workflows become inconsistent or unavailable.

1. Confirm database connectivity.
2. Verify customer and address records exist.
3. Confirm encryption configuration is available.
4. Verify `PII_ENCRYPTION_KEY` environment configuration.
5. Validate customer API responses.
6. Confirm masked response behavior.
7. Validate associated order workflows.

## Replay workflow

Replay workflows use retained raw feed data to reprocess ingestion activity.

### Replay prerequisites

Before replaying a feed:

- Confirm the raw S3 object exists
- Confirm the associated feed record exists
- Confirm the validation job is available
- Confirm database connectivity
- Confirm the processing issue has been corrected

### Replay steps

1. Locate the validation job ID for the feed.
2. Run the job using the Jobs API:

```text
POST /jobs/{job_id}/run
```

3. Monitor job status.
4. Review ETL summary results.
5. Validate product records through the Products API.


## Recovery verification

After any recovery workflow, verify platform health and data consistency.

Verification activities include:

- Confirm `/health` endpoint status
- Confirm job status is `completed`
- Review ETL processing summary
- Validate product records
- Validate customer records
- Validate shipping address records
- Confirm masked customer response behavior
- Validate order records when applicable
- Confirm analytics endpoints return expected results
- Confirm no unexpected duplicate records were created


## Data integrity considerations

Recovery workflows should preserve data integrity across ingestion and processing operations.

Important considerations include:

- Referential integrity between customers, addresses, and orders
- Preservation of encrypted customer-sensitive fields
- Product uniqueness by partner and SKU
- Idempotent feed reprocessing
- Controlled ETL execution
- Traceable job lifecycle history
- Raw feed retention in S3
- Processed data consistency in PostgreSQL

Product uniqueness is enforced using:

```text
(partner_name, sku)
```


## Backup responsibilities

### Platform administrators

Responsible for:

- Database backup planning
- Infrastructure recovery
- ECS and RDS availability
- Deployment rollback coordination

### Integration operators

Responsible for:

- Feed replay coordination
- Job status review
- ETL summary validation
- Recovery workflow verification

### Developers

Responsible for:

- Fixing processing defects
- Validating application behavior
- Supporting recovery testing
- Maintaining idempotent processing behavior


## Recovery principles

The platform follows these recovery principles:

- Preserve raw source data whenever possible
- Reprocess from retained raw feeds when needed
- Validate recovery outcomes through API responses
- Maintain traceability across recovery activities
- Avoid duplicate processing side effects
- Preserve customer-sensitive data protections during recovery
- Verify system health after recovery


## Related documentation

- [Operations](index.md)
- [Deployment change procedure](deployment-change-procedure.md)
- [Debug failed feed runbook](debug-product-feed.md)
- [Data retention and handling policy](../security/data-retention-policy.md)
- [Logging and monitoring policy](../security/logging-monitoring-policy.md)
- [Customers API](../api/customers.md)
- [Encryption policy](../security/encryption-policy.md)
- [Customer data handling policy](../security/customer-data-handling-policy.md)
- [Platform architecture and operational flow](../architecture/platform-architecture.md)