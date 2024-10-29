# app/services/price_service.py
import requests
from flask import current_app
import logging
from functools import lru_cache
from typing import Dict, Optional, List, Tuple
import time
from datetime import datetime  # Add this import

logger = logging.getLogger(__name__)

class PriceService:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.supported_coins = {
            'BTC': 'bitcoin',
            'ETH': 'ethereum',
            'USDT': 'tether',
            'BNB': 'binancecoin',
            'USDC': 'usd-coin',
            'XRP': 'ripple',
            'ADA': 'cardano',
            'DOGE': 'dogecoin',
            'SOL': 'solana',
            'TRX': 'tron'
        }
        self.last_request_time = 0
        self.rate_limit_delay = 1.0  # Minimum delay between requests in seconds
        self.app = None
        self._api_key = None

    def init_app(self, app):
        """Initialize with Flask app"""
        self.app = app
        # Get API key from config if available
        self._api_key = app.config.get('COINGECKO_API_KEY')
        logger.info("PriceService initialized successfully")

    @property
    def api_key(self):
        """Get API key from current application config"""
        if self._api_key:
            return self._api_key
        if self.app:
            return self.app.config.get('COINGECKO_API_KEY')
        return current_app.config.get('COINGECKO_API_KEY')

    def _get_headers(self) -> Dict:
        """Get headers for API requests"""
        headers = {
            'Accept': 'application/json',
        }
        if self.api_key:
            headers['x-cg-demo-api-key'] = self.api_key
        return headers

    def _rate_limit(self):
        """Implement rate limiting"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last_request)
        self.last_request_time = time.time()

    def get_all_prices(self) -> Dict:
        """Get prices for all supported cryptocurrencies"""
        try:
            # Get comma-separated list of coin IDs
            coin_ids = ','.join(self.supported_coins.values())
            
            # Rate limiting
            self._rate_limit()
            
            # Make API request
            response = requests.get(
                f"{self.base_url}/simple/price",
                headers=self._get_headers(),
                params={
                    'ids': coin_ids,
                    'vs_currencies': 'usd',
                    'include_24hr_change': 'true',
                    'include_market_cap': 'true',
                    'include_24hr_vol': 'true'
                }
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Convert response to our format
            result = {}
            for symbol, coin_id in self.supported_coins.items():
                if coin_id in data:
                    result[symbol] = {
                        'price': data[coin_id]['usd'],
                        'change_24h': data[coin_id].get('usd_24h_change', 0.0),
                        'market_cap': data[coin_id].get('usd_market_cap'),
                        'volume_24h': data[coin_id].get('usd_24h_vol')
                    }
            
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching prices from CoinGecko: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error getting all prices: {str(e)}")
            raise

    def get_price(self, symbol: str) -> Tuple[float, float]:
        """Get current price and 24h change for a cryptocurrency"""
        try:
            # Get coin ID
            coin_id = self.supported_coins.get(symbol.upper())
            if not coin_id:
                raise ValueError(f"Unsupported cryptocurrency: {symbol}")

            # Rate limiting
            self._rate_limit()
            
            # Make API request
            response = requests.get(
                f"{self.base_url}/simple/price",
                headers=self._get_headers(),
                params={
                    'ids': coin_id,
                    'vs_currencies': 'usd',
                    'include_24hr_change': 'true'
                }
            )
            
            response.raise_for_status()
            data = response.json()
            
            if coin_id not in data:
                raise ValueError(f"No price data available for {symbol}")
            
            price = data[coin_id]['usd']
            change_24h = data[coin_id].get('usd_24h_change', 0.0)
            
            return price, change_24h
            
        except Exception as e:
            logger.error(f"Error getting price for {symbol}: {str(e)}")
            raise

    def get_supported_symbols(self) -> List[str]:
        """Get list of supported cryptocurrency symbols"""
        return list(self.supported_coins.keys())
    
    def get_historical_prices(self, symbol: str, days: int = 7) -> List[Dict]:
        """Get historical price data for a cryptocurrency"""
        try:
            # Get coin ID
            coin_id = self.supported_coins.get(symbol.upper())
            if not coin_id:
                raise ValueError(f"Unsupported cryptocurrency: {symbol}")
    
            # Rate limiting
            self._rate_limit()
            
            # Make API request
            response = requests.get(
                f"{self.base_url}/coins/{coin_id}/market_chart",
                headers=self._get_headers(),
                params={
                    'vs_currency': 'usd',
                    'days': str(days),
                    'interval': 'daily'
                }
            )
            
            # Check if request was successful
            if response.status_code != 200:
                logger.error(f"CoinGecko API error: {response.status_code} - {response.text}")
                raise Exception(f"Failed to fetch price history from CoinGecko (Status: {response.status_code})")
                
            data = response.json()
            
            if 'prices' not in data:
                logger.error(f"Unexpected response format: {data}")
                raise Exception("Invalid response format from CoinGecko")
    
            # Format the data for the frontend
            prices = []
            for timestamp, price in data['prices']:
                prices.append({
                    'timestamp': datetime.fromtimestamp(timestamp/1000).isoformat(),
                    'price': float(price)  # Ensure price is a float
                })
            
            return prices
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error getting historical prices for {symbol}: {str(e)}")
            raise Exception(f"Failed to connect to CoinGecko API: {str(e)}")
        except Exception as e:
            logger.error(f"Error getting historical prices for {symbol}: {str(e)}")
            raise