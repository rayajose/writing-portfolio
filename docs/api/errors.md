# Errors

Use this page to understand how the Partner Catalog API returns errors.

---

## Error format

The API primarily uses FastAPI’s standard error response format.

```json
{
  "detail": "Human-readable error message"
}
```

### Fields

| Field  | Type   | Description              |
|--------|--------|--------------------------|
| detail | string | Description of the error |

---

## Common error scenarios

Errors may occur in the following situations:

- Missing or invalid API key
- Invalid request data (e.g., malformed CSV)
- Resource not found (feed, job, or product does not exist)
- ETL processing failure
- Database or infrastructure issues

---

## Status codes

| Status | Meaning                                                |
|--------|--------------------------------------------------------|
| 200    | Request completed successfully                         |
| 201    | Resource created successfully                          |
| 400    | Bad request (invalid input or business rule violation) |
| 401    | Missing API key                                        |
| 403    | Invalid API key                                        |
| 404    | Requested resource not found                           |
| 422    | Request validation failed                              |
| 500    | Internal server error                                  |

---

## Authentication errors

### 401 Unauthorized

Returned when the API key is missing.

#### Example

```json
{
  "detail": "Not authenticated"
}
```

---

### 403 Forbidden

Returned when the API key is invalid.

#### Example

```json
{
  "detail": "Invalid or missing API key"
}
```

---

## Resource errors

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

---

## Validation errors

### 400 Bad Request

Returned when the request is syntactically valid but fails business rules.

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

---

### 422 Unprocessable Entity

Returned when request data fails validation (handled by FastAPI).

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

---

## Job execution errors

### 400 Bad Request

Returned when attempting to execute an unsupported job type.

#### Example

```json
{
  "detail": "Only validation jobs can be run"
}
```

---

### 500 Internal Server Error (ETL Failure)

Returned when ETL processing fails during job execution.

#### Example

```json
{
  "detail": "ETL processing failed: <error message>"
}
```

---

## Infrastructure errors

### 500 Internal Server Error

Returned when an unexpected server-side error occurs.

#### Example scenarios

- Database connection failure
- S3 access or object retrieval failure
- Unhandled application exception
- Misconfigured environment variables

#### Example

```json
{
  "detail": "Internal server error"
}
```

---

## Error design

- The API uses FastAPI’s built-in error handling for consistency and simplicity
- Most error responses use the `detail` field
- Validation errors (`422`) use a structured list format defined by FastAPI
- ETL-related errors are surfaced through job status messages and API responses
- Resource identifiers follow structured formats:

  - `FDxxxxx` → Feed
  - `JSxxxxx` → Submission Job
  - `JVxxxxx` → Validation Job
  - `PRxxxxx` → Product

- Errors are predictable and human-readable to support debugging

---

## Related documentation

- [Feeds API](feeds.md)
- [Jobs API](jobs.md)
- [Products API](products.md)
