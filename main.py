from fastapi import FastAPI
from routers import feeds, jobs, products, health, analytics, orders
from db import init_db

tags_metadata = [
  {
    "name": "Feeds",
    "description": "Upload and manage partner product feeds. Feeds are ingested, validated, and tracked through the processing pipeline before products become available for querying."
  },
  {
    "name": "Jobs",
    "description": "Monitor background processing jobs for feed ingestion and validation. Jobs expose execution status, progress, and error details for troubleshooting."
  },
  {
    "name": "Products",
    "description": "Query the centralized product catalog using filtering, sorting, and cursor-based pagination to access up-to-date partner product data."
  },
  {
    "name": "Orders",
    "description": "Create and retrieve customer orders and associated order items. "
        "Orders are generated from catalog products and include calculated totals, "
        "line item pricing, and order status tracking."
  },
  {
    "name": "Health",
    "description": "Check the operational status of the API and underlying services. Used for monitoring, automated health checks, and verifying system availability."
  },
  {
    "name": "Analytics",
    "description": "Retrieve aggregated metrics derived from catalog and order data, including sales trends, revenue share, and partner performance across the platform."
  }
]

app = FastAPI(
    title="Partner Catalog API",

    description=(
        "A REST API for ingesting partner product feeds, validating data, "
        "tracking processing jobs, and querying a centralized product catalog.\n\n"
        "This project demonstrates real-world API design, including:\n"
        "- File-based data ingestion (CSV uploads)\n"
        "- Background job tracking\n"
        "- Structured error handling\n"
        "- Filtering, sorting, and pagination\n"
        "- Deployment to AWS (ECS Fargate + RDS)\n\n"
        "Authentication is handled via an API key passed in the `x-api-key` header."
    ),
    version="0.1.0",
    contact={
        "name": "Ray Jose",
        "url": "https://github.com/rayajose/writing-portfolio",
        "email": "ray.a.jose@gmail.com",
        },
license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
        },
    openapi_tags=tags_metadata,
)

init_db()

app.include_router(feeds.router, tags=["Feeds"])
app.include_router(jobs.router, tags=["Jobs"])
app.include_router(products.router, tags=["Products"])
app.include_router(health.router, tags=["Health"])
app.include_router(analytics.router, tags=["Analytics"])
app.include_router(orders.router, tags=["Orders"])