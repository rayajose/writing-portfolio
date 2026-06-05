# Webhooks

Use this API to create and manage webhook subscriptions for receiving asynchronous event notifications.

- Register webhook endpoints
- Subscribe to supported event types
- Retrieve webhook subscriptions
- Update webhook endpoint configuration
- Enable or disable webhook deliveries

> Webhook event delivery, payload formats, retry behavior, and signature validation are documented in the Webhook Integration Guide.

## Authentication

All endpoints in this resource require a valid `x-api-key` header.

Include the API key in each request:

```bash
-H "x-api-key: YOUR_API_KEY"
```

## <span class="api-endpoint api-endpoint--post">POST /webhooks</span>

Create a webhook subscription.

### Processing behavior

- Validates that the specified partner exists
- Validates all requested event types
- Generates a unique webhook identifier (`WHxxxxx`)
- Generates a webhook signing secret
- Stores the webhook subscription
- Returns the created subscription

### Request body

| Field        | Type   | Required | Description                                 |
| ------------ | ------ | -------- | ------------------------------------------- |
| `partner_id` | string | Yes      | Partner identifier                          |
| `url`        | string | Yes      | HTTPS endpoint that receives webhook events |
| `events`     | array  | Yes      | List of subscribed event types              |

### Request and response

<div class="api-example-grid">
<div>

<h3>Request</h3>

```json
{
  "partner_id": "PT00001",
  "url": "https://<base-url>/webhooks/commerce",
  "events": [
    "feed.validation.completed",
    "order.created"
  ]
}
```

</div>

<div>

<h3>Response</h3>

```json
{
  "webhook_id": "WH00001",
  "partner_id": "PT00001",
  "url": "https://<base-url>/webhooks/commerce",
  "events": [
    "feed.validation.completed",
    "order.created"
  ],
  "secret": "whsec_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "status": "active",
  "created_at": "YYYY-MM-DDTHH:MM:SSZ",
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ"
}
```

</div>
</div>

### Response fields

| Field        | Type   | Description                                          |
| ------------ | ------ | ---------------------------------------------------- |
| `webhook_id` | string | Unique webhook identifier (`WHxxxxx`)                |
| `partner_id` | string | Associated partner identifier                        |
| `url`        | string | Destination webhook URL                              |
| `events`     | array  | Subscribed event types                               |
| `secret`     | string | Webhook signing secret                               |
| `status`     | string | Subscription status                                  |
| `created_at` | string | UTC timestamp when the subscription was created      |
| `updated_at` | string | UTC timestamp when the subscription was last updated |

!!! danger "Store the webhook secret"

    The webhook secret is returned only when the subscription is created and cannot be retrieved later through the API.


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
  "detail": "Partner not found: PT99999"
}
```

#### 422 Unprocessable Entity

```json
{
  "detail": {
    "message": "Unsupported webhook event type.",
    "invalid_events": [
      "inventory.updated"
    ]
  }
}
```

## <span class="api-endpoint api-endpoint--get">GET /webhooks</span>

Retrieve webhook subscriptions.

### Processing behavior

- Retrieves webhook subscriptions from the database
- Returns subscriptions ordered by creation date

### Request and response

<div class="api-example-grid">
<div>

<h3>Request</h3>

```bash
curl -X GET http://<base-url>/webhooks \
  -H "x-api-key: YOUR_API_KEY" \
  -H "accept: application/json"
```

</div>

<div>

<h3>Response</h3>

```json
[
  {
    "webhook_id": "WH00001",
    "partner_id": "PT00001",
    "url": "https://<base-url>/webhooks/commerce",
    "events": [
      "feed.validation.completed",
      "order.created"
    ],
    "status": "active",
    "created_at": "YYYY-MM-DDTHH:MM:SSZ",
    "updated_at": "YYYY-MM-DDTHH:MM:SSZ"
  }
]
```

</div>
</div>

### Response fields

| Field        | Type   | Description                   |
| ------------ | ------ | ----------------------------- |
| `webhook_id` | string | Unique webhook identifier     |
| `partner_id` | string | Associated partner identifier |
| `url`        | string | Destination webhook URL       |
| `events`     | array  | Subscribed event types        |
| `status`     | string | Subscription status           |
| `created_at` | string | Creation timestamp            |
| `updated_at` | string | Last update timestamp         |

### Error responses

#### 401 Unauthorized

```json
{
  "detail": "Invalid or missing API key"
}
```

## <span class="api-endpoint api-endpoint--get">GET /webhooks/{webhook_id}</span>

Retrieve a specific webhook subscription.

### Processing behavior

- Retrieves the webhook subscription by identifier
- Returns subscription details when the subscription exists
- Returns a not found response if the subscription does not exist

### Path parameters

| Name         | Type   | Required | Description                           |
| ------------ | ------ | -------- | ------------------------------------- |
| `webhook_id` | string | Yes      | Unique webhook identifier (`WHxxxxx`) |

### Request and response

<div class="api-example-grid">
<div>

<h3>Request</h3>

```bash
curl -X GET http://<base-url>/webhooks/WH00001 \
  -H "x-api-key: YOUR_API_KEY" \
  -H "accept: application/json"
```

</div>

<div>

<h3>Response</h3>

```json
{
  "webhook_id": "WH00001",
  "partner_id": "PT00001",
  "url": "https://<base-url>/webhooks/commerce",
  "events": [
    "feed.validation.completed",
    "order.created"
  ],
  "status": "active",
  "created_at": "YYYY-MM-DDTHH:MM:SSZ",
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ"
}
```

</div>
</div>

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
  "detail": "Webhook subscription not found: WH99999"
}
```

## <span class="api-endpoint api-endpoint--patch">PATCH /webhooks/{webhook_id}</span>

Update a webhook subscription.

### Processing behavior

- Retrieves the existing subscription
- Updates the supplied fields
- Validates updated event types when provided
- Updates the subscription timestamp
- Returns the updated subscription

### Path parameters

| Name         | Type   | Required | Description                           |
| ------------ | ------ | -------- | ------------------------------------- |
| `webhook_id` | string | Yes      | Unique webhook identifier (`WHxxxxx`) |

### Request body

| Field    | Type   | Required | Description                                |
| -------- | ------ | -------- | ------------------------------------------ |
| `url`    | string | No       | Updated webhook endpoint URL               |
| `events` | array  | No       | Updated list of subscribed event types     |
| `status` | string | No       | Subscription status (`active`, `disabled`) |

### Request and response

<div class="api-example-grid">
<div>

<h3>Request</h3>

```json
{
  "status": "disabled"
}
```

</div>

<div>

<h3>Response</h3>

```json
{
  "webhook_id": "WH00001",
  "partner_id": "PT00001",
  "url": "https://<base-url>/webhooks/commerce",
  "events": [
    "feed.validation.completed",
    "order.created"
  ],
  "status": "disabled",
  "created_at": "YYYY-MM-DDTHH:MM:SSZ",
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ"
}
```

</div>
</div>

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
  "detail": "Webhook subscription not found: WH99999"
}
```

#### 422 Unprocessable Entity

```json
{
  "detail": {
    "message": "Unsupported webhook event type."
  }
}
```

## Additional details

- Webhook subscriptions are associated with a single partner
- Webhook signing secrets are generated automatically during subscription creation
- Webhook secrets are returned only when the subscription is created
- Disabled subscriptions do not receive event deliveries
- Multiple subscriptions may be configured for the same partner
- Supported event types are documented in the Webhook Integration Guide

## Related documentation

- [Webhook integration guide](../architecture/webhooks.md)
- [Partners](partners.md)
- [Feeds](feeds.md)
- [Jobs](jobs.md)
- [Orders](orders.md)
- [Customers](customers.md)
- [Errors](errors.md)
