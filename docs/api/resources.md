# System Resource Model

## Overview

This page describes the primary operational resources used within the Commerce Integration API.

Feeds, jobs, and products represent the core entities that model the ingestion lifecycle, from partner feed submission through asynchronous ETL processing and normalized product persistence.

These resources provide operational visibility, traceability, and structured relationships across the ingestion platform.


## Resource relationships

```mermaid
flowchart LR
    Feed --> ValidationJob
    ValidationJob --> Product
```

### Resource lifecycle

1. A partner uploads a feed.
2. The system creates processing jobs.
3. ETL workflows validate and transform ingestion data.
4. Products are normalized and stored for retrieval.
5. Operational metadata retained for troubleshooting and auditing.


## Feed

A feed represents a partner-submitted product data file entering the ingestion pipeline.

Feeds serve as the operational entry point for asynchronous validation and ETL workflows.

### Feed fields

| Field                | Description                                |
| -------------------- | ------------------------------------------ |
| `feed_id`            | Unique identifier for the feed (`FDxxxxx`) |
| `partner_name`       | Name of the submitting partner             |
| `file_name`          | Uploaded file name                         |
| `content_type`       | MIME type of uploaded file                 |
| `status`             | Feed upload status                         |
| `uploaded_at`        | Upload timestamp                           |
| `validation_job_id`  | Associated validation job ID (`JVxxxxx`)   |
| `validation_status`  | Current ETL processing state               |
| `validation_message` | ETL processing result summary              |
| `raw_file_s3_key`    | S3 object key for raw feed storage         |
| `raw_file_bucket`    | S3 bucket storing the raw feed             |

### Operational details

- Feed status reflects upload state only
- ETL lifecycle state tracked through associated validation jobs
- Raw feed files retained to support replay and troubleshooting workflows
- Feed metadata provides ingestion traceability across processing lifecycle


## Job

A job represents an asynchronous processing task executed by the ingestion platform.

Jobs provide operational visibility into ingestion, validation, transformation, and ETL execution workflows.

### Job fields

| Field        | Description                                            |
| ------------ | ------------------------------------------------------ |
| `job_id`     | Unique identifier for the job (`JSxxxxx` or `JVxxxxx`) |
| `feed_id`    | Associated feed identifier                             |
| `job_type`   | Processing task type                                   |
| `status`     | Current operational state                              |
| `created_at` | Job creation timestamp                                 |
| `message`    | Status or processing summary message                   |

### Job types

| Type         | Description                                    |
| ------------ | ---------------------------------------------- |
| `submission` | Feed upload processing                         |
| `validation` | ETL processing (`Validate → Transform → Load`) |

### Operational states

| Status        | Description                        |
| ------------- | ---------------------------------- |
| `queued`      | Job created and awaiting execution |
| `in_progress` | ETL processing currently running   |
| `completed`   | Job completed successfully         |
| `failed`      | Job encountered processing failure |

### Operational details

- Jobs support asynchronous ingestion workflows
- Lifecycle states provide operational visibility and monitoring
- Job metadata retained for troubleshooting and auditability
- Processing summaries expose ETL outcomes and validation results


## Product

A product represents a normalized catalog item derived from partner feed ingestion.

Products are generated during ETL processing and stored for querying, analytics, and downstream integration workflows.

### Product fields

| Field          | Description                                   |
| -------------- | --------------------------------------------- |
| `product_id`   | Unique identifier for the product (`PRxxxxx`) |
| `feed_id`      | Associated feed identifier                    |
| `partner_name` | Originating partner                           |
| `sku`          | Partner-defined stock keeping unit            |
| `product_name` | Product display name                          |
| `description`  | Product description                           |
| `brand`        | Product brand                                 |
| `category`     | Product category                              |
| `price`        | Product price                                 |
| `currency`     | Currency code                                 |
| `availability` | Product availability status                   |
| `created_at`   | Product ingestion timestamp                   |

### Operational details

- Products generated through ETL normalization workflows
- Duplicate prevention enforced during ingestion
- Existing records evaluated for change detection
- Products queryable independently from originating feeds


## Identifier structure

All operational resources use structured identifiers to support consistency and traceability across ingestion workflows.

| Prefix | Resource       | Example   |
| ------ | -------------- | --------- |
| `FD`   | Feed           | `FD00001` |
| `JS`   | Submission Job | `JS00001` |
| `JV`   | Validation Job | `JV00001` |
| `PR`   | Product        | `PR00001` |

### Identifier characteristics

- Generated through database-backed counters
- Uniqueness enforced at resource level
- Structured prefixes simplify operational troubleshooting and tracking


## Processing concepts

### Asynchronous processing

Feed ingestion and ETL execution occur independently from client-facing request handling.

This architecture supports:

- Non-blocking uploads
- Scalable ingestion workflows
- Background validation and transformation
- Operational resiliency during large processing events

### Data normalization

Incoming partner data is transformed into a normalized schema before persistence.

Normalization workflows include:

- Required field validation
- Structural consistency checks
- Duplicate prevention
- Change detection processing

### Traceability

Operational metadata retained throughout ingestion lifecycle includes:

- Feed identifiers
- Job lifecycle states
- ETL summaries
- Raw file storage references
- Processing timestamps

This metadata supports troubleshooting, auditing, and operational analysis.


## Related documentation

- [System Architecture and Operational Flow](../architecture/index.md)
- [Integration Guide](../api/integration-guide.md)
- [Feeds API](../api/feeds.md)
- [Jobs API](../api/jobs.md)
- [Products API](../api/products.md)