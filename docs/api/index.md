# Partner Catalog API

Use this API to upload product feeds, process them through an ETL pipeline, and query normalized product data.
This documentation supports both initial onboarding and ongoing integration workflows.

---

## Start here

Choose a path based on what you want to do:

### Get started

Set up authentication and make your first request:

- [Get started](getting_started.md)

---

### Learn the system

Follow a guided walkthrough of the ingestion workflow:

- [Your first feed ingestion](../tutorials/first-feed.md)

---

### Complete a task

Use step-by-step guides for common workflows:

- [Ingest a product feed end-to-End](ingest-product-feed.md)
- [Debug a failed feed](debug-product-feed.md)

---

### Explore the API

Look up endpoints, parameters, and response models:

- [API Reference](api-reference.md)
- [Feeds API](feeds.md)
- [Products API](products.md)
- [Jobs API](jobs.md)

---

### Understand the system

Learn how the platform is designed and how data flows:

- [Architecture](architecture.md)
- [Workflows](workflows.md)

---

## Platform overview

The ingestion workflow follows a structured pipeline:

```text
Upload feed → Validate → Transform → Load → Query products
```

- **Upload**: Partner submits a CSV product feed
- **Validate**: Structure and required fields are checked
- **Transform**: Data is normalized into product records
- **Load**: Records are inserted or updated in the database
- **Query**: Products are accessed through the API

---

## Core concepts

### Feed ingestion

- CSV upload via `multipart/form-data`
- Raw file storage in Amazon S3
- Feed metadata and job tracking

---

### ETL processing

- Extract data from uploaded files
- Transform and validate product data
- Load structured records into the database
- Triggered via job execution (`POST /jobs/{job_id}/run`)
- Results available through job status and summaries

---

### Job-based processing

- Jobs track validation and ingestion workflows
- Explicit execution model
- Status lifecycle: `queued → in_progress → completed / failed`

---

### API design

- Resource-based REST endpoints
- Cursor-based pagination
- Filtering and sorting
- Consistent JSON response models

---

## Documentation overview

This documentation includes the following:

- **Tutorials** for learning system workflows
- **How-to guides** for task-based execution
- **API reference** for endpoint details
- **Concepts** for architecture and system behavior

---

## About this project

This project demonstrates how to design and document a partner-driven data platform.

It includes:

- API design and ingestion workflows
- ETL pipeline implementation
- Job-based processing and status tracking
- Cloud deployment (AWS, Docker)
- Documentation architecture using MkDocs

---

## Additional resources
- <a href="http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com/docs" target="_blank">Swagger UI</a>
- <a href="https://github.com/rayajose/writing-portfolio" target="_blank">Documentation source (docs-as-code)</a>

---
