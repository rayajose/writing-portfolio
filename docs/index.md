# Partner Catalog API

A cloud-based REST API for ingesting, processing, and querying partner product catalogs through a structured data pipeline.

Deployed on AWS using ECS Fargate, RDS (PostgreSQL), and S3 for raw data storage.

---

## What This Project Demonstrates

* API design for data ingestion pipelines
* End-to-end ETL workflow (extract, transform, load)
* Job-based processing and pipeline orchestration
* Separation of raw and processed data layers
* Developer-focused documentation (reference + workflows)
* Cloud-native deployment architecture (AWS ECS, RDS, S3)

---

## Key Features

* Upload partner product feeds (CSV)
* Store raw data in Amazon S3
* Execute ETL processing via job-based API
* Track processing status through job resources
* Query product catalog with filtering, sorting, and pagination

---

## Explore the API

* [Getting Started](getting_started.md)
* [Feeds](feeds.md)
* [Products](products.md)
* [Jobs](jobs.md)
* [Workflows](workflows.md)
* [About This Project](about.md)

---

## Architecture

* FastAPI (Python)
* Amazon ECS (Fargate)
* Amazon RDS (PostgreSQL)
* Amazon S3 (raw data layer)
* Docker

---

## Live API

Interactive API (Swagger UI):

<p>
<a href="http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com" target="_blank">http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com</a>
</p>


---

## Source Code

<p>
<a href="https://github.com/rayajose/partner-catalog-api" target="_blank">https://github.com/rayajose/partner-catalog-api</a>
</p>