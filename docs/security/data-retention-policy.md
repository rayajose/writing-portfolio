# Data retention and handling policy

This document defines data retention, storage handling, and operational recovery practices for the Commerce Integration API platform.

The policy establishes requirements for retaining, storing, processing, and recovering operational data associated with feed ingestion, ETL processing, and platform workflows.

The practices described in this document reflect operational patterns commonly used in enterprise SaaS and integration environments.

<div class="doc-meta">
  <span>Data retention</span>
  <span>Compliance</span>
  <span>Lifecycle management</span>
  <span>Governance</span>
</div>


## Purpose

This policy is intended to:

- Define retention practices for raw and processed platform data
- Support operational traceability and replay workflows
- Establish consistent handling requirements for ingestion data
- Support troubleshooting and recovery operations
- Reduce operational risk associated with data loss
- Support audit-oriented operational recordkeeping


## Scope

This policy applies to:

- Uploaded feed files
- Feed metadata
- ETL processing summaries
- Job execution records
- Product and order data
- Operational processing metadata
- Supporting storage infrastructure

Applicable platform components include:

- Amazon S3
- PostgreSQL
- ETL processing workflows
- Feed ingestion operations
- Operational troubleshooting workflows


## Data classification overview

The platform separates operational data into raw and processed data layers.

| Data category              | Description                              | Primary storage |
| -------------------------- | ---------------------------------------- | --------------- |
| Raw ingestion data         | Uploaded partner feed files              | Amazon S3       |
| Processed application data | Normalized product and order records     | PostgreSQL      |
| Operational metadata       | Feed records, job records, ETL summaries | PostgreSQL      |
| Analytics data             | Aggregated reporting data                | PostgreSQL      |


## Raw data retention

Uploaded CSV feed files are retained in Amazon S3.

Raw feed retention supports:

- Replay workflows
- Operational recovery
- Troubleshooting
- Auditability
- Processing traceability

Example object structure:

```text
raw/partners/{partner_name}/feeds/{feed_id}/{filename}.csv
```


## Processed data retention

Processed data is retained in PostgreSQL following ETL processing workflows.

Processed records may include:

- Product records
- Order records
- Feed metadata
- Job metadata
- ETL summaries
- Validation results

Processed records support operational reporting, analytics workflows, and integration queries.


## Operational metadata retention

Operational metadata is retained to support workflow traceability and troubleshooting activities.

Retained metadata includes:

- Feed identifiers
- Job identifiers
- Upload timestamps
- Processing state transitions
- ETL processing summaries
- Validation outcomes

Example identifiers include:

```text
FD00001
JS00001
JV00001
PR00001
```


## Replay and recovery support

The platform retains raw uploaded feed data to support replay and recovery workflows.

Replay capabilities support:

- Reprocessing failed ingestion workflows
- Recovery from processing failures
- Validation troubleshooting
- Operational investigation activities

Replay workflows operate on raw feed files retained in Amazon S3.


## Data handling requirements

Operational data should be handled according to platform access control and operational security requirements.

Data handling requirements include:

- Restricting raw uploaded data to authorized operational workflows
- Maintaining operational traceability throughout ingestion processing
- Keeping processed records consistent with ETL processing outcomes
- Performing data modifications through controlled application workflows
- Preserving operational traceability during replay and recovery activities


## Data integrity protections

The platform implements processing behaviors intended to preserve ingestion consistency and operational integrity.

Integrity protections include:

- Product uniqueness validation
- Change detection during ETL processing
- Validation workflows for required fields
- Structured job lifecycle tracking
- Controlled processing workflows

Product uniqueness is enforced using:

```text
(partner_name, sku)
```


## ETL processing retention behavior

ETL workflows generate operational summaries supporting ingestion analysis and troubleshooting.

Retained ETL summary information includes:

- Inserted products
- Updated products
- Unchanged products
- Skipped rows
- Validation failures
- Processing completion status


### ETL processing result categories

| Result    | Description                |
| --------- | -------------------------- |
| Inserted  | New product created        |
| Updated   | Existing product changed   |
| Unchanged | Existing product identical |
| Skipped   | Invalid or incomplete row  |


## Storage handling considerations

### Amazon S3

Amazon S3 is used to retain immutable raw ingestion data.

Operational considerations include:

- Feed traceability
- Replay support
- Recovery workflows
- Operational auditability


### PostgreSQL

PostgreSQL stores normalized and queryable platform data.

Operational considerations include:

- Persistent product storage
- Analytics query support
- Operational metadata retention
- Feed and job lifecycle tracking


## Data access considerations

Access to retained operational data should follow least privilege principles.

Operational access restrictions should support:

- Restricted infrastructure access
- Controlled replay workflows
- Authorized troubleshooting activities
- Audit-oriented operational accountability

Related access control requirements are documented in the API access control and authentication policy.


## Data lifecycle considerations

The platform separates raw and processed data responsibilities across ingestion workflows.


### Raw data lifecycle

Raw feed files are retained independently from processed application records.

This supports:

- Reprocessing
- Recovery workflows
- Historical ingestion traceability
- Operational auditing


### Processed data lifecycle

Processed records are updated through ETL processing workflows and application operations.

Data changes occur through:

- Feed ingestion
- ETL processing
- Product synchronization workflows
- Order processing workflows


## Operational recovery considerations

Retained operational data supports recovery-oriented workflows including:

- Feed replay
- ETL reprocessing
- Validation troubleshooting
- Operational investigation
- Processing verification

Operational recovery workflows depend on preserved feed metadata, job metadata, and raw uploaded data.


## Data handling principles

The platform follows these data handling principles:

- Separate raw and processed operational data
- Preserve replay and recovery capabilities
- Maintain operational traceability
- Support audit-oriented workflows
- Restrict access using least privilege principles
- Preserve ingestion consistency during processing operations


## Related documentation

- [Security and compliance](index.md)
- [API access control policy](api-access-control-policy.md)
- [Logging and monitoring policy](logging-monitoring-policy.md)
- [Incident response plan](incident-response.md)
- [Operations](../operations/index.md)
- [Platform architecture and operational flow](../architecture/platform-architecture.md)
- [Deployment guide](../architecture/deployment.md)