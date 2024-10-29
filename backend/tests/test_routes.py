import requests
import json
from pprint import pprint

BASE_URL = 'http://127.0.0.1:5000'

def get_auth_token():
    """Get authentication token through Google OAuth (simulation for testing)"""
    try:
        # For testing purposes, you can log in through the web interface and copy the token
        # or implement a test login here
        return "your_jwt_token_here"  # Replace with actual token
    except Exception as e:
        print(f"Error getting auth token: {e}")
        return None

def test_routes():
    tests = []
    
    def run_test(name, method, endpoint, expected_status=200, data=None, headers=None, auth_required=False):
        url = f"{BASE_URL}{endpoint}"
        try:
            if auth_required and not headers:
                print(f"Skipping {name} - No auth token available")
                return
                
            if method == 'GET':
                response = requests.get(url, headers=headers)
            else:
                response = requests.post(url, json=data, headers=headers)
            
            success = response.status_code == expected_status
            result = {
                'name': name,
                'success': success,
                'status': response.status_code,
                'expected': expected_status,
                'response': response.json() if response.ok else response.text
            }
        except Exception as e:
            result = {
                'name': name,
                'success': False,
                'error': str(e)
            }
        tests.append(result)
        print(f"\nTest: {name}")
        pprint(result)
        return result

    # Test public routes first
    print("\n1. Testing public endpoints...")
    run_test('Basic API', 'GET', '/api/test')
    run_test('All Prices', 'GET', '/api/market/prices')
    run_test('Single Price', 'GET', '/api/market/price/bitcoin')

    # Get authentication token
    print("\n2. Getting authentication token...")
    token = get_auth_token()
    if token:
        auth_headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
    else:
        print("No authentication token available - skipping authenticated tests")
        return

    # Test authenticated routes
    print("\n3. Testing authenticated endpoints...")
    run_test('Portfolio Balance', 'GET', '/api/portfolio/balance', 
             headers=auth_headers, auth_required=True)
    run_test('Portfolio Holdings', 'GET', '/api/portfolio/holdings', 
             headers=auth_headers, auth_required=True)

    # Test trading endpoints
    print("\n4. Testing trading endpoints...")
    buy_data = {"symbol": "BTC", "amount": 0.1}
    sell_data = {"symbol": "BTC", "amount": 0.1}
    
    run_test('Buy Crypto', 'POST', '/api/trading/buy', 
             data=buy_data, headers=auth_headers, auth_required=True)
    run_test('Sell Crypto', 'POST', '/api/trading/sell', 
             data=sell_data, headers=auth_headers, auth_required=True)

    # Test user endpoints
    print("\n5. Testing user endpoints...")
    run_test('User Profile', 'GET', '/api/user/profile', 
             headers=auth_headers, auth_required=True)
    run_test('User Transactions', 'GET', '/api/user/transactions', 
             headers=auth_headers, auth_required=True)

    # Print summary
    print("\nTest Summary:")
    success_count = sum(1 for test in tests if test['success'])
    print(f"Total tests: {len(tests)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {len(tests) - success_count}")

if __name__ == "__main__":
    test_routes()