# Currency Converter API

A simple yet powerful REST API for converting currencies using live exchange rates. Built with Python and FastAPI.

## Features

- 🌍 **Live Exchange Rates**: Real-time currency conversion using free exchange rate API
- 📊 **Caching**: 1-hour cache to reduce API calls
- 🚀 **Fast**: Built with FastAPI for high performance
- 📖 **Interactive Documentation**: Automatic API docs at `/docs`
- 🔄 **Multiple Endpoints**: GET and POST support
- ✅ **CORS Enabled**: Works from any frontend application
- 🏥 **Health Check**: Monitor API status

## Installation

1. **Clone or navigate to the project**:
```bash
cd project1
```

2. **Create a virtual environment** (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Interactive API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### 1. Convert Currency (GET)
**Endpoint**: `GET /convert`

**Parameters**:
- `from_currency` (required): Source currency code (e.g., USD)
- `to_currency` (required): Target currency code (e.g., EUR)
- `amount` (required): Amount to convert (must be > 0)

**Example**:
```bash
curl "http://localhost:8000/convert?from_currency=USD&to_currency=EUR&amount=100"
```

**Response**:
```json
{
  "amount": 100,
  "from_currency": "USD",
  "to_currency": "EUR",
  "converted_amount": 92.50,
  "exchange_rate": 0.925,
  "timestamp": "2026-05-17T10:30:00.123456"
}
```

### 2. Convert Currency (POST)
**Endpoint**: `POST /convert`

**Request Body**:
```json
{
  "amount": 100,
  "from_currency": "USD",
  "to_currency": "EUR"
}
```

**Example**:
```bash
curl -X POST "http://localhost:8000/convert" \
  -H "Content-Type: application/json" \
  -d '{"amount": 100, "from_currency": "USD", "to_currency": "EUR"}'
```

### 3. Get Exchange Rates
**Endpoint**: `GET /rates`

**Parameters**:
- `base_currency` (optional): Base currency code (default: USD)

**Example**:
```bash
curl "http://localhost:8000/rates?base_currency=USD"
```

**Response**:
```json
{
  "base": "USD",
  "rates": {
    "EUR": 0.925,
    "GBP": 0.79,
    "JPY": 150.25,
    ...
  },
  "timestamp": "2026-05-17T10:30:00.123456",
  "cache_age_seconds": 45
}
```

### 4. Get Supported Currencies
**Endpoint**: `GET /currencies`

**Example**:
```bash
curl "http://localhost:8000/currencies"
```

**Response**:
```json
{
  "count": 161,
  "currencies": ["AED", "AFN", "ALL", ..., "USD", "ZAR", "ZMW"],
  "note": "USD is the base currency. Add other base currencies to get their rates."
}
```

### 5. API Information
**Endpoint**: `GET /`

**Example**:
```bash
curl "http://localhost:8000/"
```

### 6. Health Check
**Endpoint**: `GET /health`

**Example**:
```bash
curl "http://localhost:8000/health"
```

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2026-05-17T10:30:00.123456",
  "cache_valid": true
}
```

## Usage Examples

### Python
```python
import requests

# Using GET endpoint
response = requests.get(
    "http://localhost:8000/convert",
    params={
        "from_currency": "USD",
        "to_currency": "EUR",
        "amount": 100
    }
)
data = response.json()
print(f"100 USD = {data['converted_amount']} EUR")

# Using POST endpoint
response = requests.post(
    "http://localhost:8000/convert",
    json={
        "amount": 100,
        "from_currency": "USD",
        "to_currency": "EUR"
    }
)
data = response.json()
print(f"100 USD = {data['converted_amount']} EUR")
```

### JavaScript/Node.js
```javascript
// Using fetch
const response = await fetch(
  'http://localhost:8000/convert?from_currency=USD&to_currency=EUR&amount=100'
);
const data = await response.json();
console.log(`100 USD = ${data.converted_amount} EUR`);

// Using axios
const axios = require('axios');

axios.get('http://localhost:8000/convert', {
  params: {
    from_currency: 'USD',
    to_currency: 'EUR',
    amount: 100
  }
}).then(response => {
  console.log(`100 USD = ${response.data.converted_amount} EUR`);
});
```

### cURL
```bash
# Simple conversion
curl "http://localhost:8000/convert?from_currency=USD&to_currency=GBP&amount=50"

# Get all rates
curl "http://localhost:8000/rates?base_currency=EUR"

# List all supported currencies
curl "http://localhost:8000/currencies"
```

## Supported Currencies

The API supports 160+ currencies including:
- Major: USD, EUR, GBP, JPY, CHF, CAD, AUD
- Asian: INR, CNY, SGD, HKD, KRW, THB
- And many more...

Get the full list with `GET /currencies`

## Error Handling

### 400 - Bad Request
```json
{
  "detail": "Currency 'XXX' not supported"
}
```

### 503 - Service Unavailable
```json
{
  "detail": "Failed to fetch exchange rates: Connection error"
}
```

## Caching

- Exchange rates are cached for **1 hour**
- Reduces external API calls and improves performance
- Cache is automatically refreshed when expired
- Check `cache_age_seconds` in the `/rates` response to see cache age

## Deployment

### Using Docker
```bash
docker build -t currency-converter .
docker run -p 8000:8000 currency-converter
```

### Using Heroku
```bash
git push heroku main
```

### Using Gunicorn (Production)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

## Notes

- The free API used (`exchangerate-api.com`) has rate limits. For production, consider getting an API key.
- All amounts are rounded to 2 decimal places
- Timestamps are in ISO 8601 format (UTC)

## API Key (Optional)

For better rate limits and reliability, you can get a free API key from:
- https://exchangerate-api.com/

Then update the `fetch_exchange_rates()` function in `main.py` with your API key.

## License

MIT License - Feel free to use for any purpose!

## Support

For issues or suggestions, check the code or create an issue in your repository.
