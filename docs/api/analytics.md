# Analytics

Use this API to retrieve aggregated sales and revenue insights.

- Retrieve aggregated sales and revenue metrics across partners
- Analyze product and order data through precomputed summaries
- Support reporting and dashboard integrations through analytics endpoints


## Authentication

All endpoints in this resource require a valid `x-api-key` header.

Include the API key in each request:

```bash
-H "x-api-key: YOUR_API_KEY"
```


## <span class="api-endpoint api-endpoint--get">GET /analytics/sales-by-partner</span>

Retrieve total units sold and revenue by partner.

### Processing behavior

- Aggregates order data by `partner_name`
- Calculates total units sold and revenue per partner
- Returns partners sorted by highest revenue


### Request and response

<div class="api-example-grid">
<div>

<h3>Request</h3>

```bash
curl -X 'GET' \
  'http://<base-url>/analytics/sales-by-partner' \
  -H 'accept: application/json' \
  -H 'x-api-key: YOUR_API_KEY'
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


### Response fields

| Field            | Type             | Description                                     |
| ---------------- | ---------------- | ----------------------------------------------- |
| `analytics_type` | string           | Type of analytics returned (`sales_by_partner`) |
| `results`        | array            | List of aggregated sales results by partner     |
| `partner_name`   | string           | Name of the partner                             |
| `units_sold`     | integer          | Total number of units sold for the partner      |
| `total_sales`    | string (decimal) | Total revenue for the partner                   |


## <span class="api-endpoint api-endpoint--get">GET /analytics/sales-over-time</span>

Retrieve sales metrics aggregated over time.

### Processing behavior

- Aggregates order data over time based on the specified `grain`
- Calculates total units sold and revenue for each time interval
- Returns results grouped and ordered chronologically


### Query parameters

| Name    | Type   | Required | Description                                          |
| ------- | ------ | -------- | ---------------------------------------------------- |
| `grain` | string | No       | Time interval for aggregation (`daily` or `monthly`) |

Defaults to `daily`.


### Request and response

<div class="api-example-grid">
<div>

<h3>Request</h3>

```bash
curl -X 'GET' \
  'http://<base-url>/analytics/sales-over-time?grain=daily' \
  -H 'accept: application/json' \
  -H 'x-api-key: YOUR_API_KEY'
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


### Response fields

| Field            | Type             | Description                                                 |
| ---------------- | ---------------- | ----------------------------------------------------------- |
| `analytics_type` | string           | Type of analytics returned (`sales_over_time`)              |
| `grain`          | string           | Time interval used for aggregation (`daily` or `monthly`)   |
| `results`        | array            | List of aggregated sales results by time period             |
| `sales_period`   | string           | Time period for the aggregation (format depends on `grain`) |
| `units_sold`     | integer          | Total number of units sold during the period                |
| `total_sales`    | string (decimal) | Total revenue for the period                                |


### Error responses

#### 401 Unauthorized

Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```

#### 422 Unprocessable Entity

Returned when request validation fails for an invalid `grain` value.

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

## <span class="api-endpoint api-endpoint--get">GET /analytics/revenue-share</span>

Retrieve each partner’s percentage contribution to total revenue.

### Processing behavior

- Aggregates total revenue by `partner_name`
- Calculates each partner’s percentage contribution relative to overall revenue
- Returns results sorted by highest revenue contribution


### Request and response

<div class="api-example-grid">
<div>

<h3>Request</h3>

```bash
curl -X 'GET' \
  'http://<base-url>/analytics/revenue-share' \
  -H 'accept: application/json' \
  -H 'x-api-key: YOUR_API_KEY'
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
      "revenue_pct": 29.90
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


### Response fields

| Field            | Type             | Description                                            |
| ---------------- | ---------------- | ------------------------------------------------------ |
| `analytics_type` | string           | Type of analytics returned (`revenue_share`)           |
| `results`        | array            | List of revenue share results by partner               |
| `partner_name`   | string           | Name of the partner                                    |
| `total_revenue`  | string (decimal) | Total revenue generated by the partner                 |
| `revenue_pct`    | number (decimal) | Percentage of total revenue contributed by the partner |


### Error responses

#### 401 Unauthorized

Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```


## Additional details

- Metrics are computed from processed product and order data
- Analytics responses are generated from precomputed aggregation queries
- Analytics data is available through API endpoints


## Related documentation

- [Errors](errors.md)
- [Products](products.md)