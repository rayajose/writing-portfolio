# Resources

This section defines the core resources used by the Partner Catalog API.

---

## Feed

A Feed represents a product data file submitted by a partner for ingestion.

### Fields

* `feed_id` — unique identifier for the feed (FDxxxxx)
* `partner_name` — name of the submitting partner
* `file_name` — name of the uploaded file
* `content_type` — MIME type of the uploaded file
* `status` — feed upload status (`uploaded`)
* `uploaded_at` — timestamp when the feed was uploaded
* `validation_job_id` — associated validation job ID (JVxxxxx)
* `validation_status` — current ETL job status (`queued`, `running`, `completed`, `failed`)
* `validation_message` — result of ETL processing
* `raw_file_s3_key` — S3 object key for the raw feed file
* `raw_file_bucket` — S3 bucket storing the raw feed

---

### Notes

* Feed status reflects upload state only
* Processing state is tracked via the associated validation job

---

## Job

A Job represents a processing task such as feed submission or ETL execution.

Jobs provide visibility into and control over the ingestion pipeline.

### Fields

* `job_id` — unique identifier for the job (JSxxxxx or JVxxxxx)
* `feed_id` — associated feed
* `job_type` — type of job
* `status` — current job status
* `created_at` — timestamp when the job was created
* `message` — status or result message

---

### Job Types

| Type       | Description                                       |
|------------|---------------------------------------------------|
| submission | Feed upload processing                            |
| validation | ETL processing (S3 → transform → PostgreSQL load) |

---

### Status Values

| Status    | Description                        |
|-----------|------------------------------------|
| queued    | Job created and awaiting execution |
| running   | ETL processing in progress         |
| completed | Job completed successfully         |
| failed    | Job encountered an error           |

---

## Product

A Product represents a normalized item derived from a partner feed.

Products are created during ETL processing and stored for querying.

### Fields

* `product_id` — unique identifier for the product (PRxxxxx)
* `feed_id` — associated feed
* `partner_name` — originating partner
* `sku` — partner-defined stock keeping unit
* `product_name` — display name of the product
* `description` — product description
* `brand` — product brand
* `category` — product category
* `price` — product price (numeric)
* `currency` — currency code (e.g., USD)
* `availability` — availability status (e.g., in_stock)
* `created_at` — timestamp when product was ingested

---

## Identifier Format

All resources use structured identifiers for consistency and traceability:

| Prefix | Resource       | Example |
|--------|----------------|---------|
| FD     | Feed           | FD00001 |
| JS     | Submission Job | JS00001 |
| JV     | Validation Job | JV00001 |
| PR     | Product        | PR00001 |

---

## Health Endpoint

Used to verify API and database availability.

### GET /health

Returns the operational status of the API.

**Response**

```json
{
  "status": "ok",
  "database": "connected"
}
```

---

## Notes

* All resources use `snake_case` field naming in API responses
* Identifiers are generated using database-backed counters
* Raw data is stored in S3 and processed via ETL before becoming queryable
* Products are derived from feeds but can be queried independently
