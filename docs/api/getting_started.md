# Get started

Use the Commerce Integration API to upload product feeds, process them through ETL workflows, query normalized catalog data, and create transactional orders.

<div class="doc-meta">
  <span>API v1</span>
  <span>Authentication required</span>
  <span>CSV upload</span>
  <span>ETL workflow</span>
</div>


## Base URLs

| Target     | URL                                                                                                                                                                         |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Local      | `http://localhost:8000`                                                                                                                                                     |
| AWS        | `http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com`                                                                                                         |
| Swagger UI | <a href="http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com/docs" target="_blank">http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com/docs</a> |


## Authenticate requests

Include your API key in each request:

```text
x-api-key: YOUR_API_KEY
```

Requests without a valid API key return `401 Unauthorized` or `403 Forbidden`.

!!! note "Demo authentication"

    The API uses a demo API key for documentation and portfolio purposes. Production-style API access and additional credentials can be discussed upon request.


## Quickstart

Use this workflow to ingest catalog data, query products, and create an order.


### 1. Upload a feed

```bash
curl -X POST http://localhost:8000/feeds/upload \
  -H "x-api-key: YOUR_API_KEY" \
  -F "file=@electronics_catalog.csv" \
  -F "partner_name=Tronics"
```


### Example response

```json
{
  "feed_id": "FD00001",
  "status": "uploaded",
  "job_id": "JS00001"
}
```


### 2. Run ETL processing

```bash
curl -X POST http://localhost:8000/jobs/JV00001/run \
  -H "x-api-key: YOUR_API_KEY"
```


### 3. Query products

```bash
curl -X GET http://localhost:8000/products?limit=5 \
  -H "x-api-key: YOUR_API_KEY"
```


### Example response

```json
{
  "count": 1,
  "items": [
    {
      "product_id": "PR00001",
      "feed_id": "FD00001",
      "partner_name": "Acme Corp",
      "sku": "ACM-001",
      "product_name": "Running Shoes",
      "description": "Lightweight running shoes designed for comfort and performance.",
      "brand": "Acme",
      "category": "Footwear",
      "price": 79.99,
      "currency": "USD",
      "availability": "in_stock",
      "created_at": "2026-04-15T10:00:00Z"
    }
  ]
}
```


### 4. Create an order

```bash
curl -X POST http://localhost:8000/orders \
  -H "x-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "partner_name": "Acme Corp",
    "customer_reference": "ORDER-1001",
    "customer_id": "CU00001",
    "shipping_address_id": "AD00001",
    "items": [
      {
        "product_id": "PR00001",
        "quantity": 2
      }
    ]
  }'
```


### Example response

```json
{
  "order_id": "OR00001",
  "partner_name": "Acme Corp",
  "customer_reference": "ORDER-1001",
  "customer_id": "CU00001",
  "shipping_address_id": "AD00001",
  "status": "created",
  "total_amount": 159.98,
  "currency": "USD",
  "items": [
    {
      "order_item_id": "OI00001",
      "product_id": "PR00001",
      "sku": "ACM-001",
      "product_name": "Running Shoes",
      "quantity": 2,
      "unit_price": 79.99,
      "line_total": 159.98
    }
  ]
}
```


## Understand the workflow

Product data becomes available only after ingestion and ETL processing complete.

<div class="diagram-card" markdown="1">
![Ingestion and order flow](../api/screenshots/ingestion-order-flow.svg)
</div>


## Use query parameters

Use query parameters to filter, sort, and paginate API results.


### Pagination

| Parameter | Description                                      |
| --------- | ------------------------------------------------ |
| `limit`   | Number of results. Default: `10`. Maximum: `100` |
| `cursor`  | Cursor for the next page of results              |


### Filtering

| Parameter      | Description            |
| -------------- | ---------------------- |
| `partner_name` | Filter by partner      |
| `feed_id`      | Filter by feed         |
| `brand`        | Filter by brand        |
| `category`     | Filter by category     |
| `availability` | Filter by availability |


### Sorting

| Parameter | Description                                        |
| --------- | -------------------------------------------------- |
| `sort_by` | Sort field (`price`, `created_at`, `product_name`) |
| `order`   | Sort direction (`asc` or `desc`)                   |


## Handle errors

The API uses standard HTTP status codes.

| Status | Meaning                        |
| ------ | ------------------------------ |
| `200`  | Request completed successfully |
| `201`  | Resource created successfully  |
| `400`  | Invalid request                |
| `401`  | Missing API key                |
| `403`  | Invalid API key                |
| `404`  | Resource not found             |
| `409`  | Request conflict               |
| `422`  | Validation failure             |
| `500`  | Internal server error          |


### Example error

```json
{
  "detail": "Invalid or missing API key"
}
```


## Resource identifiers

The platform uses structured identifiers for feeds, jobs, customers, products, addresses, orders, and fulfillment workflows.

| Prefix    | Resource         |
| --------- | ---------------- |
| `FDxxxxx` | Feed             |
| `JSxxxxx` | Submission job   |
| `JVxxxxx` | Validation job   |
| `JFxxxxx` | Fulfillment job  |
| `CUxxxxx` | Customer         |
| `ADxxxxx` | Customer address |
| `PRxxxxx` | Product          |
| `ORxxxxx` | Order            |
| `OIxxxxx` | Order item       |


## Next steps

- Follow [Ingest a product feed end-to-end](ingest-product-feed.md)
- Use [Feeds](feeds.md) to manage uploads
- Use [Jobs](jobs.md) to track processing
- Use [Products](products.md) to query catalog data
- Use [Customers](customers.md) to create fictional customers and shipping addresses
- Use [Orders](orders.md) to create and retrieve order data
- Use [Analytics](analytics.md) to analyze sales and revenue
- See [Debug a product feed failure](../operations/debug-product-feed.md) for troubleshooting workflows