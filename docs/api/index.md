# Commerce Integration API

The Commerce Integration API is a commerce data ingestion, catalog management, and analytics platform designed to support recurring partner retailer product feeds and downstream order workflows.

Retail partners can submit product data on a scheduled or event-driven basis (for example, daily or hourly, depending on how frequently pricing and inventory change). The system ingests, validates, and processes these feeds to maintain an up-to-date, queryable product catalog.

The API enables:

- Ingestion and processing of partner product feeds
- Tracking product pricing, availability, and catalog changes across partners
- Transactional order creation using catalog products
- Generation of sales and revenue analytics
- Monitoring and troubleshooting ingestion workflows and ETL processing

On the backend, the system provides full visibility into the ingestion pipeline, including feed status, validation results, ETL execution, and order processing workflows. This allows operators and integrators to quickly identify and resolve issues related to data quality, failed uploads, processing failures, or downstream order activity.

The result is a scalable interface for managing partner commerce data and deriving operational and business insights from catalog and sales activity.

## Start here

Choose a path based on what you want to do.

### Get started

Set up authentication and make your first request.

- [Get started](getting_started.md)

### Learn the system

Follow a guided walkthrough of the ingestion workflow.

- [Your first feed ingestion](../tutorials/first-feed.md)

### Complete a task

Use step-by-step guides for common workflows.

- [Ingest a product feed end-to-end](ingest-product-feed.md)
- [Debug a failed feed](debug-product-feed.md)

### Explore the API

Look up endpoints, parameters, and response models.

- [API Reference](api-reference.md)

### Understand the system

Learn how the platform is designed and how data flows.

- [Architecture](architecture.md)
- [Workflows](workflows.md)

## Platform overview

The platform follows a structured ingestion and order-processing workflow.

```text
Upload feed
  → Validate
  → Transform
  → Load catalog data
  → Query products
  → Create orders
  → Generate analytics
```

- **Upload**: Partner submits a CSV product feed
- **Validate**: Structure and required fields are checked
- **Transform**: Data is normalized into product records
- **Load**: Records are inserted or updated in PostgreSQL
- **Query**: Products are accessed through the API
- **Order**: Orders are created from catalog products
- **Analytics**: Sales and revenue metrics are aggregated from order activity

## Core concepts

This section explains the fundamental concepts behind ingestion, processing, order management, and API interaction.

### Feed ingestion

- CSV upload via `multipart/form-data`
- Raw file storage in Amazon S3
- Feed metadata and job tracking
- Partner-driven catalog synchronization

### ETL processing

- Extract data from uploaded files
- Transform and validate product data
- Load structured records into PostgreSQL
- Perform change detection to avoid unnecessary updates
- Triggered via job execution (`POST /jobs/{job_id}/run`)
- Results available through job status and ETL summaries

### Job-based processing

- Jobs track validation and ingestion workflows
- Explicit execution model
- Status lifecycle:
  `queued → running → completed / failed`
- Validation and ETL execution visibility

### Product catalog management

- Query products using pagination, filtering, and sorting
- Retrieve products by feed
- Maintain partner-specific catalog records
- Support large-scale catalog synchronization workflows

### Order processing

- Orders are created transactionally using catalog products
- Product pricing is copied into order items at creation time
- Order totals are calculated from associated line items
- Orders and order items are persisted relationally in PostgreSQL
- Historical order pricing is preserved independently from future catalog changes

### Analytics and reporting

- Revenue and sales aggregation
- Sales-by-partner reporting
- Sales-over-time reporting
- Revenue share analysis
- Operational reconciliation and dashboard support

### API design

- Resource-based REST endpoints
- Cursor-based pagination
- Filtering and sorting
- Consistent JSON response models
- Structured resource identifiers

## Documentation overview

This documentation includes the following:

- **Tutorials** for learning system workflows
- **How-to guides** for task-based execution
- **API reference** for endpoint details
- **Concepts** for architecture and system behavior

## About this project

This project demonstrates how to design, implement, and document a partner-driven commerce data platform.

It includes:

- API design and ingestion workflows
- ETL pipeline implementation
- Order and order item relational modeling
- Job-based processing and status tracking
- PostgreSQL-backed data persistence
- Automated API regression testing with `pytest`
- Cloud deployment using AWS and Docker
- Documentation architecture using MkDocs and docs-as-code practices

## Additional resources

- <a href="http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com/docs" target="_blank">Swagger UI</a>
- <a href="https://github.com/rayajose/writing-portfolio" target="_blank">Documentation source (docs-as-code)</a>