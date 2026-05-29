# Deployment guide

This page explains how to deploy the Commerce Integration API to AWS using a containerized, cloud-native architecture supporting feed ingestion, ETL processing, customer management, order workflows, analytics services, and operational monitoring.

The application and its documentation are maintained in a single repository (`writing-portfolio`). The API is deployed using Docker and AWS services, while documentation is published through GitHub Pages.

For visual confirmation of the deployed environment, see [Screenshots](../api/screenshots.md).

<div class="doc-meta">
  <span>AWS deployment</span>
  <span>Containerized services</span>
  <span>ECS Fargate</span>
  <span>Infrastructure workflows</span>
</div>

## Architecture overview

The Commerce Integration API is deployed using the following AWS services:

- FastAPI application runtime packaged as a Docker container
- Amazon ECR container image registry (`<ecr-repository>`)
- Amazon ECS (Fargate) serverless container orchestration
- Application Load Balancer (ALB) for public HTTP access and traffic routing
- Amazon RDS (PostgreSQL) for product catalog, customer, order, fulfillment, and analytics data
- Amazon S3 for raw uploaded feed storage

The source code and documentation are maintained in the `writing-portfolio` repository. AWS resources continue to use the original application naming convention (`<ecr-repository>`).

!!! note "Single repository model"

    The API application, infrastructure documentation, and technical portfolio content are maintained within a unified docs-as-code repository workflow.

## Container configuration

### Image URI

```text
<aws-account-id>.dkr.ecr.<aws-region>.amazonaws.com/<ecr-repository>:v1.3.0
```

Versioned image tags are used for deployments. The `latest` tag is maintained for convenience and rollback scenarios.

### Container port

```text
8000
```

## ECS service configuration

- Launch type: Fargate
- Desired tasks: 1 (set to 0 when not in use)
- Deployment strategy: Rolling update
- Load balancing enabled through an ALB target group

!!! tip "Cost optimization"

    ECS services can be scaled down to zero running tasks when the environment is not actively being demonstrated or tested.

## Networking

### VPC

```text
vpc-03a81166f39b94bd9
```

### Subnets

```text
subnet-0397a6bfd705d1c76
subnet-07a21f9409bffa8e9
```

### Public IP assignment

```text
Enabled
```

## ECS security group

```text
sg-00778f0b6fabbf1af
```

### Purpose

- Allows outbound traffic to RDS and external services
- Serves as the trusted source for database access

## Load balancer (ALB)

### DNS name

```text
http://<application-load-balancer-dns-name>-1398338240.<aws-region>.elb.amazonaws.com
```

### Listener

- HTTP :80 → Target Group

### Target group

- Protocol: HTTP
- Port: 8000
- Health check path: `/health`

## Database (RDS PostgreSQL)

### Configuration

- Engine: PostgreSQL
- Port: 5432
- Database name: `partner_catalog`

### Security group

```text
sg-07a78daece2d2cf47
```

### Inbound rules

Allow PostgreSQL traffic from the ECS security group:

```text
sg-00778f0b6fabbf1af
```

Optional:

- Developer IP address for direct administrative access

### Notes

- RDS is not publicly accessible
- Only ECS tasks are permitted to connect

!!! warning "Database availability"

    ECS tasks depend on active PostgreSQL connectivity during application startup. Containers may fail health checks if the database is unavailable.

## Raw data storage (Amazon S3)

### Purpose

- Stores uploaded CSV feed files
- Serves as the raw system of record
- Supports ETL extraction and transformation workflows
- Enables feed reprocessing and auditability
- Preserves replay capability for downstream workflows

## Environment variables

Configured in the ECS task definition.

### Database configuration

```bash
DB_TYPE=postgres
DB_HOST=<rds-endpoint>
DB_PORT=5432
DB_NAME=partner_catalog
DB_USER=postgres
DB_PASSWORD=<secured>
```

### Security configuration

```bash
API_KEY=<secured>
PII_ENCRYPTION_KEY=<secured>
```

### Optional S3 configuration

```bash
S3_RAW_BUCKET=partner-catalog-raw-rayj
```

### Notes

- Defines the S3 bucket used for raw feed storage
- Used by the ETL pipeline to locate uploaded feed files
- `PII_ENCRYPTION_KEY` supports field-level encryption for customer-sensitive data
- Secrets should be externalized and never committed to source control
- Configuration can be externalized for different deployment environments

## S3 and ETL integration

- Raw feed files are stored in Amazon S3
- The application uses the AWS SDK (`boto3`) during ETL processing
- ETL processing is triggered through the Jobs API (`POST /jobs/{job_id}/run`)
- ETL compares incoming data against existing records to avoid unnecessary updates
- Product records support downstream customer and order workflows
- Raw uploaded feed files remain available for reprocessing, troubleshooting, and auditability
- ECS tasks require network access to S3

!!! note "IAM permissions"

    IAM permissions for Amazon S3 access are required in a production environment and are only partially configured in this demonstration deployment.

## Customer workflow considerations

Customer-sensitive workflows use field-level encryption for selected database fields including:

- Email addresses
- Phone numbers
- Street addresses
- Postal codes

Customer API responses expose masked values instead of raw sensitive values.

Customer lifecycle workflows support:

- Customer creation
- Customer retrieval
- Customer order history retrieval
- Customer deletion
- Bulk customer deletion

Customer deletion operations preserve historical order integrity by preventing deletion of customers or shipping addresses referenced by existing orders.

Deployment environments must ensure:

- `PII_ENCRYPTION_KEY` is configured
- Secrets remain externalized from source code
- Operational logs avoid sensitive customer data

## Deployment workflow

### 1. Authenticate to ECR

```bash
aws ecr get-login-password --region <aws-region> \
| docker login --username AWS --password-stdin <aws-account-id>.dkr.ecr.<aws-region>.amazonaws.com
```

### 2. Build the image

Replace the version number as appropriate for the release.

```bash
docker build -t <ecr-repository>:v1.3.0 .
```

### 3. Tag the image

```bash
docker tag <ecr-repository>:v1.3.0 \
<aws-account-id>.dkr.ecr.<aws-region>.amazonaws.com/<ecr-repository>:v1.3.0
```

### 4. Push the versioned image

```bash
docker push \
<aws-account-id>.dkr.ecr.<aws-region>.amazonaws.com/<ecr-repository>:v1.3.0
```

### 5. Update the latest tag

```bash
docker tag <ecr-repository>:v1.3.0 \
<aws-account-id>.dkr.ecr.<aws-region>.amazonaws.com/<ecr-repository>:latest

docker push \
<aws-account-id>.dkr.ecr.<aws-region>.amazonaws.com/<ecr-repository>:latest
```

### 6. Deploy to ECS

1. Register a new ECS task definition revision.
2. Update the container image tag if using versioned images.
3. Update the ECS service to use the new task definition revision.
4. Enable **Force new deployment**.
5. Deploy.

!!! tip "Rolling deployments"

    ECS rolling deployments allow updated containers to replace running tasks with minimal operational interruption.

## Start / stop workflow (cost control)

This workflow explains how to scale down ECS services and pause database resources to reduce AWS costs when the system is not in use.

### Stop the application

1. ECS → Service → Update
2. Set **Desired tasks = 0**
3. Deploy
4. RDS → Actions → **Stop temporarily**

### Start the application

1. RDS → **Start database**
2. Wait until status = **Available**
3. ECS → Service → Update
4. Set **Desired tasks = 1**
5. Deploy

## Health check behavior

- ALB performs HTTP health checks against `/health`
- The container must start successfully and establish database connectivity
- Encryption configuration must be available during application startup
- Failed health checks result in automatic task replacement by ECS

!!! warning "Health check dependency"

    Successful ALB health checks require both application startup completion and successful database connectivity.

## Troubleshooting

Use this section to diagnose and resolve common infrastructure and deployment issues.

### Container fails to start

#### Symptom

```text
CannotPullContainerError
```

#### Cause

- Image not available in ECR

#### Resolution

- Verify the image tag
- Confirm the image was successfully pushed to ECR

### Container exits immediately

#### Symptom

```text
Exit code 1
```

#### Cause

- Application startup failure
- Most commonly caused by database connectivity issues

#### Resolution

- Verify environment variables
- Confirm RDS accessibility from ECS

### Database connection timeout

#### Error

```text
psycopg.errors.ConnectionTimeout
```

#### Cause

- RDS security group does not allow inbound traffic from ECS

#### Resolution

- Add the ECS security group to the RDS inbound rules for port 5432

### Missing encryption key configuration

#### Error

```text
RuntimeError: PII_ENCRYPTION_KEY environment variable is not set.
```

#### Cause

- Encryption configuration missing from the ECS task definition

#### Resolution

- Add `PII_ENCRYPTION_KEY` to ECS task configuration
- Redeploy ECS tasks
- Verify application startup completes successfully

## Cost considerations

This deployment incurs cost from the following AWS services:

- ECS Fargate
- Amazon RDS
- Application Load Balancer

### Cost reduction strategies

- Stop the ECS service when not in use
- Stop the RDS instance when not in use
- Retain snapshots instead of continuously running the database

!!! note "Temporary RDS shutdown"

    Amazon RDS automatically restarts temporarily stopped database instances after approximately seven days.

AWS resources retain the original application naming convention (`<ecr-repository>`).

## Operational notes

- Database schema initialization occurs at application startup (`init_db()`)
- The database must be reachable for the container to start successfully
- Customer-sensitive fields are encrypted before database persistence
- Customer API responses expose masked values only
- Customer deletion operations enforce referential integrity checks before deleting customer and address records
- Bulk customer deletion workflows provide per-record success and failure reporting
- Single-task deployments may experience brief downtime during deployments
- ETL processing is executed on demand through the Jobs API
- Product data is persisted to PostgreSQL only after ETL completes
- Raw uploaded data remains stored in S3 for reprocessing and auditability

### ETL change detection behavior

- New products are inserted
- Existing products are updated only when data changes
- Unchanged products are skipped

### Idempotent ETL processing

- Re-running the same feed does not create duplicate updates
- Supports safe reprocessing and operational consistency

!!! tip "Safe reprocessing"

    ETL change-detection logic prevents duplicate product updates when previously processed feeds are re-executed.

## Operational security considerations

Deployment environments should:

- Restrict database access to authorized infrastructure components
- Protect API keys and encryption secrets
- Avoid logging customer-sensitive values
- Restrict access to raw uploaded feed data
- Separate development and production credentials

For deployment evidence, see [Screenshots](../api/screenshots.md).