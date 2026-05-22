# Customers API

Use this API to create and retrieve fictional customer records and shipping addresses used for order fulfillment workflows.

- Create customer records for order workflows
- Store customer contact and address fields using field-level encryption
- Return masked customer data in API responses
- Create and retrieve customer shipping addresses

## Authentication

All endpoints in this resource require a valid `x-api-key` header.

Include the API key in each request:

```bash
-H "x-api-key: YOUR_API_KEY"
```

## `POST /customers`

Use this endpoint to create a fictional customer record.

### Processing behavior

- The system creates a customer record with a unique customer identifier.
- Sensitive fields such as email address and phone number are encrypted before storage.
- The API response returns masked customer data instead of raw sensitive values.
- The current implementation is intended for demo and documentation purposes only and does not store real customer PII.

### Request body

| Field        | Type   | Required | Description            |
| ------------ | ------ | -------- | ---------------------- |
| `first_name` | string | Yes      | Customer first name    |
| `last_name`  | string | Yes      | Customer last name     |
| `email`      | string | Yes      | Customer email address |
| `phone`      | string | No       | Customer phone number  |

### Request and response

<div class="api-example-grid">

<div>

<h3>Request</h3>

```bash
curl -X POST http://api.example.com/customers \
  -H "accept: application/json" \
  -H "x-api-key: demo-secret-key" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Alex",
    "last_name": "Morgan",
    "email": "alex.morgan@example.com",
    "phone": "555-0101"
  }'
```

</div>

<div>

<h3>Response</h3>

```json
{
  "customer_id": "CU00001",
  "first_name": "Alex",
  "last_name": "Morgan",
  "email_masked": "al***@example.com",
  "phone_masked": "***-***-0101",
  "created_at": "2026-05-20 13:15:30",
  "updated_at": "2026-05-20 13:15:30"
}
```

</div>

</div>

### Response fields

| Field          | Type   | Description                                        |
| -------------- | ------ | -------------------------------------------------- |
| `customer_id`  | string | Unique customer identifier (`CUxxxxx`)             |
| `first_name`   | string | Customer first name                                |
| `last_name`    | string | Customer last name                                 |
| `email_masked` | string | Masked email address returned for display use      |
| `phone_masked` | string | Masked phone number returned for display use       |
| `created_at`   | string | Date and time the customer record was created      |
| `updated_at`   | string | Date and time the customer record was last updated |

### Error responses

#### 401 Unauthorized

Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```

## `GET /customers`

Use this endpoint to retrieve all fictional customer records.

### Processing behavior

- The system retrieves all customer records currently stored in the platform.
- Sensitive values are decrypted internally only long enough to create masked response fields.
- The response does not return encrypted values or raw sensitive values.
- Results are returned ordered by customer identifier.

### Request and response

<div class="api-example-grid">

<div>

<h3>Request</h3>

```bash
curl -X GET http://api.example.com/customers \
  -H "accept: application/json" \
  -H "x-api-key: demo-secret-key"
```

</div>

<div>

<h3>Response</h3>

```json
[
  {
    "customer_id": "CU00001",
    "first_name": "Alex",
    "last_name": "Morgan",
    "email_masked": "al***@example.com",
    "phone_masked": "***-***-0101",
    "created_at": "2026-05-20 13:15:30",
    "updated_at": "2026-05-20 13:15:30"
  }
]
```

</div>

</div>

### Response fields

| Field          | Type   | Description                                        |
| -------------- | ------ | -------------------------------------------------- |
| `customer_id`  | string | Unique customer identifier (`CUxxxxx`)             |
| `first_name`   | string | Customer first name                                |
| `last_name`    | string | Customer last name                                 |
| `email_masked` | string | Masked email address returned for display use      |
| `phone_masked` | string | Masked phone number returned for display use       |
| `created_at`   | string | Date and time the customer record was created      |
| `updated_at`   | string | Date and time the customer record was last updated |

### Error responses

#### 401 Unauthorized

Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```


## `GET /customers/{customer_id}`

Use this endpoint to retrieve a specific fictional customer record.

### Processing behavior

- The system looks up the customer by `customer_id`.
- Sensitive values are decrypted internally only long enough to create masked response fields.
- The response does not return encrypted values or raw sensitive values.
- If the customer does not exist, the system returns a not found response.

### Path parameters

| Name          | Type   | Required | Description                            |
| ------------- | ------ | -------- | -------------------------------------- |
| `customer_id` | string | Yes      | Unique customer identifier (`CUxxxxx`) |

### Request and response

<div class="api-example-grid">

<div>

<h3>Request</h3>

```bash
curl -X GET http://api.example.com/customers/CU00001 \
  -H "accept: application/json" \
  -H "x-api-key: demo-secret-key"
```

</div>

<div>

<h3>Response</h3>

```json
{
  "customer_id": "CU00001",
  "first_name": "Alex",
  "last_name": "Morgan",
  "email_masked": "al***@example.com",
  "phone_masked": "***-***-0101",
  "created_at": "2026-05-20 13:15:30",
  "updated_at": "2026-05-20 13:15:30"
}
```

</div>

</div>

### Response fields

| Field          | Type   | Description                                        |
| -------------- | ------ | -------------------------------------------------- |
| `customer_id`  | string | Unique customer identifier (`CUxxxxx`)             |
| `first_name`   | string | Customer first name                                |
| `last_name`    | string | Customer last name                                 |
| `email_masked` | string | Masked email address returned for display use      |
| `phone_masked` | string | Masked phone number returned for display use       |
| `created_at`   | string | Date and time the customer record was created      |
| `updated_at`   | string | Date and time the customer record was last updated |

### Error responses

#### 401 Unauthorized

Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```

#### 404 Not found

Returned when the request contains a `customer_id` not currently in the system.

```json
{
  "detail": "Customer not found"
}
```

## `POST /customers/{customer_id}/addresses`

Use this endpoint to create a shipping address for a fictional customer.

### Processing behavior

- The system verifies that the customer exists.
- The system creates a shipping address associated with the customer.
- Sensitive address fields are encrypted before storage.
- The API response returns masked address fields instead of raw sensitive values.

### Path parameters

| Name          | Type   | Required | Description                            |
| ------------- | ------ | -------- | -------------------------------------- |
| `customer_id` | string | Yes      | Unique customer identifier (`CUxxxxx`) |

### Request body

| Field           | Type   | Required | Description                  |
| --------------- | ------ | -------- | ---------------------------- |
| `address_line1` | string | Yes      | Primary street address       |
| `address_line2` | string | No       | Secondary address details    |
| `city`          | string | Yes      | City                         |
| `state`         | string | Yes      | State or region              |
| `postal_code`   | string | Yes      | Postal or ZIP code           |
| `country`       | string | No       | Country code. Defaults to US |

### Request and response

<div class="api-example-grid">

<div>

<h3>Request</h3>

```bash
curl -X POST http://api.example.com/customers/CU00001/addresses \
  -H "accept: application/json" \
  -H "x-api-key: demo-secret-key" \
  -H "Content-Type: application/json" \
  -d '{
    "address_line1": "123 Example Street",
    "address_line2": "Apt 4B",
    "city": "Seattle",
    "state": "WA",
    "postal_code": "98101",
    "country": "US"
  }'
```

</div>

<div>

<h3>Response</h3>

```json
{
  "address_id": "AD00001",
  "customer_id": "CU00001",
  "address_line1_masked": "123 ***",
  "city": "Seattle",
  "state": "WA",
  "postal_code_masked": "***01",
  "country": "US",
  "created_at": "2026-05-20 13:17:42"
}
```

</div>

</div>

### Response fields

| Field                  | Type   | Description                                  |
| ---------------------- | ------ | -------------------------------------------- |
| `address_id`           | string | Unique address identifier (`ADxxxxx`)        |
| `customer_id`          | string | Customer associated with the address         |
| `address_line1_masked` | string | Masked primary street address                |
| `city`                 | string | City                                         |
| `state`                | string | State or region                              |
| `postal_code_masked`   | string | Masked postal or ZIP code                    |
| `country`              | string | Country code                                 |
| `created_at`           | string | Date and time the address record was created |

### Error responses

#### 401 Unauthorized

Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```

#### 404 Not found

Returned when the request contains a `customer_id` not currently in the system.

```json
{
  "detail": "Customer not found: CU00000"
}
```

## `GET /customers/addresses/{address_id}`

Use this endpoint to retrieve a specific customer shipping address.

### Processing behavior

- The system looks up the shipping address by `address_id`.
- Sensitive address values are decrypted internally only long enough to create masked response fields.
- The response does not return encrypted values or raw sensitive address values.
- If the address does not exist, the system returns a not found response.

### Path parameters

| Name         | Type   | Required | Description                           |
| ------------ | ------ | -------- | ------------------------------------- |
| `address_id` | string | Yes      | Unique address identifier (`ADxxxxx`) |

### Request and response

<div class="api-example-grid">

<div>

<h3>Request</h3>

```bash
curl -X GET http://api.example.com/customers/addresses/AD00001 \
  -H "accept: application/json" \
  -H "x-api-key: demo-secret-key"
```

</div>

<div>

<h3>Response</h3>

```json
{
  "address_id": "AD00001",
  "customer_id": "CU00001",
  "address_line1_masked": "123 ***",
  "city": "Seattle",
  "state": "WA",
  "postal_code_masked": "***01",
  "country": "US",
  "created_at": "2026-05-20 13:17:42"
}
```

</div>

</div>

### Response fields

| Field                  | Type   | Description                                  |
| ---------------------- | ------ | -------------------------------------------- |
| `address_id`           | string | Unique address identifier (`ADxxxxx`)        |
| `customer_id`          | string | Customer associated with the address         |
| `address_line1_masked` | string | Masked primary street address                |
| `city`                 | string | City                                         |
| `state`                | string | State or region                              |
| `postal_code_masked`   | string | Masked postal or ZIP code                    |
| `country`              | string | Country code                                 |
| `created_at`           | string | Date and time the address record was created |

### Error responses

#### 401 Unauthorized

Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```

#### 404 Not found

Returned when the request contains an `address_id` not currently in the system.

```json
{
  "detail": "Address not found"
}
```

## Security behavior

- Customer data in this demo environment uses fictional sample records only.
- Email, phone, street address, and postal code values are encrypted before storage.
- API responses return masked values instead of raw sensitive data.
- Encrypted database fields are not exposed in normal API responses.
- Payment card data is not collected or stored by this API.

## Additional details

- Customers use the `CUxxxxx` identifier format.
- Customer addresses use the `ADxxxxx` identifier format.
- Customer records can be associated with order workflows in later implementation phases.
- The current implementation demonstrates field-level encryption and masked response handling for PII-like data.
- This API is intended for portfolio demonstration and should not be used with real customer PII without additional production controls.

## Related documentation

- [Orders API](orders.md)
- [Products API](products.md)
- [Analytics API](analytics.md)
- [Errors](errors.md)