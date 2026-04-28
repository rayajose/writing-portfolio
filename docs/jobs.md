# Jobs API

The Jobs API provides visibility into and control over processing operations such as feed submission and ETL execution.

---

## Authentication

All requests must include:

```id="n4m6pf"
x-api-key: <your-api-key>
```

---

## Get Job

**GET** `/jobs/{job_id}`

Returns status and metadata for a job.

---

### Example Request

```http id="3r9q3n"
GET /jobs/JS00001
```

---

### Response (200 OK)

```json id="qz9f9n"
{
  "job_id": "JS00001",
  "job_type": "submission",
  "status": "completed",
  "created_at": "2026-04-06T14:17:27+00:00",
  "feed_id": "FD00001",
  "message": "Feed upload accepted."
}
```

---

### Field Definitions

| Field      | Description                                             |
|------------|---------------------------------------------------------|
| job_id     | Unique job identifier (JSxxxxx or JVxxxxx)              |
| job_type   | Type of job (`submission`, `validation`)                |
| status     | Job status (`queued`, `running`, `completed`, `failed`) |
| created_at | UTC timestamp when job was created                      |
| feed_id    | Associated feed ID                                      |
| message    | Optional status message                                 |

---

## Run Job

**POST** `/jobs/{job_id}/run`

Executes a validation job and triggers ETL processing.

---

### Example Request

```bash id="8qg4rm"
curl -X POST http://127.0.0.1:8000/jobs/JV00001/run \
  -H "x-api-key: demo-secret-key"
```

---

### Response (200 OK)

```json id="rm2b6s"
{
  "job_id": "JV00001",
  "status": "completed"
}
```

---

### Behavior

* Only **validation jobs (JVxxxxx)** can be executed
* Triggers ETL pipeline:

  * Reads raw CSV from S3
  * Cleans and validates data
  * Loads products into PostgreSQL
* Updates job status and message with ingestion results

---

## Job Types

| Type       | Description                                     |
|------------|-------------------------------------------------|
| submission | Feed upload processing                          |
| validation | ETL processing (S3 → transform → database load) |

---

## Job Lifecycle

Jobs transition through the following states:

```text id="bn6g3r"
queued → running → completed
                ↘ failed
```

| Status    | Description                        |
|-----------|------------------------------------|
| queued    | Job created and awaiting execution |
| running   | ETL processing in progress         |
| completed | Job finished successfully          |
| failed    | Job encountered an error           |

---

## Pipeline Context

Jobs are part of the ingestion pipeline:

```text id="k6bz0c"
Upload → Submission Job → Validation Job → ETL Processing → Products Loaded
```

---

## Error Responses

#### 404 Not Found

```json id="y7lqxb"
{
  "detail": "Job JS99999 not found."
}
```

#### 400 Bad Request

```json id="6j2x2p"
{
  "detail": "Only validation jobs can be run"
}
```

---

## Related Endpoints

* `POST /feeds/upload` — creates submission and validation jobs
* `GET /feeds/{feed_id}` — retrieve feed and pipeline status
* `GET /products/by-feed/{feed_id}` — retrieve ingested products
