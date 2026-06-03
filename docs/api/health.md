# Health

Use this API to verify the operational status of the platform and its core dependencies.

- Check overall API availability
- Validate database connectivity
- Support monitoring and automated health checks

> This endpoint is lightweight and intended for frequent use by load balancers and monitoring systems.


## <span class="api-endpoint api-endpoint--get">GET /health</span>

Retrieve the current health status of the API and database connection.

### Processing behavior

- Attempts to establish a database connection
- Closes the connection immediately after validation
- Returns a healthy status when the database connection succeeds
- Returns an error status when the database connection fails


### Request and response

<div class="api-example-grid">
<div>

<h3>Request</h3>

```bash
curl -X GET http://<base-url>/health \
  -H "accept: application/json"
```

</div>

<div>

<h3>Healthy response</h3>

```json
{
  "status": "ok",
  "database": "connected"
}
```

<h3>Unhealthy response</h3>

```json
{
  "status": "error",
  "database": "unreachable"
}
```

</div>
</div>


### Response fields

| Field      | Type   | Description                                                 |
| ---------- | ------ | ----------------------------------------------------------- |
| `status`   | string | Overall system status (`ok` or `error`)                     |
| `database` | string | Database connectivity status (`connected` or `unreachable`) |


### Error handling

This endpoint does not return standard HTTP error codes for dependency failures.

Instead, failures are reflected in the response body:

- `status: error` indicates a system or dependency issue
- `database: unreachable` indicates a failed database connection


## Additional details

- This endpoint is safe to call frequently and has no side effects
- Intended for use by monitoring tools, uptime checks, and load balancers
- Does not expose internal error details


## Related documentation

- [Errors](errors.md)