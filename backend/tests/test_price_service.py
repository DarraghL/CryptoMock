import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

def test_price_service():
    """Test price service functionality"""
    from app import create_app
    from app.services import price_service
    
    app = create_app()
    
    with app.app_context():
        # Test getting all prices
        prices = price_service.get_all_prices()
        print("\nAll prices:")
        for symbol, data in prices.items():
            print(f"{symbol}: ${data['price']:,.2f} ({data['change_24h']:.2f}%)")
        
        # Test getting single price
        btc_price, btc_change = price_service.get_price('BTC')
        print(f"\nBitcoin price: ${btc_price:,.2f} ({btc_change:.2f}%)")

if __name__ == "__main__":
    test_price_service()