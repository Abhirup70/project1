"""
Example client for the Currency Converter API
Run this after starting the server with: python main.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"


def test_convert_get():
    """Test GET conversion endpoint"""
    print("\n" + "="*60)
    print("TEST 1: Convert USD to EUR (GET)")
    print("="*60)
    
    response = requests.get(
        f"{BASE_URL}/convert",
        params={
            "from_currency": "USD",
            "to_currency": "EUR",
            "amount": 100
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Success!")
        print(f"  {data['amount']} {data['from_currency']} = {data['converted_amount']} {data['to_currency']}")
        print(f"  Exchange Rate: {data['exchange_rate']}")
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.json())


def test_convert_post():
    """Test POST conversion endpoint"""
    print("\n" + "="*60)
    print("TEST 2: Convert GBP to JPY (POST)")
    print("="*60)
    
    response = requests.post(
        f"{BASE_URL}/convert",
        json={
            "amount": 50,
            "from_currency": "GBP",
            "to_currency": "JPY"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Success!")
        print(f"  {data['amount']} {data['from_currency']} = {data['converted_amount']} {data['to_currency']}")
        print(f"  Exchange Rate: {data['exchange_rate']}")
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.json())


def test_get_rates():
    """Test get rates endpoint"""
    print("\n" + "="*60)
    print("TEST 3: Get Exchange Rates (EUR base)")
    print("="*60)
    
    response = requests.get(
        f"{BASE_URL}/rates",
        params={"base_currency": "EUR"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Success!")
        print(f"  Base Currency: {data['base']}")
        print(f"  Total Rates: {len(data['rates'])}")
        print(f"  Sample rates:")
        for i, (currency, rate) in enumerate(list(data['rates'].items())[:5]):
            print(f"    {currency}: {rate}")
        print(f"  Cache Age: {data['cache_age_seconds']} seconds")
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.json())


def test_supported_currencies():
    """Test get supported currencies endpoint"""
    print("\n" + "="*60)
    print("TEST 4: Get Supported Currencies")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/currencies")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Success!")
        print(f"  Total Supported: {data['count']} currencies")
        print(f"  Sample currencies: {', '.join(data['currencies'][:10])}")
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.json())


def test_health_check():
    """Test health check endpoint"""
    print("\n" + "="*60)
    print("TEST 5: Health Check")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/health")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ API is {data['status']}")
        print(f"  Cache Valid: {data['cache_valid']}")
    else:
        print(f"✗ Error: {response.status_code}")


def test_invalid_currency():
    """Test error handling with invalid currency"""
    print("\n" + "="*60)
    print("TEST 6: Error Handling (Invalid Currency)")
    print("="*60)
    
    response = requests.get(
        f"{BASE_URL}/convert",
        params={
            "from_currency": "USD",
            "to_currency": "INVALID",
            "amount": 100
        }
    )
    
    if response.status_code != 200:
        print(f"✓ Correctly handled error!")
        print(f"  Status Code: {response.status_code}")
        print(f"  Error: {response.json()['detail']}")
    else:
        print(f"✗ Should have returned an error")


def test_api_info():
    """Test API info endpoint"""
    print("\n" + "="*60)
    print("TEST 7: API Information")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Success!")
        print(f"  Service: {data['service']}")
        print(f"  Version: {data['version']}")
        print(f"  Available Endpoints:")
        for endpoint, path in data['endpoints'].items():
            print(f"    - {endpoint}: {path}")
    else:
        print(f"✗ Error: {response.status_code}")


def test_multiple_conversions():
    """Test multiple conversions"""
    print("\n" + "="*60)
    print("TEST 8: Batch Conversions")
    print("="*60)
    
    conversions = [
        ("USD", "EUR", 100),
        ("USD", "GBP", 100),
        ("USD", "JPY", 100),
        ("USD", "INR", 100),
        ("USD", "CAD", 100),
    ]
    
    print(f"Converting $100 to different currencies:")
    for from_curr, to_curr, amount in conversions:
        response = requests.get(
            f"{BASE_URL}/convert",
            params={
                "from_currency": from_curr,
                "to_currency": to_curr,
                "amount": amount
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✓ {data['amount']} {data['from_currency']} = {data['converted_amount']} {data['to_currency']}")
        else:
            print(f"  ✗ Error converting to {to_curr}")


if __name__ == "__main__":
    print("\n" + "🌍" * 20)
    print("Currency Converter API - Test Suite")
    print("🌍" * 20)
    
    try:
        # Run all tests
        test_api_info()
        test_convert_get()
        test_convert_post()
        test_get_rates()
        test_supported_currencies()
        test_health_check()
        test_invalid_currency()
        test_multiple_conversions()
        
        print("\n" + "="*60)
        print("✓ All tests completed!")
        print("="*60)
        print("\n📖 Check the API docs at: http://localhost:8000/docs")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API!")
        print("Make sure the server is running with: python main.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
