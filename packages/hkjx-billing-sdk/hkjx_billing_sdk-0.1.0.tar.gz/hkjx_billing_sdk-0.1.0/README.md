# A1 Huakunjingxiu Billing SDK

Python SDK for interacting with the A1 Huakunjingxiu Billing API.

## Installation

```bash
pip install billing-sdk
```

## Usage

```python
from billing import Client

# Initialize client
client = Client(api_key="your_api_key")

# Create an invoice
invoice = client.create_invoice(
    amount=100.00,
    description="Monthly subscription"
)

# Get invoice details
invoice_details = client.get_invoice(invoice["id"])

# List invoices
invoices = client.list_invoices(limit=10)
```

## Error Handling

The SDK provides several exception types:

```python
from billing import (
    BillingError,
    AuthenticationError,
    InvalidRequestError,
    APIError
)

try:
    # API calls
except AuthenticationError as e:
    print("Invalid API key")
except InvalidRequestError as e:
    print("Invalid request parameters")
except APIError as e:
    print("Server error occurred")
except BillingError as e:
    print("General billing error")
```

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

## License

MIT
