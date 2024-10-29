# backend/tests/test_api_connection.py
import requests
import os
from dotenv import load_dotenv

def test_coingecko_connection():
    load_dotenv()
    
    api_key = os.getenv('COINGECKO_API_KEY')
    base_url = 'https://api.coingecko.com/api/v3'
    
    # Test API connection with authentication
    headers = {
        'x-cg-demo-api-key': api_key
    }
    
    try:
        # Ping API
        response = requests.get(f'{base_url}/ping', headers=headers)
        print(f"API Connection Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Get Bitcoin price as a test
        price_response = requests.get(
            f'{base_url}/simple/price?ids=bitcoin&vs_currencies=usd',
            headers=headers
        )
        print("\nBitcoin Price Test:")
        print(f"Status: {price_response.status_code}")
        print(f"Data: {price_response.json()}")
        
    except Exception as e:
        print(f"API connection failed: {str(e)}")

if __name__ == "__main__":
    test_coingecko_connection()