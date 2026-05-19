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

| Requirement     | Description                                             |
| --------------- | ------------------------------------------------------- |
| File format     | CSV                                                     |
| Encoding        | UTF-8 recommended                                       |
| Header row      | Required                                                |
| Delimiter       | Comma `,`                                               |
| File extension  | `.csv` recommended                                      |
| Content type    | `text/csv`, `text/plain`, or `application/vnd.ms-excel` |
| Required fields | `sku`, `product_name`                                   |


## Required columns

The following columns are required for each product record:

| Column         | Type   | Required | Description                                |
| -------------- | ------ | -------- | ------------------------------------------ |
| `sku`          | string | Yes      | Partner-provided unique product identifier |
| `product_name` | string | Yes      | Display name of the product                |

Rows missing `sku` or `product_name` are skipped during ETL processing.


## Recommended columns

The following columns are recommended for complete product records:

| Column         | Type    | Required | Description                                     |
| -------------- | ------- | -------- | ----------------------------------------------- |
| `brand`        | string  | No       | Product brand or manufacturer                   |
| `category`     | string  | No       | Product category                                |
| `price`        | decimal | No       | Product price (numeric, no currency symbol)     |
| `currency`     | string  | No       | Three-letter currency code (for example, `USD`) |
| `availability` | string  | No       | Product availability status                     |
| `description`  | string  | No       | Product description                             |


## Example CSV

```csv
sku,product_name,brand,category,price,currency,availability,description
SKU-1001,Wireless Mouse,Logitech,Electronics,24.99,USD,in_stock,Ergonomic wireless mouse
SKU-1002,USB-C Cable,Anker,Electronics,12.99,USD,in_stock,6-foot USB-C charging cable
SKU-1003,Laptop Stand,Generic,Office Accessories,39.99,USD,out_of_stock,Adjustable aluminum laptop stand
```


## What happens

- Validate CSV structure  
- Store the raw file in Amazon S3  
- Create submission and validation jobs  
- Process data during ETL  
- Insert, update, or skip product records  


## Validation

During ETL processing, the system validates each row.

| Condition                                      | Result               |
| ---------------------------------------------- | -------------------- |
| Valid row with new `sku`                       | Product is inserted  |
| Valid row with existing `sku` and changed data | Product is updated   |
| Valid row with existing `sku` and no changes   | Product is unchanged |
| Row missing `sku`                              | Row is skipped       |
| Row missing `product_name`                     | Row is skipped       |
| Malformed CSV structure                        | Validation may fail  |


## Product uniqueness

Products are uniquely identified by the combination of:

```
partner_name + sku
```
This constraint prevents duplicate product ingestion for the same partner.
This also means two different partners may use the same SKU without conflict.


## Formatting guidelines

Follow these guidelines when preparing a CSV file:

* Include exactly one header row
* Do not leave required fields blank
* Use consistent column names
* Avoid duplicate `sku` values within the same partner feed
* Use plain numeric values for prices, such as `19.99`
* Do not include currency symbols in the `price` field
* Use consistent availability values, such as `in_stock` or `out_of_stock`

## Related documentation

- [Feeds API](../api/feeds.md)