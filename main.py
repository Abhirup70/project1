from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import requests
import os
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
import json

app = FastAPI(
    title="Currency Converter API",
    description="Convert money from one currency to another using latest exchange rates",
    version="1.0.0"
)

# Add CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="."), name="static")

# In-memory cache for exchange rates
exchange_cache = {
    "data": {},
    "timestamp": None,
    "ttl": 3600  # Cache expires in 1 hour
}


class ConversionRequest(BaseModel):
    """Request model for currency conversion"""
    amount: float
    from_currency: str
    to_currency: str


class ConversionResponse(BaseModel):
    """Response model for currency conversion"""
    amount: float
    from_currency: str
    to_currency: str
    converted_amount: float
    exchange_rate: float
    timestamp: str


def is_cache_valid():
    """Check if cached exchange rates are still valid"""
    if exchange_cache["timestamp"] is None:
        return False
    return datetime.now() - exchange_cache["timestamp"] < timedelta(seconds=exchange_cache["ttl"])


def fetch_exchange_rates(base_currency: str = "USD") -> dict:
    """Fetch exchange rates from free API"""
    try:
        # Using exchangerate-api.com free tier (no API key required for basic usage)
        # Alternative free APIs: fixer.io, open-exchange-rates
        url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return data.get("rates", {})
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=503,
            detail=f"Failed to fetch exchange rates: {str(e)}"
        )


def get_exchange_rates(base_currency: str = "USD") -> dict:
    """Get exchange rates with caching"""
    # Check if we have valid cached data
    if is_cache_valid() and base_currency in exchange_cache["data"]:
        return exchange_cache["data"][base_currency]
    
    # Fetch new rates
    rates = fetch_exchange_rates(base_currency)
    
    # Update cache
    exchange_cache["data"][base_currency] = rates
    exchange_cache["timestamp"] = datetime.now()
    
    return rates


@app.get("/index.html")
async def get_index():
    """Serve the HTML UI"""
    return FileResponse("index.html", media_type="text/html")


@app.get("/", tags=["Info"])
def root():
    """API information and available endpoints"""
    return {
        "service": "Currency Converter API",
        "version": "1.0.0",
        "description": "Convert money between different currencies using live exchange rates",
        "endpoints": {
            "convert": "/convert",
            "rates": "/rates",
            "supported_currencies": "/currencies",
            "ui": "/index.html"
        },
        "example": {
            "url": "/convert?from_currency=USD&to_currency=EUR&amount=100",
            "method": "GET"
        }
    }


@app.get("/convert", response_model=ConversionResponse, tags=["Conversion"])
def convert(
    from_currency: str = Query(..., description="Source currency code (e.g., USD)"),
    to_currency: str = Query(..., description="Target currency code (e.g., EUR)"),
    amount: float = Query(..., gt=0, description="Amount to convert (must be > 0)")
):
    """
    Convert currency from one to another
    
    Example: /convert?from_currency=USD&to_currency=EUR&amount=100
    """
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    
    try:
        # Fetch rates with base currency as source
        rates = get_exchange_rates(from_currency)
        
        if to_currency not in rates:
            raise HTTPException(
                status_code=400,
                detail=f"Currency '{to_currency}' not supported"
            )
        
        exchange_rate = rates[to_currency]
        converted_amount = amount * exchange_rate
        
        return ConversionResponse(
            amount=amount,
            from_currency=from_currency,
            to_currency=to_currency,
            converted_amount=round(converted_amount, 2),
            exchange_rate=exchange_rate,
            timestamp=datetime.now().isoformat()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid currency code or conversion failed: {str(e)}"
        )


@app.post("/convert", response_model=ConversionResponse, tags=["Conversion"])
def convert_post(request: ConversionRequest):
    """
    Convert currency via POST request
    
    Request body: {"amount": 100, "from_currency": "USD", "to_currency": "EUR"}
    """
    from_currency = request.from_currency.upper()
    to_currency = request.to_currency.upper()
    
    if request.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amount must be greater than 0"
        )
    
    try:
        rates = get_exchange_rates(from_currency)
        
        if to_currency not in rates:
            raise HTTPException(
                status_code=400,
                detail=f"Currency '{to_currency}' not supported"
            )
        
        exchange_rate = rates[to_currency]
        converted_amount = request.amount * exchange_rate
        
        return ConversionResponse(
            amount=request.amount,
            from_currency=from_currency,
            to_currency=to_currency,
            converted_amount=round(converted_amount, 2),
            exchange_rate=exchange_rate,
            timestamp=datetime.now().isoformat()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Conversion failed: {str(e)}"
        )


@app.get("/rates", tags=["Rates"])
def get_rates(
    base_currency: str = Query("USD", description="Base currency code")
):
    """
    Get current exchange rates for a base currency
    
    Example: /rates?base_currency=USD
    """
    base_currency = base_currency.upper()
    
    try:
        rates = get_exchange_rates(base_currency)
        
        return {
            "base": base_currency,
            "rates": rates,
            "timestamp": datetime.now().isoformat(),
            "cache_age_seconds": (datetime.now() - exchange_cache["timestamp"]).total_seconds() if exchange_cache["timestamp"] else 0
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to fetch rates: {str(e)}"
        )


@app.get("/currencies", tags=["Info"])
def get_supported_currencies():
    """Get list of all supported currencies"""
    try:
        rates = get_exchange_rates("USD")
        currencies = sorted(list(rates.keys()) + ["USD"])
        
        return {
            "count": len(currencies),
            "currencies": currencies,
            "note": "USD is the base currency. Add other base currencies to get their rates."
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Failed to fetch currencies: {str(e)}"
        )


@app.get("/health", tags=["Info"])
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "cache_valid": is_cache_valid()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
