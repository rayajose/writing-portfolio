# Products

Use this API to retrieve product data from partner catalog feeds.

- Retrieve products across partners
- Filter products by multiple attributes
- Sort results using supported fields
- Paginate results using `limit` and `cursor`
- Retrieve individual product records by ID

> Product data becomes available only after ETL processing completes.
> See [Workflows](../architecture/workflows.md) for the full ingestion workflow.


## Authentication

All endpoints in this resource require a valid `x-api-key` header.

Include the API key in each request:

```bash
-H "x-api-key: YOUR_API_KEY"
```


## <span class="api-endpoint api-endpoint--get">GET /products</span>

Retrieve product records from uploaded partner feeds.

Supports filtering, sorting, and cursor-based pagination.

### Processing behavior

- Retrieves product records from the database
- Applies filters, sorting, and pagination
- Returns results with an optional `next_cursor` value


### Query parameters

| Name           | Type    | Required | Description                                                                           |
| -------------- | ------- | -------- | ------------------------------------------------------------------------------------- |
| `partner_id`   | string  | No       | Filter by partner identifier                                                          |
| `partner_name` | string  | No       | Filter by partner name                                                                |
| `feed_id`      | string  | No       | Filter by feed identifier                                                             |
| `sku`          | string  | No       | Filter by SKU                                                                         |
| `brand`        | string  | No       | Filter by brand                                                                       |
| `category`     | string  | No       | Filter by category                                                                    |
| `availability` | string  | No       | Filter by availability                                                                |
| `limit`        | integer | No       | Number of results to return. Default: `10`. Maximum: `100`                            |
| `cursor`       | string  | No       | Pagination cursor from the previous response                                          |
| `sort_by`      | string  | No       | Sort field (`product_id`, `created_at`, `price`, `product_name`, `brand`, `category`) |
| `order`        | string  | No       | Sort direction (`asc` or `desc`). Defaults to `asc`                                   |


#### Sorting examples

```text
GET /products?sort_by=price&order=asc
GET /products?sort_by=product_name&order=asc
```

#### Pagination examples

```text
GET /products?limit=5
GET /products?limit=5&cursor=PR00010
```


### Request and response

<div class="api-example-grid">
<div>

<h3>Request</h3>

```bash
curl -X GET http://api.example.com/products?limit=10&order=asc \
  -H "accept: application/json" \
  -H "x-api-key: YOUR_API_KEY"
```

</div>

<div>

<h3>Response</h3>

```json
{
  "count": 5,
  "items": [
    {
      "product_id": "PR00001",
      "feed_id": "FD00001",
      "partner_id": "PT00001",
      "partner_name": "Acme Corp",
      "sku": "EL-3001",
      "product_name": "Acme widget 3000",
      "description": "The best widget in the Acme collection.",
      "brand": "Acme",
      "category": "Widgets",
      "price": 999.0,
      "currency": "USD",
      "availability": "in_stock",
      "created_at": "YYYY-MM-DDTHH:MM:SSZ"
    }
  ],
  "next_cursor": "PR00005"
}
```

</div>
</div>


### Response fields

| Field         | Type    | Description                                  |
| ------------- | ------- | -------------------------------------------- |
| `count`       | integer | Number of items returned in the current page |
| `items`       | array   | List of product objects                      |
| `next_cursor` | string  | Cursor for the next page of results          |


### Error responses

#### 401 Unauthorized

Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```

#### 400 Bad Request

Returned when the request contains an invalid `sort_by` value.

Allowed values are `product_id`, `price`, `product_name`, `brand`, `category`, and `created_at`.

```json
{
  "detail": "Invalid sort_by value. Allowed values: product_id, price, product_name, brand, category, created_at."
}
```

Returned when the request contains an invalid `order` value.

Allowed values are `asc` and `desc`.

```json
{
  "detail": "Invalid order value. Allowed values: asc, desc."
}
```

Returned when cursor pagination is used with a `sort_by` value other than `product_id`.

```json
{
  "detail": "Cursor pagination is currently supported only with sort_by=product_id."
}
```


## <span class="api-endpoint api-endpoint--get">GET /products/{product_id}</span>

Retrieve a single product record by `product_id`.

### Processing behavior

- Retrieves the product by unique identifier
- Returns product details when the product exists
- Returns a not found response if the product does not exist


### Path parameters

| Name         | Type   | Required | Description                           |
| ------------ | ------ | -------- | ------------------------------------- |
| `product_id` | string | Yes      | Unique product identifier (`PRxxxxx`) |


### Request and response

<div class="api-example-grid">
<div>

<h3>Request</h3>

```bash
curl -X GET http://api.example.com/products/PR00001 \
  -H "accept: application/json" \
  -H "x-api-key: YOUR_API_KEY"
```

</div>

<div>

<h3>Response</h3>

```json
{
  "product_id": "PR00001",
  "feed_id": "FD00001",
  "partner_id": "PT00001",
  "partner_name": "Acme Corp",
  "sku": "EL-3001",
  "product_name": "Acme widget 3000",
  "description": "The best widget in the Acme collection.",
  "brand": "Acme",
  "category": "Widgets",
  "price": 999.0,
  "currency": "USD",
  "availability": "in_stock",
  "created_at": "YYYY-MM-DDTHH:MM:SSZ"
}
```

</div>
</div>


### Response fields

| Field          | Type   | Description                                 |
| -------------- | ------ | ------------------------------------------- |
| `partner_id`   | string | Filter by partner identifier                |
| `product_id`   | string | Unique product identifier (`PRxxxxx`)       |
| `feed_id`      | string | Feed identifier associated with the product |
| `partner_name` | string | Name of the partner supplying the product   |
| `sku`          | string | Partner-defined SKU (may be `null`)         |
| `product_name` | string | Product display name                        |
| `description`  | string | Product description (may be `null`)         |
| `brand`        | string | Product brand (may be `null`)               |
| `category`     | string | Product category (may be `null`)            |
| `price`        | number | Product price (may be `null`)               |
| `currency`     | string | Currency code such as `USD` (may be `null`) |
| `availability` | string | Product availability status (may be `null`) |
| `created_at`   | string | UTC timestamp when the product was created  |


### Error responses

#### 401 Unauthorized

Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```

#### 404 Not Found

Returned when the request contains a `product_id` not currently in the system.

```json
{
  "detail": "Product PR00001 not found."
}
```


## <span class="api-endpoint api-endpoint--get">GET /products/by-feed/{feed_id}</span>

Retrieve all products associated with a specific feed.

### Processing behavior

- Retrieves products associated with the specified `feed_id`
- Returns product records when the feed exists
- Returns an empty result set when no products are associated with the feed


### Path parameters

| Name      | Type   | Required | Description                        |
| --------- | ------ | -------- | ---------------------------------- |
| `feed_id` | string | Yes      | Unique feed identifier (`FDxxxxx`) |


### Request and response

<div class="api-example-grid">
<div>

<h3>Request</h3>

```bash
curl -X GET http://api.example.com/products/by-feed/FD00001 \
  -H "accept: application/json" \
  -H "x-api-key: YOUR_API_KEY"
```

</div>

<div>

<h3>Response</h3>

```json
{
  "count": 10,
  "items": [
    {
      "product_id": "PR00011",
      "feed_id": "FD00001",
      "partner_id": "PT00001",
      "partner_name": "Acme Corp",
      "sku": "JW-1001",
      "product_name": "Acme widget 3000",
      "description": "The best widget in the Acme collection.",
      "brand": "Acme",
      "category": "Widgets",
      "price": 999.99,
      "currency": "USD",
      "availability": "in_stock",
      "created_at": "YYYY-MM-DDTHH:MM:SSZ"
    }
  ]
}
```

</div>
</div>


### Response fields

| Field         | Type    | Description                                  |
| ------------- | ------- | -------------------------------------------- |
| `count`       | integer | Number of items returned in the current page |
| `items`       | array   | List of product objects                      |
| `next_cursor` | string  | Cursor for the next page of results          |

If the specified `feed_id` has no associated products, the response returns `count: 0` and an empty `items` array.

```json
{
  "count": 0,
  "items": []
}
```


### Error responses

#### 401 Unauthorized

Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```


## Additional details

- Product data is sourced from partner CSV feeds processed through the ETL pipeline
- Products are not available until ETL processing completes
- Raw feed data is stored in Amazon S3 and transformed before loading into PostgreSQL
- Not all product fields are guaranteed to be populated
- Results are ordered by `created_at` in descending order by default unless overridden
- Cursor-based pagination uses `product_id` for efficient traversal of large datasets


## Related documentation

- [Workflows](../architecture/workflows.md)
- [Errors](errors.md)
- [Feeds](feeds.md)
- [Jobs](jobs.md)