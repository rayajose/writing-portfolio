# About This Project

This project simulates a real-world partner integration system for ingesting, processing, and serving product catalog data through a cloud-based data pipeline.

---

## My Role

* Designed REST API endpoints and ingestion workflows
* Implemented a full ETL pipeline (extract, transform, load)
* Integrated Amazon S3 for raw data storage
* Built job-based processing and pipeline orchestration
* Modeled request and response schemas using Pydantic
* Authored all developer documentation (MkDocs)
* Designed documentation structure and navigation
* Deployed application using Docker and AWS (ECS, RDS, S3)

---

## Key Design Concepts

### Data Ingestion Pipeline

* CSV upload via multipart/form-data
* Raw file storage in Amazon S3
* Separation of raw and processed data layers
* Structured feed metadata and job tracking

---

### ETL Processing

* Extract: Read CSV files from S3

* Transform: Clean, normalize, and validate product data

* Load: Insert structured data into PostgreSQL

* Job-driven execution via `POST /jobs/{job_id}/run`

* Status tracking and result messaging through job resources

---

### Job-Based Processing

* Submission jobs track feed uploads
* Validation jobs execute ETL processing
* Explicit job execution model (API-triggered)
* Status lifecycle: `queued → running → completed / failed`

---

### API Design

* Resource-based REST endpoints
* Cursor-based pagination for scalability
* Filtering and sorting on product queries
* Consistent JSON response models
* Structured identifiers for traceability (FD, JS, JV, PR)

---

### Cloud-Native Architecture

* Containerized FastAPI application (Docker)
* Deployed on Amazon ECS Fargate
* PostgreSQL hosted on Amazon RDS
* Raw data stored in Amazon S3
* Application exposed via Application Load Balancer

---

## Summary

This project demonstrates the design and implementation of a production-style data ingestion system, including:

* API-driven ingestion
* Cloud storage integration
* ETL processing pipeline
* Job orchestration and observability
* Scalable, layered architecture
