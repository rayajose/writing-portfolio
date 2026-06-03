# Customers

Use this API to create and retrieve fictional customer records and shipping addresses used for order fulfillment workflows.

- Create customer records for order workflows
- Store customer contact and address fields using field-level encryption
- Return masked customer data in API responses
- Create and retrieve customer shipping addresses
- Delete one or more customer records when no orders reference the customer or related shipping addresses
- Preserve order history by blocking customer deletion when orders depend on the customer record


## Authentication

All endpoints in this resource require a valid `x-api-key` header.

Include the API key in each request:

```bash
-H "x-api-key: YOUR_API_KEY"
```


## <span class="api-endpoint api-endpoint--post">POST /customers</span>

Create a fictional customer record.

### Processing behavior

- Creates a customer record with a unique customer identifier
- Encrypts sensitive fields such as email address and phone number before storage
- Returns masked customer data instead of raw sensitive values
- Uses fictional sample data for demonstration purposes only


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
curl -X POST http://<base-url>/customers \
  -H "accept: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Alex",
    "last_name": "Morgan",
    "email": "alex.morgan@example.com",
    "phone": "405-555-0101"
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
  "created_at": "YYYY-MM-DDTHH:MM:SSZ",
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ"
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


## <span class="api-endpoint api-endpoint--get">GET /customers</span>

Retrieve all fictional customer records.

### Processing behavior

- Retrieves all customer records stored in the platform
- Decrypts sensitive values only long enough to create masked response fields
- Does not return encrypted values or raw sensitive values
- Returns results ordered by customer identifier


### Request and response

<div class="api-example-grid">

<div>

<h3>Request</h3>

```bash
curl -X GET http://<base-url>/customers \
  -H "accept: application/json" \
  -H "x-api-key: YOUR_API_KEY"
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
    "created_at": "YYYY-MM-DDTHH:MM:SSZ",
    "updated_at": "YYYY-MM-DDTHH:MM:SSZ"
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

## <span class="api-endpoint api-endpoint--delete">DELETE /customers</span>

Delete multiple fictional customer records.

### Processing behavior

- Accepts a list of customer identifiers
- Deletes each customer that is not referenced by existing orders
- Deletes associated customer addresses only when they are not referenced by orders
- Preserves order history by blocking deletion when an order references the customer or shipping address
- Returns a per-customer result for deleted, failed, and not found records


### Request body

| Field          | Type  | Required | Description                            |
| -------------- | ----- | -------- | -------------------------------------- |
| `customer_ids` | array | Yes      | List of customer identifiers to delete |


### Request and response

<div class="api-example-grid">

<div>

<h3>Request</h3>

```bash
curl -X DELETE http://<base-url>/customers \
  -H "accept: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_ids": [
      "CU00001",
      "CU00002",
      "CU00003"
    ]
  }'
```

</div>

<div> <h3>Response</h3>

```json
{
  "deleted_count": 1,
  "failed_count": 2,
  "results": [
    {
      "customer_id": "CU00001",
      "status": "deleted",
      "message": "Customer CU00001 was successfully deleted"
    },
    {
      "customer_id": "CU00002",
      "status": "failed",
      "message": "Customer cannot be deleted because existing orders reference this customer."
    },
    {
      "customer_id": "CU00003",
      "status": "not_found",
      "message": "Customer not found"
    }
  ]
}
```
</div>

</div>

### Response fields

| Field           | Type   | Description                            |
| --------------- | ------ | -------------------------------------- |
| `deleted_count` | number | Number of customer records deleted     |
| `failed_count`  | number | Number of customer records not deleted |
| `results`       | array  | Per-customer deletion result details   |


### Result fields

| Field         | Type   | Description                                        |
| ------------- | ------ | -------------------------------------------------- |
| `customer_id` | string | Customer identifier included in the request        |
| `status`      | string | Result status: `deleted`, `failed`, or `not_found` |
| `message`     | string | Human-readable deletion result message             |


### Error responses

#### 401 Unauthorized

Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```

## <span class="api-endpoint api-endpoint--delete">DELETE /customers/{customer_id}</span>

Delete a specific fictional customer record.

### Processing behavior
Looks up the customer by customer_id
Deletes the customer when no existing orders reference the customer or related shipping addresses
Deletes associated customer addresses only when they are not referenced by orders
Preserves order history by blocking deletion when an order depends on the customer record
Returns a confirmation message when deletion succeeds

### Path parameters

| Name          | Type   | Required | Description                            |
| ------------- | ------ | -------- | -------------------------------------- |
| `customer_id` | string | Yes      | Unique customer identifier (`CUxxxxx`) |

### Request and response
<div class="api-example-grid"> <div> <h3>Request</h3>

```bash
curl -X DELETE http://<base-url>/customers/CU00001 \
  -H "accept: application/json" \
  -H "x-api-key: YOUR_API_KEY"
```
</div> 

<div> 

<h3>Response</h3>

```json
{
  "message": "Customer CU00001 was successfully deleted"
}
```

</div> </div>

### Response fields

| Field     | Type   | Description                         |
| --------- | ------ | ----------------------------------- |
| `message` | string | Customer deletion confirmation text |

### Error responses

#### 401 Unauthorized

Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```

#### 404 Not Found

Returned when the request contains a customer_id not currently in the system.

```json
{
  "detail": "Customer not found"
}
```
#### 409 Conflict

Returned when existing orders reference the customer or one of the customer’s shipping addresses.

```json
{
  "detail": "Customer cannot be deleted because existing orders reference this customer."
}
```

## <span class="api-endpoint api-endpoint--get">GET /customers/{customer_id}/orders</span>

Retrieve all orders associated with a fictional customer record.

### Processing behavior

- Verifies that the customer exists
- Retrieves all orders associated with the specified `customer_id`
- Returns results ordered by newest order first
- Supports customer-centric order history and fulfillment visibility
- Returns a not found response if the customer does not exist


### Path parameters

| Name          | Type   | Required | Description                            |
| ------------- | ------ | -------- | -------------------------------------- |
| `customer_id` | string | Yes      | Unique customer identifier (`CUxxxxx`) |


### Request and response

<div class="api-example-grid">

<div>

<h3>Request</h3>

```bash
curl -X GET http://<base-url>/customers/CU00001/orders \
  -H "accept: application/json" \
  -H "x-api-key: YOUR_API_KEY"
```

</div>

<div>

<h3>Response</h3>

```json
[
  {
    "order_id": "OR00001",
    "customer_id": "CU00001",
    "customer_reference": "WEB-ORDER-1001",
    "shipping_address_id": "AD00001",
    "status": "completed",
    "currency": "USD",
    "total_amount": 149.99,
    "created_at": "YYYY-MM-DDTHH:MM:SSZ",
    "updated_at": "YYYY-MM-DDTHH:MM:SSZ"
  }
]
```

</div>

</div>


### Response fields

| Field                 | Type   | Description                                |
| --------------------- | ------ | ------------------------------------------ |
| `order_id`            | string | Unique order identifier (`ORxxxxx`)        |
| `customer_id`         | string | Customer associated with the order         |
| `customer_reference`  | string | External or client-facing order reference  |
| `shipping_address_id` | string | Shipping address associated with the order |
| `status`              | string | Current order status                       |
| `currency`            | string | Currency associated with the order total   |
| `total_amount`        | number | Total order amount                         |
| `created_at`          | string | Date and time the order was created        |
| `updated_at`          | string | Date and time the order was last updated   |


### Error responses

#### 401 Unauthorized

Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```

#### 404 Not Found

Returned when the request contains a `customer_id` not currently in the system.

```json
{
  "detail": "Customer not found"
}
```


## <span class="api-endpoint api-endpoint--get">GET /customers/{customer_id}</span>

Retrieve a specific fictional customer record.

### Processing behavior

- Looks up the customer by `customer_id`
- Decrypts sensitive values only long enough to create masked response fields
- Does not return encrypted values or raw sensitive values
- Returns a not found response if the customer does not exist


### Path parameters

| Name          | Type   | Required | Description                            |
| ------------- | ------ | -------- | -------------------------------------- |
| `customer_id` | string | Yes      | Unique customer identifier (`CUxxxxx`) |


### Request and response

<div class="api-example-grid">

<div>

<h3>Request</h3>

```bash
curl -X GET http://<base-url>/customers/CU00001 \
  -H "accept: application/json" \
  -H "x-api-key: YOUR_API_KEY"
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
  "created_at": "YYYY-MM-DDTHH:MM:SSZ",
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ"
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

#### 404 Not Found

Returned when the request contains a `customer_id` not currently in the system.

```json
{
  "detail": "Customer not found"
}
```


## <span class="api-endpoint api-endpoint--post">POST /customers/{customer_id}/addresses</span>

Create a shipping address for a fictional customer.

### Processing behavior

- Verifies that the customer exists
- Creates a shipping address associated with the customer
- Encrypts sensitive address fields before storage
- Returns masked address fields instead of raw sensitive values


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
curl -X POST http://<base-url>/customers/CU00001/addresses \
  -H "accept: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
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
  "created_at": "YYYY-MM-DDTHH:MM:SSZ"
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

#### 404 Not Found

Returned when the request contains a `customer_id` not currently in the system.

```json
{
  "detail": "Customer not found: CU00000"
}
```


## <span class="api-endpoint api-endpoint--get">GET /customers/addresses/{address_id}</span>

Retrieve a specific customer shipping address.

### Processing behavior

- Looks up the shipping address by `address_id`
- Decrypts sensitive address values only long enough to create masked response fields
- Does not return encrypted values or raw sensitive address values
- Returns a not found response if the address does not exist


### Path parameters

| Name         | Type   | Required | Description                           |
| ------------ | ------ | -------- | ------------------------------------- |
| `address_id` | string | Yes      | Unique address identifier (`ADxxxxx`) |


### Request and response

<div class="api-example-grid">

<div>

<h3>Request</h3>

```bash
curl -X GET http://<base-url>/customers/addresses/AD00001 \
  -H "accept: application/json" \
  -H "x-api-key: YOUR_API_KEY"
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
  "created_at": "YYYY-MM-DDTHH:MM:SSZ"
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

#### 404 Not Found

Returned when the request contains an `address_id` not currently in the system.

```json
{
  "detail": "Address not found"
}
```


## Security behavior

- Customer data uses fictional sample records only
- Email, phone, street address, and postal code values are encrypted before storage
- API responses return masked values instead of raw sensitive data
- Encrypted database fields are not exposed in API responses
- Payment card data is not collected or stored by this API


## Additional details

- Customers use the `CUxxxxx` identifier format
- Customer addresses use the `ADxxxxx` identifier format
- Customer records can be associated with order workflows in later implementation phases
- The current implementation demonstrates field-level encryption and masked response handling for PII-like data
- This API is intended for portfolio demonstration purposes and should not be used with real customer PII without additional production controls


## Related documentation

- [Orders](orders.md)
- [Products](products.md)
- [Analytics](analytics.md)
- [Errors](errors.md)