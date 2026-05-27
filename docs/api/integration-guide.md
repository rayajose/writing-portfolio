# Integration guide

Use this guide to build a commerce data integration workflow using the Commerce Integration API.

The platform supports ingestion-driven commerce workflows using ETL processing, asynchronous job execution, customer and order management workflows, analytics aggregation, and cloud-native infrastructure patterns.

<div class="doc-meta">
  <span>Partner integration</span>
  <span>REST</span>
  <span>JSON</span>
  <span>Workflow guide</span>
</div>


## Overview

The Commerce Integration API supports the following integration workflow:

1. Prepare a partner product feed
2. Upload the feed
3. Monitor validation and ETL processing
4. Query product data
5. Create fictional customer and shipping address records
6. Create and retrieve order data
7. Retrieve analytics data


## When to use this guide

Use this guide to design, implement, or document a repeatable commerce data integration workflow.

This guide explains how ingestion, ETL, catalog retrieval, customer workflows, order processing, and analytics workflows interact across the platform.

For a step-by-step walkthrough of a single feed upload, see [Ingest a product feed end-to-end](ingest-product-feed.md).

For complete endpoint details, see:

- [Feeds](feeds.md)
- [Jobs](jobs.md)
- [Products](products.md)
- [Customers](customers.md)
- [Orders](orders.md)
- [Analytics](analytics.md)


## Integration architecture

The Commerce Integration API uses an asynchronous ingestion pipeline designed to support large partner product feeds and long-running processing workflows.

When a partner uploads a feed:

1. The raw CSV file is stored in Amazon S3
2. A feed record is created
3. A validation job verifies file structure and required fields
4. ETL processing transforms and loads product data into PostgreSQL
5. Products become available through query endpoints
6. Fictional customer and shipping address records can be created
7. Orders can be created from catalog products
8. Analytics endpoints aggregate transactional data

<div class="diagram-card" markdown="1">
![Integration architecture](../api/screenshots/integration-architecture.svg)
</div>


## Asynchronous processing

Feed ingestion occurs asynchronously. Uploading a feed does not immediately make products available in the catalog.

Integrations should:

- Track validation and ETL status
- Handle delayed processing
- Retry failed operations when appropriate
- Avoid assuming immediate catalog availability after upload

!!! note "Eventual consistency"

    Product data may not be immediately available after feed upload because validation and ETL processing occur asynchronously.


## Scalability considerations

The ingestion pipeline is designed to support scalable commerce data processing across multiple partner integrations and large product catalogs.

Key characteristics include:

- Asynchronous ingestion workflows
- Independent validation and ETL processing
- Support for large batch product feeds
- Incremental catalog update workflows
- Replay support for failed processing operations
- Decoupled storage and processing layers


## Integration design

Before implementing a partner integration, define how product feeds will be generated, validated, monitored, and consumed by downstream systems.


### Feed delivery

Determine how partners will provide catalog updates.

Common approaches include:

- Full catalog feeds submitted on a schedule
- Incremental feeds containing only changed products
- Event-driven uploads triggered by inventory or pricing changes

Large catalogs may require batching or scheduled uploads to reduce processing overhead.


### Data validation

Validate feed files before upload whenever possible.

Recommended validations include:

- Required header verification
- CSV format validation
- Duplicate SKU detection
- Price and currency formatting validation
- Availability value normalization

!!! warning "Pre-validation"

    Performing validation before upload reduces failed ETL jobs and unnecessary processing.


### Job monitoring

Because ingestion occurs asynchronously, integrations should monitor validation and ETL job status throughout processing.

Recommended practices include:

- Polling job status endpoints at scheduled intervals
- Logging failed jobs for troubleshooting
- Alerting on repeated validation or ETL failures
- Tracking processing duration for large feeds


### Product retrieval

Determine how downstream systems will retrieve product data.

For large catalogs:

- Use pagination
- Filter results whenever possible
- Avoid unnecessary full catalog retrievals
- Cache frequently requested product data when appropriate


### Order processing

Orders are created transactionally using catalog product data.

During order creation:

- Product availability is validated
- Product pricing is copied into each order item
- Line totals are calculated at order creation time
- Order totals are calculated from associated order items

!!! tip "Transactional consistency"

    Product pricing is copied into order records during order creation to preserve historical transactional accuracy.


### Customer workflows

Customer and shipping address records support transactional order workflows.

The following customer-sensitive fields are encrypted before storage:

- Email addresses
- Phone numbers
- Street addresses
- Postal codes

API responses return masked values instead of raw customer-sensitive values.

This demonstrates field-level encryption and controlled exposure of customer-sensitive data.


### Analytics

Analytics endpoints provide:

- Partner revenue reporting
- Product performance analysis
- Operational dashboards
- Feed processing reconciliation
- Sales trend analysis

Analytics endpoints aggregate data from orders, products, and transactional workflows.


## ETL processing behavior

After validation completes successfully, the ETL pipeline transforms and loads product data into the catalog database.

During processing, each product row is evaluated independently to determine whether the product should be inserted, updated, left unchanged, or skipped.


### ETL result definitions

| Result    | Description                                                                                |
| --------- | ------------------------------------------------------------------------------------------ |
| Inserted  | A new product was created because the partner and SKU combination did not previously exist |
| Updated   | An existing product was updated because one or more fields changed                         |
| Unchanged | An existing product matched the incoming data and required no update                       |
| Skipped   | The row failed validation or required field checks                                         |


### Change detection

The ETL pipeline performs change detection to avoid unnecessary database updates.

For existing products, the system compares incoming values against the current catalog record. Products are updated only when one or more fields change.

Benefits include:

- Reduced database writes
- Improved processing efficiency
- Reduced downstream synchronization overhead
- More accurate update tracking

Because unchanged products are not rewritten, repeated feed submissions support idempotent processing behavior.

!!! note "Idempotent ETL behavior"

    Existing products are updated only when incoming feed data changes.


## Error handling and resilience

Integrations should account for validation failures, ETL processing issues, malformed product data, delayed processing, and order creation failures.

Because feed ingestion is asynchronous, failures may occur after a successful upload response is returned.


### Common failure scenarios

| Scenario                  | Description                                                 |
| ------------------------- | ----------------------------------------------------------- |
| Invalid CSV format        | The uploaded file does not meet CSV formatting requirements |
| Missing required headers  | Required fields such as `sku` or `product_name` are missing |
| Invalid product data      | Product rows contain malformed or unsupported values        |
| ETL processing failure    | An internal processing error prevents product ingestion     |
| Product unavailable       | A requested product cannot be used to create an order       |
| Missing order resource    | A requested order does not exist                            |
| Missing customer resource | A referenced customer or shipping address does not exist    |
| Authentication failure    | The request does not include a valid API key                |


### Recommended practices

Implementations should:

- Log upload, job, product, and order identifiers
- Monitor validation and ETL job status
- Retry failed uploads when appropriate
- Alert on repeated processing failures
- Retain source feed files for replay workflows
- Avoid logging raw customer-sensitive values
- Verify product availability before creating orders


### Troubleshooting

When troubleshooting failed processing:

1. Review validation job output
2. Identify invalid rows or formatting issues
3. Correct feed data issues
4. Re-upload the corrected feed
5. Verify successful ETL completion
6. Verify product availability before creating orders

For troubleshooting procedures, see [Debug a product feed failure](../operations/debug-product-feed.md).


## Related documentation


### Tutorials and workflows

- [Ingest a product feed end-to-end](ingest-product-feed.md)
- [Debug a product feed failure](../operations/debug-product-feed.md)


### API reference

- [Feeds](feeds.md)
- [Jobs](jobs.md)
- [Products](products.md)
- [Orders](orders.md)
- [Analytics](analytics.md)


### Specifications and architecture

- [CSV feed file specification](../specs/csv-feed-file-spec.md)
- [System architecture](architecture.md)


## Summary

The Commerce Integration API provides a scalable ingestion, catalog management, order processing, and analytics platform for integrating external commerce data into downstream systems.

Successful integrations should account for validation workflows, ETL processing behavior, monitoring requirements, downstream product consumption, and transactional order workflows when designing production ingestion pipelines.