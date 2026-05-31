# API reference

Use this section to explore API endpoints, transactional workflows, authentication requirements, request formats, and response models across the Commerce Integration API platform.

<div class="doc-meta">
  <span>REST API</span>
  <span>OpenAPI</span>
  <span>Pagination</span>
  <span>Filtering</span>
  <span>Transactional workflows</span>
</div>



### [Partners](partners.md)

Create and manage partner organizations that submit product feeds to the platform. Partner workflows support onboarding, lifecycle management, feed configuration, and partner identification through unique partner IDs used throughout ingestion and catalog operations.



### [Jobs](jobs.md)

Monitor asynchronous processing jobs for ingestion, validation, ETL execution, and fulfillment workflows. Jobs expose execution status, operational metadata, and ETL processing results.


### [Products](products.md)

Retrieve normalized product catalog data using filtering, sorting, and cursor-based pagination. Product records are sourced from processed partner feeds and support downstream order and analytics workflows.


### [Customers](customers.md)

Create and retrieve fictional customer and shipping address records used by transactional order workflows. Customer-sensitive fields are encrypted before storage and returned as masked values in API responses.


### [Orders](orders.md)

Create and retrieve customer orders and associated order items. Order workflows support transactional order creation, calculated totals, and line item pricing derived from catalog products.


### [Health](health.md)

Retrieve operational health status for the API and database connection. Health workflows support monitoring, automated health checks, and deployment validation.


### [Analytics](analytics.md)

Retrieve aggregated metrics derived from product, order, and transactional workflow data, including sales trends, revenue share, and partner performance analytics.

### [Errors](errors.md)

Review standard error responses, HTTP status codes, validation failures, authentication errors, resource lookup failures, and operational error handling patterns used throughout the API.


## Security and operational behavior

The platform demonstrates security-oriented API behaviors including:

- Authenticated API access using `x-api-key`
- Field-level encryption for customer-sensitive fields
- Masked API response handling
- Structured operational identifiers
- Transactional relational workflows
- Operational traceability across ingestion and order processing