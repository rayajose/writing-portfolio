# CSV Feed File Specification

## Purpose

The `/feeds/upload` endpoint accepts partner product data as a CSV file. The file is stored as raw input and processed by the ETL pipeline to create or update product records.

---

## File Requirements

CSV files must meet the following requirements:

| Requirement     | Description                                             |
|-----------------|---------------------------------------------------------|
| File format     | CSV                                                     |
| Encoding        | UTF-8 recommended                                       |
| Header row      | Required                                                |
| Delimiter       | Comma `,`                                               |
| File extension  | `.csv` recommended                                      |
| Content type    | `text/csv`, `text/plain`, or `application/vnd.ms-excel` |
| Required fields | `sku`, `product_name`                                   |

---

## Required Columns

The following columns are required for each product record:

| Column         | Type   | Required | Description                                |
|----------------|--------|----------|--------------------------------------------|
| `sku`          | string | Yes      | Partner-provided unique product identifier |
| `product_name` | string | Yes      | Display name of the product                |

Rows missing either `sku` or `product_name` are skipped during ETL processing.

---

## Recommended Columns

The following columns are recommended for complete product records:

| Column         | Type    | Required | Description                                 |
|----------------|---------|----------|---------------------------------------------|
| `brand`        | string  | No       | Product brand or manufacturer               |
| `category`     | string  | No       | Product category                            |
| `price`        | decimal | No       | Product price (numeric, no currency symbol) |
| `currency`     | string  | No       | Three-letter currency code, such as `USD`   |
| `availability` | string  | No       | Product availability status                 |
| `description`  | string  | No       | Product description                         |

---

## Example CSV

```csv
sku,product_name,brand,category,price,currency,availability,description
SKU-1001,Wireless Mouse,Logitech,Electronics,24.99,USD,in_stock,Ergonomic wireless mouse
SKU-1002,USB-C Cable,Anker,Electronics,12.99,USD,in_stock,6-foot USB-C charging cable
SKU-1003,Laptop Stand,Generic,Office Accessories,39.99,USD,out_of_stock,Adjustable aluminum laptop stand
```

---

## Validation Behavior

During ETL processing, the system validates each row.

| Condition                                      | Result               |
|------------------------------------------------|----------------------|
| Valid row with new `sku`                       | Product is inserted  |
| Valid row with existing `sku` and changed data | Product is updated   |
| Valid row with existing `sku` and no changes   | Product is unchanged |
| Row missing `sku`                              | Row is skipped       |
| Row missing `product_name`                     | Row is skipped       |
| Malformed CSV structure                        | Validation may fail  |

---

## Product Uniqueness

Products are uniquely identified by the combination of:

```
partner_name + sku
```

This means two different partners may use the same SKU without conflict.

---

## Formatting Guidelines

Follow these guidelines when preparing a CSV file:

* Include exactly one header row
* Do not leave required fields blank
* Use consistent column names
* Avoid duplicate `sku` values within the same partner feed
* Use plain numeric values for prices, such as `19.99`
* Do not include currency symbols in the `price` field
* Use consistent availability values, such as `in_stock` or `out_of_stock`

---

## Upload Example

```bash
curl -X POST "http://<host>/feeds/upload" \
  -H "x-api-key: <api-key>" \
  -F "partner_name=Tronics" \
  -F "file=@electronics_catalog.csv"
```

---

## Successful Upload Response

```json
{
  "feed_id": "FD00010",
  "partner_name": "Tronics",
  "file_name": "electronics_catalog.csv",
  "content_type": "text/csv",
  "status": "uploaded",
  "validation_job_id": "JV00010"
}
```
