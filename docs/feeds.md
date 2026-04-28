# Feeds API

The Feeds API allows clients to upload product feeds, store raw data, and track processing through a validation and ETL pipeline.

---

## Authentication

All requests must include an API key:

```
x-api-key: <your-api-key>
```

---

## Upload Feed

**POST** `/feeds/upload`

Uploads a CSV product feed, stores the raw file in S3, and creates associated job records for processing.

---

### Request

**Headers**

```bash
x-api-key: demo-secret-key
Content-Type: multipart/form-data
```

**Form Data**

| Field        | Type   | Required | Description                  |
| ------------ | ------ | -------- | ---------------------------- |
| partner_name | string | yes      | Name of the partner          |
| file         | file   | yes      | CSV file containing products |

---

### Example Request

```bash
curl -X POST http://127.0.0.1:8000/feeds/upload \
  -H "x-api-key: demo-secret-key" \
  -F "partner_name=Acme Corp" \
  -F "file=@sample_catalog.csv"
```

---

### Response (201 Created)

```json
{
  "feed_id": "FD00001",
  "status": "uploaded",
  "job_id": "JS00001"
}
```

---

### Behavior

* Validates file type (CSV only)

* Validates CSV structure (header row required)

* Stores raw file in **Amazon S3**

* Creates:

  * **Submission Job (JSxxxxx)** → tracks upload processing
  * **Validation Job (JVxxxxx)** → tracks ETL processing

* Persists feed metadata for later retrieval

> Note: Product data is **not ingested during upload**. Ingestion occurs during ETL processing.

---

### Error Responses

#### 400 Bad Request

```json
{ "detail": "Only CSV uploads are supported at this time." }
```

```json
{ "detail": "Uploaded file is empty." }
```

```json
{ "detail": "Invalid CSV file: CSV header row is missing." }
```

---

## Get Feed

**GET** `/feeds/{feed_id}`

Returns metadata for a specific feed, including pipeline status and raw file location.

---

### Example Request

```http
GET /feeds/FD00001
```

---

### Response (200 OK)

```json
{
  "feed_id": "FD00001",
  "partner_name": "Acme Corp",
  "file_name": "sample_catalog.csv",
  "content_type": "text/csv",
  "status": "uploaded",
  "uploaded_at": "2026-04-06T14:17:27+00:00",
  "validation_job_id": "JV00001",
  "validation_status": "completed",
  "validation_message": "ETL processing completed. Products ingested: 10.",
  "raw_file_s3_key": "raw/partners/acme/feeds/FD00001/sample_catalog.csv",
  "raw_file_bucket": "partner-catalog-raw-rayj"
}
```

---

### Field Definitions

| Field              | Description                                             |
| ------------------ | ------------------------------------------------------- |
| feed_id            | Unique feed identifier (FDxxxxx)                        |
| partner_name       | Partner that submitted the feed                         |
| file_name          | Original uploaded file name                             |
| content_type       | MIME type of uploaded file                              |
| status             | Feed upload status (`uploaded`)                         |
| uploaded_at        | UTC timestamp of upload                                 |
| validation_job_id  | Validation job ID (JVxxxxx)                             |
| validation_status  | Job status (`queued`, `running`, `completed`, `failed`) |
| validation_message | Human-readable ETL result                               |
| raw_file_s3_key    | S3 object key for raw feed                              |
| raw_file_bucket    | S3 bucket storing raw file                              |

---

## Pipeline Flow

```text
Upload → Stored in S3 → Validation Job Created → ETL Processing → Products Loaded into PostgreSQL
```

---

## Related Endpoints

* `GET /feeds` — List all feeds
* `GET /jobs/{job_id}` — Retrieve job status
* `POST /jobs/{job_id}/run` — Execute ETL processing
* `GET /products/by-feed/{feed_id}` — Retrieve products for a feed
