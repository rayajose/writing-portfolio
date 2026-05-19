# Screenshots

Use this page to view the deployed Commerce Integration API running in an AWS environment.

<div class="doc-meta">
  <span>AWS deployment</span>
  <span>ECS Fargate</span>
  <span>Infrastructure</span>
  <span>Operational visibility</span>
</div>

## Live platform access

### Swagger UI

<p>
<a href="swagger-overview.png" class="glightbox" target="_blank">
  <img src="swagger-overview.png" alt="Swagger Overview" class="screenshot-img">
</a>
</p>

### Health endpoint

Use the `/health` endpoint to verify API availability and database connectivity.

<p>
<a href="swagger-health-check-endpoint.png" class="glightbox" target="_blank">
  <img src="swagger-health-check-endpoint.png" alt="Health Check Endpoint" class="screenshot-img">
</a>
</p>

## Container orchestration and deployment
Amazon ECS Fargate manages container orchestration, deployment lifecycle, running tasks, and container runtime configuration for the API service.

### Deployment
<p>
<a href="pcapi-ecs-service-deployment-overview.png" class="glightbox" target="_blank">
  <img src="pcapi-ecs-service-deployment-overview.png" alt="Deployment" class="screenshot-img">
</a>
</p>

### ECS service deployment
<p>
<a href="pcapi-ecs-service-performance-monitoring.png" class="glightbox" target="_blank">
  <img src="pcapi-ecs-service-performance-monitoring.png" alt="Performance Monitoring" class="screenshot-img">
</a>
</p>

### Running ECS tasks
<p>
<a href="pcapi-ecs-service-tasks.png" class="glightbox" target="_blank">
  <img src="pcapi-ecs-service-tasks.png" alt="Tasks" class="screenshot-img">
</a>
</p>

### ECS task definition
Shows container configuration, environment variables, and image settings used during deployment.
<p>
<a href="pcapi-ecs-service-task-definition.png" class="glightbox" target="_blank">
  <img src="pcapi-ecs-service-task-definition.png" alt="Task Definition" class="screenshot-img">
</a>
</p>

## Container configuration
<p>
<a href="pcapi-ecs-service-container-details.png" class="glightbox" target="_blank">
  <img src="pcapi-ecs-service-container-details.png" alt="Container Details" class="screenshot-img">
</a>
</p>

## Container registry

### Amazon ECR repository

The container image for the API is stored in Amazon Elastic Container Registry and used by ECS during deployment.
<p>
<a href="pcapi-ecr-repo.png" class="glightbox" target="_blank">
  <img src="pcapi-ecr-repo.png" alt="ECR Repo" class="screenshot-img">
</a>
</p>

## Traffic routing and load balancing

### Application Load Balancer listeners
<p>
<a href="pcapi-ec2-alb-listeners.png" class="glightbox" target="_blank">
  <img src="pcapi-ec2-alb-listeners.png" alt="ALB Listeners" class="screenshot-img">
</a>
</p>

### Network mapping
<p>
<a href="pcapi-ec2-alb-network-mapping.png" class="glightbox" target="_blank">
  <img src="pcapi-ec2-alb-network-mapping.png" alt="ALB Network Map" class="screenshot-img">
</a>
</p>

### Target group health checks
The target group monitors the health of running tasks using an HTTP health check endpoint to ensure traffic is only routed to healthy containers.
<p>
<a href="pcapi-ec2-target-group-health-check.png" class="glightbox" target="_blank">
  <img src="pcapi-ec2-target-group-health-check.png" alt="Target Group Health Checks" class="screenshot-img">
</a>
</p>

## Database infrastructure

### Amazon RDS PostgreSQL

The API persists data in a PostgreSQL database hosted on Amazon RDS, providing managed storage and availability.
<p>
    <a href="pcapi-rds.png" class="glightbox" target="_blank">
        <img src="pcapi-rds.png" alt="RDS" class="screenshot-img">
    </a>
</p>

## MkDocs documentation site
Documentation is generated using MkDocs Material and published through GitHub Pages as part of the same docs-as-code workflow used for the portfolio.