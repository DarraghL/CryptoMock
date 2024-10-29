import requests
import json
from pprint import pprint
import os
import time
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

class APITester:
    def __init__(self):
        self.base_url = 'http://127.0.0.1:5000'
        self.token = None
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.token_file = 'test_token.json'

    def get_fresh_token(self):
        """Get a fresh token through Google OAuth"""
        print("\nPlease follow these steps to get a fresh token:")
        print("1. Open this URL in your browser: http://127.0.0.1:5000")
        print("2. Log in with Google")
        print("3. Open browser DevTools (F12)")
        print("4. Look in the Console for the authentication response")
        print("5. Copy the access_token value")
        
        token = input("\nPaste your JWT token here: ").strip()
        if token:
            # Save token with timestamp
            with open(self.token_file, 'w') as f:
                json.dump({
                    'access_token': token,
                    'timestamp': time.time()
                }, f)
            return token
        return None

    def get_token(self):
        """Get JWT token with automatic refresh"""
        try:
            # Check for existing token
            if os.path.exists(self.token_file):
                with open(self.token_file, 'r') as f:
                    data = json.load(f)
                    token = data.get('access_token')
                    timestamp = data.get('timestamp', 0)
                    
                    # Check if token is less than 50 minutes old
                    if time.time() - timestamp < 50 * 60:
                        print("Using existing token")
                        self.token = token
                        return True
            
            # Get fresh token if none exists or is expired
            print("Getting fresh token...")
            token = self.get_fresh_token()
            if token:
                self.token = token
                return True
            
            return False
            
        except Exception as e:
            print(f"Error getting token: {str(e)}")
            return False

    def run_test(self, name, method, endpoint, expected_status=200, data=None, auth_required=False):
        """Run a single API test"""
        url = f"{self.base_url}{endpoint}"
        headers = self.headers.copy()
        
        if auth_required:
            if not self.token and not self.get_token():
                print(f"Skipping {name} - No valid token available")
                return False, None
            headers['Authorization'] = f'Bearer {self.token}'

        try:
            print(f"\n=== {name} ===")
            print(f"URL: {url}")
            if data:
                print("Request Data:")
                pprint(data)
            
            if method == 'GET':
                response = requests.get(url, headers=headers)
            else:
                response = requests.post(url, json=data, headers=headers)
            
            print(f"Status Code: {response.status_code}")
            print("Response:")
            pprint(response.json() if response.ok else response.text)
            
            # Handle token expiration
            if response.status_code == 401 and auth_required:
                print("Token expired. Getting fresh token...")
                if self.get_token():
                    headers['Authorization'] = f'Bearer {self.token}'
                    # Retry request
                    if method == 'GET':
                        response = requests.get(url, headers=headers)
                    else:
                        response = requests.post(url, json=data, headers=headers)
                    print("Retry Status Code:", response.status_code)
                    print("Retry Response:")
                    pprint(response.json() if response.ok else response.text)
            
            return response.status_code == expected_status, response
            
        except Exception as e:
            print(f"Error in {name}: {str(e)}")
            return False, None

    def test_all(self):
        """Run all API tests"""
        results = []
        
        # 1. Test public endpoints
        print("\n=== Testing Public Endpoints ===")
        
        # Test basic API endpoint
        results.append(self.run_test(
            "Basic API Test",
            'GET',
            '/api/test'
        ))

        # Test market endpoints
        results.append(self.run_test(
            "Get All Prices",
            'GET',
            '/api/market/prices'
        ))
        
        results.append(self.run_test(
            "Get Bitcoin Price",
            'GET',
            '/api/market/price/BTC'  # Using uppercase symbol
        ))

        # 2. Test authenticated endpoints
        print("\n=== Testing Authenticated Endpoints ===")
        
        # Portfolio endpoints
        results.append(self.run_test(
            "Get Portfolio Balance",
            'GET',
            '/api/portfolio/balance',
            auth_required=True
        ))
        
        results.append(self.run_test(
            "Get Portfolio Holdings",
            'GET',
            '/api/portfolio/holdings',
            auth_required=True
        ))

        # Trading endpoints
        buy_data = {
            "symbol": "BTC",
            "amount": 0.01  # Small amount for testing
        }
        results.append(self.run_test(
            "Buy Crypto",
            'POST',
            '/api/trading/buy',
            data=buy_data,
            auth_required=True
        ))

        # Wait a bit between trades
        time.sleep(1)

        sell_data = {
            "symbol": "BTC",
            "amount": 0.005  # Sell half
        }
        results.append(self.run_test(
            "Sell Crypto",
            'POST',
            '/api/trading/sell',
            data=sell_data,
            auth_required=True
        ))

        # User endpoints
        results.append(self.run_test(
            "Get User Profile",
            'GET',
            '/api/user/profile',
            auth_required=True
        ))
        
        results.append(self.run_test(
            "Get User Transactions",
            'GET',
            '/api/user/transactions',
            auth_required=True
        ))

        # Print summary
        success_count = sum(1 for result, _ in results if result)
        print(f"\n=== Test Summary ===")
        print(f"Total tests: {len(results)}")
        print(f"Successful: {success_count}")
        print(f"Failed: {len(results) - success_count}")

        # Return overall success/failure
        return success_count == len(results)

def main():
    """Main test runner"""
    try:
        print("Starting API Tests...")
        tester = APITester()
        success = tester.test_all()
        
        if success:
            print("\n✅ All tests passed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Some tests failed!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\nError running tests: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()