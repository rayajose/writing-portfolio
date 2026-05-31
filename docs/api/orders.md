# Orders

Use this API to create and retrieve customer orders.

- Create orders from catalog products
- Retrieve order details and line items
- List submitted orders
- Track order status and calculated totals
- Associate orders with fictional customer and shipping address records


## Authentication

All endpoints in this resource require a valid `x-api-key` header.

Include the API key in each request:

```bash
-H "x-api-key: YOUR_API_KEY"
```


## <span class="api-endpoint api-endpoint--post">POST /orders</span>

Create an order from one or more catalog products.

### Processing behavior

- Creates a parent order with status `created`
- Optionally associates customer and shipping address records with the order
- Stores customer and shipping records separately from transactional order items
- Verifies that each requested `product_id` exists
- Creates order items for available products
- Calculates order totals
- Determines the partner from the selected catalog products
- Ensures all order items belong to the same partner
- Stores both `partner_id` and `partner_name` on the order for reporting and retrieval


### Request body

| Field                 | Type   | Required | Description                             |
| --------------------- | ------ | -------- | --------------------------------------- |
| `customer_reference`  | string | No       | External customer or order reference    |
| `customer_id`         | string | No       | Customer identifier (`CUxxxxx`)         |
| `shipping_address_id` | string | No       | Shipping address identifier (`ADxxxxx`) |
| `items`               | array  | Yes      | List of products included in the order  |


### Item fields

| Field        | Type    | Required | Description                                 |
| ------------ | ------- | -------- | ------------------------------------------- |
| `product_id` | string  | Yes      | Product identifier (`PRxxxxx`)              |
| `quantity`   | integer | Yes      | Quantity to order. Must be greater than `0` |


### Request and response

<div class="api-example-grid">

<div>

<h3>Request</h3>

```bash
curl -X POST http://api.example.com/orders \
  -H "accept: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_reference": "CR00001",
    "customer_id": "CU00001",
    "shipping_address_id": "AD00001",
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
  "partner_id": "PT00001",
  "partner_name": "RayTech Corp.",
  "customer_reference": "CR00001",
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
      "line_total": 10.99,
      "customer_id": "CU00001",
      "shipping_address_id": "AD00001"
    }
  ]
}
```

</div>

</div>


### Response fields

| Field                 | Type   | Description                            |
| --------------------- | ------ | -------------------------------------- |
| `order_id`            | string | Unique order identifier (`ORxxxxx`)    |
| `partner_id`          | string | Partner identifier (`PTxxxxx`)         |
| `partner_name`        | string | Partner associated with the order      |
| `customer_reference`  | string | External customer or order reference   |
| `customer_id`         | string | Associated customer identifier         |
| `shipping_address_id` | string | Associated shipping address identifier |
| `status`              | string | Order status                           |
| `total_amount`        | number | Total amount for all order items       |
| `currency`            | string | Currency code                          |
| `items`               | array  | Line items included in the order       |


### Error responses

#### 400 Bad Request

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

#### 404 Not Found

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


## <span class="api-endpoint api-endpoint--get">GET /orders</span>

Retrieve submitted orders.

### Processing behavior

- Retrieves orders sorted by order ID descending
- Supports filtering by partner identifier
- Supports filtering by partner name
- Retrieves associated order items for each order
- Returns order counts and order details

### Query parameters

| Name           | Type   | Required | Description                  |
| -------------- | ------ | -------- | ---------------------------- |
| `partner_id`   | string | No       | Filter by partner identifier |
| `partner_name` | string | No       | Filter by partner name       |

### Request and response

<div class="api-example-grid">

<div>

<h3>Request</h3>

```bash
curl -X GET "http://api.example.com/orders?partner_id=PT00001" \
  -H "accept: application/json" \
  -H "x-api-key: YOUR_API_KEY"
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
      "partner_id": "PT00001",
      "partner_name": "RayTech Corp.",
      "customer_reference": "CR00001",
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


## <span class="api-endpoint api-endpoint--get">GET /orders/{order_id}</span>

Retrieve a specific order and its line items.

### Processing behavior

- Looks up the order by `order_id`
- Retrieves associated order items
- Returns a not found response if the order does not exist


### Path parameters

| Name       | Type   | Required | Description                         |
| ---------- | ------ | -------- | ----------------------------------- |
| `order_id` | string | Yes      | Unique order identifier (`ORxxxxx`) |


### Request and response

<div class="api-example-grid">

<div>

<h3>Request</h3>

```bash
curl -X GET http://api.example.com/orders/OR00001 \
  -H "accept: application/json" \
  -H "x-api-key: YOUR_API_KEY"
```

</div>

<div>

<h3>Response</h3>

```json
{
  "order_id": "OR00001",
  "partner_id": "PT00001",
  "partner_name": "RayTech Corp.",
  "customer_reference": "CR00001",
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
| `partner_id`         | string | Partner identifier (`PTxxxxx`)       |
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

#### 404 Not Found

Returned when the request contains an `order_id` not currently in the system.

```json
{
  "detail": "Order not found: OR00000"
}
```


## Additional details

- Orders use the `ORxxxxx` identifier format
- Order items use the `OIxxxxx` identifier format
- Order totals are calculated from order item line totals
- Product details such as `sku`, `product_name`, and `unit_price` are copied into order items at order creation time
- New orders are created with status `created`
- Orders can optionally reference customer and shipping address records
- Customer and shipping records are maintained separately from transactional order items
- Orders store both `partner_id` and `partner_name`
- All products in an order must belong to the same partner
- Partner ownership is derived from catalog products during order creation


## Related documentation

- [Feeds](feeds.md)
- [Products](products.md)
- [Analytics](analytics.md)
- [Errors](errors.md)