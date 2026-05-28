# Jobs

Use this API to retrieve job status and run validation jobs for ETL processing.

- Retrieve job details and track processing status
- Trigger validation jobs for uploaded feeds
- Monitor ETL execution and processing results


## Authentication

All endpoints in this resource require a valid `x-api-key` header.

Include the API key in each request:

```bash
-H "x-api-key: YOUR_API_KEY"
```


## <span class="api-endpoint api-endpoint--get">GET /jobs/{job_id}</span>

Retrieve status and metadata for a job.

### Processing behavior

- Looks up the job by `job_id`
- Returns job metadata including job type, status, associated `feed_id`, and timestamps
- Returns ETL processing summary details for completed validation jobs


### Path parameters

| Name     | Type   | Required | Description                                    |
| -------- | ------ | -------- | ---------------------------------------------- |
| `job_id` | string | Yes      | Unique job identifier (`JSxxxxx` or `JVxxxxx`) |


### Request and response

<div class="api-example-grid">

<div>

<h3>Request</h3>

```bash
curl -X GET http://api.example.com/jobs/JV00012 \
  -H "accept: application/json" \
  -H "x-api-key: YOUR_API_KEY"
```

</div>

<div>

<h3>Response</h3>

```json
{
  "job_id": "JV00001",
  "feed_id": "FD00001",
  "status": "completed",
  "job_type": "validation"
}
```

</div>

</div>


### Response fields

| Field      | Type   | Description                                             |
| ---------- | ------ | ------------------------------------------------------- |
| `job_id`   | string | Unique job identifier (`JSxxxxx` or `JVxxxxx`)          |
| `feed_id`  | string | Associated feed identifier                              |
| `status`   | string | Job status (`queued`, `running`, `completed`, `failed`) |
| `job_type` | string | Job type (`submission` or `validation`)                 |


### Error responses

#### 401 Unauthorized

Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```

#### 404 Not Found

Returned when the request contains a `job_id` not currently in the system.

```json
{
  "error_code": "JOB_NOT_FOUND",
  "message": "Job JV00000 not found",
  "details": {
    "job_id": "JV00000"
  }
}
```


## <span class="api-endpoint api-endpoint--post">POST /jobs/{job_id}/run</span>

Run a validation job and trigger ETL processing.

### Processing behavior

- Allows execution of validation jobs only (`JVxxxxx`)
- Reads raw CSV data from object storage
- Cleans and validates product data
- Loads products into PostgreSQL
- Detects changes and avoids unnecessary updates
- Updates job status and ETL processing summary details


### Path parameters

| Name     | Type   | Required | Description                       |
| -------- | ------ | -------- | --------------------------------- |
| `job_id` | string | Yes      | Unique job identifier (`JVxxxxx`) |


### Request and response

<div class="api-example-grid">

<div>

<h3>Request</h3>

```bash
curl -X POST http://api.example.com/jobs/JV00001/run \
  -H "x-api-key: YOUR_API_KEY"
```

</div>

<div>

<h3>Response</h3>

```json
{
  "job_id": "JV00001",
  "status": "completed"
}
```

</div>

</div>


### Response fields

| Field    | Type   | Description                                             |
| -------- | ------ | ------------------------------------------------------- |
| `job_id` | string | Unique job identifier (`JVxxxxx`)                       |
| `status` | string | Job status (`queued`, `running`, `completed`, `failed`) |


### Error responses

#### 401 Unauthorized

Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```

#### 400 Bad Request

Returned when the request is malformed or contains a submission job identifier.

```json
{
  "detail": "Only validation jobs can be run"
}
```

#### 404 Not Found

Returned when the request contains a `job_id` not currently in the system.

```json
{
  "detail": "Job not found"
}
```


## Additional details

- Job processing is asynchronous
- Jobs move through `queued` → `running` → `completed` or `failed`
- Poll `GET /jobs/{job_id}` to monitor processing status
- Only validation jobs (`JVxxxxx`) can be executed through the API
- Each job is associated with a single `feed_id`
- Re-running a validation job processes the same feed data


## Related documentation

- [Feeds](feeds.md)
- [Products](products.md)
- [Workflows](../architecture/workflows.md)
- [Errors](errors.md)