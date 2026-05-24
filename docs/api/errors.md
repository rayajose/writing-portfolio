# Errors

Use this page to understand how the Commerce Integration API returns and handles errors.

## Error format

The API primarily uses FastAPI’s standard error response format.

```json
{
  "detail": "Human-readable error message"
}
```


### Response fields

| Field    | Type   | Description              |
| -------- | ------ | ------------------------ |
| `detail` | string | Description of the error |


## Common error scenarios

Errors can occur in the following situations:

- Missing or invalid API key
- Invalid request data, such as malformed CSV input
- Requested resource does not exist
- Product availability conflicts during order creation
- Invalid customer or shipping address references
- ETL processing failures
- Database or infrastructure failures


## Status codes

| Status | Meaning                                                |
| ------ | ------------------------------------------------------ |
| `200`  | Request completed successfully                         |
| `201`  | Resource created successfully                          |
| `400`  | Bad Request (`invalid input or business rule failure`) |
| `401`  | Unauthorized (`missing API key`)                       |
| `403`  | Forbidden (`invalid API key`)                          |
| `404`  | Requested resource not found                           |
| `409`  | Request conflict or unavailable resource               |
| `422`  | Request validation failed                              |
| `500`  | Internal server error                                  |


## Authentication errors

Authentication errors occur when a request is missing valid credentials or includes an invalid API key.


### 401 Unauthorized

Returned when the API key is missing.

#### Example

```json
{
  "detail": "Not authenticated"
}
```


### 403 Forbidden

Returned when the API key is invalid.

#### Example

```json
{
  "detail": "Invalid API key"
}
```


## Resource errors

Resource errors occur when a requested resource does not exist in the system.


### 404 Not Found

Returned when a requested resource does not exist.

#### Example: Feed not found

```json
{
  "detail": "Feed FD99999 not found."
}
```

#### Example: Job not found

```json
{
  "detail": "Job JS99999 not found."
}
```

#### Example: Product not found

```json
{
  "detail": "Product PR99999 not found."
}
```

#### Example: Customer not found

```json
{
  "detail": "Customer CU99999 not found."
}
```

#### Example: Address not found

```json
{
  "detail": "Address AD99999 not found."
}
```

#### Example: Order not found

```json
{
  "detail": "Order OR99999 not found."
}
```


## Validation errors

Validation errors occur when request data fails validation or violates business rules.


### 400 Bad Request

Returned when the request is syntactically valid but fails business validation rules.

#### Example: Unsupported file type

```json
{
  "detail": "Only CSV uploads are supported at this time."
}
```

#### Example: Empty file

```json
{
  "detail": "Uploaded file is empty."
}
```

#### Example: Invalid CSV

```json
{
  "detail": "Invalid CSV file: CSV header row is missing."
}
```

#### Example: Empty order

```json
{
  "detail": "Order must contain at least one item."
}
```

#### Example: Invalid customer reference

```json
{
  "detail": "Customer not found: CU99999"
}
```

#### Example: Invalid shipping address reference

```json
{
  "detail": "Shipping address not found: AD99999"
}
```


### 409 Conflict

Returned when the request conflicts with the current resource state.

#### Example: Product unavailable

```json
{
  "detail": "Product is not available: PR00001"
}
```


### 422 Unprocessable Entity

Returned when request data fails schema validation.

FastAPI automatically generates these validation responses.

#### Example

```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "Validation error message",
      "type": "validation_error_type"
    }
  ]
}
```


## Job execution errors

Job execution errors occur when job execution requests are invalid or when ETL processing fails.


### 400 Bad Request

Returned when attempting to execute an unsupported job type.

#### Example

```json
{
  "detail": "Only validation jobs can be run"
}
```


### 500 Internal Server Error

Returned when ETL processing fails during job execution.

#### Example

```json
{
  "detail": "ETL processing failed: <error message>"
}
```


## Infrastructure errors

Infrastructure errors occur when system-level failures affect application availability or data access.


### 500 Internal Server Error

Returned when an unexpected server-side error occurs.

#### Example scenarios

- Database connection failure
- Object storage access failure
- Unhandled application exception
- Misconfigured environment variables
- Missing encryption key configuration


#### Example

```json
{
  "detail": "Internal server error"
}
```


## Error design

- The API uses FastAPI built-in error handling for consistency and simplicity
- Most error responses use the `detail` field
- Validation errors (`422`) use the structured response format generated by FastAPI
- ETL-related failures are surfaced through job status messages and API responses
- Orders use transactional validation before persistence
- Resource identifiers follow structured formats
- Customer-sensitive values are not exposed in error responses
- Encrypted database values are never returned through API responses
- Error messages are designed to be predictable and human-readable


### Resource identifier formats

| Prefix    | Resource         |
| --------- | ---------------- |
| `FDxxxxx` | Feed             |
| `JSxxxxx` | Submission job   |
| `JVxxxxx` | Validation job   |
| `CUxxxxx` | Customer         |
| `ADxxxxx` | Customer address |
| `PRxxxxx` | Product          |
| `ORxxxxx` | Order            |
| `OIxxxxx` | Order item       |


## Related documentation

- [Feeds](feeds.md)
- [Jobs](jobs.md)
- [Products](products.md)
- [Customers](customers.md)
- [Orders](orders.md)
- [Analytics](analytics.md)