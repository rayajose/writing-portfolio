# Jobs API

Use this API to retrieve job status and run validation jobs for ETL processing.

---

- Retrieve job details and track processing status
- Trigger validation jobs for uploaded feeds
- Monitor ETL execution and results

---

## Authentication

All endpoints in this resource require a valid `x-api-key` header.

Include the API key in each request:

```bash
-H "x-api-key: YOUR_API_KEY"
```


---
##  GET /jobs/{job_id}

Use this endpoint to retrieve the status and metadata for a job.

### What happens

- The system looks up the job by `job_id`
- Returns job metadata including type, status, associated `feed_id`, and timestamps
- If the job has completed, includes the ETL result summary (for validation jobs)

---

### Path parameters

| Name     | Type   | Required | Description                                |
| -------- | ------ | -------- | ------------------------------------------ |
| `job_id` | string | Yes      | Unique job identifier (JSxxxxx or JVxxxxx) |

---

### Request and response

<div  class="api-example-grid">

<div>

<h3>Request</h3>

```bash
curl -X 'GET' \
  'http://api.example.com/jobs/JV00012' \
  -H 'accept: application/json' \
  -H 'x-api-key: demo-secret-key'
```

</div>


<div>

<h3>Response</h3>

```json
{
  "job_id": "JV00012",
  "feed_id": "FD00012",
  "status": "completed",
  "job_type": "validation"
}
```

</div>

</div>




---

### Response fields

| Field      | Type   | Description                                             |
| ---------- | ------ | ------------------------------------------------------- |
| `job_id`   | string | Unique job identifier (JSxxxxx or JVxxxxx)              |
| `feed_id`  | string | Associated feed ID                                      |
| `status`   | string | Job status (`queued`, `running`, `completed`, `failed`) |
| `job_type` | string | UTC timestamp when job was created                      |

---

### Error responses

#### 401 Unauthorized
Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```

#### 404 Not found
Returned when the request contains a `job_id` not currently in system.

```json
{
  "error_code": "JOB_NOT_FOUND",
  "message": "Job JV00000 not found",
  "details": {
    "job_id": "JV00000"
  }
}
```

---

## POST /jobs/{job_id}/run

Use this endpoint to start a validation job and trigger ETL processing.

### What happens

- Only **validation jobs (JVxxxxx)** can be executed
- Triggers ETL pipeline:
  - Reads raw CSV from S3
  - Cleans and validates data
  - Loads products into PostgreSQL
  - Detects changes and avoids unnecessary updates
- Updates job status and message with ETL results summary

---

### Path parameters

| Name     | Type   | Required | Description                     |
| -------- | ------ | -------- | ------------------------------- |
| `job_id` | string | Yes      | Unique job identifier (JVxxxxx) |

---

### Request and response

<div  class="api-example-grid">

<div>

<h3>Example request</h3>

```bash
curl -X POST http://api.example.com/jobs/JV00001/run \
  -H "x-api-key: demo-secret-key"
```

</div>


<div>

<h3>Example response</h3>

```json
{
  "job_id": "JV00001",
  "status": "completed"
}
```

</div>

</div>




---

### Response fields

| Field    | Type   | Description                                             |
| -------- | ------ | ------------------------------------------------------- |
| `job_id` | string | Unique job identifier (JVxxxxx)                         |
| `status` | string | Job status (`queued`, `running`, `completed`, `failed`) |

---
### Error responses

#### 401 Unauthorized
Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```

#### 400 Bad request
Returned when the request is malformed or contains a submission job id.

```json
{
  "detail": "Only validation jobs can be run"
}
```

#### 404 Not found
Returned when the request contains a `job_id` not currently in system.

```json
{
  "detail": "Job not found"
}
```

## Additional details

- Job processing is asynchronous. Jobs move through `queued` → `running` → `completed` or `failed`, and status must be polled via `GET /jobs/{job_id}`.
- Only validation jobs (`JVxxxxx`) can be executed via the API. Each job is tied to a single `feed_id` and is idempotent at the feed level (re-running processes the same feed data).

---

## Related documentation

- [Workflows](workflows.md)
- [Errors](errors.md)
- [Feeds API](feeds.md)
- [Products API](products.md)
