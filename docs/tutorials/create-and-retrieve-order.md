# Create and retrieve an order

Create an order using catalog products, then retrieve the order to validate stored pricing and transactional persistence.

In this tutorial, you will:

1. Retrieve products from the catalog
2. Create an order
3. Retrieve the order
4. Validate pricing and totals


## Before you begin

Before starting this tutorial:

- The API environment must be running
- Product data must already exist in the catalog
- You must have access to Swagger UI, Bruno, Postman, or curl

If products are not yet available in the catalog, complete the following tutorial first:

- [Upload your first product feed](first-feed.md)


## Workflow overview

<div class="diagram-card" markdown="1">
![Create and retrieve order](../api/screenshots/create-retrieve-order-workflow.svg)
</div>


## Step 1: Retrieve products

Before creating an order, retrieve products from the catalog.

For request parameters, filters, sorting options, and pagination behavior, see the [Get products](../api/products.md#get-products) endpoint documentation.

In this example, retrieve running shoes sold by the partner, **GoFasters**. Set the following parameters in the request.

| Parameter      | Value         |
| -------------- | ------------- |
| `partner_name` | GoFasters     |
| `category`     | Running Shoes |

### Request

```http
GET /products
```

### Example request

```bash
curl -X GET 'http://<base-url>/products?partner_name=GoFasters&category=Running%20Shoes' \
  -H 'x-api-key: YOUR_API_KEY'
```

### Example response

```json
{
  "count": 10,
  "items": [
    ...
    {
      "product_id": "PR00176",
      "feed_id": "FD00001",
      "partner_id": "PT00001",
      "partner_name": "GoFasters",
      "sku": "RS1002",
      "product_name": "Adidas Ultraboost 22",
      "description": "High-cushion running shoe with Boost midsole for energy return and Primeknit upper",
      "brand": "Adidas",
      "category": "Running Shoes",
      "price": 189.99,
      "currency": "USD",
      "availability": "in_stock",
      "created_at": "YYYY-MM-DDTHH:MM:SSZ"
    },
    {
      "product_id": "PR00177",
      "feed_id": "FD00001",
      "partner_id": "PT00001",
      "partner_name": "GoFasters",
      "sku": "RS1003",
      "product_name": "ASICS Gel-Nimbus 25",
      "description": "Premium neutral running shoe with GEL cushioning and soft FF Blast+ foam",
      "brand": "ASICS",
      "category": "Running Shoes",
      "price": 159.99,
      "currency": "USD",
      "availability": "in_stock",
      "created_at": "YYYY-MM-DDTHH:MM:SSZ"
    },
    {
      "product_id": "PR00178",
      "feed_id": "FD00001",
      "partner_id": "PT00001",
      "partner_name": "GoFasters",
      "sku": "RS1004",
      "product_name": "Brooks Ghost 15",
      "description": "Smooth ride with balanced cushioning and engineered air mesh upper",
      "brand": "Brooks",
      "category": "Running Shoes",
      "price": 139.99,
      "currency": "USD",
      "availability": "in_stock",
      "created_at": "YYYY-MM-DDTHH:MM:SSZ"
    },
    {
      "product_id": "PR00179",
      "feed_id": "FD00001",
      "partner_id": "PT00001",
      "partner_name": "GoFasters",
      "sku": "RS1005",
      "product_name": "HOKA Clifton 9",
      "description": "Lightweight running shoe with plush cushioning and early-stage Meta-Rocker design",
      "brand": "HOKA",
      "category": "Running Shoes",
      "price": 144.99,
      "currency": "USD",
      "availability": "in_stock",
      "created_at": "YYYY-MM-DDTHH:MM:SSZ"
    },
    ...
    {
      "product_id": "PR00182",
      "feed_id": "FD00001",
      "partner_id": "PT00001",
      "partner_name": "GoFasters",
      "sku": "RS1008",
      "product_name": "On Cloudrunner",
      "description": "Stability-focused running shoe with CloudTec cushioning and Helion foam",
      "brand": "On",
      "category": "Running Shoes",
      "price": 149.99,
      "currency": "USD",
      "availability": "in_stock",
      "created_at": "YYYY-MM-DDTHH:MM:SSZ"
    }
    ...
  ]
}
```


## Step 2: Select products

Use the following products for this tutorial.

| Product        | Product ID | Quantity |
| -------------- | ---------- | -------- |
| HOKA Clifton 9 | PR00179    | 1        |
| On Cloudrunner | PR00182    | 1        |


## Step 3: Create an order

Create an order using product IDs and quantities.

For request schema details and response definitions, see the [Create order](../api/orders.md#post-orders) endpoint documentation.

### Request

```http
POST /orders
```

### Request body

```json
{
    "partner_name": "GoFasters",
    "customer_reference": "CR00001",
    "customer_id": "CU00001",
    "shipping_address_id": "AD00001",
    "items": [
      {
        "product_id": "PR00179",
        "quantity": 1
      },
      {
        "product_id": "PR00182",
        "quantity": 1
      }
    ]
}
```

### Example request

```bash
curl -X POST "http://<base-url>/orders" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "partner_name": "GoFasters",
        "customer_reference": "CR00001",
        "customer_id": "CU00001",
        "shipping_address_id": "AD00001",
        "items": [
      {
          "product_id": "PR00179",
          "quantity": 1
      },
      {
          "product_id": "PR00182",
          "quantity": 1
      }
    ]
}'
```

### Example response

```json
{
  "order_id": "OR00001",
  "partner_name": "GoFasters",
  "customer_reference": "CR00001",
  "status": "created",
  "total_amount": 294.98,
  "currency": "USD",
  "items": [
    {
      "order_item_id": "OI00022",
      "product_id": "PR00179",
      "sku": "RS1005",
      "product_name": "HOKA Clifton 9",
      "quantity": 1,
      "unit_price": 144.99,
      "line_total": 144.99,
      "customer_id": "CU00001",
      "shipping_address_id": "AD00001"
    },
    {
      "order_item_id": "OI00023",
      "product_id": "PR00182",
      "sku": "RS1008",
      "product_name": "On Cloudrunner",
      "quantity": 1,
      "unit_price": 149.99,
      "line_total": 149.99,
      "customer_id": "CU00001",
      "shipping_address_id": "AD00001"
    }
  ]
}
```

## Step 4: Retrieve the order

Retrieve the order to validate stored order data and pricing.

For endpoint details, see the [Get order](../api/orders.md#get-orders) endpoint documentation.

### Request

```http
GET /orders/OR00039
```

### Example request

```bash
curl -X GET "http://<base-url>/orders/OR00039"
```

### Example response

```json
{
  "order_id": "OR00001",
  "partner_name": "GoFasters",
  "customer_reference": "CR00001",
  "status": "created",
  "total_amount": 294.98,
  "currency": "USD",
  "items": [
    {
      "order_item_id": "OI00022",
      "product_id": "PR00179",
      "sku": "RS1005",
      "product_name": "HOKA Clifton 9",
      "quantity": 1,
      "unit_price": 144.99,
      "line_total": 144.99,
      "customer_id": "CU00001",
      "shipping_address_id": "AD00001"
    },
    {
      "order_item_id": "OI00023",
      "product_id": "PR00182",
      "sku": "RS1008",
      "product_name": "On Cloudrunner",
      "quantity": 1,
      "unit_price": 149.99,
      "line_total": 149.99,
      "customer_id": "CU00001",
      "shipping_address_id": "AD00001"
    }
  ]
}
```


## Validate order behavior

After creating the order, validate the following behavior.

| Validation             | Expected behavior                        |
| ---------------------- | ---------------------------------------- |
| Order ID generation    | Unique order identifier returned         |
| Product lookup         | Product data retrieved from catalog      |
| Historical pricing     | Prices stored at order creation time     |
| Line totals            | Quantity × unit price                    |
| Order total            | Sum of all line totals                   |
| Relational persistence | Orders and order items stored separately |


## Validate historical pricing

Orders preserve historical pricing, independently, from future catalog updates.

Example workflow:

1. A product price is 49.99
2. An order is created
3. A future product feed updates the catalog price to 59.99
4. The existing order continues to store the original 49.99 price

This behavior preserves historical transaction accuracy.


## Troubleshoot common issues

### Product not found

Example response:

```json
{
  "detail": "Product PR99999 not found"
}
```

To resolve this issue:

- Verify the product exists
- Confirm the product ID is correct
- Retrieve products again before creating the order


### Product out of stock

Example response:

```json
{
  "detail": "Product is not available: PR00074"
}
```

This error occurs when the requested product exists in the catalog but is currently unavailable for ordering.

To resolve this issue:

- Retrieve the product again to verify availability status
- Confirm the product is marked as `in_stock`
- Select an alternative product if inventory is unavailable

Example query:

```http
GET /products?partner_name=GoFasters&category=Running%20Shoes&availability=in_stock
```

### Invalid quantity

Example response:

```json
{
  "detail": "Quantity must be greater than zero"
}
```

To resolve this issue:

- Ensure all quantities are positive integers


### Empty order items

Example response:

```json
{
  "detail": "Order must contain at least one item"
}
```

To resolve this issue:

- Include at least one item in the request body


## Related documentation

- [Products API](../api/products.md)
- [Orders API](../api/orders.md)
- [Analytics API](../api/analytics.md)