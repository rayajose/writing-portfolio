# Python SDK guide

Use this guide to interact with the Commerce Integration API using a lightweight Python client.

The client provides reusable methods for feed ingestion, job monitoring, product retrieval, customer workflows, and transactional order creation without requiring raw HTTP request handling.

<div class="doc-meta">
  <span>Python SDK</span>
  <span>API integration</span>
  <span>Developer tooling</span>
  <span>Automation workflows</span>
</div>


## What the client provides

The client supports:

- Reusable API client methods
- Authentication header management
- Filtering, sorting, and pagination
- Customer and order workflows
- Transactional API interactions
- Standard HTTP exception handling


## Example files

The repository includes the following SDK examples:

- `examples/sdk/client.py`
- `examples/sdk/example_usage.py`
- `examples/sdk/customer_workflow.py`

These files demonstrate SDK-style interaction patterns for the Commerce Integration API.


## Authentication

Include an API key in all requests using the `x-api-key` header.

```python
headers = {
    "x-api-key": "YOUR_API_KEY"
}
```


## Install dependencies

```bash
pip install requests
```


## Example client

```python
import requests


class CommerceIntegrationClient:
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

        params = {
            k: v for k, v in params.items()
            if v is not None
        }

        response = requests.get(
            url,
            headers=self.headers,
            params=params
        )

        response.raise_for_status()
        return response.json()

    def create_customer(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str | None = None
    ):
        url = f"{self.base_url}/customers"

        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone
        }

        response = requests.post(
            url,
            headers=self.headers,
            json=payload
        )

        response.raise_for_status()
        return response.json()

    def create_customer_address(
        self,
        customer_id: str,
        address_line1: str,
        city: str,
        state: str,
        postal_code: str,
        address_line2: str | None = None,
        country: str = "US"
    ):
        url = (
            f"{self.base_url}/customers/"
            f"{customer_id}/addresses"
        )

        payload = {
            "address_line1": address_line1,
            "address_line2": address_line2,
            "city": city,
            "state": state,
            "postal_code": postal_code,
            "country": country
        }

        response = requests.post(
            url,
            headers=self.headers,
            json=payload
        )

        response.raise_for_status()
        return response.json()

    def create_order(
        self,
        partner_name: str,
        items: list,
        customer_reference: str | None = None,
        customer_id: str | None = None,
        shipping_address_id: str | None = None
    ):
        url = f"{self.base_url}/orders"

        payload = {
            "partner_name": partner_name,
            "customer_reference": customer_reference,
            "customer_id": customer_id,
            "shipping_address_id": shipping_address_id,
            "items": items
        }

        payload = {
            k: v for k, v in payload.items()
            if v is not None
        }

        response = requests.post(
            url,
            headers=self.headers,
            json=payload
        )

        response.raise_for_status()
        return response.json()
```


## Upload a feed

```python
client = CommerceIntegrationClient(
    base_url="http://127.0.0.1:8000",
    api_key="YOUR_API_KEY"
)

response = client.upload_feed(
    partner_name="Running Warehouse",
    file_path="running_shoes.csv"
)

print(response)
```


## Check job status

```python
job = client.get_job("JS00001")

print(job)
```


## Retrieve products

```python
products = client.get_products(limit=5)

print(products)
```


## Create a customer

```python
customer = client.create_customer(
    first_name="Alex",
    last_name="Morgan",
    email="alex.morgan@example.com",
    phone="555-0101"
)

print(customer)
```


## Create a shipping address

```python
address = client.create_customer_address(
    customer_id="CU00001",
    address_line1="123 Example Street",
    city="Seattle",
    state="WA",
    postal_code="98101"
)

print(address)
```


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


## Create an order

```python
order = client.create_order(
    partner_name="Running Warehouse",
    customer_reference="ORDER-1001",
    customer_id="CU00001",
    shipping_address_id="AD00001",
    items=[
        {
            "product_id": "PR00001",
            "quantity": 1
        }
    ]
)

print(order)
```


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


## Error handling

The client uses `response.raise_for_status()` to raise exceptions for HTTP errors.

The SDK can also surface validation errors related to:

- Missing customer records
- Invalid shipping addresses
- Product availability conflicts

```python
import requests

try:
    products = client.get_products(limit=5)

except requests.exceptions.HTTPError as error:
    print(f"Request failed: {error}")
```


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

The example retrieves product data from the API and prints the response.


## Additional details

This client is intentionally lightweight and is not distributed as a standalone package.

You can extend the client with:

- Retries
- Structured logging
- Custom error handling
- OAuth authentication
- Request tracing
- Async processing support
- SDK packaging workflows

Customer-sensitive API responses return masked values and do not expose encrypted database fields directly.


## Related documentation

- [Get started](../architecture/getting_started.md)
- [Integration guide](../architecture/integration-guide.md)
- [Feeds](../api/feeds.md)
- [Jobs](../api/jobs.md)
- [Products](../api/products.md)
- [Customers](../api/customers.md)
- [Orders](../api/orders.md)
- [Analytics](../api/analytics.md)