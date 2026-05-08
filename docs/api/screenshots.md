# Screenshots

Use this page to view the deployed Commerce Integration API running in an AWS environment.

## Live API documentation
<p>
<a href="swagger-overview.png" class="glightbox" target="_blank">
  <img src="swagger-overview.png" alt="Swagger Overview" width="100%">
</a>
</p>

## Health endpoint

Use the `/health` endpoint to verify API availability and database connectivity.

<p>
<a href="swagger-health-check-endpoint.png" class="glightbox" target="_blank">
  <img src="swagger-health-check-endpoint.png" alt="Health Check Endpoint" width="100%">
</a>
</p>

## ECS task definition and container configuration
The task definition specifies the container image from Amazon ECR and runtime configuration, including environment variables used for database connectivity.

### Deployment
<p>
<a href="pcapi-ecs-service-deployment-overview.png" class="glightbox" target="_blank">
  <img src="pcapi-ecs-service-deployment-overview.png" alt="Deployment" width="100%">
</a>
</p>

### Performance monitoring
<p>
<a href="pcapi-ecs-service-performance-monitoring.png" class="glightbox" target="_blank">
  <img src="pcapi-ecs-service-performance-monitoring.png" alt="Performance Monitoring" width="100%">
</a>
</p>

### Tasks
<p>
<a href="pcapi-ecs-service-tasks.png" class="glightbox" target="_blank">
  <img src="pcapi-ecs-service-tasks.png" alt="Tasks" width="100%">
</a>
</p>

## ECS task definition
Shows container configuration, environment variables, and image settings used during deployment.
<p>
<a href="pcapi-ecs-service-task-definition.png" class="glightbox" target="_blank">
  <img src="pcapi-ecs-service-task-definition.png" alt="Task Definition" width="100%">
</a>
</p>

## Container details
<p>
<a href="pcapi-ecs-service-container-details.png" class="glightbox" target="_blank">
  <img src="pcapi-ecs-service-container-details.png" alt="Container Details" width="100%">
</a>
</p>

## Amazon ECR repository
The container image for the API is stored in Amazon Elastic Container Registry and used by ECS during deployment.
<p>
<a href="pcapi-ecr-repo.png" class="glightbox" target="_blank">
  <img src="pcapi-ecr-repo.png" alt="ECR Repo" width="100%">
</a>
</p>

## Application load balancer

### Rules and listeners
<p>
<a href="pcapi-ec2-alb-listeners.png" class="glightbox" target="_blank">
  <img src="pcapi-ec2-alb-listeners.png" alt="ALB Listeners" width="100%">
</a>
</p>

### Network mapping
<p>
<a href="pcapi-ec2-alb-network-mapping.png" class="glightbox" target="_blank">
  <img src="pcapi-ec2-alb-network-mapping.png" alt="ALB Network Map" width="100%">
</a>
</p>

## Target group health checks
The target group monitors the health of running tasks using an HTTP health check endpoint to ensure traffic is only routed to healthy containers.
<p>
<a href="pcapi-ec2-target-group-health-check.png" class="glightbox" target="_blank">
  <img src="pcapi-ec2-target-group-health-check.png" alt="Target Group Health Checks" width="100%">
</a>
</p>

## Amazon RDS PostgreSQL database
The API persists data in a PostgreSQL database hosted on Amazon RDS, providing managed storage and availability.
<p>
    <a href="pcapi-rds.png" class="glightbox" target="_blank">
        <img src="pcapi-rds.png" alt="RDS" width="100%">
    </a>
</p>

## MkDocs documentation site
Documentation is generated using MkDocs and hosted via GitHub Pages.