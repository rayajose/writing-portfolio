# Feeds

Use this API to upload product feeds, store raw feed data, and process feeds through validation and ETL workflows.

- Upload product feed files for ingestion into the platform
- Store and track raw feed data and metadata
- Trigger and monitor validation and ETL processing workflows


## Authentication

All endpoints in this resource require a valid `x-api-key` header.

Include the API key in each request:

```bash
-H "x-api-key: YOUR_API_KEY"
```


## <span class="api-endpoint api-endpoint--post">POST /feeds/upload</span>

Upload a CSV product feed and create associated processing jobs.

### Feed file specification

For complete CSV formatting rules, supported fields, validation requirements, and file constraints, see the [CSV feed file specification](../specs/csv-feed-file-spec.md).

### Processing behavior

- Validates that the supplied partner exists and is active
- Validates file type (`.csv` only)
- Validates CSV structure and required headers
- Validates supported values
- Rejects feeds containing invalid field values
- Stores the raw file in object storage
- Creates submission (`JSxxxxx`) and validation (`JVxxxxx`) job records
- Persists feed metadata for later retrieval
- Starts ETL processing asynchronously

!!! note "Asynchronous ingestion"

    Product data is not ingested during upload. Validation and ETL processing occur asynchronously after the upload is accepted.

## Request body (multipart/form-data)

| Field        | Type   | Required | Description                    |
| ------------ | ------ | -------- | ------------------------------ |
| `partner_id` | string | Yes      | Partner identifier (`PTxxxxx`) |
| `file`       | file   | Yes      | CSV file containing products   |

### Request and response

<div class="api-example-grid">
<div>

<h3>Request</h3>

```bash
curl -X POST http://<base-url>/feeds/upload \
  -H "x-api-key: YOUR_API_KEY" \
  -F "partner_id=PT00001" \
  -F "file=@acme-product-catalog.csv"
```

</div>

<div>

<h3>Response</h3>

```json
{
  "feed_id": "FD00001",
  "status": "processing",
  "job_id": "JS00001"
}
```

</div>
</div>

### Response fields

| Field     | Type   | Description                           |
| --------- | ------ | ------------------------------------- |
| `feed_id` | string | Unique feed identifier                |
| `status`  | string | Feed upload status (`processing`)     |
| `job_id`  | string | Submission job identifier (`JSxxxxx`) |

### Error responses

#### 401 Unauthorized

Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```

#### 404 Not Found

Returned when the specified partner does not exist.

```json
{
  "detail": "Partner not found."
}
```

#### 400 Bad Request

Returned when the partner is not active.

```json
{
  "detail": "Partner is paused and cannot submit feeds."
}
```

Returned when the request contains a file format other than `.csv`.

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

Returned when the request contains a `.csv` file that is not UTF-8 encoded.

```json
{
  "detail": "CSV file must be UTF-8 encoded."
}
```

Returned when the request contains a `.csv` file missing one or more required headers.

```json
{
  "detail": "Invalid CSV file: Missing required CSV headers: availability, product_name"
}
```

Returned when the request contains an unsupported field value.

```json
{
  "detail": "Invalid CSV file: Invalid availability value 'available' on row 2. Allowed values: in_stock, out_of_stock."
}
```

For complete CSV requirements and validation rules, see the [CSV feed file specification](../specs/csv-feed-file-spec.md).

## <span class="api-endpoint api-endpoint--get">GET /feeds/{feed_id}</span>

Retrieve metadata for a specific feed.

### Processing behavior

- Looks up the feed by `feed_id`
- Returns feed metadata, timestamps, and associated job information
- Includes object storage details for the raw uploaded file
- Returns a `404 Not Found` response if the feed does not exist


### Path parameters

| Name      | Type   | Required | Description                        |
| --------- | ------ | -------- | ---------------------------------- |
| `feed_id` | string | Yes      | Unique feed identifier (`FDxxxxx`) |


### Request and response

<div class="api-example-grid">
<div>

<h3>Request</h3>

```bash
curl -X GET http://<base-url>/feeds/FD00001 \
  -H "accept: application/json" \
  -H "x-api-key: YOUR_API_KEY"
```

</div>

<div>

<h3>Response</h3>

```json
{
  "feed_id": "FD00001",
  "partner_id": "PT00001",
  "partner_name": "Acme Corp",
  "file_name": "acme-product-catalog.csv",
  "content_type": "text/csv",
  "status": "uploaded",
  "uploaded_at": "YYYY-MM-DDTHH:MM:SSZ",
  "validation_job_id": "JV00001",
  "validation_status": "completed",
  "validation_message": "ETL processing completed. Products processed: 13. Inserted: 1. Updated: 0. Deleted: 1.Unchanged: 12. Skipped: 0.",
  "raw_file_s3_key": "raw/partners/acme-corp/feeds/FD00001/acme-product-catalog.csv",
  "raw_file_bucket": "commerce-integration-raw"
}
```

</div>
</div>


### Response fields

| Field                | Type   | Description                                             |
| -------------------- | ------ | ------------------------------------------------------- |
| `feed_id`            | string | Unique feed identifier (`FDxxxxx`)                      |
| `partner_id`         | string | Partner identifier (`PTxxxxx`)                          |
| `partner_name`       | string | Partner that submitted the feed                         |
| `file_name`          | string | Original uploaded file name                             |
| `content_type`       | string | MIME type of the uploaded file                          |
| `status`             | string | Feed upload status (`uploaded`)                         |
| `uploaded_at`        | string | UTC timestamp of upload                                 |
| `validation_job_id`  | string | Validation job identifier (`JVxxxxx`)                   |
| `validation_status`  | string | Job status (`queued`, `running`, `completed`, `failed`) |
| `validation_message` | string | Human-readable ETL processing summary                   |
| `raw_file_s3_key`    | string | Object storage key for the raw feed                     |
| `raw_file_bucket`    | string | Object storage bucket storing the raw feed              |


### Error responses

#### 401 Unauthorized

Returned when the request is missing or includes an invalid `x-api-key` header.

```json
{
  "detail": "Invalid or missing API key"
}
```

#### 404 Not Found

Returned when the request contains a `feed_id` not currently in the system.

```json
{
  "detail": "Feed FD000201 not found."
}
```


## Additional details

- Feed processing is asynchronous
- Uploading a feed does not immediately make product data available
- Use `validation_status` to track ETL processing progress
- Product data becomes queryable only after validation and ETL processing complete successfully
- Feed IDs (`FDxxxxx`) and job IDs (`JSxxxxx`, `JVxxxxx`) use fixed formats for system traceability


## Related documentation

- [Workflows](../architecture/workflows.md)
- [Errors](errors.md)
- [Products](products.md)
- [Jobs](jobs.md)