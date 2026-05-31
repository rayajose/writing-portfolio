# Partners

Use this API to create, retrieve, and manage partner organizations that submit product feeds to the platform.

* Create partner records for feed providers
* Track partner lifecycle status
* Store partner contact and feed configuration metadata
* Associate uploaded feeds with managed partner identifiers

## Authentication

All endpoints in this resource require a valid `x-api-key` header.

Include the API key in each request:

```bash
-H "x-api-key: YOUR_API_KEY"
```

## <span class="api-endpoint api-endpoint--post">POST /partners</span>

Create a partner record.

### Processing behavior

* Generates a partner ID using the `PTxxxxx` format
* Stores partner metadata in PostgreSQL
* Sets the partner status to `active` by default
* Returns the created partner record

## Request body

| Field                 | Type   | Required | Description                                       |
| --------------------- | ------ | -------- | ------------------------------------------------- |
| `partner_name`        | string | Yes      | Name of the partner organization                  |
| `contact_email`       | string | No       | Partner contact email address                     |
| `feed_type`           | string | No       | Feed type submitted by the partner                |
| `default_file_format` | string | No       | Default file format used for partner feed uploads |

### Request and response

<div class="api-example-grid">
<div>

<h3>Request</h3>

```bash
curl -X POST http://api.example.com/partners \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "partner_name": "Acme Corp",
    "contact_email": "integrations@acme.example",
    "feed_type": "product_catalog",
    "default_file_format": "csv"
  }'
```

</div>

<div>

<h3>Response</h3>

```json
{
  "partner_id": "PT00001",
  "partner_name": "Acme Corp",
  "status": "active",
  "contact_email": "integrations@acme.example",
  "feed_type": "product_catalog",
  "default_file_format": "csv",
  "created_at": "YYYY-MM-DDTHH:MM:SS",
  "updated_at": "YYYY-MM-DDTHH:MM:SS"
}
```

</div>
</div>

### Response fields

| Field                 | Type   | Description                                   |
| --------------------- | ------ | --------------------------------------------- |
| `partner_id`          | string | Unique partner identifier (`PTxxxxx`)         |
| `partner_name`        | string | Name of the partner organization              |
| `status`              | string | Partner lifecycle status                      |
| `contact_email`       | string | Partner contact email address                 |
| `feed_type`           | string | Feed type submitted by the partner            |
| `default_file_format` | string | Default file format used for feed uploads     |
| `created_at`          | string | Timestamp when the partner record was created |
| `updated_at`          | string | Timestamp when the partner record was updated |

### Error responses

#### 401 Unauthorized

Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```

#### 422 Unprocessable Entity

Returned when the request body is missing a required field or includes an invalid value.

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "partner_name"],
      "msg": "Field required"
    }
  ]
}
```

## <span class="api-endpoint api-endpoint--get">GET /partners</span>

Retrieve partner records.

### Processing behavior

* Returns partner records sorted by creation timestamp
* Includes partner status, contact, and feed configuration metadata
* Use this endpoint to find the `partner_id` required for feed uploads

### Request and response

<div class="api-example-grid">
<div>

<h3>Request</h3>

```bash
curl -X GET http://api.example.com/partners \
  -H "accept: application/json" \
  -H "x-api-key: YOUR_API_KEY"
```

</div>

<div>

<h3>Response</h3>

```json
[
  {
    "partner_id": "PT00001",
    "partner_name": "Acme Corp",
    "status": "active",
    "contact_email": "integrations@acme.example",
    "feed_type": "product_catalog",
    "default_file_format": "csv",
    "created_at": "YYYY-MM-DDTHH:MM:SS",
    "updated_at": "YYYY-MM-DDTHH:MM:SS"
  }
]
```

</div>
</div>

### Response fields

| Field                 | Type   | Description                                   |
| --------------------- | ------ | --------------------------------------------- |
| `partner_id`          | string | Unique partner identifier (`PTxxxxx`)         |
| `partner_name`        | string | Name of the partner organization              |
| `status`              | string | Partner lifecycle status                      |
| `contact_email`       | string | Partner contact email address                 |
| `feed_type`           | string | Feed type submitted by the partner            |
| `default_file_format` | string | Default file format used for feed uploads     |
| `created_at`          | string | Timestamp when the partner record was created |
| `updated_at`          | string | Timestamp when the partner record was updated |

### Error responses

#### 401 Unauthorized

Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```

## <span class="api-endpoint api-endpoint--get">GET /partners/{partner_id}</span>

Retrieve a specific partner by partner ID.

### Processing behavior

* Looks up the partner by `partner_id`
* Returns partner lifecycle and feed configuration metadata
* Returns a `404 Not Found` response if the partner does not exist

### Path parameters

| Name         | Type   | Required | Description                           |
| ------------ | ------ | -------- | ------------------------------------- |
| `partner_id` | string | Yes      | Unique partner identifier (`PTxxxxx`) |

### Request and response

<div class="api-example-grid">
<div>

<h3>Request</h3>

```bash
curl -X GET http://api.example.com/partners/PT00001 \
  -H "accept: application/json" \
  -H "x-api-key: YOUR_API_KEY"
```

</div>

<div>

<h3>Response</h3>

```json
{
  "partner_id": "PT00001",
  "partner_name": "Acme Corp",
  "status": "active",
  "contact_email": "integrations@acme.example",
  "feed_type": "product_catalog",
  "default_file_format": "csv",
  "created_at": "YYYY-MM-DDTHH:MM:SS",
  "updated_at": "YYYY-MM-DDTHH:MM:SS"
}
```

</div>
</div>

### Response fields

| Field                 | Type   | Description                                   |
| --------------------- | ------ | --------------------------------------------- |
| `partner_id`          | string | Unique partner identifier (`PTxxxxx`)         |
| `partner_name`        | string | Name of the partner organization              |
| `status`              | string | Partner lifecycle status                      |
| `contact_email`       | string | Partner contact email address                 |
| `feed_type`           | string | Feed type submitted by the partner            |
| `default_file_format` | string | Default file format used for feed uploads     |
| `created_at`          | string | Timestamp when the partner record was created |
| `updated_at`          | string | Timestamp when the partner record was updated |

### Error responses

#### 401 Unauthorized

Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```

#### 404 Not Found

Returned when the request contains a `partner_id` not currently in the system.

```json
{
  "detail": "Partner not found"
}
```

## Partner status values

| Status       | Description                                            |
| ------------ | ------------------------------------------------------ |
| `active`     | Partner can submit product feeds                       |
| `paused`     | Partner is temporarily prevented from submitting feeds |
| `offboarded` | Partner is no longer allowed to submit feeds           |

## Additional details

* Partner IDs use the `PTxxxxx` format for system traceability
* Feed upload requests must include a valid `partner_id`
* Partner names must be unique
* New partners are created with `active` status by default
* Paused or offboarded partners cannot submit new feeds

## Related documentation

* [Feeds](feeds.md)
* [Jobs](jobs.md)
* [Products](products.md)
* [Errors](errors.md)
* [Partner onboarding](../operations/onboarding.md)
