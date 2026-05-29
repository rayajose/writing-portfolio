# Application deployment procedure

This procedure defines the workflow for planning, validating, deploying, and verifying application changes for the Commerce Integration API platform.

The procedure supports controlled deployment activities across application, infrastructure, and operational workflows while reducing deployment-related risk.


## Purpose

This procedure is intended to:

- Standardize deployment workflows
- Reduce deployment-related risk
- Support repeatable release procedures
- Provide rollback guidance
- Improve deployment visibility
- Ensure deployment verification activities are completed consistently


## Scope

This procedure applies to:

- FastAPI application updates
- Docker image deployments
- ECS service updates
- ETL processing updates
- Database schema changes
- Operational configuration changes
- Documentation-related deployment activities


## Deployment architecture overview

The Commerce Integration API is deployed using:

- Amazon ECS (Fargate)
- Amazon ECR
- Amazon RDS (PostgreSQL)
- Amazon S3
- Application Load Balancer (ALB)

Application containers are deployed through ECS services using Docker images stored in Amazon ECR.


## Deployment prerequisites

Before deployment:

- Validate application changes locally
- Verify Docker image builds complete successfully
- Confirm required environment variables
- Review database schema changes
- Evaluate operational impact
- Confirm existing services are healthy


## Local validation workflow

Validate application behavior locally before deployment.

Recommended validation activities include:

- API endpoint validation
- ETL processing validation
- Database connectivity testing
- Swagger UI verification
- Job execution testing
- Order and analytics validation


### Example local startup

```bash
uvicorn main:app --reload
```


### Example validation endpoints

```text
/health
/products
/jobs/{job_id}
/orders
```


## Build and publish workflow


### Authenticate to Amazon ECR

```bash
aws ecr get-login-password --region <aws-region> \
| docker login --username AWS --password-stdin <aws-account-id>.dkr.ecr.<aws-region>.amazonaws.com
```


### Build Docker image

```bash
docker build -t partner-catalog-api .
```


### Tag Docker image

```bash
docker tag partner-catalog-api:latest \
<aws-account-id>.dkr.ecr.<aws-region>.amazonaws.com/partner-catalog-api:latest
```


### Push Docker image

```bash
docker push <aws-account-id>.dkr.ecr.<aws-region>.amazonaws.com/partner-catalog-api:latest
```


## ECS deployment workflow

Deploy updated application images through the ECS service configuration.


### Deployment steps

1. Open the ECS service
2. Select the active service
3. Update the service
4. Enable **Force new deployment**
5. Deploy the updated task set


### Deployment behavior

- ECS replaces running tasks using rolling deployment behavior
- ALB health checks validate container availability
- Failed tasks are replaced automatically


## Deployment verification

Validate deployment success after rollout completes.


### Verification activities

- Confirm ECS tasks reach healthy status
- Confirm ALB target health status
- Verify `/health` endpoint responses
- Validate Swagger UI accessibility
- Validate database connectivity
- Execute representative API requests
- Confirm ETL processing functionality


### Example verification endpoint

```text
/health
```


## Database change considerations

Validate database schema changes carefully before deployment.

Consider:

- Backward compatibility
- ETL processing impact
- Existing data integrity
- Analytics query compatibility
- Order workflow compatibility

Validate schema changes locally before updating deployed environments.


## Deployment failure handling

Deployment failures should trigger investigation and recovery procedures.


### Common deployment failures

| Failure type                  | Example                          |
| ----------------------------- | -------------------------------- |
| Container startup failure     | Application runtime error        |
| Database connectivity failure | PostgreSQL connection timeout    |
| Health check failure          | `/health` endpoint unavailable   |
| Image deployment failure      | Invalid or unavailable image     |
| Schema mismatch               | Database structure inconsistency |


## Rollback considerations

If deployment validation fails:

- Review ECS task logs
- Review deployment configuration
- Confirm database accessibility
- Verify image integrity
- Redeploy the previous known-good configuration if required

Rollback procedures should prioritize restoring application availability and processing stability.


## Operational monitoring during deployment

Monitor deployment activity throughout rollout and validation workflows.

Recommended monitoring activities include:

- ECS task state monitoring
- ALB health check monitoring
- API availability validation
- ETL workflow validation
- Database connectivity verification


## Responsibilities


### Platform administrators

Responsible for:

- Infrastructure configuration
- ECS deployment operations
- Deployment validation
- Rollback coordination


### Developers

Responsible for:

- Application validation
- Docker image preparation
- Local testing
- Change verification


### Integration operators

Responsible for:

- Workflow verification
- ETL validation
- Feed processing confirmation
- Operational issue escalation


## Deployment principles

The platform follows these deployment principles:

- Validate locally before deployment
- Use controlled deployment workflows
- Verify operational health after rollout
- Preserve rollback capability
- Monitor deployment activity
- Reduce operational disruption during updates


## Related documentation

- [Operations](index.md)
- [Deployment guide](../architecture/deployment.md)
- [Platform architecture and operational flow](../architecture/platform-architecture.md)
- [Debug a product feed failure](debug-product-feed.md)
- [Backup and recovery procedure](backup-recovery-procedure.md)