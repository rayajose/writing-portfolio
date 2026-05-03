# Deployment Guide
> The Partner Catalog API application and its documentation are maintained in a single repository as part of this writing portfolio.
 The API is deployed separately using Docker and AWS (ECS, RDS, S3), while documentation is published via GitHub Pages.

This document describes the deployment of the Partner Catalog API to AWS using a containerized, managed infrastructure.

For visual confirmation of the deployed environment, see [Screenshots](screenshots.md).

---

## Architecture Overview

The Partner Catalog API is deployed using the following AWS services:

* **FastAPI** — application runtime packaged as a Docker container
* **Amazon ECR** — container image registry (`partner-catalog-api`)
* **Amazon ECS (Fargate)** — serverless container orchestration
* **Application Load Balancer (ALB)** — public HTTP endpoint and traffic routing
* **Amazon RDS (PostgreSQL)** — relational database for processed product data
* **Amazon S3** — raw data layer for uploaded feed files

The source code and documentation are maintained in the `writing-portfolio` repository. The deployed API continues to use AWS resource names based on the application name, `partner-catalog-api`.

---

## Container Configuration

**Image URI**

```text
792233688886.dkr.ecr.us-east-2.amazonaws.com/partner-catalog-api:latest
```

**Container Port**

```text
8000
```

---

## ECS Service Configuration

* Launch type: Fargate
* Desired tasks: 1 (set to 0 when not in use)
* Deployment strategy: Rolling update
* Load balancing: Enabled (via ALB target group)

---

## Networking

* VPC: `vpc-03a81166f39b94bd9`
* Subnets:

  * `subnet-0397a6bfd705d1c76`
  * `subnet-07a21f9409bffa8e9`
* Public IP assignment: Enabled

**ECS Security Group**

```text
sg-00778f0b6fabbf1af
```

* Allows outbound traffic to RDS and external services
* Used as the trusted source for database access

---

## Load Balancer (ALB)

**DNS Name**

```text
http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com
```

**Listener**

* HTTP :80 → Target Group

**Target Group**

* Protocol: HTTP
* Port: 8000
* Health check path: `/health`

---

## Database (RDS PostgreSQL)

* Engine: PostgreSQL
* Port: 5432
* Database name: `partner_catalog`

## Raw Data Storage (S3)

* Stores uploaded CSV feed files
* Acts as the system of record for raw partner data
* Used by the ETL process to extract and transform data
* Enables reprocessing and auditability

### Security Group

```text
sg-07a78daece2d2cf47
```

**Inbound Rules**

* PostgreSQL (5432) from ECS security group:

```text
sg-00778f0b6fabbf1af
```

* Optional: developer IP for direct access

**Notes**

* RDS is not publicly accessible
* Only ECS tasks are permitted to connect

---

## Environment Variables

Configured in the ECS task definition:

```text
DB_TYPE=postgres
DB_HOST=<rds-endpoint>
DB_PORT=5432
DB_NAME=partner_catalog
DB_USER=postgres
DB_PASSWORD=<secured>
```

### Optional (S3 Configuration)

```text
S3_RAW_BUCKET=partner-catalog-raw-rayj
```

* Defines the S3 bucket used to store raw feed files
* Used by the ETL process to locate and read uploaded data
* Can be externalized for different environments (dev, staging, prod)


---

## S3 and ETL Integration

* Raw feed files are stored in Amazon S3
* The application uses AWS SDK (`boto3`) to read files during ETL processing
* ETL is triggered via API (`POST /jobs/{job_id}/run`)
* ETL compares incoming data against existing records to avoid unnecessary updates
* The ECS task must have network access to S3

> Note: IAM permissions for S3 access are required in a production setup (not fully configured in this demo).


---

## Deployment Workflow

### 1. Authenticate to ECR

```bash
aws ecr get-login-password --region us-east-2 \
| docker login --username AWS --password-stdin 792233688886.dkr.ecr.us-east-2.amazonaws.com
```

### 2. Build Image

```bash
docker build -t partner-catalog-api .
```

### 3. Tag Image

```bash
docker tag partner-catalog-api:latest \
792233688886.dkr.ecr.us-east-2.amazonaws.com/partner-catalog-api:latest
```

### 4. Push Image

```bash
docker push 792233688886.dkr.ecr.us-east-2.amazonaws.com/partner-catalog-api:latest
```

### 5. Deploy to ECS

* Update the ECS service
* Enable **Force new deployment**

---

## Start / Stop Workflow (Cost Control)

### Stop the application

1. ECS → Service → Update
2. Set **Desired tasks = 0**
3. Deploy
4. RDS → Actions → **Stop temporarily**

---

### Start the application

1. RDS → **Start database**
2. Wait until status = **Available**
3. ECS → Service → Update
4. Set **Desired tasks = 1**
5. Deploy

---

## Health Check Behavior

* ALB performs HTTP health checks against `/health`
* Container must start successfully and establish database connectivity
* Failed health checks result in task replacement by ECS

---

## Troubleshooting

### Container fails to start

**Symptom**

* `CannotPullContainerError`

**Cause**

* Image not available in ECR

**Resolution**

* Verify image tag and push to ECR

---

### Container exits immediately

**Symptom**

* Exit code 1

**Cause**

* Application startup failure (commonly database connectivity)

**Resolution**

* Verify environment variables
* Confirm RDS accessibility from ECS

---

### Database connection timeout

**Error**

```text
psycopg.errors.ConnectionTimeout
```

**Cause**

* RDS security group does not allow inbound traffic from ECS

**Resolution**

* Add ECS security group to RDS inbound rules (port 5432)

---

## Cost Considerations

This deployment incurs cost from:

* ECS Fargate (compute)
* RDS (database instance)
* Application Load Balancer

To reduce cost:

* Stop ECS service when not in use
* Stop RDS instance when not in use (auto-restarts after ~7 days)
* Retain snapshots instead of running the database continuously

---

## Operational Notes

* Database schema is initialized at application startup (`init_db()`)
* The database must be reachable for the container to start successfully
* Single-task deployments may experience brief downtime during updates
* ETL processing is executed on-demand via the Jobs API
* Product data is loaded into PostgreSQL only after ETL completes
* Raw data remains stored in S3 for reprocessing and auditability
* ETL processing includes change detection:
  - New products are inserted
  - Existing products are only updated when data changes
  - Unchanged products are skipped

* ETL processing is idempotent:
  - Re-running the same feed does not create duplicate updates
  - Ensures efficient reprocessing and consistency

---

For deployment evidence, see [Screenshots](screenshots.md).
