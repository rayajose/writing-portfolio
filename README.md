# Commerce Integration Platform

> Cloud-native commerce integration platform demonstrating REST APIs, systems integration, ETL processing, cloud deployment, and modern technical documentation.

The Commerce Integration Platform is a production-style application that models how modern commerce systems onboard partners, ingest product catalogs, process transactional data, deliver webhook notifications, and expose operational insights through a browser-based administration console.

This repository contains the **FastAPI backend** and the **Technical Writing Portfolio** that documents the platform. Together they demonstrate backend development, cloud architecture, developer documentation, operational procedures, and docs-as-code practices.

---

# Explore the Platform

## 📖 Technical Writing Portfolio

Comprehensive documentation covering platform architecture, tutorials, implementation guides, operations, security, and API reference.

https://rayajose.github.io/writing-portfolio/

---

## 🖥️ Operations Console

A browser-based administrative application for monitoring and managing the platform.

https://d2mg19x9fth17i.cloudfront.net

> The Operations Console is maintained in a separate repository.

---

## 🔌 Interactive API (Swagger)

Explore and test REST endpoints through the OpenAPI interface.

https://d2nbg35whekpke.cloudfront.net/docs

> **Note:** The API may be temporarily offline outside demonstration periods to control cloud costs.

---

# Repository Contents

This repository includes:

- FastAPI backend
- REST API
- OpenAPI (Swagger)
- MkDocs documentation
- Platform architecture documentation
- Tutorials
- How-to guides
- Operations documentation
- Security documentation
- AWS deployment configuration

---

# Purpose

This project demonstrates how technical documentation supports an entire cloud-native platform rather than a standalone API.

The platform models production-style workflows including:

- Partner onboarding
- Product catalog ingestion
- ETL processing
- Background job execution
- Customer and order management
- Webhook delivery
- Business analytics
- Operational monitoring
- Developer enablement

Rather than documenting isolated endpoints, the portfolio demonstrates how documentation supports every stage of a modern software platform.

---

# Platform Overview

External partners submit product catalog feeds that are validated, processed, transformed, and made available for downstream commerce operations.

The backend provides services for:

- Partner management
- Feed ingestion
- Processing jobs
- Product catalog
- Customers
- Orders
- Analytics
- Webhook subscriptions
- Webhook delivery tracking

These services are consumed by external integrations, the browser-based Operations Console, and the interactive Swagger interface.

---

# Documentation

Documentation is maintained using a docs-as-code workflow and published with **MkDocs Material**.

The Technical Writing Portfolio includes:

- Platform Guide
- Tutorials
- How-to Guides
- Architecture & Concepts
- API Reference
- Operations
- Security
- Supporting Materials

The documentation demonstrates multiple content types commonly produced by senior technical writers, including developer documentation, operational procedures, implementation guidance, architecture documentation, and security documentation.

---

# REST API

REST endpoints are organized around the following resources:

- Partners
- Feeds
- Jobs
- Products
- Customers
- Orders
- Analytics
- Webhooks

Interactive endpoint documentation is available through OpenAPI (Swagger).

---

# ETL Processing

The ingestion pipeline models production-style data processing.

Features include:

- Feed validation
- Change detection
- Data transformation
- Background job execution
- Idempotent processing
- Processing statistics

Rows are classified as:

- Inserted
- Updated
- Unchanged
- Skipped

This minimizes unnecessary database writes while providing accurate operational reporting.

---

# Analytics

The analytics layer provides operational and business reporting.

Available reporting includes:

- Sales by partner
- Sales over time
- Revenue distribution
- Top-performing products

Analytics operate directly on transactional platform data.

---

# Technology Stack

## Backend

- FastAPI
- Python

## Database

- PostgreSQL (Amazon RDS)

## Cloud Infrastructure

- Amazon ECS Fargate
- Amazon RDS
- Amazon S3
- Amazon ECR
- Amazon CloudFront
- Application Load Balancer
- Docker

## Documentation

- MkDocs Material
- Markdown
- OpenAPI / Swagger

---

# Repository Structure

```text
app/
├── routers/
├── schemas/
├── models/
├── services/
├── utils/
├── db.py
└── main.py

docs/
├── platform/
├── tutorials/
├── how-to/
├── architecture/
├── api/
├── operations/
├── security/
└── supporting-materials/
```

---

# Running Locally

## Python

```bash
python -m venv .venv

.\.venv\Scripts\activate

pip install -r requirements.txt

uvicorn main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## Docker

```bash
docker build -t commerce-platform .

docker run -p 8000:8000 ^
  -e DB_TYPE=postgres ^
  -e DB_HOST=host.docker.internal ^
  -e DB_PORT=5432 ^
  -e DB_NAME=partner_catalog ^
  -e DB_USER=postgres ^
  -e DB_PASSWORD=your_password ^
  commerce-platform
```

---

# Authentication

Protected endpoints require:

```text
x-api-key: demo-secret-key
```

---

# Related Project

## Operations Console

The Operations Console is a React application that provides operational visibility into the Commerce Integration Platform.

Features include:

- Dashboard
- Feed management
- Product catalog
- Orders
- Partners
- Webhooks
- Analytics
- Global search

Repository:
https://github.com/rayajose/<operations-console-repo>

Live application:
https://d2mg19x9fth17i.cloudfront.net/

---

# What This Project Demonstrates

- FastAPI application development
- REST API design
- Cloud-native architecture
- PostgreSQL data modeling
- ETL processing
- Background job orchestration
- Partner integration workflows
- Transactional commerce services
- Webhook delivery
- Business analytics
- AWS deployment
- Docs-as-code
- Platform architecture documentation
- Developer documentation
- Operational procedures
- Security documentation

---

# Author

**Ray Jose**

📖 Technical Writing Portfolio  
https://rayajose.github.io/writing-portfolio/

🖥️ Operations Console  
https://d2mg19x9fth17i.cloudfront.net/

💻 GitHub  
https://github.com/rayajose
