# Analytics API

Use this API to expose read-only endpoints for aggregated insights.

- Retrieve aggregated sales and revenue metrics across partners
- Analyze product and order data through precomputed summaries
- Support reporting and dashboards with queryable analytics endpoints

---

## Authentication

All endpoints in this resource require a valid `x-api-key` header.

Include the API key in each request:

```bash
-H "x-api-key: YOUR_API_KEY"
```

---

## GET /analytics/sales-by-partner

Use this endpoint to retrieve total units and revenue by partner.

### What happens

- The system aggregates order data grouped by `partner_name`
- Calculates total units sold and total revenue per partner
- Returns a list of partners sorted by total revenue (highest first)

---

### Request and response

<div  class="api-example-grid">
<div>

<h3>Request</h3>

```bash
curl -X 'GET' \
  'http://api.example.com/analytics/sales-by-partner' \
  -H 'accept: application/json' \
  -H 'x-api-key: demo-secret-key'
```

</div>

<div>

<h3>Response</h3>

```json
{
  "analytics_type": "sales_by_partner",
  "results": [
    {
      "partner_name": "RayTech Corp.",
      "units_sold": 31,
      "total_sales": "14759.79"
    },
    {
      "partner_name": "Tronics",
      "units_sold": 23,
      "total_sales": "11750.86"
    },
    {
      "partner_name": "Joyeria Reina",
      "units_sold": 17,
      "total_sales": "11296.39"
    }
  ]
}
```

</div>
</div>

---

### Response fields

| Field            | Type    | Description                                     |
| ---------------- | ------- | ----------------------------------------------- |
| `analytics_type` | string  | Type of analytics returned (`sales_by_partner`) |
| `results`        | array   | List of aggregated sales results by partner     |
| `partner_name`   | string  | Name of the partner                             |
| `units_sold`     | integer | Total number of units sold for the partner      |
| `total_sales`    | string  | Total revenue for the partner (currency value)  |


---

## GET /analytics/sales-over-time

Use this endpoint to retrieve time-based sales metrics.

### What happens

- The system aggregates order data over time based on the specified `grain`
- Calculates total units sold and total revenue for each time interval
- Returns results grouped and ordered chronologically

---

### Query parameters

| Name    | Type   | Required | Description                                          |
| ------- | ------ | -------- | ---------------------------------------------------- |
| `grain` | string | No       | Time interval for aggregation (`daily` or `monthly`) |

Defaults to `daily` if `grain` parameter is not sent with the request.

---

### Request and response

<div  class="api-example-grid">
<div>

<h3>Request</h3>

```bash
curl -X 'GET' \
  'http://api.example.com/analytics/sales-over-time?grain=daily' \
  -H 'accept: application/json' \
  -H 'x-api-key: demo-secret-key'
```

</div>

<div>

<h3>Response</h3>

```json
{
  "analytics_type": "sales_over_time",
  "grain": "daily",
  "results": [
    {
      "sales_period": "2026-04-01",
      "units_sold": 15,
      "total_sales": "2145.87"
    },
    {
      "sales_period": "2026-04-02",
      "units_sold": 7,
      "total_sales": "1274.93"
    },
    {
      "sales_period": "2026-04-03",
      "units_sold": 13,
      "total_sales": "2341.89"
    }
  ]
}
```

</div>
</div>

---

### Response fields

| Field            | Type    | Description                                                 |
| ---------------- | ------- | ----------------------------------------------------------- |
| `analytics_type` | string  | Type of analytics returned (`sales_over_time`)              |
| `grain`          | string  | Time interval used for aggregation (`daily` or `monthly`)   |
| `results`        | array   | List of aggregated sales results by time period             |
| `sales_period`   | string  | Time period for the aggregation (format depends on `grain`) |
| `units_sold`     | integer | Total number of units sold during the period                |
| `total_sales`    | string  | Total revenue for the period (currency value)               |


---

### Error responses

#### 401 Unauthorized
Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```

#### 422 Unprocessable entity
Returned when request validation fails  for invalid `grain` value.

```json
{
  "detail": [
    {
      "type": "enum",
      "loc": [
        "query",
        "grain"
      ],
      "msg": "Input should be 'daily' or 'monthly'",
      "input": "weekly",
      "ctx": {
        "expected": "'daily' or 'monthly'"
      }
    }
  ]
}
```

---

## GET /analytics/revenue-share

Use this endpoint to retrieve each partner’s percentage contribution to total revenue.

### What happens

- The system aggregates total revenue by `partner_name`
- Calculates each partner’s percentage contribution relative to overall revenue
- Returns results sorted by highest revenue contribution

---

### Request and response

<div  class="api-example-grid">
<div>

<h3>Request</h3>

```bash
curl -X 'GET' \
  'http://api.example.com/analytics/revenue-share' \
  -H 'accept: application/json' \
  -H 'x-api-key: demo-secret-key'
```

</div>

<div>

<h3>Response</h3>

```json
{
  "analytics_type": "revenue_share",
  "results": [
    {
      "partner_name": "RayTech Corp.",
      "total_revenue": "14759.79",
      "revenue_pct": 37.55
    },
    {
      "partner_name": "Tronics",
      "total_revenue": "11750.86",
      "revenue_pct": 29.9
    },
    {
      "partner_name": "Joyeria Reina",
      "total_revenue": "11296.39",
      "revenue_pct": 28.74
    }
  ]
}
```

</div>
</div>

---

### Response fields

| Field            | Type   | Description                                            |
| ---------------- | ------ | ------------------------------------------------------ |
| `analytics_type` | string | Type of analytics returned (`revenue_share`)           |
| `results`        | array  | List of revenue share results by partner               |
| `partner_name`   | string | Name of the partner                                    |
| `total_revenue`  | string | Total revenue generated by the partner                 |
| `revenue_pct`    | number | Percentage of total revenue contributed by the partner |

---

### Error responses

#### 401 Unauthorized

Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```

---

## Additional details

- Metrics are computed from processed product and order data  
- Aggregations are optimized for read-heavy workloads  
- Results are exposed through API endpoints for external consumption

---

## Related documentation

- [Workflows](workflows.md)
- [Errors](errors.md)
- [Products API](products.md)