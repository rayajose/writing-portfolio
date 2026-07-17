# Create a customer

This guide shows how to create and verify a customer record using the Commerce Integration API.

Use this workflow during account onboarding, order preparation, or customer testing workflows.

## Overview

In this guide, you will:

1. Create a customer
2. Review the customer record
3. Verify customer order history

## Prerequisites

| Requirement       | Description                                                                                                                              |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| API base URL      | Replace `<base-url>` with the base URL of your Commerce Integration API deployment. For example: `https://d2nbg35whekpke.cloudfront.net` |
| API key           | `x-api-key: YOUR_API_KEY`                                                                                                                |
| Valid `.csv` file | See [CSV feed file specification](../specs/csv-feed-file-spec.md)                                                                        |

!!! note

    Request examples in this guide use the `<base-url>` placeholder so they can be used with local, staging, or production deployments.

## 1. Create a customer

Run the `POST /customers` endpoint to create a customer record.

Record the `customer_id` value from the response for use in the next step. In this example, the `customer_id` is `CU00001`.

### Example request

```bash
curl -X POST http://<base-url>/customers \
  -H "x-api-key: YOUR_API_KEY" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jordan",
    "last_name": "Lee",
    "email": "jordan.lee@example.com",
    "phone": "405-555-0100"
  }'
```

### Example response

```json
{
  "customer_id": "CU00001",
  "first_name": "Jordan",
  "last_name": "Lee",
  "email_masked": "jo***@example.com",
  "phone_masked": "***-***-0100",
  "created_at": "YYYY-MM-DDTHH:MM:SSZ",
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ"
}
```

## 2. Review the customer record

Run the `GET /customers/{customer_id}` endpoint using the `customer_id` from the previous step.

In this example, the `customer_id` is `CU00001`.

### Example request

```bash
curl -X GET http://<base-url>/customers/CU00001 \
  -H "x-api-key: YOUR_API_KEY"
```

### Example response

```json
{
  "customer_id": "CU00001",
  "first_name": "Jordan",
  "last_name": "Lee",
  "email_masked": "jo***@example.com",
  "phone_masked": "***-***-0100",
  "created_at": "YYYY-MM-DDTHH:MM:SSZ",
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ"
}
```

### Verify the customer record

Confirm the following values are present in the response:

| Field          | Description                                             |
| -------------- | ------------------------------------------------------- |
| `customer_id`  | Unique customer identifier                              |
| `email_masked` | Masked customer email address returned in API responses |
| `phone_masked` | Masked customer phone number returned in API responses  |
| `created_at`   | Timestamp when the customer record was created          |
| `updated_at`   | Timestamp when the customer record was last updated     |

## 3. Verify customer order history

Run the `GET /customers/{customer_id}/orders` endpoint using the `customer_id` from step 1 (`CU00012`).

### Example request

```bash
curl -X GET http://<base-url>/customers/CU00001/orders \
  -H "x-api-key: YOUR_API_KEY"
```

### Example response

```json
[
  {
    "order_id": "OR00077",
    "customer_id": "CU00001",
    "customer_reference": "CR00001",
    "shipping_address_id": "AD00001",
    "status": "created",
    "currency": "USD",
    "total_amount": 2699.97,
    "created_at": "YYYY-MM-DDTHH:MM:SSZ",
    "updated_at": "YYYY-MM-DDTHH:MM:SSZ"
  }
]
```

### Validation behavior

The API validates customer records before creation.

Validation includes:

* Required field checks
* Email format validation
* Duplicate email detection
* JSON payload validation


## Related documentation

* [Customers](../api/customers.md)
* [Create and retrieve an order](../tutorials/create-and-retrieve-order.md)
* [Orders](../api/orders.md)
