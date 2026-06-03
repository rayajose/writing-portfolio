# Get started

Use the Commerce Integration API to upload product feeds, process them through ETL workflows, query normalized catalog data, and create transactional orders.

<div class="doc-meta">
  <span>API v1</span>
  <span>Authentication required</span>
  <span>CSV upload</span>
  <span>ETL workflow</span>
</div>


## Base URLs

| Target           | URL                                                                      |
| ---------------- | ------------------------------------------------------------------------ |
| Base URL (local) | `http://localhost:8000`                                                  |
| Base URL (live)  | `http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com`      |
| Swagger UI       | `http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com/docs` |


## Authenticate requests

!!! note "Requesting API access"

    The live API is protected by API key authentication.

    Recruiters, hiring managers, and reviewers interested in evaluating the platform may request a demonstration API key by contacting <a href="mailto:ray.a.jose@gmail.com">ray.a.jose@gmail.com</a>.

    API keys are issued for portfolio review purposes only and provide access to sample data within the demonstration environment.

Include your API key in each request:

```text
x-api-key: YOUR_API_KEY
```

Requests without a valid API key return `401 Unauthorized` or `403 Forbidden`.

## Quickstart

Use this workflow to upload a product feed, monitor processing, query catalog data, and create an order.


### 1. Upload a feed

#### Example request

```bash
curl -X POST http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com/feeds/upload \
  -H "x-api-key: YOUR_API_KEY" \
  -F "partner_name=Acme Corp" \
  -F "file=@acme-product-catalog.csv"
```


#### Example response

```json
{
  "feed_id": "FD00001",
  "partner_id": "PT00001",
  "partner_name": "Acme Corp",
  "status": "uploaded",
  "job_id": "JS00001"
}
```



### 2. Monitor processing status

After upload validation succeeds, the platform automatically processes the feed through ETL workflows.

#### Example request

```bash
curl -X GET http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com/feeds/JV00001 \
  -H "x-api-key: YOUR_API_KEY"
```

#### Example response

```json
{
  "feed_id": "FD00001",
  "partner_id": "PT00001",
  "partner_name": "Acme Corp",
  "file_name": "acme-product-catalog.csv",
  "content_type": "text/csv",
  "status": "uploaded",
  "uploaded_at": "YYYY-MM-DDTHH:MM:SSZ",
  "validation_job_id": "JV00001",
  "validation_status": "completed",
  "validation_message": "ETL processing completed. Products processed: 13. Inserted: 1. Updated: 0. Deleted: 1.Unchanged: 12. Skipped: 0.",
  "raw_file_s3_key": "raw/partners/acme-corp/feeds/FD00001/acme-product-catalog.csv",
  "raw_file_bucket": "commerce-integration-raw"
}
```

### 3. Query products

#### Example request

=== "curl"

    ```bash
    curl -X GET "http://<base-url>/products?limit=5" \
      -H "x-api-key: YOUR_API_KEY"
    ```

=== "Python"

    ```python
    import requests

    base_url = "http://<base-url>"
    api_key = "YOUR_API_KEY"

    response = requests.get(
        f"{base_url}/products",
        headers={"x-api-key": api_key},
        params={"limit": 5},
    )

    response.raise_for_status()
    print(response.json())
    ```

=== "JavaScript"

    ```javascript
    const baseUrl = "http://<base-url>";
    const apiKey = "YOUR_API_KEY";

    const response = await fetch(`${baseUrl}/products?limit=5`, {
      headers: {
        "x-api-key": apiKey,
      },
    });

    if (!response.ok) {
      throw new Error(`Request failed: ${response.status}`);
    }

    const data = await response.json();
    console.log(data);
    ```


#### Example response

```json
{
  "count": 1,
  "items": [
    {
      "product_id": "PR00001",
      "partner_id": "PT00001",
      "feed_id": "FD00001",
      "partner_name": "Acme Corp",
      "sku": "ACM-001",
      "product_name": "Acme Widget 3000",
      "description": "The best widget in the Acme collection.",
      "brand": "Acme",
      "category": "Widgets",
      "price": 79.99,
      "currency": "USD",
      "availability": "in_stock",
      "created_at": "YYYY-MM-DDTHH:MM:SSZ"
    }
  ]
}
```


### 4. Create an order

#### Example request

```bash
curl -X POST http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com/orders \
  -H "x-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_reference": "CR00001",
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


#### Example response

```json
{
  "order_id": "OR00001",
  "partner_id": "PT00001",
  "partner_name": "Acme Corp",
  "customer_reference": "CR00001",
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
| `partner_id`   | Filter by partner ID   |
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
| `PTxxxxx` | Partner          |
| `JSxxxxx` | Submission job   |
| `JVxxxxx` | Validation job   |
| `JFxxxxx` | Fulfillment job  |
| `CUxxxxx` | Customer         |
| `ADxxxxx` | Customer address |
| `PRxxxxx` | Product          |
| `ORxxxxx` | Order            |
| `OIxxxxx` | Order item       |


## Next steps

- Follow [Ingest a product feed](../how-to/ingest-product-feed.md)
- Use [Feeds](../api/feeds.md) to manage uploads
- Use [Partners](../api/partners.md) to manage partner records
- Use [Jobs](../api/jobs.md) to track processing
- Use [Products](../api/products.md) to query catalog data
- Use [Customers](../api/customers.md) to create fictional customers and shipping addresses
- Use [Orders](../api/orders.md) to create and retrieve order data
- Use [Analytics](../api/analytics.md) to analyze sales and revenue
- See [Debug a product feed failure](../operations/debug-product-feed.md) for troubleshooting workflows