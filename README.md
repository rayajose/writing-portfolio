# Partner Catalog API

> Production-style API, data platform, and documentation portfolio demonstrating ETL, analytics, and developer enablement

A production-style system that simulates how multi-partner platforms ingest, process, analyze, and serve product catalog data.

This project goes beyond a typical API implementation by combining:

* Backend system design
* Data pipeline modeling (ETL + analytics)
* Real-world documentation use cases (SOPs, how-to guides, security docs)

---

## Purpose

This project demonstrates how technical documentation supports real systems, including:

* REST API design and developer documentation
* Data ingestion and ETL workflows
* Analytical querying and reporting
* Operational procedures and troubleshooting
* Security and incident response documentation

---

## Live API

Swagger UI:
http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com/docs

> Note: The API may be temporarily offline outside of demonstration periods to control cloud costs.

---

## Documentation (Docs-as-Code)

All documentation is managed using a **docs-as-code approach**:

* Written in Markdown
* Version-controlled alongside code
* Structured for developer and operational use
* Published via MkDocs

### Live Documentation

https://rayajose.github.io/writing-portfolio/

---

## Documentation Scope

This repository is supported by a broader documentation set that reflects real-world use cases:

### API & Developer Documentation

* REST API reference
* SDK usage examples
* Request/response patterns

### SOP (Operational Documentation)

* Partner feed onboarding process
* System initialization and validation workflows
* Repeatable operational procedures

### How-To Guides

* End-to-end feed ingestion workflow
* Debugging failed feeds
* ETL execution and validation

### Security Documentation

* Incident response plan
* System recovery considerations
* Operational risk awareness

All documentation is tied to the same system and data model, demonstrating consistency across content types.

---

## System Overview

The Partner Catalog API simulates a real-world ingestion platform where external partners submit product data feeds that are processed and made available for querying and analytics.

---

## Project Evolution

### Phase 1–2 — API + Ingestion

* Feed upload and processing
* Job-based workflows
* Product retrieval

### Phase 3 — ETL Pipeline

* Change detection (insert/update/unchanged/skip)
* Idempotent processing
* Data validation and transformation

### Phase 4 — Analytics Layer

* Orders fact table
* Aggregated queries (product, partner, time)
* Revenue distribution analysis
* API endpoints for analytics delivery

---

## Analytics Layer

The system includes a business intelligence layer built on top of operational data.

### Data Model

* `products` (dimension)
* `orders` (fact table)
* `partner_name` (dimension)
* `order_date` (time dimension)

### Analytics Use Cases

* Sales by partner
* Sales over time (daily / monthly)
* Top-performing products
* Revenue share by partner

### Example Query (Revenue Share)

```sql
SELECT
    partner_name,
    SUM(total_amount) AS total_revenue,
    ROUND(
        100.0 * SUM(total_amount) / SUM(SUM(total_amount)) OVER (),
        2
    ) AS revenue_pct
FROM orders
GROUP BY partner_name;
```

### Analytics API Endpoints

* `GET /analytics/sales-by-partner`
* `GET /analytics/sales-over-time`
* `GET /analytics/top-products`
* `GET /analytics/revenue-share`

---

## ETL Behavior (Core Design Feature)

The ETL pipeline uses change detection:

* Inserted → New product
* Updated → Data changed
* Unchanged → No change
* Skipped → Invalid rows

This ensures:

* Idempotent reprocessing
* No unnecessary database writes
* Accurate change tracking

---

## Architecture

```
app/
├── main.py
├── routers/
│   ├── feeds.py
│   ├── jobs.py
│   ├── products.py
│   └── analytics.py
├── schemas/
│   ├── feeds.py
│   ├── jobs.py
│   ├── products.py
│   └── analytics.py
├── db.py
```

---

## Data Domains

The dataset spans multiple partner types:

* Craft beer (Microbrews Brothers)
* Consumer electronics (RayTech, Tronics)
* Vinyl records (Cid's Vintage Records)
* Jewelry (Joyeria Reina)

This enables realistic analytics scenarios such as:

* High-volume vs high-value comparisons
* Revenue concentration
* Product mix analysis

---

## Tech Stack

* FastAPI (Python)
* PostgreSQL (Amazon RDS)
* Docker
* Amazon ECS (Fargate)
* Application Load Balancer
* Amazon ECR
* MkDocs

---

## Run Locally

### Python

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

### Docker

```bash
docker build -t partner-catalog-api .

docker run -p 8000:8000 ^
  -e DB_TYPE=postgres ^
  -e DB_HOST=host.docker.internal ^
  -e DB_PORT=5432 ^
  -e DB_NAME=partner_catalog ^
  -e DB_USER=postgres ^
  -e DB_PASSWORD=your_password ^
  partner-catalog-api
```

---

## Authentication

All endpoints require:

```
x-api-key: demo-secret-key
```

---

## What This Project Demonstrates

* API and backend system design
* ETL pipeline architecture with change detection
* Analytical querying and data modeling
* API-driven analytics delivery
* Documentation across multiple content types
* Docs-as-code workflows using Markdown and MkDocs

This project reflects a **production-style system with supporting documentation**, not just a standalone API.

---

## Author

Ray Jose

* Portfolio: https://rayajose.github.io/writing-portfolio/
* GitHub: https://github.com/rayajose
