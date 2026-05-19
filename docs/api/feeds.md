# Feeds API

Use this API to upload product feeds, store raw data, and process them through the validation and ETL pipeline.

- Upload feed files for ingestion into the platform
- Store and track raw feed data and metadata
- Trigger and monitor validation and ETL processing workflows


## Authentication

All endpoints in this resource require a valid `x-api-key` header.

Include the API key in each request:

```bash
-H "x-api-key: YOUR_API_KEY"
```


## `POST /feeds/upload`

Use this endpoint to upload a CSV product feed, store the raw file in object storage, and create associated job records for processing.

### Processing behavior

- Validates file type (CSV only)
- Validates CSV structure (header row required)
- Validates CSV structure (requires `product_name` and `sku` headers)
- Stores raw file in object storage
- Creates a submission job (JSxxxxx) and validation job (JVxxxxx)
- Persists feed metadata for later retrieval

> Note: Product data is **not ingested during upload**. Ingestion occurs during ETL processing.


## Request body (multipart/form-data)

| Field          | Type   | Required | Description                  |
| -------------- | ------ | -------- | ---------------------------- |
| `partner_name` | string | yes      | Name of the partner          |
| `file`         | file   | yes      | CSV file containing products |


### Request and response

<div  class="api-example-grid">
<div>

<h3>Request</h3>

```bash
curl -X POST http://api.example.com/feeds/upload \
  -H "x-api-key: demo-secret-key" \
  -F "partner_name=Acme Corp" \
  -F "file=@sample_catalog.csv"
```

</div>

<div>

<h3>Response</h3>

```json
{
  "feed_id": "FD00003",
  "status": "processing",
  "job_id": "JS00003"
}
```

</div>
</div>


### Response fields

| Field     | Type   | Description                        |
| --------- | ------ | ---------------------------------- |
| `feed_id` | string | Unique feed identifier             |
| `status`  | string | Feed upload status  (`processing`) |
| `job_id`  | string | Unique job identifier (JSxxxxx)    |


### Error responses

#### 401 Unauthorized

Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```

#### 400 Bad request
Returned when the request contains a file formant other than `.csv`.

```json
{ 
  "detail": "Only CSV uploads are supported at this time."
}
```

Returned when the request contains an empty `.csv` file.
```json
{ 
  "detail": "Uploaded file is empty."
}
```

Returned when the request contains a `.csv` file not UTF-8 encoded.
```json
{ 
  "detail": "CSV file must be UTF-8 encoded."
}
```

Returned when the request contains a `.csv` file missing the column headers `product_name` or `sku`. Both are required.
```json
{ 
  "detail": "Invalid CSV file: Missing required CSV headers: product_name, sku"
}
```


## `GET /feeds/{feed_id}`

Use this endpoint to retrieve metadata for a specific feed, including pipeline status and raw file location.

### Processing behavior

- The system looks up the feed by `feed_id`
- Returns feed metadata, including status, timestamps, and associated job information
- Includes raw file storage details such as object storage bucket and object key
- If the feed does not exist, a `404 Not Found` response is returned



### Path parameters

| Name      | Type   | Required | Description                      |
| --------- | ------ | -------- | -------------------------------- |
| `feed_id` | string | Yes      | Unique feed identifier (FDxxxxx) |


### Request and response

<div  class="api-example-grid">
<div>

<h3>Request</h3>

```bash
curl -X 'GET' \
  'http://api.example.com/feeds/FD00003' \
  -H 'accept: application/json' \
  -H 'x-api-key: demo-secret-key'
```

</div>

<div>

<h3>Response</h3>

```json
{
  "feed_id": "FD00003",
  "partner_name": "Acme Corp",
  "file_name": "sample_catalog.csv",
  "content_type": "text/csv",
  "status": "uploaded",
  "uploaded_at": "2026-04-06T14:17:27+00:00",
  "validation_job_id": "JV00003",
  "validation_status": "completed",
  "validation_message": "ETL processing completed. Products processed: 13. Inserted: 1. Updated: 0. Unchanged: 12. Skipped: 0.",
  "raw_file_s3_key": "raw/partners/acme/feeds/FD00001/sample_catalog.csv",
  "raw_file_bucket": "partner-catalog-raw-rayj"
}
```

</div>
</div>


### Response fields
| Field                | Type   | Description                                             |
| -------------------- | ------ | ------------------------------------------------------- |
| `feed_id`            | string | Unique feed identifier (FDxxxxx)                        |
| `partner_name`       | string | Partner that submitted the feed                         |
| `file_name`          | string | Original uploaded file name                             |
| `content_type`       | string | MIME type of the uploaded file                          |
| `status`             | string | Feed upload status (`uploaded`)                         |
| `uploaded_at`        | string | UTC timestamp of upload                                 |
| `validation_job_id`  | string | Validation job ID (JVxxxxx)                             |
| `validation_status`  | string | Job status (`queued`, `running`, `completed`, `failed`) |
| `validation_message` | string | Human-readable ETL result summary                       |
| `raw_file_s3_key`    | string | S3 object key for raw feed                              |
| `raw_file_bucket`    | string | S3 bucket storing raw file                              |


### Error responses

#### 401 Unauthorized
Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```

#### 404 Not found
Returned when the request contains a `feed_id` not currently in system.

```json
{
  "detail": "Feed FD000201 not found."
}
```

## Additional details

* Feed processing is asynchronous. Uploading a feed does not immediately make product data available.
* Use the `validation_status` field to track ETL progress (`queued`, `running`, `completed`, `failed`).
* Product data becomes queryable only after validation and ETL processing complete successfully.
* Feed IDs (`FDxxxxx`) and job IDs (`JSxxxxx`, `JVxxxxx`) follow fixed formats for traceability across the system.


## Related documentation

- [Workflows](../architecture/workflows.md)
- [Errors](errors.md)
- [Products API](products.md)
- [Jobs API](jobs.md)