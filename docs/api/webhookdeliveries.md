# Webhook Deliveries

Use this API to retrieve webhook delivery attempts recorded by the platform.

- Review webhook delivery history
- Verify event delivery status
- Inspect request payloads
- Inspect receiver response codes and response bodies
- Troubleshoot failed webhook deliveries

Webhook delivery records are created automatically when the platform sends supported webhook events to active webhook subscriptions.

## Authentication

All endpoints in this resource require a valid `x-api-key` header.

Include the API key in each request:

```bash
-H "x-api-key: YOUR_API_KEY"
```

## <span class="api-endpoint api-endpoint--get">GET /webhook-deliveries</span>

Retrieve webhook delivery attempts.

### Processing behavior

- Retrieves webhook delivery records from the database
- Returns delivery attempts ordered by creation date
- Includes partner information, event type, delivery status, response code, request payload, and response body

### Request and response

<div class="api-example-grid">
<div>

<h3>Request</h3>

```bash
curl -X GET http://<base-url>/webhook-deliveries \
  -H "x-api-key: YOUR_API_KEY" \
  -H "accept: application/json"
```

</div>

<div>

<h3>Response</h3>

```json
{
  "total": 1,
  "items": [
    {
      "delivery_id": "WD00001",
      "webhook_id": "WH00001",
      "partner_id": "PT00001",
      "partner_name": "Acme Corp",
      "event_type": "feed.validation.completed",
      "status": "succeeded",
      "response_code": 200,
      "request_payload": {
        "event_type": "feed.validation.completed",
        "feed_id": "FD00041",
        "partner_id": "PT00001",
        "status": "completed",
        "summary": {
          "processed": 10,
          "inserted": 0,
          "updated": 0,
          "deleted": 0,
          "unchanged": 10,
          "skipped": 1
        }
      },
      "response_body": "OK",
      "created_at": "YYYY-MM-DDTHH:MM:SSZ"
    }
  ]
}
```

</div>
</div>

### Response fields

| Field   | Type   | Description                               |
| ------- | ------ | ----------------------------------------- |
| `total` | number | Total number of delivery records returned |
| `items` | array  | List of webhook delivery records          |

### Delivery item fields

| Field             | Type   | Description                                           |
| ----------------- | ------ | ----------------------------------------------------- |
| `delivery_id`     | string | Unique webhook delivery identifier (`WDxxxxx`)        |
| `webhook_id`      | string | Associated webhook subscription identifier            |
| `partner_id`      | string | Associated partner identifier                         |
| `partner_name`    | string | Associated partner name                               |
| `event_type`      | string | Webhook event type that was delivered                 |
| `status`          | string | Delivery status (`succeeded` or `failed`)             |
| `response_code`   | number | HTTP response code returned by the receiving endpoint |
| `request_payload` | object | JSON payload sent to the receiving endpoint           |
| `response_body`   | string | Response body returned by the receiving endpoint      |
| `created_at`      | string | Timestamp when the delivery attempt was recorded      |

### Delivery status values

| Status      | Description                                                                       |
| ----------- | --------------------------------------------------------------------------------- |
| `succeeded` | The receiving endpoint returned a 2xx HTTP response                               |
| `failed`    | The receiving endpoint returned a non-2xx response or the delivery attempt failed |

### Error responses

#### 401 Unauthorized

```json
{
  "detail": "Invalid or missing API key"
}
```

## <span class="api-endpoint api-endpoint--get">GET /webhook-deliveries/{delivery_id}</span>

Retrieve a specific webhook delivery attempt.

### Processing behavior

- Retrieves the webhook delivery record by identifier
- Returns delivery details when the record exists
- Returns a not found response if the delivery record does not exist

### Path parameters

| Name          | Type   | Required | Description                                    |
| ------------- | ------ | -------- | ---------------------------------------------- |
| `delivery_id` | string | Yes      | Unique webhook delivery identifier (`WDxxxxx`) |

### Request and response

<div class="api-example-grid">
<div>

<h3>Request</h3>

```bash
curl -X GET http://<base-url>/webhook-deliveries/WD00001 \
  -H "x-api-key: YOUR_API_KEY" \
  -H "accept: application/json"
```

</div>

<div>

<h3>Response</h3>

```json
{
  "delivery_id": "WD00001",
  "webhook_id": "WH00001",
  "partner_id": "PT00001",
  "partner_name": "Acme Corp",
  "event_type": "order.created",
  "status": "succeeded",
  "response_code": 200,
  "request_payload": {
    "event_type": "order.created",
    "order": {
      "order_id": "OR00054",
      "partner_id": "PT00001",
      "partner_name": "Acme Corp",
      "status": "created",
      "total_amount": 149.99,
      "currency": "USD"
    }
  },
  "response_body": "OK",
  "created_at": "YYYY-MM-DDTHH:MM:SSZ"
}
```

</div>
</div>

### Response fields

| Field             | Type   | Description                                           |
| ----------------- | ------ | ----------------------------------------------------- |
| `delivery_id`     | string | Unique webhook delivery identifier                    |
| `webhook_id`      | string | Associated webhook subscription identifier            |
| `partner_id`      | string | Associated partner identifier                         |
| `partner_name`    | string | Associated partner name                               |
| `event_type`      | string | Webhook event type that was delivered                 |
| `status`          | string | Delivery status                                       |
| `response_code`   | number | HTTP response code returned by the receiving endpoint |
| `request_payload` | object | JSON payload sent to the receiving endpoint           |
| `response_body`   | string | Response body returned by the receiving endpoint      |
| `created_at`      | string | Timestamp when the delivery attempt was recorded      |

### Error responses

#### 401 Unauthorized

```json
{
  "detail": "Invalid or missing API key"
}
```

#### 404 Not Found

```json
{
  "detail": "Webhook delivery not found"
}
```

## Supported event types

The platform currently records delivery attempts for these webhook event types:

| Event type                  | Description                                                         |
| --------------------------- | ------------------------------------------------------------------- |
| `feed.validation.completed` | Sent after feed validation and ETL processing complete successfully |
| `order.created`             | Sent after an order is created successfully                         |

## Additional details

- Webhook delivery records are created automatically when webhook events are sent
- A delivery is marked `succeeded` when the receiving endpoint returns a 2xx HTTP response
- A delivery is marked `failed` when the receiving endpoint returns a non-2xx response or the request fails
- Delivery records include the request payload sent to the receiving endpoint
- Delivery records include the response code and response body returned by the receiving endpoint
- Disabled webhook subscriptions do not receive event deliveries
- Delivery records are retained for audit and troubleshooting purposes

## Related documentation

- [Webhooks](webhooks.md)
- [Webhook integration guide](../architecture/webhooks.md)
- [Partners](partners.md)
- [Feeds](feeds.md)
- [Jobs](jobs.md)
- [Orders](orders.md)
- [Errors](errors.md)
