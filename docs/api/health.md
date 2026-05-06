# Health API

Use this API to verify the operational status of the system and its core dependencies.

- Check overall API availability  
- Validate database connectivity  
- Support monitoring and automated health checks  

> Note: This endpoint is lightweight and intended for frequent use by load balancers and monitoring systems.


## GET /health

Use this endpoint to retrieve the current health status of the API and its database connection.

### What happens

- The system attempts to establish a database connection  
- If successful, the connection is immediately closed and the system reports a healthy status  
- If the connection fails, the system returns an error status indicating database unavailability 


### Request and response

<div  class="api-example-grid">
<div>

<h3>Request</h3>

```bash
curl -X 'GET' \
  'http://api.example.com/health' \
  -H 'accept: application/json'
```

</div>

<div>

<h3>Response</h3>


```json
Healthy

{
  "status": "ok",
  "database": "connected"
}
```



```json
Unhealthy

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



### Error responses

This endpoint does not return standard HTTP error codes for system failures.

Instead, failures are reflected in the response body:

- status: error indicates a system or dependency issue
- database: unreachable indicates a failed database connection

## Additional details

- This endpoint is safe to call frequently and has no side effects
- Intended for use by monitoring tools, uptime checks, and load balancers
- Does not expose internal error details for security reasons


## Related documentation

- [Workflows](workflows.md)
- [Errors](errors.md)