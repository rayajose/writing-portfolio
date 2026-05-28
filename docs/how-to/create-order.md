# Create an order

This guide shows how to create and verify an order using the Commerce Integration API.

Use this workflow during checkout integration testing, order processing validation, or customer transaction workflows.

## Overview

In this guide, you will:

1. Create an order
2. Review order details
3. Verify customer order history

## Prerequisites

| Requirement      | Description                                                         |
| ---------------- | ------------------------------------------------------------------- |
| Base URL (local) | `http://localhost:8000`                                             |
| Base URL (AWS)   | `http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com` |
| API key          | `x-api-key: YOUR_API_KEY`                                           |
| Customer ID      | Existing customer identifier                                        |
| Product ID       | Existing product identifier                                         |

### Required resources

Before creating an order, ensure the following resources already exist:

* Customer record
* Product catalog entry

Related documentation:

* [Create a customer](create-customer.md)
* [Ingest a product feed](ingest-product-feed.md)

## 1. Create an order

Run the `POST /orders` endpoint to create an order.

Record the `order_id` value from the response for use in the next step. In this example, the `order_id` is `OR00001`.

### Example request

```bash
curl -X POST http://api.example.com/orders \
  -H "x-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "partner_name": "Retail Store Name",
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

### Example response

```json
{
  "order_id": "OR00001",
  "partner_name": "Retail Store Name",
  "customer_reference": "CR00001",
  "status": "created",
  "total_amount": 9.99,
  "currency": "USD",
  "items": [
    {
      "order_item_id": "OI00002",
      "product_id": "PR00001",
      "sku": "TWXL1001",
      "product_name": "T-Shirt, White, XL",
      "quantity": 1,
      "unit_price": 9.99,
      "line_total": 9.99,
      "customer_id": "CU00001",
      "shipping_address_id": "AD00001"
    }
  ]
}
```

## 2. Review order details

Run the `GET /orders/{order_id}` endpoint using the `order_id` from the previous step.

In this example, the `order_id` is `OR00001`.

### Example request

```bash
curl -X GET http://api.example.com/orders/OR00001 \
  -H "x-api-key: YOUR_API_KEY"
```

### Example response

```json
{
  "order_id": "OR00001",
  "partner_name": "Retail Store Name",
  "customer_reference": "CR00001",
  "status": "created",
  "total_amount": 9.99,
  "currency": "USD",
  "items": [
    {
      "order_item_id": "OI00002",
      "product_id": "PR00001",
      "sku": "TWXL1001",
      "product_name": "T-Shirt, White, XL",
      "quantity": 1,
      "unit_price": 9.99,
      "line_total": 9.99,
      "customer_id": "CU00001",
      "shipping_address_id": "AD00001"
    }
  ]
}
```

### Verify the order record

Confirm the following values are present in the response:

| Field          | Description                               |
| -------------- | ----------------------------------------- |
| `order_id`     | Unique order identifier                   |
| `customer_id`  | Customer associated with the order        |
| `status`       | Current order processing status           |
| `total_amount` | Total order amount                        |
| `created_at`   | Timestamp when the order was created      |
| `updated_at`   | Timestamp when the order was last updated |

## 3. Verify customer order history

Run the `GET /customers/{customer_id}/orders` endpoint using the `customer_id` from step 1 (`CU00012`).

### Example request

```bash
curl -X GET http://api.example.com/customers/CU00001/orders \
  -H "x-api-key: YOUR_API_KEY"
```

### Example response

```json
[
   {
     "order_id": "OR00001",
     "customer_id": "CU00001",
     "customer_reference": "CR00001",
     "shipping_address_id": "AD00001",
     "status": "created",
     "currency": "USD",
     "total_amount": 9.99,
     "created_at": "YYYY-MM-DDTHH:MM:SSZ",
     "updated_at": "YYYY-MM-DDTHH:MM:SSZ"
    }
]
```

### Validation behavior

The API validates order requests before order creation.

Validation includes:

* Customer existence validation
* Product existence validation
* Quantity validation
* Inventory availability validation
* JSON payload validation

## Related documentation

* [Orders](../api/orders.md)
* [Customers](../api/customers.md)
* [Create a customer](create-customer.md)
* [Create and retrieve an order](../tutorials/create-and-retrieve-order.md)
