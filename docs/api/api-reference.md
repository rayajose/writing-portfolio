# API reference

Use this section to explore API endpoints, transactional workflows, request formats, authentication requirements, and response models across the Commerce Integration API platform.

<div class="doc-meta">
  <span>REST API</span>
  <span>OpenAPI</span>
  <span>Pagination</span>
  <span>Filtering</span>
  <span>Transactional workflows</span>
</div>

### [Feeds API](feeds.md)

Upload and manage partner product feeds. Feeds are ingested, validated, transformed through ETL workflows, and tracked through asynchronous processing pipelines before products become available for transactional and analytics workflows.

### [Jobs API](jobs.md)

Monitor asynchronous processing jobs for ingestion, validation, ETL execution, and fulfillment workflows. Jobs expose execution status, operational metadata, and troubleshooting details.

### [Products API](products.md)

Query the centralized product catalog using filtering, sorting, and cursor-based pagination to access normalized partner product data used by downstream order and analytics workflows.

### [Customers API](customers.md)

Create and retrieve fictional customer and shipping address records used by transactional order workflows. Customer-sensitive fields are encrypted before storage and returned as masked values in API responses.

### [Orders API](orders.md)

Create and retrieve customer orders and associated order items. The Orders API supports transactional order creation using catalog products, calculated order totals, and line item pricing.

### [Health API](health.md)

Check the operational status of the API, database connectivity, and supporting infrastructure services. Used for monitoring, automated health checks, and deployment verification workflows.

### [Analytics API](analytics.md)

Retrieve aggregated metrics derived from product, order, and transactional workflow data, including sales trends, revenue share, and partner performance analytics across the platform.

## Security and operational behavior

The platform demonstrates security-oriented API behaviors including:

- Authenticated API access using `x-api-key`
- Field-level encryption for customer-sensitive fields
- Masked API response handling
- Structured operational identifiers
- Transactional relational workflows
- Operational traceability across ingestion and order processing