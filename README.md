# Commerce Integration Platform API

> FastAPI backend for a cloud-native commerce integration platform demonstrating REST APIs, ETL processing, systems integration, cloud deployment, and technical documentation.

This repository contains the backend services that power the **Commerce Integration Platform**. The API provides REST endpoints for partner onboarding, product catalog ingestion, transactional order processing, analytics, and webhook delivery while modeling production-style integration workflows.

The backend is part of a broader portfolio that demonstrates modern technical writing through a complete cloud-native platform.

---

# Explore the Platform

### 📖 Technical Writing Portfolio

Comprehensive documentation covering platform architecture, tutorials, implementation guides, operations, security, and API reference.

https://rayajose.github.io/writing-portfolio/

### 🖥️ Operations Console

Browser-based administrative application for monitoring platform activity.

https://d2mg19x9fth17i.cloudfront.net/

### 🔌 Interactive API (Swagger)

Explore and test REST endpoints through the OpenAPI interface.

http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com/docs

> **Note:** The API may be temporarily offline outside of demonstration periods to control cloud costs.

---

# Purpose

This project demonstrates how backend services support a modern commerce integration platform while showcasing technical documentation across an entire software ecosystem.

The platform models real-world workflows including:

- Partner onboarding
- Product catalog ingestion
- ETL processing
- Background job execution
- Customer and order management
- Webhook delivery
- Business analytics
- Operational monitoring
- Developer enablement

---

# Platform Overview

External partners submit product catalog feeds that are validated, processed, transformed, and made available for transactional and analytical workloads.

The API provides services for:

- Partner management
- Feed ingestion
- Processing jobs
- Product catalog
- Customers
- Orders
- Analytics
- Webhook subscriptions
- Webhook delivery tracking

These services support both external integrations and the browser-based Operations Console.

---

# API Resources

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

A primary objective of the platform is modeling realistic ingestion and processing behavior.

Features include:

- Feed validation
- Change detection
- Data transformation
- Background job execution
- Idempotent processing
- Processing statistics

Processing outcomes include:

- Inserted
- Updated
- Unchanged
- Skipped

This approach minimizes unnecessary database writes while providing accurate operational reporting.

---

# Analytics

The platform includes reporting endpoints supporting both operational monitoring and business analysis.

Available reporting includes:

- Sales by partner
- Sales over time
- Revenue distribution
- Top-performing products

Analytics operate directly on transactional platform data.

---

# Documentation

Documentation is maintained using a docs-as-code workflow and published with **MkDocs Material**.

The Technical Writing Portfolio includes:

- Platform Guide
- Tutorials
- How-to Guides
- Architecture
- API Reference
- Operations
- Security
- Supporting Materials

Rather than documenting isolated endpoints, the portfolio demonstrates how documentation supports an entire cloud-native platform throughout its lifecycle.

---

# Technology Stack

## Backend

- FastAPI
- Python

## Database

- PostgreSQL (Amazon RDS)

## Cloud

- Amazon ECS Fargate
- Application Load Balancer
- Amazon S3
- Amazon ECR
- Amazon CloudFront
- Docker

## Documentation

- Markdown
- MkDocs Material
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

```
http://127.0.0.1:8000/docs
```

---

## Docker

```bash
docker build -t commerce-platform-api .

docker run -p 8000:8000 ^
  -e DB_TYPE=postgres ^
  -e DB_HOST=host.docker.internal ^
  -e DB_PORT=5432 ^
  -e DB_NAME=partner_catalog ^
  -e DB_USER=postgres ^
  -e DB_PASSWORD=your_password ^
  commerce-platform-api
```

---

# Authentication

Protected endpoints require:

```text
x-api-key: demo-secret-key
```

---

# What This Repository Demonstrates

- FastAPI application development
- REST API design
- Production-style ETL workflows
- Background job processing
- Partner integration patterns
- Transactional commerce services
- Analytics services
- Webhook delivery
- PostgreSQL data modeling
- AWS cloud deployment
- OpenAPI documentation
- Docs-as-code practices

---

# Related Projects

- **Technical Writing Portfolio** — Comprehensive platform documentation built with MkDocs
- **Operations Console** — React administrative application for monitoring and managing the platform

---

# Author

**Ray Jose**

📖 Technical Writing Portfolio  
https://rayajose.github.io/writing-portfolio/

🖥️ Operations Console  
https://d2mg19x9fth17i.cloudfront.net/

💻 GitHub  
https://github.com/rayajose