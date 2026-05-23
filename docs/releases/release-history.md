# Release notes

This page documents notable platform, API, infrastructure, and documentation changes for the Commerce Integration API project.

The release history reflects the evolution of the platform from an initial ingestion prototype into a cloud-deployed commerce integration system supporting ETL processing, operational workflows, analytics services, and security-oriented documentation.

## Version 1.1.0

Introduced customer management workflows, field-level encryption, masked API responses, and customer-linked order support.

### Added

- Customers API for fictional customer record management
- Customer shipping address workflows
- Field-level encryption for:
  - Email addresses
  - Phone numbers
  - Street addresses
  - Postal codes
- Masked API response handling for customer-sensitive fields
- Customer identifier format:

```text
CUxxxxx
```

- Customer address identifier format:

```text
ADxxxxx
```

- Customer-to-order association support:
  - `customer_id`
  - `shipping_address_id`
- Customer API regression test coverage
- Encryption helper utilities and masking utilities

### Changed

- Expanded Orders API to support customer and shipping address references
- Updated relational order schema to support customer-linked workflows
- Enhanced Swagger/OpenAPI documentation for customer resources
- Improved platform security modeling for PII-like data handling
- Expanded documentation coverage for security-oriented API behavior

### Fixed

- Improved handling of sensitive customer data in API responses
- Prevented encrypted database values from being exposed through customer endpoints
- Improved test environment configuration for encryption-enabled workflows


## Version 1.0.0

Initial production-style platform release introducing operational maturity, order workflows, analytics services, and expanded platform documentation.

### Added

- Orders API for transactional order creation workflows
- Analytics endpoints for:
  - Revenue by partner
  - Sales trends over time
  - Revenue share reporting
- PostgreSQL-backed order persistence
- Order analytics data model
- Operational documentation:
  - Deployment change procedure
  - Backup and recovery procedure
  - Debug failed feed runbook
- Security and compliance documentation:
  - API access control and authentication policy
  - Logging and monitoring standard
  - Data retention and handling policy
  - Incident response plan
- Webhook integration guide
- Python SDK guide
- Expanded architecture and operational workflow documentation
- Platform release history documentation

### Changed

- Updated architecture documentation to reflect explicit job-based ETL execution
- Improved Mermaid workflow diagrams for readability within MkDocs layouts
- Reorganized navigation structure across API, architecture, operations, and security sections
- Expanded operational traceability documentation throughout ingestion workflows
- Improved documentation consistency across API reference sections

### Fixed

- Corrected discrepancies between local and deployed database schemas
- Updated Swagger UI deployment configuration
- Improved deployment synchronization between ECS task definitions and live application behavior
- Corrected feed upload response documentation to align with actual API behavior


## Version 0.9.0

Introduced ETL processing workflows, raw data storage architecture, analytics foundations, and cloud deployment enhancements.

### Added

- ETL processing pipeline
- Amazon S3 raw feed storage
- Validation job workflows
- Explicit ETL execution endpoint:

```text
POST /jobs/{job_id}/run
```

- Change detection during ETL processing
- Product synchronization logic supporting:
  - Inserted records
  - Updated records
  - Unchanged records
  - Skipped records
- Cursor-based pagination support for Products API
- Analytics service foundation
- AWS deployment architecture:
  - ECS Fargate
  - Application Load Balancer
  - Amazon RDS
  - Amazon ECR
  - Amazon S3

### Changed

- Migrated processed data storage from SQLite to PostgreSQL
- Separated raw and processed data layers
- Updated architecture to support replay and recovery workflows
- Expanded job lifecycle tracking behavior

### Fixed

- Improved ingestion consistency during repeated ETL execution
- Reduced unnecessary database updates through change detection logic
- Corrected processing behavior for invalid feed rows


## Version 0.8.0

Introduced core ingestion APIs, feed processing workflows, and product query capabilities.

### Added

- Feeds API
- Jobs API
- Products API
- Health API
- Multipart CSV upload workflow
- Structured identifier generation:
  - `FDxxxxx`
  - `JSxxxxx`
  - `JVxxxxx`
  - `PRxxxxx`
- Product filtering and sorting
- Swagger UI integration
- API key authentication using:

```text
x-api-key
```

- Initial MkDocs documentation site
- Integration workflow documentation
- Product feed file specification

### Changed

- Standardized API response formatting
- Improved request validation behavior
- Refined ingestion workflow modeling

### Fixed

- Corrected CSV validation edge cases
- Improved API error handling consistency
- Updated endpoint documentation examples


## Version 0.7.0

Initial platform foundation release focused on ingestion-driven commerce workflows and API architecture experimentation.

### Added

- Initial FastAPI application structure
- Prototype feed ingestion workflows
- Basic relational data model
- Initial product persistence logic
- Docker-based local development environment
- Early API documentation structure
- Swagger/OpenAPI support
- Initial ETL workflow concepts

### Changed

- Refined platform scope toward commerce integration workflows
- Renamed project from Partner Catalog API to Commerce Integration API for broader integration alignment

### Fixed

- Early routing and schema validation issues
- Initial database initialization inconsistencies


## Documentation release highlights

The platform documentation evolved alongside the implementation and infrastructure architecture.

Major documentation additions across releases included:

- API reference documentation
- ETL workflow documentation
- Operational procedures
- Security and compliance documentation
- Architecture diagrams
- Deployment guidance
- Integration tutorials
- Troubleshooting workflows
- Recovery procedures
- SDK documentation


## Related documentation

- [API and integrations](../api/index.md)
- [Architecture and deployment](../architecture/index.md)
- [Operations](../operations/index.md)
- [Security and compliance](../security/index.md)
- [Deployment guide](../architecture/deployment.md)