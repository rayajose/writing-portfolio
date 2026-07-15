# API reference

The Commerce Integration Platform exposes a REST API for partner integrations, catalog management, transactional order processing, analytics, and operational monitoring. This section provides endpoint reference documentation, request and response models, authentication requirements, and API behavior for each platform resource.

<div class="doc-meta">
  <span>REST API</span>
  <span>OpenAPI</span>
  <span>Pagination</span>
  <span>Filtering</span>
  <span>Transactional workflows</span>
</div>

## Explore the API

The API is organized by platform resource and operational capability.

Reference documentation includes:

- Partner management
- Product feed ingestion
- Asynchronous job processing
- Product catalog management
- Customer management
- Order processing
- Platform health monitoring
- Analytics
- Webhook management
- Standard error handling

### [Partners](partners.md)

Create and manage partner organizations that submit product feeds to the platform. Partner workflows support onboarding, lifecycle management, feed configuration, and unique partner identification throughout ingestion and catalog operations.

### [Feeds](feeds.md)

Upload and monitor product catalog feeds submitted by partner organizations. Feed resources provide operational visibility into ingestion requests and validation outcomes.

### [Jobs](jobs.md)

Monitor asynchronous processing jobs for ingestion, validation, ETL execution, and fulfillment workflows. Jobs expose execution status, operational metadata, and processing results.

### [Products](products.md)

Retrieve normalized product catalog data using filtering, sorting, and cursor-based pagination. Product records are sourced from processed partner feeds and support downstream ordering and analytics workflows.

### [Customers](customers.md)

Create and retrieve customer and shipping address records used by transactional order workflows. Customer-sensitive fields are encrypted before storage and returned as masked values in API responses.

### [Orders](orders.md)

Create and retrieve customer orders and associated order items. Order workflows support transactional order creation, calculated totals, and catalog-based pricing.

### [Health](health.md)

Retrieve operational health information for the platform API and database connection. Health endpoints support monitoring, automated health checks, and deployment validation.

### [Analytics](analytics.md)

Retrieve aggregated metrics derived from transactional platform data, including sales trends, revenue distribution, and partner performance analytics.

### [Webhooks](webhooks.md)

Configure webhook subscriptions and delivery endpoints for supported platform events. Webhook resources support event-driven integrations and outbound notification workflows.

### [Webhook deliveries](webhookdeliveries.md)

Review webhook delivery history, response codes, retry behavior, and operational delivery metadata for troubleshooting and audit purposes.

### [Errors](errors.md)

Review standard error responses, HTTP status codes, validation failures, authentication errors, resource lookup failures, and operational error handling patterns used throughout the API.

## Security and operational behavior

The API incorporates security and operational controls that support reliable platform operation, including:

- Authenticated API access using the `x-api-key` request header
- Field-level encryption for customer-sensitive data
- Masked API response handling
- Structured operational resource identifiers
- Transactional relational workflows
- Operational traceability across ingestion, processing, and order management

## Related documentation

- [Platform guide](../platform/index.md)
- [Architecture](../architecture/index.md)
- [How-to guides](../how-to/index.md)
- [Operations](../operations/index.md)
