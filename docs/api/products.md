# Products API

Use this API to retrieve product data from partner catalog feeds.

- Retrieve all products across partners
- Filter products by multiple attributes
- Sort results by supported fields
- Paginate results using `limit` and `cursor`
- Retrieve a single product by ID

> Product data becomes available only after ETL processing completes.
> See [Workflows](workflows.md) for the full ingestion process.

---

## Authentication

All endpoints in this resource require a valid `x-api-key` header.

Include the API key in each request:

```bash
-H "x-api-key: YOUR_API_KEY"
```

---

## GET /products

Use this endpoint to retrieve product records from uploaded partner feeds.

Supports filtering, sorting, and cursor-based pagination.

### What happens

- Retrieve product records from the database  
- Apply filters, sorting, and pagination  
- Return results with an optional `next_cursor`  

---

### Query parameters

| Name           | Type   | Required | Description                                                                   |
|----------------|--------|----------|-------------------------------------------------------------------------------|
| `partner_name` | string | No       | Partner name filter                                                           |
| `feed_id`      | string | No       | Filter by feed ID                                                             |
| `sku`          | string | No       | Filter by SKU                                                                 |
| `brand`        | string | No       | Filter by brand                                                               |
| `category`     | string | No       | Filter by category                                                            |
| `availability` | string | No       | Filter by availability                                                        |
| `limit`        | int    | No       | Number of results to return (default: 10, max: 100)                           |
| `cursor`       | string | No       | Cursor for pagination. Use the `next_cursor` value from the previous response |
| `sort_by`      | string | No       | Field to sort by (created_at, price, product_name, brand, category)           |
| `order`        | string | No       | Sort direction (`asc` [ascending], `desc` [decending], default: `desc`)                               |

---

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

---

### Example request

```bash
curl -X 'GET' \
  'http://api.example.com/products?limit=10&order=asc' \
  -H 'accept: application/json' \
  -H 'x-api-key: demo-secret-key'
```

---

### Example Response

```json
{
  "count": 5,
  "items": [
    {
      "product_id": "PR00001",
      "feed_id": "FD00001",
      "partner_name": "Tech Haven",
      "sku": "EL-3001",
      "product_name": "iPhone 15 Pro",
      "description": "Apple smartphone with A17 Pro chip and titanium design",
      "brand": "Apple",
      "category": "Smartphones",
      "price": 999.0,
      "currency": "USD",
      "availability": "in_stock",
      "created_at": "2026-04-08T12:00:00Z"
    }
  ],
  "next_cursor": "PR00005"
}
```

---

### Response fields

| Field         | Type   | Description                                  |
|---------------|--------|----------------------------------------------|
| `count`       | int    | Number of items returned in the current page |
| `items`       | array  | List of product objects                      |
| `next_cursor` | string | Cursor for next page (if more results exist) |

---

### Error responses

#### 401 Unauthorized
Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```

#### 400 Bad request
Returned when the request contains an invalid `sort_by` value. Allowed values are `product_id`, `price`, `product_name`, `brand`, `category`, or `created_at`.

```json
{
  "detail": "Invalid sort_by value. Allowed values: product_id, price, product_name, brand, category, created_at."
}
```

Returned when the request contains `order` value for sort direction. Allowed values are `asc` or `desc`.
```json
{
  "detail": "Invalid order value. Allowed values: asc, desc."
}
```

Returned when the request contains a `sort_by` value other than `product_id`.
```json
{
  "detail": "Cursor pagination is currently supported only with sort_by=product_id."
}
```

---

## GET /products/{product_id}

Use this endpoint to retrieve a single product record by `product_id` from uploaded partner feeds.

---

### What happens

- Retrieve the product by its unique ID  
- Return product details if the product exists  
- Return an error if the product is not found

### Path parameters

| Name         | Type   | Required | Description                       |
|--------------|--------|----------|-----------------------------------|
| `product_id` | string | Yes      | Unique identifier for the product |


---

### Example request

```bash
curl -X 'GET' \
  'http://api.example.com/products/PR00001' \
  -H 'accept: application/json' \
  -H 'x-api-key: demo-secret-key'
```

---

### Example response

```json
{
  "product_id": "PR00001",
  "feed_id": "FD00001",
  "partner_name": "Tech Haven",
  "sku": "EL-3001",
  "product_name": "iPhone 15 Pro",
  "description": "Apple smartphone with A17 Pro chip and titanium design",
  "brand": "Apple",
  "category": "Smartphones",
  "price": 999.0,
  "currency": "USD",
  "availability": "in_stock",
  "created_at": "2026-04-08T12:00:00Z"
}
```

---

### Response fields

| Field          | Type   | Description                                        |
|----------------|--------|----------------------------------------------------|
| `product_id`   | string | Unique identifier for the product (PRxxxxx)        |
| `feed_id`      | string | Identifier of the feed that produced the product   |
| `partner_name` | string | Name of the partner that supplied the product      |
| `sku`          | string | Partner-defined SKU (may be null)                  |
| `product_name` | string | Display name of the product                        |
| `description`  | string | Product description (may be null)                  |
| `brand`        | string | Product brand (may be null)                        |
| `category`     | string | Product category (may be null)                     |
| `price`        | number | Product price (may be null)                        |
| `currency`     | string | Currency code (e.g., USD) (may be null)            |
| `availability` | string | Availability status (e.g., in_stock) (may be null) |
| `created_at`   | string | UTC timestamp when the product was created         |

---

### Error responses

#### 401 Unauthorized
Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```

#### 404 Not found
Returned when the request contains a `product_id` not currently in the system.

```json
{
  "detail": "Product PR00001 not found."
}
```

---

## GET /products/by-feed/{feed_id}

Returns all products associated with a specific feed.


### What happens

- Retrieve all products associated with the specified feed ID   
- Return product records when the feed exists  
- Return an error if the feed is not found


### Path parameters

| Name      | Type   | Required | Description                    |
|-----------|--------|----------|--------------------------------|
| `feed_id` | string | Yes      | Unique identifier for the feed |

---

### Example request

```bash
curl -X 'GET' \
  'http://api.example.com/products/by-feed/FD00002' \
  -H 'accept: application/json' \
  -H 'x-api-key: demo-secret-key'
```

---

### Example response

```json
{
  "count": 10,
  "items": [
    {
      "product_id": "PR00001",
      "feed_id": "FD00001",
      "partner_name": "Elite Jewelry",
      "sku": "JW-1001",
      "product_name": "Diamond Stud Earrings",
      "price": 899.99,
      "currency": "USD",
      "availability": "in_stock",
      "created_at": "2026-04-08T12:00:00Z"
    }
  ]
}
```

### Response fields

| Field         | Type   | Description                                  |
|---------------|--------|----------------------------------------------|
| `count`       | int    | Number of items returned in the current page |
| `items`       | array  | List of product objects                      |
| `next_cursor` | string | Cursor for next page (if more results exist) |

If the specified `feed_id` has no associated products or not valid, the response returns count: 0 and an empty items array.

```json
{
  "count": 0,
  "items": []
}
```

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

- Product data is sourced from partner CSV feeds processed through the ETL pipeline
- Products are **not available until ETL processing completes**
- Raw feed data is stored in Amazon S3 and transformed before loading into PostgreSQL
- Not all fields are guaranteed to be populated for every product
- Results are ordered by `created_at` in descending order by default unless overridden
- Cursor-based pagination uses `product_id` for efficient traversal of large datasets

---

## Related documentation

- [Workflows](workflows.md)
- [Errors](errors.md)
- [Feeds API](feeds.md)
- [Jobs API](jobs.md)
