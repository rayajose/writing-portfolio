# Release notes

This page documents notable platform, API, infrastructure, and documentation changes for the Commerce Integration API project.

The version history reflects the evolution of the platform from an initial ingestion prototype into a cloud-native commerce integration platform supporting ETL processing, order management, analytics services, operational workflows, and security-oriented documentation.

## Version 1.4.0

This release introduces partner management capabilities and expands partner relationships across feed ingestion, product catalog, and order processing workflows. The release establishes partners as a first-class platform resource and improves traceability between partner onboarding, feed processing, catalog management, and transactional order data.

### Added

- Added partner management resource
- Added `GET /partners`
- Added `GET /partners/{partner_id}`
- Added `POST /partners`
- Added partner database table
- Added partner identifier (`PTxxxxx`) generation
- Added partner endpoint test coverage
- Added partner onboarding support for feed ingestion workflows

### Changed

- Added `partner_id` to feed records
- Added `partner_id` to product records
- Added `partner_id` to order records
- Updated feed upload processing to associate partner identifiers with ingested data
- Updated product responses to include partner identifiers
- Updated order responses to include partner identifiers
- Expanded platform description and API metadata to reflect partner management, fulfillment, and analytics capabilities
- Updated API documentation, examples, and operational procedures to include partner management workflows

### Fixed

- Resolved production schema mismatches discovered during deployment validation
- Added missing partner-related database structures to deployed environments
- Initialized partner identifier counters required for partner creation workflows
- Improved deployment validation procedures by documenting schema parity verification and seed data validation requirements



## Version 1.3.0

Version 1.3.0 introduces customer deletion capabilities, including support for bulk customer deletion, referential integrity validation, and safeguards that preserve historical order data.

### Added

- Added `DELETE /customers/{customer_id}` endpoint for deleting individual customer records.
- Added `DELETE /customers` endpoint for bulk customer deletion using a list of customer identifiers.
- Added bulk deletion response reporting, including per-customer success, failure, and not-found status details.
- Added customer deletion safeguards that prevent removal of customer records referenced by existing orders.
- Added validation preventing deletion of customer addresses referenced by order shipping records.

### Changed

- Updated customer deletion processing to preserve historical order integrity by blocking deletion of dependent customer and address records.
- Updated customer service logic to evaluate both customer and shipping address relationships before allowing deletion.
- Updated customer API documentation with single and bulk customer deletion workflows and examples.

### Fixed

- Fixed customer address retrieval handling for legacy or invalid encrypted address data.
- Improved error handling during customer deletion operations to prevent foreign key constraint violations from being exposed as internal server errors.

## Version 1.2.0

Version 1.2.0 expands customer-centric retrieval capabilities by introducing customer order history endpoints and related API documentation updates.

### Added

- Added `GET /customers/{customer_id}/orders` endpoint.
- Added customer-specific order retrieval support.
- Added customer order history responses.
- Added customer-based order query examples to API documentation.

### Changed

- Expanded Orders API capabilities to support customer-centric retrieval workflows.
- Improved relational retrieval of orders and associated order items.

### Fixed

- Improved order retrieval consistency for downstream analytics and reporting workflows.

## Version 1.1.0

Version 1.1.0 introduces customer management workflows, field-level encryption, masked API responses, and customer-linked order support.

### Added

- Customers API for fictional customer record management.
- Customer shipping address workflows.
- Field-level encryption for:

  - Email addresses
  - Phone numbers
  - Street addresses
  - Postal codes
- Masked API response handling for customer-sensitive fields.
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
- Customer API regression test coverage.
- Encryption helper utilities and masking utilities.

### Changed

- Expanded Orders API to support customer and shipping address references.
- Updated relational order schema to support customer-linked workflows.
- Enhanced Swagger/OpenAPI documentation for customer resources.
- Improved platform security modeling for PII-like data handling.
- Expanded documentation coverage for security-oriented API behavior.

### Fixed

- Improved handling of sensitive customer data in API responses.
- Prevented encrypted database values from being exposed through customer endpoints.
- Improved test environment configuration for encryption-enabled workflows.

## Version 1.0.0

Version 1.0.0 establishes the first production-style platform release, introducing order workflows, analytics services, operational documentation, and security-focused guidance.

### Added

- Orders API for transactional order creation workflows.
- Analytics endpoints for:

  - Revenue by partner
  - Sales trends over time
  - Revenue share reporting
- PostgreSQL-backed order persistence.
- Order analytics data model.
- Operational documentation:

  - Deployment change procedure
  - Backup and recovery procedure
  - Debug a product feed failure
- Security and compliance documentation:

  - API access control and authentication policy
  - Logging and monitoring standard
  - Data retention and handling policy
  - Incident response plan
- Webhook integration guide.
- Python SDK guide.
- Expanded architecture and operational workflow documentation.
- Version history documentation.

### Changed

- Updated architecture documentation to reflect explicit job-based ETL execution.
- Improved Mermaid workflow diagrams for readability within MkDocs layouts.
- Reorganized navigation structure across API, architecture, operations, and security sections.
- Expanded operational traceability documentation throughout ingestion workflows.
- Improved documentation consistency across API reference sections.

### Fixed

- Corrected discrepancies between local and deployed database schemas.
- Updated Swagger UI deployment configuration.
- Improved deployment synchronization between ECS task definitions and live application behavior.
- Corrected feed upload response documentation to align with actual API behavior.

## Version 0.9.0

Version 0.9.0 introduces ETL processing workflows, raw data storage architecture, analytics foundations, and cloud deployment capabilities.

### Added

- ETL processing pipeline.
- Amazon S3 raw feed storage.
- Validation job workflows.
- Explicit ETL execution endpoint:

```text
POST /jobs/{job_id}/run
```

- Change detection during ETL processing.
- Product synchronization logic supporting:

  - Inserted records
  - Updated records
  - Unchanged records
  - Skipped records
- Cursor-based pagination support for Products API.
- Analytics service foundation.
- AWS deployment architecture:

  - ECS Fargate
  - Application Load Balancer
  - Amazon RDS
  - Amazon ECR
  - Amazon S3

### Changed

- Migrated processed data storage from SQLite to PostgreSQL.
- Separated raw and processed data layers.
- Updated architecture to support replay and recovery workflows.
- Expanded job lifecycle tracking behavior.

### Fixed

- Improved ingestion consistency during repeated ETL execution.
- Reduced unnecessary database updates through change detection logic.
- Corrected processing behavior for invalid feed rows.

## Version 0.8.0

Version 0.8.0 introduces core ingestion APIs, feed processing workflows, and product catalog query capabilities.

### Added

- Feeds API.
- Jobs API.
- Products API.
- Health API.
- Multipart CSV upload workflow.
- Structured identifier generation:

  - `FDxxxxx`
  - `JSxxxxx`
  - `JVxxxxx`
  - `PRxxxxx`
- Product filtering and sorting.
- Swagger UI integration.
- API key authentication using:

```text
x-api-key
```

- Initial MkDocs documentation site.
- Integration workflow documentation.
- Product feed file specification.

### Changed

- Standardized API response formatting.
- Improved request validation behavior.
- Refined ingestion workflow modeling.

### Fixed

- Corrected CSV validation edge cases.
- Improved API error handling consistency.
- Updated endpoint documentation examples.

## Version 0.7.0

Version 0.7.0 establishes the initial platform foundation focused on ingestion-driven commerce workflows and API architecture development.

### Added

- Initial FastAPI application structure.
- Prototype feed ingestion workflows.
- Basic relational data model.
- Initial product persistence logic.
- Docker-based local development environment.
- Early API documentation structure.
- Swagger/OpenAPI support.
- Initial ETL workflow concepts.

### Changed

- Refined platform scope toward commerce integration workflows.
- Renamed project from Partner Catalog API to Commerce Integration API for broader integration alignment.

### Fixed

- Early routing and schema validation issues.
- Initial database initialization inconsistencies.

## Documentation highlights by version

The platform documentation evolved alongside the implementation and infrastructure architecture.

Major documentation additions across versions included:

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

<!-- - [API and integrations](../api/index.md)-->
- [Architecture and concepts](../architecture/index.md)
- [Operations](../operations/index.md)
- [Security and compliance](../security/index.md)
- [Deployment guide](../architecture/deployment.md)
