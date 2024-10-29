from flask import Blueprint, jsonify
from app.services import price_service, price_updater
import logging

logger = logging.getLogger(__name__)
market_bp = Blueprint('market', __name__, url_prefix='/api/market')

@market_bp.route('/prices', methods=['GET'])
def get_prices():
    """Get current prices for all supported cryptocurrencies"""
    try:
        # Force a fresh fetch from CoinGecko
        prices = price_service.get_all_prices()  # This will now always get fresh prices
        return jsonify(prices)
    except Exception as e:
        logger.error(f"Error fetching prices: {str(e)}")
        return jsonify({'error': str(e)}), 500

@market_bp.route('/price/<symbol>', methods=['GET'])
def get_price(symbol):
    """Get current price for a specific cryptocurrency"""
    try:
        # Convert symbol to uppercase for consistency
        symbol = symbol.upper()
        # Handle common names
        symbol_map = {
            'BITCOIN': 'BTC',
            'ETHEREUM': 'ETH',
        }
        symbol = symbol_map.get(symbol, symbol)
        
        price, change_24h = price_service.get_price(symbol)
        return jsonify({
            'symbol': symbol,
            'price': price,
            'change_24h': change_24h
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error fetching price for {symbol}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@market_bp.route('/history/<symbol>', methods=['GET'])
def get_price_history(symbol):
    """Get historical prices for a cryptocurrency"""
    try:
        # Convert symbol to uppercase and validate
        symbol = symbol.upper()
        if symbol not in price_service.supported_coins:
            return jsonify({'error': f'Unsupported cryptocurrency: {symbol}'}), 400

        # Fetch historical prices with 7 days of data
        history = price_service.get_historical_prices(symbol, days=7)
        
        if not history:
            return jsonify({'error': 'No price history available'}), 404

        return jsonify({
            'symbol': symbol,
            'history': history
        })
    except ValueError as e:
        logger.error(f"Value error getting history for {symbol}: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error getting history for {symbol}: {str(e)}")
        return jsonify({'error': 'Failed to fetch price history'}), 500
    
@market_bp.route('/test', methods=['GET'])
def test_price_service():
    """Test the price service is working"""
    try:
        # Get Bitcoin price as a test
        price, change = price_service.get_price('BTC')
        return jsonify({
            'status': 'success',
            'message': 'Price service is working',
            'test_data': {
                'btc_price': price,
                'btc_24h_change': change
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@market_bp.route('/prices/latest', methods=['GET'])
def get_latest_prices():
    """Get latest prices from database"""
    try:
        # Use the imported price_updater instance instead of creating a new one
        prices = price_updater.get_latest_prices()
        return jsonify(prices)
    except Exception as e:
        logger.error(f"Error getting latest prices: {str(e)}")
        return jsonify({'error': str(e)}), 500