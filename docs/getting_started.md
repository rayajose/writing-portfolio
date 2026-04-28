# Getting Started

This guide helps you quickly begin using the Partner Catalog API, including authentication, making requests, and understanding responses.

---

## Base URL

Local:

```text id="w2z0yo"
http://localhost:8000
```

Production:

```text id="n8g2k7"
http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com
```

Interactive API (Swagger UI):

```text id="t6b5hj"
http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com/docs
```

---

## Authentication

All requests require an API key passed in the request header:

```text id="q4l7cx"
x-api-key: demo-secret-key
```

---

## Quick Example

Retrieve a list of products:

```bash id="2jfq0r"
curl -X GET "http://localhost:8000/products?limit=5" \
  -H "x-api-key: demo-secret-key"
```

---

## Example Response

```json id="7e5mxl"
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

---

## Important Note

Product data is only available **after ETL processing completes**.

Typical workflow:

```text id="gqf3al"
Upload feed → Run ETL job → Query products
```

See [Workflows](workflows.md) for the full ingestion process.

---

## Common Query Parameters

### Pagination

| Parameter | Description                                         |
|-----------|-----------------------------------------------------|
| `limit`   | Number of results to return (default: 10, max: 100) |
| `cursor`  | Cursor for retrieving the next page of results      |

---

### Filtering

| Parameter      | Description            |
|----------------|------------------------|
| `partner_name` | Filter by partner name |
| `feed_id`      | Filter by feed ID      |
| `brand`        | Filter by brand        |
| `category`     | Filter by category     |
| `availability` | Filter by availability |

---

### Sorting

| Parameter | Description                                                    |
|-----------|----------------------------------------------------------------|
| `sort_by` | Field to sort by (`price`, `created_at`, `product_name`, etc.) |
| `order`   | Sort order: `asc` or `desc`                                    |

---

## Error Handling

The API uses standard HTTP status codes:

| Status Code | Meaning                                                |
|-------------|--------------------------------------------------------|
| 200         | Request successful                                     |
| 400         | Bad request (invalid input or business rule violation) |
| 401         | Unauthorized (missing API key)                         |
| 403         | Forbidden (invalid API key)                            |
| 404         | Resource not found                                     |
| 500         | Internal server error                                  |

### Example Error Response

```json id="r3k0t8"
{
  "detail": "Invalid or missing API key"
}
```

---

## Next Steps

* Start with [Workflows](workflows.md) to understand the full ingestion pipeline
* Review [Feeds](feeds.md) for uploading product feeds
* Explore [Jobs](jobs.md) for ETL execution and status tracking
* Use [Products](products.md) for querying catalog data

---
