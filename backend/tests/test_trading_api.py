import pytest
from app import create_app, db
from app.services import price_service, trading_service
from app.models.user import User
from app.models.portfolio import Portfolio
from app.models.transaction import Transaction
import json
import time

def test_trading_flow():
    """Test complete trading flow: buy and sell"""
    app = create_app()
    
    with app.app_context():
        print("\n=== Testing Trading Flow ===")
        
        try:
            # 1. Create test user with initial balance
            user = User.query.filter_by(email='test@example.com').first()
            if not user:
                user = User(
                    email='test@example.com',
                    username='test_user',
                    initial_balance=100000.0,
                    current_balance=100000.0
                )
                db.session.add(user)
                db.session.commit()
            
            initial_balance = user.current_balance
            print(f"\nInitial balance: ${initial_balance:,.2f}")

            # 2. Test buying Bitcoin
            symbol = 'BTC'
            buy_amount = 0.01  # Small amount for testing
            
            # Get current price with rate limiting
            current_price, change_24h = price_service.get_price(symbol)
            print(f"\nCurrent {symbol} price: ${current_price:,.2f}")
            print(f"24h change: {change_24h:.2f}%")
            
            print(f"\nTesting Buy Order:")
            print(f"Buying {buy_amount} {symbol} at ${current_price:,.2f}")
            
            # Calculate expected cost
            expected_cost = buy_amount * current_price
            print(f"Expected cost: ${expected_cost:,.2f}")
            
            # Execute buy
            print("\nExecuting buy order...")
            buy_result = trading_service.execute_buy(user.id, symbol, buy_amount)
            print("Buy Result:", json.dumps(buy_result, indent=2))
            
            # Verify purchase
            time.sleep(1)  # Rate limiting
            portfolio = Portfolio.query.filter_by(
                user_id=user.id,
                crypto_symbol=symbol
            ).first()
            
            assert portfolio is not None, "Portfolio should exist after buying"
            assert abs(portfolio.quantity - buy_amount) < 0.00001, \
                f"Should have {buy_amount} {symbol}, but has {portfolio.quantity}"
            
            print(f"\nPortfolio verified: {portfolio.quantity} {symbol}")
            
            # 3. Test selling half the position
            time.sleep(1)  # Rate limiting
            sell_amount = buy_amount / 2
            print(f"\nTesting Sell Order:")
            print(f"Selling {sell_amount} {symbol} at current market price")
            
            # Execute sell
            sell_result = trading_service.execute_sell(user.id, symbol, sell_amount)
            print("\nSell Result:", json.dumps(sell_result, indent=2))
            
            # Verify sale
            time.sleep(1)  # Rate limiting
            portfolio = Portfolio.query.filter_by(
                user_id=user.id,
                crypto_symbol=symbol
            ).first()
            
            assert portfolio is not None, "Portfolio should exist after partial sell"
            expected_remaining = buy_amount - sell_amount
            assert abs(portfolio.quantity - expected_remaining) < 0.00001, \
                f"Should have {expected_remaining} {symbol} left, but has {portfolio.quantity}"
            
            print(f"\nPortfolio verified: {portfolio.quantity} {symbol} remaining")
            
            # 4. Get portfolio summary
            time.sleep(1)  # Rate limiting
            print("\nGetting Portfolio Summary:")
            summary = trading_service.get_portfolio_summary(user.id)
            print(json.dumps(summary, indent=2))
            
            # Optional: Clean up test data
            print("\nCleaning up test data...")
            if portfolio.quantity == 0:
                db.session.delete(portfolio)
            # Uncomment to delete test user
            # db.session.delete(user)
            db.session.commit()
            
            print("\n=== Test completed successfully! ===")
            
        except Exception as e:
            print(f"\n❌ Test failed: {str(e)}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    test_trading_flow()