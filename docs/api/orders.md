# Orders API

Use this API to create and retrieve customer orders.

- Create orders from catalog products
- Retrieve order details and line items
- List submitted orders
- Track order status and calculated totals

## Authentication

All endpoints in this resource require a valid `x-api-key` header.

Include the API key in each request:

```bash
-H "x-api-key: YOUR_API_KEY"
```

## POST /orders

Use this endpoint to create an order from one or more catalog products.

### What happens
- The system creates a parent order with status created.
- For each requested item, the system verifies that the product_id exists.
- If the product is available, the system creates an order item with product details, quantity, unit price, and line total.
- The system calculates the order total and updates the order record.

### Request body

| Field                | Type   | Required | Description                                   |
| -------------------- | ------ | -------- | --------------------------------------------- |
| `partner_name`       | string | Yes      | Name of the partner associated with the order |
| `customer_reference` | string | No       | External customer or order reference          |
| `items`              | array  | Yes      | List of products to include in the order      |

### Item fields

| Field        | Type    | Required | Description                                 |
| ------------ | ------- | -------- | ------------------------------------------- |
| `product_id` | string  | Yes      | Product identifier (`PRxxxxx`)              |
| `quantity`   | integer | Yes      | Quantity to order. Must be greater than `0` |

### Request and response

<div  class="api-example-grid">

<div>

<h3>Request</h3>

```bash
curl -X POST http://api.example.com/orders \
  -H "accept: application/json" \
  -H "x-api-key: demo-secret-key" \
  -H "Content-Type: application/json" \
  -d '{
    "partner_name": "RayTech Corp.",
    "customer_reference": "CUST-1001",
    "items": [
      {
        "product_id": "PR00001",
        "quantity": 1
      }
    ]
  }'
```

</div>


<div>

<h3>Response</h3>

```json
{
  "order_id": "OR00001",
  "partner_name": "RayTech Corp.",
  "customer_reference": "CUST-1001",
  "status": "created",
  "total_amount": 10.99,
  "currency": "USD",
  "items": [
    {
      "order_item_id": "OI00001",
      "product_id": "PR00021",
      "sku": "BR-4001",
      "product_name": "All Day IPA",
      "quantity": 1,
      "unit_price": 10.99,
      "line_total": 10.99
    }
  ]
}
```

</div>

</div>

### Response fields
| Field                | Type   | Description                          |
| -------------------- | ------ | ------------------------------------ |
| `order_id`           | string | Unique order identifier (`ORxxxxx`)  |
| `partner_name`       | string | Partner associated with the order    |
| `customer_reference` | string | External customer or order reference |
| `status`             | string | Order status                         |
| `total_amount`       | number | Total amount for all order items     |
| `currency`           | string | Currency code                        |
| `items`              | array  | Line items included in the order     |

### Error responses

#### 400 Bad request

Returned when the order does not contain any items.

```json
{
  "detail": "Order must contain at least one item."
}
```

#### 401 Unauthorized
Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```

#### 404 Not found

Returned when a requested product does not exist.

```json
{
  "detail": "Product not found: PR00000"
}
```

#### 409 Conflict

Returned when a requested product is not available.

```json
{
  "detail": "Product is not available: PR00001"
}
```

## GET /orders

Use this endpoint to retrieve submitted orders.

### What happens

- The system retrieves order IDs sorted by creation time.
- For each order, the system retrieves associated order items.
- The response returns a count and list of orders.

### Request and response

<div  class="api-example-grid">

<div>

<h3>Request</h3>

```bash
curl -X GET http://api.example.com/orders \
  -H "accept: application/json" \
  -H "x-api-key: demo-secret-key"
```

</div>


<div>

<h3>Response</h3>

```json
{
  "count": 1,
  "items": [
    {
      "order_id": "OR00001",
      "partner_name": "RayTech Corp.",
      "customer_reference": "CUST-1001",
      "status": "created",
      "total_amount": 10.99,
      "currency": "USD",
      "items": [
        {
          "order_item_id": "OI00001",
          "product_id": "PR00021",
          "sku": "BR-4001",
          "product_name": "All Day IPA",
          "quantity": 1,
          "unit_price": 10.99,
          "line_total": 10.99
        }
      ]
    }
  ]
}
```

</div>

</div>

### Response fields

| Field   | Type    | Description                    |
| ------- | ------- | ------------------------------ |
| `count` | integer | Number of orders returned      |
| `items` | array   | List of order response objects |


### Error responses

#### 401 Unauthorized
Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```

## GET /orders/{order_id}

Use this endpoint to retrieve a specific order and its line items.

### What happens

- The system looks up the order by order_id.
- The system retrieves the order’s associated order items.
- If the order does not exist, the system returns a not found response.

### Path parameters

| Name       | Type   | Required | Description                         |
| ---------- | ------ | -------- | ----------------------------------- |
| `order_id` | string | Yes      | Unique order identifier (`ORxxxxx`) |


### Request and response

<div  class="api-example-grid">

<div>

<h3>Request</h3>

```bash
curl -X GET http://api.example.com/orders/OR00001 \
  -H "accept: application/json" \
  -H "x-api-key: demo-secret-key"
```

</div>


<div>

<h3>Response</h3>

```json
{
  "order_id": "OR00001",
  "partner_name": "RayTech Corp.",
  "customer_reference": "CUST-1001",
  "status": "created",
  "total_amount": 10.99,
  "currency": "USD",
  "items": [
    {
      "order_item_id": "OI00001",
      "product_id": "PR00021",
      "sku": "BR-4001",
      "product_name": "All Day IPA",
      "quantity": 1,
      "unit_price": 10.99,
      "line_total": 10.99
    }
  ]
}
```

</div>

</div>

### Response fields

| Field                | Type   | Description                          |
| -------------------- | ------ | ------------------------------------ |
| `order_id`           | string | Unique order identifier (`ORxxxxx`)  |
| `partner_name`       | string | Partner associated with the order    |
| `customer_reference` | string | External customer or order reference |
| `status`             | string | Order status                         |
| `total_amount`       | number | Total amount for all order items     |
| `currency`           | string | Currency code                        |
| `items`              | array  | Line items included in the order     |

### Order item fields

| Field           | Type    | Description                              |
| --------------- | ------- | ---------------------------------------- |
| `order_item_id` | string  | Unique order item identifier (`OIxxxxx`) |
| `product_id`    | string  | Product identifier (`PRxxxxx`)           |
| `sku`           | string  | Partner product SKU                      |
| `product_name`  | string  | Product name copied from the catalog     |
| `quantity`      | integer | Quantity ordered                         |
| `unit_price`    | number  | Product price at order creation          |
| `line_total`    | number  | Unit price multiplied by quantity        |

### Error responses

#### 401 Unauthorized
Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```

#### 404 Not found

Returned when the request contains an `order_id` not currently in the system.

```json
{
  "detail": "Order not found: OR00000"
}
```

## Additional details

- Orders use the ORxxxxx identifier format.
- Order items use the OIxxxxx identifier format.
- Order totals are calculated from order item line totals.
- Product details such as sku, product_name, and unit_price are - - copied into the order item at order creation time.
- The current implementation creates orders with status created.


## Related documentation

- [Feeds API](feeds.md)
- [Products API](products.md)
- [Analytics API](analytics.md)
- [Errors](errors.md)