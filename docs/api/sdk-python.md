# Python SDK guide

Use this guide to interact with the Partner Catalog API using a lightweight Python client.
This client provides reusable methods for uploading feeds, checking jobs, and retrieving product data without writing raw HTTP requests.

## What the client does

- Wrap API endpoints in reusable methods  
- Handle authentication headers  
- Support filtering, sorting, and pagination  
- Raise exceptions for failed requests  

---

## Example files

The client and example scripts are available in the repository:

- `examples/sdk/client.py`
- `examples/sdk/example_usage.py`

These files demonstrate how to interact with the API using an SDK-style approach.

---

## Authentication

Include an API key in all requests using the `x-api-key` header.

```python
headers = {
    "x-api-key": "demo-secret-key"
}
```

---

## Install dependencies

```bash
pip install requests
```

---

## Example client

```python
import requests

class PartnerCatalogClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "x-api-key": api_key
        }

    def upload_feed(self, partner_name: str, file_path: str):
        url = f"{self.base_url}/feeds/upload"

        with open(file_path, "rb") as csv_file:
            files = {"file": csv_file}
            data = {"partner_name": partner_name}

            response = requests.post(
                url,
                headers=self.headers,
                files=files,
                data=data
            )

        response.raise_for_status()
        return response.json()

    def get_job(self, job_id: str):
        url = f"{self.base_url}/jobs/{job_id}"

        response = requests.get(
            url,
            headers=self.headers
        )

        response.raise_for_status()
        return response.json()

    def get_products(
        self,
        partner_name: str = None,
        brand: str = None,
        category: str = None,
        availability: str = None,
        sort_by: str = "created_at",
        order: str = "asc",
        limit: int = 10,
        cursor: str = None
    ):
        url = f"{self.base_url}/products"

        params = {
            "partner_name": partner_name,
            "brand": brand,
            "category": category,
            "availability": availability,
            "sort_by": sort_by,
            "order": order,
            "limit": limit,
            "cursor": cursor
        }

        params = {k: v for k, v in params.items() if v is not None}

        response = requests.get(
            url,
            headers=self.headers,
            params=params
        )

        response.raise_for_status()
        return response.json()
```

---

## Usage example

```python
client = PartnerCatalogClient(
    base_url="http://127.0.0.1:8000",
    api_key="demo-secret-key"
)

response = client.upload_feed(
    partner_name="Running Warehouse",
    file_path="running_shoes.csv"
)

print(response)
```

---

## Check job status

```python
job = client.get_job("JS00001")
print(job)
```

---

## Retrieve products

```python
products = client.get_products(limit=5)
print(products)
```

---

## Filter and sort products

```python
products = client.get_products(
    category="Running Shoes",
    availability="in_stock",
    sort_by="price",
    order="asc",
    limit=5
)

print(products)
```

---

## Cursor-based pagination
Use cursor-based pagination to retrieve large result sets.

```python
first_page = client.get_products(limit=5)

next_cursor = first_page.get("next_cursor")

if next_cursor:
    second_page = client.get_products(
        limit=5,
        cursor=next_cursor
    )

    print(second_page)
```

---

## Error handling

The client uses `response.raise_for_status()` to raise exceptions for HTTP errors.

```python
import requests

try:
    products = client.get_products(limit=5)
except requests.exceptions.HTTPError as error:
    print(f"Request failed: {error}")
```

---
## Run the example locally

Start the API:

```bash
uvicorn main:app --reload
```

Navigate to the SDK example directory:

```bash
cd examples/sdk
```

Run the example:

```bash
python example_usage.py
```
The script will retrieve product data from the API and print the response.

---

## Additional details

This client is intentionally lightweight and not distributed as a standalone package. You can extend it with retries, logging, or custom error handling.
