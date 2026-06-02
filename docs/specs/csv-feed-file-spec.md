# CSV feed file specification

<div class="doc-meta">
  <span>File specification</span>
  <span>CSV schema</span>
  <span>Data validation</span>
  <span>Partner onboarding</span>
</div>

## Purpose

Uploaded files are stored as raw input and processed by the ETL pipeline to create or update product records.


## File requirements

CSV files must meet the following requirements:

| Requirement     | Description                                                                                    |
| --------------- | ---------------------------------------------------------------------------------------------- |
| File format     | CSV                                                                                            |
| Encoding        | UTF-8 recommended                                                                              |
| Header row      | Required                                                                                       |
| Delimiter       | Comma `,`                                                                                      |
| File extension  | `.csv` recommended                                                                             |
| Content type    | `text/csv`, `text/plain`, or `application/vnd.ms-excel`                                        |
| Required fields | `sku`, `product_name`, `description`, `brand`, `category`, `price`, `currency`, `availability` |

!!! note "CSV compatibility"

    CSV files generated from spreadsheet applications should be exported using UTF-8 encoding to avoid character and delimiter inconsistencies during ETL validation.

## Required columns

The following columns are required for each product record:

| Column         | Type    | Required | Description                                     |
| -------------- | ------- | -------- | ----------------------------------------------- |
| `sku`          | string  | Yes      | Partner-provided unique product identifier      |
| `product_name` | string  | Yes      | Display name of the product                     |
| `description`  | string  | Yes      | Product description                             |
| `brand`        | string  | Yes      | Product brand or manufacturer                   |
| `category`     | string  | Yes      | Product category                                |
| `price`        | decimal | Yes      | Product price (numeric, no currency symbol)     |
| `currency`     | string  | Yes      | Three-letter currency code (for example, `USD`) |
| `availability` | string  | Yes      | Product availability status                     |

Files missing any required column are rejected during upload validation.


## Example feed

```csv
sku,product_name,brand,category,price,currency,availability,description
SKU-1001,Wireless Mouse,Logitech,Electronics,24.99,USD,in_stock,Ergonomic wireless mouse
SKU-1002,USB-C Cable,Anker,Electronics,12.99,USD,in_stock,6-foot USB-C charging cable
SKU-1003,Laptop Stand,Generic,Office Accessories,39.99,USD,out_of_stock,Adjustable aluminum laptop stand
```


## Processing behavior

- Validate CSV headers
- Validate required field values
- Validate price format
- Validate currency format
- Validate availability values
- Store the raw file in Amazon S3
- Create submission and validation jobs
- Process data during ETL
- Insert, update, remove, or skip product records  


## Validation

During ETL processing, the system validates each row.

| Condition                                      | Result               |
| ---------------------------------------------- | -------------------- |
| Missing required column                        | Feed is rejected     |
| Missing required field value                   | Feed is rejected     |
| Invalid price value                            | Feed is rejected     |
| Invalid currency code                          | Feed is rejected     |
| Invalid `availability` value                   | Feed is rejected     |
| Valid row with new `sku` and `in_stock`        | Product is inserted  |
| Valid row with existing `sku` and changed data | Product is updated   |
| Valid row with existing `sku` and no changes   | Product is unchanged |
| Existing product marked `out_of_stock`         | Product is removed   |
| New product marked `out_of_stock`              | Row is skipped       |
| Malformed CSV structure                        | Validation may fail  |

!!! tip "Idempotent processing"

    Existing product records are updated only when incoming feed data changes, reducing unnecessary database updates during recurring feed ingestion.

### Field validation rules

| Field          | Validation rule                            | Allowed examples           | Invalid examples              |
| -------------- | ------------------------------------------ | -------------------------- | ----------------------------- |
| `price`        | Numeric value greater than or equal to `0` | `19.99`, `0`, `125`        | `-5.00`, `$19.99`, `abc`      |
| `currency`     | Three-letter currency code                 | `USD`, `EUR`, `GBP`        | `US`, `USDD`, `123`           |
| `availability` | Must be one of the supported values        | `in_stock`, `out_of_stock` | `available`, `instock`, `yes` |

## Product uniqueness

Products are uniquely identified by the combination of:

```
partner_id + sku
```
This constraint prevents duplicate product ingestion for the same partner while allowing different partners to use identical SKU values independently.

The same SKU may be used by multiple partners without conflict because product uniqueness is enforced per `partner_id`.


## Formatting guidelines

Follow these guidelines when preparing a CSV file:

- Include exactly one header row
- Do not leave required fields blank
- Use consistent column names
- Avoid duplicate `sku` values within the same partner feed
- Use plain numeric values for prices, such as `19.99`
- Do not include currency symbols in the `price` field
- Use only the supported availability values: `in_stock` and `out_of_stock`

## Related documentation

- [Feeds](../api/feeds.md)