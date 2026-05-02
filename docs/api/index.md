# Partner Catalog API — Case Study

## End-to-End Developer Documentation for a Partner Integration Platform

This project demonstrates how I design and build developer-facing documentation for a partner-driven platform, including API reference, workflows, data ingestion, and operational behavior.

The system enables external partners to submit product data, validate it, and make it available for querying—without requiring direct engineering support.

---

## Problem Space

Partner-driven platforms often face challenges with:

- Inconsistent data ingestion from external sources  
- Lack of visibility into processing status  
- High dependency on engineering teams for onboarding and troubleshooting  
- Poor documentation around workflows and failure handling  

---

## Solution

The Partner Catalog API addresses these challenges through a combination of API design, asynchronous processing, and structured documentation.

The platform provides:

- A REST API for uploading and managing partner product feeds  
- An asynchronous job system for validation and processing  
- A structured ETL pipeline for ingesting and normalizing data  
- Query endpoints for retrieving processed product data  

Documentation is designed to support both **initial onboarding** and **ongoing operational use**, enabling self-service integration.

---

## My Role

I designed and implemented both the system and its documentation, including:

- REST API design and ingestion workflows  
- ETL pipeline (extract, transform, load)  
- Job-based processing and pipeline orchestration  
- Cloud deployment using Docker and AWS (ECS, RDS, S3)  
- Documentation architecture and content (MkDocs)  
- Developer experience design (onboarding, workflows, reference)  

---

## Architecture Overview

The system is built using:

- **FastAPI** for API design and documentation  
- **PostgreSQL (RDS)** for persistent storage  
- **Amazon S3** for raw file storage  
- **Docker + AWS ECS (Fargate)** for deployment  
- **Application Load Balancer** for public access  

The documentation reflects how these components interact—not just how individual endpoints behave.

---

## Key System Concepts

### Data Ingestion Pipeline

- CSV upload via `multipart/form-data`  
- Raw file storage in Amazon S3  
- Separation of raw and processed data layers  
- Structured feed metadata and job tracking  

---

### ETL Processing

- **Extract**: Read CSV files from S3  
- **Transform**: Clean, normalize, and validate product data  
- **Load**: Insert structured data into PostgreSQL  

- Job-driven execution via `POST /jobs/{job_id}/run`  
- Status tracking and result messaging through job resources  

---

### Job-Based Processing

- Submission jobs track feed uploads  
- Validation jobs execute ETL processing  
- Explicit job execution model (API-triggered)  
- Status lifecycle: `queued → running → completed / failed`  

---

### API Design

- Resource-based REST endpoints  
- Cursor-based pagination for scalability  
- Filtering and sorting on product queries  
- Consistent JSON response models  
- Structured identifiers for traceability (FD, JS, JV, PR)  

---

## Documentation Structure

### Getting Started

Quick onboarding for developers, including authentication, base URLs, and example requests.

→ [View Getting Started](getting_started.md)

---

### API Reference

Detailed endpoint documentation, request/response models, and supported parameters.

- Feed upload via multipart requests  
- Job tracking and status monitoring  
- Product retrieval with filtering, sorting, and pagination  

→ [View API Reference](api-reference.md)

---

### Workflows

Step-by-step guides showing how to use the system in real scenarios.

- Uploading a partner feed  
- Tracking validation jobs  
- Retrieving processed data  

→ [View Workflows](workflows.md)

---

### SDK Guide (Python)

Example client implementation demonstrating how developers can integrate programmatically.

- Reusable request patterns  
- Authentication handling  
- Example data retrieval  

→ [View SDK Guide](sdk-python.md)

---

## What This Demonstrates

This project reflects my ability to:

**Design documentation for real systems**  
Not just endpoints, but workflows, dependencies, and outcomes.

**Support asynchronous processing models**  
Clear explanation of job states, background processing, and status tracking.

**Enable self-service integration**  
Developers can onboard and use the system without direct engineering support.

**Document data pipelines**  
Includes ingestion, validation, transformation, and storage layers.

**Bridge technical and operational needs**  
Documentation supports both developers and internal operations teams.

---

## Key Concepts Covered

- REST API design and documentation  
- Multipart file uploads  
- Background job processing  
- ETL pipeline integration  
- Pagination (cursor-based and offset-based)  
- Filtering and sorting strategies  
- Data validation workflows  
- Error handling and status modeling  

---

## Live Documentation

- Swagger UI:  
  http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com/docs  

- GitHub Repository:  
  https://github.com/rayajose/partner-catalog-api  

---

## Why This Matters

This project demonstrates how documentation can:

- Reduce onboarding friction for external partners  
- Improve visibility into system behavior  
- Support scalable platform growth  
- Decrease reliance on engineering teams  

It reflects a documentation approach focused on **usability, clarity, and real-world application**.